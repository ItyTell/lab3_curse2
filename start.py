from tkinter import *
root = Tk()
root.minsize(720, 600)

def f():
    print(list.get(list.curselection()))


list = Listbox(root, selectmode=SINGLE, width=15, height=5)
list.pack(pady=100)




for i in ['Python', 'Java', 'C', 'C++']:
    list.insert(END, i)
butt = Button(root, text='Друкувати', command=f)
butt.pack(side=LEFT, padx=5)
root.mainloop()
