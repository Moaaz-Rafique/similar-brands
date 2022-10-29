import difflib as dl
import itertools
import os
from datetime import datetime
from traceback import print_tb
import pandas as pd
import tkinter as tk
from tkinter import Canvas, OptionMenu, StringVar, filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from pandastable import Table
root = tk.Tk()
root.title('Group brands')
root.geometry('1200x800')
root.focus()
csv_file = None
currentIndex = 0

def update_links(row, similar_brand_keys, input_records, selected_column):
    links_group = [row[selected_column]]
    for i in similar_brand_keys:
        if not isinstance(row[i], float):
            links_group.append(row[i])

    r2_index = 0
    linkedRows = []
    for r2 in input_records:
        if r2[selected_column] in links_group:
            linkedRows.append(r2_index+1)
            r2 = None
        r2_index += 1
    return linkedRows


def update_df(pt, original_df, input_records, selected_column):
    df = pt.model.df
    global currentIndex
    if (currentIndex+10) > len(df):
        showinfo(
            title='Output',  message="Completed All"
        )        
        return 

    print("shesdksafkafsj", )
    all_keys = df.keys()
    similar_brand_keys = []
    for i in all_keys:
        if 'Similar Brand ' in i:
            similar_brand_keys.append(i)

    for index, row in df.iterrows():
        updatedLinks = update_links(
            row, similar_brand_keys, input_records, selected_column)
        try:
            df["Linked rows"][index] = updatedLinks
            if row['Alias']:
                for link in updatedLinks:
                    df['Alias'][link-1] = df['Alias'][index]
                    # print("Animation")
        except Exception as e:
            print(e)
    pt.model.df = df
    mask_0 = pt.model.df[selected_column].notnull()
    for i in pt.model.df:
        pt.setColorByMask(i, mask_0, 'white')
    mask_1 = pt.model.df['Alias'].notnull()
    for i in pt.model.df:
        pt.setColorByMask(i, mask_1, 'green')
    # print(len(df) , (currentIndex ))
    pt.update_rowcolors()    
    currentIndex = currentIndex + 10
    if len(df) > (currentIndex + 10):
        pt.child.model.df = df[currentIndex:currentIndex+10]
    else:
        pt.child.model.df = df[-10:]
    # pt.child.setColorbyValue()
    try:
        pt.child.setRowColors(rows=[2], clr='#3776ab', cols=[1])
    except Exception as e:
        print("error:2")
    # try:
    try:
        pt.child.setRowColors(rows=[12], clr='#3776ab', cols=[1])
    except Exception as e:
        print("error:3")
    try:
        pt.child.setRowColors(rows=[22], clr='#3776ab', cols=[1])
    except Exception as e:
        print("error:4")
    try:
        pt.child.setRowColors(rows=[32], clr='#3776ab', cols=[1])
    except Exception as e:
        print("error:5")
    pt.child.redraw()




def row_style(row):
    if row["Similar Brand 1"].isnull():
        pd.Series('background-color: red', row.index)
    else:
        pd.Series('background-color: green', row.index)


def get_close_matches_icase(word, possibilities, *args, **kwargs):
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


def save_and_finalize(base_df, df, open_btn, save_button, frame, update_btn, undo_btn, prev_btn):

    for index, row in df.iterrows():
        if isinstance(row["Linked rows"], list):
            for i in row["Linked rows"]:
                if row["Alias"]:
                    base_df["Alias"][i-1] = row["Alias"]
                else:
                    print("Sheesh", row)
        else:
            if row["Alias"]:
                base_df["Alias"][index] = row["Alias"]
    # base_df.drop(columns=["Linked rows"],  inplace=True)

    base_df.to_csv(
        f'Brands_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv', index=False)
    showinfo(
        title='Output',  message="File created successfully"
    )
    save_button.pack_forget()
    undo_btn.pack_forget()
    update_btn.pack_forget()
    prev_btn.pack_forget()
    frame.pack_forget()
    open_btn.pack(expand=True)
    root.update()


def undo_df(pt):
    pt.undo()
    pt.redraw()
    root.update()

def goback(pt):
    global currentIndex
    if currentIndex-10 >= 0:
        currentIndex-=10
    else:
        currentIndex = 0
    pt.child.model.df = pt.model.df[currentIndex:currentIndex+10]
    pt.child.redraw()
def selected_column(selected_column,
                    input_records,
                    dataframe,
                    filename,
                    btn,
                    drop,
                    open_btn):
    canvas = Canvas(root, width=1200, height=800, bg="SpringGreen2")
    canvas.create_text(600, 350, text="Loading Data in the background",
                       fill="black", font=('Helvetica 15 bold'))
    canvas.pack(expand=True)
    btn.pack_forget()
    drop.pack_forget()
    root.update()
    groups = []
    my_brands = dataframe[selected_column].values

    input_records = input_records[-135:-100]
    my_brands = my_brands[-135:-100]

    for r in input_records:
        temp_record = r.copy()
        temp_record['Alias'] = ''
        i = r[selected_column]
        group = get_close_matches_icase(i, my_brands, cutoff=.75, n=500)
        r2_index = 0
        linkedRows = []
        for r2 in input_records:
            if r2[selected_column] in group:
                linkedRows.append(r2_index+1)
                r2 = None
            r2_index += 1

        if len(group) > 0:
            my_brands = [brand for brand in my_brands if brand not in group]
        for g in range(len(group)):
            temp_record[f"Similar Brand {g}"] = group[g]
        if len(linkedRows):
            temp_record["Linked rows"] = linkedRows
        groups.append(temp_record)

    canvas.pack_forget()
    root.update()
    base_df = pd.DataFrame(groups)
    base_df.dropna(how='all', inplace=True)
    base_df.dropna(how='all', inplace=True, axis=1)
    base_df['Alias'] = None
    base_df.drop(columns=["Similar Brand 0"], inplace=True)

    df = base_df
    frame = tk.Frame(root, height=800, width=1000)
    frame.pack(expand=True,side=tk.LEFT)
    pt = Table(frame, dataframe=df, width=1000, height=800)
    # pt.show()
    global currentIndex
    pt.createChildTable(pt.model.df[currentIndex:10], title="Shhehhhsh")
    
    frame1 = tk.Frame(root, height=800, width=200)
    frame1.pack(side=tk.LEFT)
    undo_button = ttk.Button(
        frame1,
        text='Undo actions',
        command=lambda: undo_df(pt)
    )
    # pt.se
    # pt.child.redraw()    
    # undo_button.grid(row=1,column=5)
    
    undo_button.pack(expand=True)
    update_csv_button = ttk.Button(
        frame1,
        text='Update Linked rows',
        command=lambda: update_df(
            pt, df, input_records, selected_column
        )
    )
    # update_csv_button.grid(row=2,column=5)

    update_csv_button.pack(expand=True)
    prev_btn = ttk.Button(
            frame1,
            text='Prev rows',
            command=lambda: goback(pt)
        )
        # update_csv_button.grid(row=2,column=5)

    prev_btn.pack(expand=True)
    save_button = ttk.Button(
        frame1,
        text='Save CSV',
        command=lambda: save_and_finalize(
            base_df, pt.model.df, open_btn, save_button, frame, update_csv_button, undo_button, prev_btn)
    )

    # save_button.grid(row=3,column=5)
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
    # csv_file['Alias'] = None

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


open_button = ttk.Button(
    root,
    text='Select CSV',
    command=lambda: select_file(csv_file, open_button)
)
open_button.pack(expand=True)
root.mainloop()
