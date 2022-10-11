import difflib as dl
import os
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import Canvas, OptionMenu, StringVar, filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo


root = tk.Tk()
root.title('Group brands')
# root.resizable(False, False)
root.geometry('600x300')
root.focus()
csv_file = None

keys = [
    f"Similar Brand {i+1}" for i in range(50)
]
# print(keys)


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
    global keys
    canvas = Canvas(root, width=600, height=300, bg="SpringGreen2")    
    # Add a text in Canvas
    canvas.create_text(300, 150, text="Loading Data in the background",
                       fill="black", font=('Helvetica 15 bold'))
    canvas.pack(expand=True)
    btn.pack_forget()
    drop.pack_forget()
    root.update()
    groups = []    
    # print(dataframe[selected_column])
    keys = list(input_records[0].keys()) + keys
    my_brands = dataframe[selected_column].values
    for r in input_records:
        temp_record = r.copy()
        i = r[selected_column]
        group = dl.get_close_matches(i, my_brands,cutoff=.75, n=500)        
        print(len(groups)+1, i, len(group))
        for g in range(len(group)):
            temp_record[f"Similar Brand {g+1}"] = group[g]                    
        groups.append(temp_record)

    print(len(groups))
    df = pd.DataFrame(groups)
    # df.rename(columns={"0": selected_column}, inplace=True)

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

