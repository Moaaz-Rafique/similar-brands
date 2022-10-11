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
import pandas as pd
df = pd.read_csv("brand_sim_75_500.csv")

df.dropna(how='all', inplace=True)

df.to_csv("removed_empty.csv", index=False)


