import tkinter as tk
from tkinter import ttk

root = tk.Tk()
tree = ttk.Treeview(root, show = "headings")
tree.pack()
tree.heading('A', 'B')
tree.insert("", "end", "A", text="A")
tree.insert("", "end", "B", text="B")
tree.insert("A", "end", "A.1", text="A.1")
tree.insert("A.1", "end", "A.1.1", text="A.1.1")
tree.insert("A", "end", "A.2", text="A.2")
tree.insert("A.2", "end", "A.2.1", text="A.2.1")
tree.insert("A.2", "end", "A.2.2", text="A.2.2")
tree.insert("B", "end", "B.1", text="B.1")
tree.insert("B", "end", "B.2", text="B.2")
tree.insert("B.1", "end", "B.1.1", text="B.1.1")

def open_children(parent):
    tree.item(parent, open=True)
    for child in tree.get_children(parent):
        open_children(child)

def handleOpenEvent(event):
    open_children(tree.focus())

tree.bind('<<TreeviewOpen>>', handleOpenEvent)
root.mainloop()