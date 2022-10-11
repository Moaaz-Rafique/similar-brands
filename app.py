import difflib as dl
import os
from datetime import datetime
from numpy import number
import pandas as pd
import tkinter as tk
from tkinter import Canvas, OptionMenu, StringVar, filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from pandastable import Table, TableModel


root = tk.Tk()
root.title('Group brands')
# root.resizable(False, False)
root.geometry('1200x300')
root.focus()
csv_file = None


def selected_column(selected_column,
                    input_records,
                    dataframe,
                    filename,
                    btn,
                    drop,
                    open_btn):
    """   # selected_column(v.get(),
    #                 csv_file.to_dict(orient='records'),
    #                 csv_file,
    #                 filename,
    #                 column_btn,
    #                 drop,
    #                 btn
    #                 )
    # """
    
    canvas = Canvas(root, width=1200, height=300, bg="SpringGreen2")    
    # Add a text in Canvas
    canvas.create_text(300, 150, text="Loading Data in the background",
                       fill="black", font=('Helvetica 15 bold'))
    canvas.pack(expand=True)
    btn.pack_forget()
    drop.pack_forget()
    root.update()
    groups = []    

    my_brands = dataframe[selected_column].values
    for r in input_records[:30]:
        temp_record = r.copy()
        i = r[selected_column]
        group = dl.get_close_matches(i, my_brands,cutoff=.75, n=500)        
        print(len(groups)+1, i, len(group))
        for g in range(len(group)):
            temp_record[f"Similar Brand {g+1}"] = group[g]                    
        groups.append(temp_record)

    print(len(groups))
    canvas.pack_forget()
    df = pd.DataFrame(groups)
    # for index, row in df.iterrows():
    #     showinfo(
    #     title=index,  message=row.__str__()
    # )    

    
    for index, row in df.iterrows():
        number_of_key = 0
        for y in df.keys():
            w = tk.Text(root, width=15, height=2)
            w.grid(row=index,column=number_of_key)
            try:
                w.insert(tk.END, df[y][index])
            except Exception as e:
                print(e)
            number_of_key += 1
    
    # x = input()
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
    root.config(yscrollcommand = scrollbar.set)
  
    # setting scrollbar command parameter 
    # to listbox.yview method its yview because
    # we need to have a vertical view
    root.config(command = root.yview)
    # root.state("zoomed")
    root.update()


    df.to_csv(f'Brands_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv', index=False)
    showinfo(
        title='Output',  message="File was created Successfully"
    )

    open_btn.pack(expand=True)
    print("Everything was loaded successfully")


def select_file(csv_file, btn):
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Select a csv',
        initialdir='/',
        filetypes=filetypes)
    if filename:
        showinfo(
            title='Selected File',
            message=os.path.split(filename)[1]
        )
    else:
        showinfo(
            title='Error',
            message="File not loaded, Try again"
        )
    csv_file = pd.read_csv(filename)
    options = csv_file.keys()

    v = StringVar(root, "Select a column")

    btn.pack_forget()
    drop = OptionMenu(root, v, *options)
    column_btn = ttk.Button(
        root,
        text='Select',
        command=lambda: selected_column(v.get(),
                                        csv_file.to_dict(orient='records'),
                                        csv_file,
                                        filename,
                                        column_btn,
                                        drop,
                                        btn
                                        )
    )
    drop.pack(expand=True)
    column_btn.pack(expand=True)
# open button


open_button = ttk.Button(
    root,
    text='Select CSV',
    command=lambda: select_file(csv_file, open_button)
)


# Loop is used to create multiple Radiobuttons
# rather than creating each button separately


open_button.pack(expand=True)


# run the application
root.mainloop()

