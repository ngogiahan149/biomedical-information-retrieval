from tkinter import *
from nltk.stem import PorterStemmer, LancasterStemmer
def simpleSearch(text, entry, foreground ='red'):

    text.tag_remove('found', '1.0', END)
    keyword = entry.get()
    if keyword:
        idx = '1.0'
        idx = text.search(keyword, idx, nocase=1,
                        stopindex=END)
        if not idx: 
            return
        lastidx = '%s+%dc' % (idx, len(keyword))
        
        text.tag_add('found', idx, lastidx)
        idx = lastidx
        text.tag_config('found', foreground = foreground)
def searchFunc(frame, entry):
    for widget in frame.winfo_children():
        if widget.winfo_class() == 'Text':
            simpleSearch(widget, entry, foreground = 'red')
def PorterStemming(text):
    porter = PorterStemmer()
    print(porter.stem(text))

PorterStemming("cats")
