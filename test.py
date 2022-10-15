# from multiprocessing import Process, Manager
# # x=

# def dothing(L, i, x):  # the managed list `L` passed explicitly.
#     # global x
#     for j in range(5):
#         text = "Process " + str(i) + ", Element " + str(j)
#         if len(x)>0:
#             print(x.pop())
#         L.append(text)

# L = []
# x=[] 
# if __name__ == "__main__":
#     with Manager() as manager:
#         L = manager.list()  # <-- can be shared between processes.
#         x = manager.list([1,2,4,6,7,8,9])
#         processes = []

#         for i in range(5):
#             p = Process(target=dothing, args=(L,i, x))  # Passing the list
#             p.start()
#             processes.append(p)

#         for p in processes:
#             p.join()

#         L = list(L) 
#         x = list(x)
        
# print(L)
# print("numbers", x)
# import pandas as pd
# df = pd.read_csv("brand_sim_75_500.csv")

# df.dropna(how='all', inplace=True)

# df.to_csv("removed_empty.csv", index=False)


from tkinter import *
from pandastable import Table, TableModel
from tkinter import ttk

class TestApp(Frame):
        """Basic test frame for the table"""
        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400')
            self.main.title('Table app')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            df = TableModel.getSampleData()
            self.table = pt = Table(f, dataframe=df)
            pt.show()
            return

app = TestApp()
#launch the app

open_button = ttk.Button(
    app,
    text='Select CSV',
    command=lambda: print("sdf")
)


open_button.pack(expand=True)

app.mainloop()