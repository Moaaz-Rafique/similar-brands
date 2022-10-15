import difflib as dl
import itertools
import os
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import Canvas, OptionMenu, StringVar, filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from pandastable import Table

root = tk.Tk()
root.title('Group brands')
# root.resizable(False, False)
root.geometry('1200x800')
root.focus()
csv_file = None


def get_close_matches_icase(word, possibilities, *args, **kwargs):
    """ Case-insensitive version of difflib.get_close_matches """

    lword = word.lower()
    lpos = {}

    for p in possibilities:
        if p.lower() not in lpos:
            lpos[p.lower()] = [p]
        else:
            lpos[p.lower()].append(p)
    lmatches = dl.get_close_matches(lword, lpos.keys(), *args, **kwargs)
    ret = [lpos[m] for m in lmatches]
    ret = itertools.chain.from_iterable(ret)
    return list(ret)


def save_and_finalize(base_df, df, open_btn, save_button, frame):
    
    for index, row in df.iterrows():
        # print(row['Alias'], row['key'])                
        for i in row["Linked rows"]:
            try:
                base_df["Alias"][i]= row["Alias"]
            except:
                print("bas error")

    base_df.drop(columns = ["Linked rows"],  inplace = True )

    base_df.to_csv(
        f'Brands_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv', index=False)
    showinfo(
        title='Output',  message="File created successfully"
    )
    save_button.pack_forget()
    frame.pack_forget()
    open_btn.pack(expand=True)
    root.update()


def selected_column(selected_column,
                    input_records,
                    dataframe,
                    filename,
                    btn,
                    drop,
                    open_btn):
    canvas = Canvas(root, width=1200, height=800, bg="SpringGreen2")
    # Add a text in Canvas
    canvas.create_text(600, 350, text="Loading Data in the background",
                       fill="black", font=('Helvetica 15 bold'))
    canvas.pack(expand=True)
    btn.pack_forget()
    drop.pack_forget()
    root.update()
    groups = []
    my_brands = dataframe[selected_column].values

    # input_records = input_records[-200:-100]
    # my_brands = my_brands[-200:-100]

    for r in input_records:
        temp_record = r.copy()
        i = r[selected_column]
        group = get_close_matches_icase(i, my_brands, cutoff=.75, n=500)
        r2_index=0
        linkedRows = []
        for r2 in input_records:
            if r2[selected_column] in group:
                linkedRows.append(r2_index)
                r2 = None
            r2_index+=1


        if len(group) > 0:
            my_brands = [brand for brand in my_brands if brand not in group]
        print(len(my_brands))

        # print(len(groups)+1, i, len(group))

        for g in range(len(group)):
            temp_record[f"Similar Brand {g+1}"] = group[g]
        temp_record["Linked rows"] = linkedRows
        groups.append(temp_record)

    print("groups length", len(groups))
    canvas.pack_forget()
    root.update()
    base_df = pd.DataFrame(groups)
    base_df.dropna(how='all', inplace=True)
    base_df.dropna(how='all', inplace=True, axis=1)
    base_df['Alias'] = base_df[selected_column]
    # base_df.drop()
    try:
        df = base_df.dropna(axis=0, subset=[f"Similar Brand 1"])
    except:
        print("No matches were found")
    

    frame = tk.Frame(root, height=800, width=1200)
    frame.pack()
    pt = Table(frame, dataframe=df, width=1200)
    pt.show()
    save_button = ttk.Button(
        root,
        text='Save CSV',
        command=lambda: save_and_finalize(
            base_df, pt.model.df, open_btn, save_button, frame)
    )

    save_button.pack(expand=True)
    root.update()
    showinfo(
        title='Output',  message="Groups formed successfully"
    )


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
open_button.pack(expand=True)
root.mainloop()
