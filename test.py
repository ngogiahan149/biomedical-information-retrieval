from tkinter import * 
root = Tk()
text = Text(root)
text.insert("abc")
print(text.winfo_class())