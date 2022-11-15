from tkinter import *
import os
from load_word2vec import *
from DocumentSimilarity import *
#Define Path
lung_cancer_path = r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_LungCancer.json"
brain_cancer_path = r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_BrainCancer.json"
gastric_cancer_path = r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_GastricCancer.json"
alzheimer_path = r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_Alzheimer.json"
diabetes_path = r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_Diabetes.json"

#----------Main screen-------------
window = Tk()
window.title("TF-IDF")
window.resizable(True, True)  # This code helps to disable windows from resizing
window.configure(bg = "white")

# Create frames
wd_width = 500
wd_height = 300

# child frames = input, model, predict
ipframe = Frame(window, width=wd_width, height=2/5*wd_height - 10)
ipframe.grid(row=0, column=0, padx=5, pady=5)

modelframe = Frame(window, width=wd_width, height=2/5*wd_height - 10)
modelframe.grid(row=1, column=0, padx=5, pady=5)

canvas = Canvas(modelframe, width=1200, height = 500)
scrollbar = Scrollbar(modelframe, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, width=1400, height=500, padx = 10, bg = 'white')

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

predictframe = Frame(window)
predictframe.grid(row=2, column=0, padx=5, pady=5)

inputLabel = Label(ipframe, text = "Input", anchor = 'w')
inputLabel.grid(row = 1, column = 0, padx=5, pady=5, sticky = "W")

# Textbox = Entry()
inputText = Entry(ipframe, width=100)
inputText.grid(row=1, column=1, padx=5, pady=5, columnspan=4)

chooseCategory = Label(ipframe, text = "Choose category to search")
chooseCategory.grid(row = 2, column = 0, padx=5, pady=5)

LungCancerButton = Button(ipframe, 
                            width=12,
                            borderwidth=0,
                            highlightthickness=0,
                            text = "Lung Cancer",
                            activebackground = '#4F0B21',
                            activeforeground = 'white',
                            relief="flat",
                            background = '#850E35',
                            fg = 'white',
                            font = ('RobotoRoman Regular', 8, 'bold'),
                            command = lambda: rank_corpus(lung_cancer_path, inputText.get(), scrollable_frame))
LungCancerButton.grid(row = 2, column = 1)

BrainCancerButton = Button(ipframe, 
                            width=12,
                            borderwidth=0,
                            highlightthickness=0,
                            text = "Brain Cancer",
                            activebackground = '#4F0B21',
                            activeforeground = 'white',
                            relief="flat",
                            background = '#850E35',
                            fg = 'white',
                            font = ('RobotoRoman Regular', 8, 'bold'),
                            command = lambda: rank_corpus(brain_cancer_path, inputText.get(), scrollable_frame))
BrainCancerButton.grid(row = 2, column = 2,)

GastricCancerButton = Button(ipframe, 
                            width=12,
                            borderwidth=0,
                            highlightthickness=0,
                            text = "Gastric Cancer",
                            activebackground = '#4F0B21',
                            activeforeground = 'white',
                            relief="flat",
                            background = '#850E35',
                            fg = 'white',
                            font = ('RobotoRoman Regular', 8, 'bold'),
                            command = lambda: rank_corpus(gastric_cancer_path, inputText.get(), scrollable_frame))
GastricCancerButton.grid(row = 2, column = 3)

AlzheimerButton = Button(ipframe, 
                            width=12,
                            borderwidth=0,
                            highlightthickness=0,
                            text = "Alzheimer",
                            activebackground = '#4F0B21',
                            activeforeground = 'white',
                            relief="flat",
                            background = '#850E35',
                            fg = 'white',
                            font = ('RobotoRoman Regular', 8, 'bold'),
                            command = lambda: rank_corpus(alzheimer_path, inputText.get(), scrollable_frame))
AlzheimerButton.grid(row = 2, column = 4)

DiabetesButton = Button(ipframe, 
                            width=12,
                            borderwidth=0,
                            highlightthickness=0,
                            text = "Diabetes",
                            activebackground = '#4F0B21',
                            activeforeground = 'white',
                            relief="flat",
                            background = '#850E35',
                            fg = 'white',
                            font = ('RobotoRoman Regular', 8, 'bold'),
                            command = lambda: rank_corpus(diabetes_path, inputText.get(), scrollable_frame))
DiabetesButton.grid(row = 2, column = 5)

# AllButton = Button(ipframe, 
#                             width=12,
#                             borderwidth=0,
#                             highlightthickness=0,
#                             text = "All",
#                             activebackground = '#4F0B21',
#                             activeforeground = 'white',
#                             relief="flat",
#                             background = '#850E35',
#                             fg = 'white',
#                             font = ('RobotoRoman Regular', 8, 'bold'),
#                             command = lambda: All(inputText.get(), scrollable_frame))
# AllButton.grid(row = 2, column = 5)


# End window
window.state("zoomed")
window.mainloop()