from tkinter import *
import re

# lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field', 'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']
lista = ['Update in COVID-19 in the intensive care unit from the 2020 HELLENIC Athens International symposium', 'Jordi Rello\xa01,\xa0Mirko Belliato\xa02,\xa0Meletios-Athanasios Dimopoulos\xa03,\xa0Evangelos J Giamarellos-Bourboulis\xa04,\xa0Vladimir Jaksic\xa05,\xa0Ignacio Martin-Loeches\xa06,\xa0Iosif Mporas\xa07,\xa0Paolo Pelosi\xa08,\xa0Garyphallia Poulakou\xa09,\xa0Spyridon Pournaras\xa010,\xa0Maximiliano Tamae-Kakazu\xa011,\xa0Jean-François Timsit\xa012,\xa0Grant Waterer\xa013,\xa0Sofia Tejada\xa014,\xa0George Dimopoulos\xa015', 'The 2020 International Web Scientific']

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w.lower())]

if __name__ == '__main__':
    window = Tk()
    window.geometry("1300x800")
    window.configure(bg = "#FFF5E4")

    #set up GUI with canvas
    canvas = Canvas(
        window,
        bg = "#FFF5E4",
        height = 800,
        width = 1300,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    
    canvas.create_rectangle(
        11.0,
        18.0,
        163.0,
        450.0,
        fill="#FFFFFF",
        outline="")
    # Rectangle for file content
    
    frame = Frame(canvas, width = 1000, height = 400, background = "white")
    frame.place(
        x = 191.0,
        y = 68.0,
    )
    entry = AutocompleteEntry(lista, window)
    entry.place(
            x=200,
            y=100,
            width=245.0,
            height=20.0,
        )
    print(entry.get())
    # Button(text='nothing').grid(row=1, column=0)
    # Button(text='nothing').grid(row=2, column=0)
    # Button(text='nothing').grid(row=3, column=0)

    window.mainloop()