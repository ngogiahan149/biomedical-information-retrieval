from tkinter import filedialog
from tkinter.messagebox import showinfo

def open_xml():
    filetypes = (
        ('xml files', '*.xml'),
    )

    filename = filedialog.askopenfile(
        title='Choose an xml file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
def open_json():
    filetypes = (
        ('json files', '*.json'),
    )

    filename = filedialog.askopenfile(
        title='Choose a json file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
