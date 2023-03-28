from tkinter import *
import os
from load_word2vec import *


#Function
# def OpenModel(event):
#     filetypes = (
#         ('model files', "*"),
#     )

#     filePath = filedialog.askopenfile(
#         title='Choose a model file',
#         initialdir='/',
#         filetypes=filetypes)
#     if filePath:
#         realpath = os.path.abspath(filePath.name)
#         print(realpath)
#         tb_SelectModel.delete(0, 'end')
#         tb_SelectModel.insert(END, realpath)

#----------Main screen-------------
window = Tk()
window.title("Word2Vec")
window.resizable(True, True)  # This code helps to disable windows from resizing
window.configure(bg = "white")

# Create frames
wd_width = 500
wd_height = 300

# child frames = input, model, predict
ipframe = Frame(window, width=wd_width, height=2/5*wd_height - 10)
ipframe.grid(row=0, column=0, padx=5, pady=5)

modelframe = Frame(window)
modelframe.grid(row=1, column=0, padx=5, pady=5)

predictframe = Frame(window)
predictframe.grid(row=2, column=0, padx=5, pady=5)

# add elements to frames
#---Input frame-------------------------------------------
# lb_InputText = Label(ipframe, text='Input text in vocab:')
# lb_InputText.grid(row=0, column=0, padx=5, pady=5)

lb_CompareText = Label(ipframe, text='Input text not in vocab:')
lb_CompareText.grid(row=1, column=0, padx=5, pady=5)

# lb_SelectModel = Label(ipframe, text='Choose model:')
# lb_SelectModel.grid(row=2, column=0, padx=5, pady=5)


# Textbox = Entry()
# tb_InputText = Entry(ipframe, width=100)
# tb_InputText.grid(row=0, column=1, padx=5, pady=5, columnspan=4)

# Textbox = Entry()
tb_InputSpecialText = Entry(ipframe, width=100)
tb_InputSpecialText.grid(row=1, column=1, padx=5, pady=5, columnspan=4)

#Load model
fasttext_cbow = FastText.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\fastcbow_6205doc_5winsize_200epochs")
fasttext_skipgram = FastText.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\fastskipgram_6205doc_5winsize_200epochs")

skipgram = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\skipgram_6205doc_5winsize_200epochs")
cbow = gensim.models.Word2Vec.load(r"D:\NCKU\Biomedical Information Retrieval\HW1\Model\cbow_6205doc_5winsize_200epochs")
btn_Check= Button(
    ipframe, 
    width=10,
    borderwidth=0,
    highlightthickness=0,
    text = "Check",
    activebackground = '#4F0B21',
    activeforeground = 'white',
    relief="flat",
    background = '#850E35',
    fg = 'white',
    font = ('RobotoRoman Regular', 8, 'bold'),
    
    #Version 1 with compare 2 sentences
    # command = lambda: Analyze(tb_InputText.get(), tb_CompareText1.get(), tb_CompareText2.get(), 
    #     modelframe, tb_SelectModel.get(), predictframe)
    command = lambda: Check(tb_InputSpecialText.get(), modelframe, predictframe, fasttext_cbow, fasttext_skipgram, cbow, skipgram)
    )
btn_Check.grid(row=2, column=2, padx=5, pady=5)
# tb_CompareText1 = Entry(ipframe, width=50)
# tb_CompareText1.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

# tb_CompareText2 = Entry(ipframe, width=50)
# tb_CompareText2.grid(row=1, column=3, padx=5, pady=5,columnspan=2)

# Textbox = Entry()
# tb_SelectModel = Entry(ipframe, width=50)
# tb_SelectModel.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
# tb_SelectModel.bind("<1>", OpenModel)
# btn_AnalyzeModel = Button(
#     ipframe, 
#     width=10,
#     borderwidth=0,
#     highlightthickness=0,
#     text = "Analyze",
#     activebackground = '#4F0B21',
#     activeforeground = 'white',
#     relief="flat",
#     background = '#850E35',
#     fg = 'white',
#     font = ('RobotoRoman Regular', 8, 'bold'),
    
#     #Version 1 with compare 2 sentences
#     # command = lambda: Analyze(tb_InputText.get(), tb_CompareText1.get(), tb_CompareText2.get(), 
#     #     modelframe, tb_SelectModel.get(), predictframe)
#     command = lambda: Analyze(tb_InputText.get(), modelframe, tb_SelectModel.get(), predictframe, tb_InputSpecialText.get())
#     )
# btn_AnalyzeModel.grid(row=2, column=3, padx=5, pady=5)
# btn_AnalyzeAllModel = Button(
#     ipframe, 
#     width=10,
#     borderwidth=0,
#     highlightthickness=0,
#     text = "Analyze all",
#     activebackground = '#4F0B21',
#     activeforeground = 'white',
#     relief="flat",
#     background = '#850E35',
#     fg = 'white',
#     font = ('RobotoRoman Regular', 8, 'bold'),

#     #Version 1 with compare 2 sentences
#     # command = lambda: AnalyzeAll(tb_InputText.get(), tb_CompareText1.get(), tb_CompareText2.get(), modelframe, predictframe)
#     command = lambda: Analyze(tb_InputText.get(), modelframe, tb_SelectModel.get(), predictframe, tb_InputSpecialText.get())
#     )
# btn_AnalyzeAllModel.grid(row=2, column=4, padx=5, pady=5)
# btn_SelectAllModel = Button(
#     ipframe, 
#     width=25,
#     borderwidth=0,
#     highlightthickness=0,
#     text = "Choose all models",
#     activebackground = '#4F0B21',
#     activeforeground = 'white',
#     relief="flat",
#     background = '#850E35',
#     fg = 'white',
#     font = ('RobotoRoman Regular', 8, 'bold'),)
# btn_SelectAllModel.grid(row=2, column=2, padx=5, pady=5)
#---End Input frame---------------------------------------

# End window
window.state("zoomed")
window.mainloop()