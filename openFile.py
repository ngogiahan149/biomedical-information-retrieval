from tkinter import *
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo
import xml.etree.ElementTree as ET
import pandas as pd
import json
from textSummarize import *

def open_xml():
    filetypes = (
        ('xml files', '*.xml'),
    )

    fileName = filedialog.askopenfile(
        title='Choose an xml file',
        initialdir='/',
        filetypes=filetypes)
    return fileName

def open_json():
    filetypes = (
        ('json files', '*.json'),
    )

    fileName = filedialog.askopenfile(
        title='Choose a json file',
        initialdir='/',
        filetypes=filetypes)
    #Choose JSON file
    fileName = open_json()  

    #Open JSON file
    f = open(fileName, encoding="utf8")    

    #Return JSON file as a dictionary
    data = json.load(f)     
    return data
def parse_xml():
    # filename = open_xml()
    tree = ET.parse(r'D:\NCKU\Biomedical Information Retrieval\HW1\Data\test1.xml')

    root = tree.getroot()
    cols = ["PMID", "Journal ISSN",  "Journal Title", "ISO Abbreviation", 
    "Article Title", "Language", "Abstract", "Author", "Keyword List", "Publication Type", "Journal Country"]
    rows = []
    for paper in root.findall('PubmedArticle'):  
        PMID = paper.find('MedlineCitation/PMID').text
        Article = paper.find("MedlineCitation/Article")
        JournalISSN = Article.find("Journal/ISSN").text
        JournalTitle = Article.find("Journal/Title").text
        ISOAbbreviation = Article.find("Journal/ISOAbbreviation").text
        ArticleTitle = Article.find('ArticleTitle').text
        AbstractList = Article.findall('Abstract/AbstractText')
        AuthorList = Article.findall('AuthorList/Author')
        Language = Article.find('Language').text
        PublicationTypeList = Article.findall('PublicationTypeList/PublicationType')
        JournalCountry = paper.find('MedlineCitation/MedlineJournalInfo/Country').text
        KeywordList = paper.findall('MedlineCitation/KeywordList/Keyword')
        # rows.append({
        #     "PMID": PMID, 
        #     "JournalISSN": JournalISSN,
        #     "JournalTitle": JournalTitle,
        #     "ISOAbbreviation": ISOAbbreviation,
        #     "ArticleTitle": ArticleTitle,
        #     "AbstractList": AbstractList,
        #     "AuthorList": AuthorList,
        #     "Language": Language,
        #     "PublicationTypeList": PublicationTypeList,
        # })
        rows.append([
            PMID, 
            JournalISSN,
            JournalTitle,
            ISOAbbreviation,
            ArticleTitle,
            Language,
         AbstractList,
            AuthorList,
            KeywordList,
            PublicationTypeList,
            JournalCountry,
        ])
    return rows, cols

def display_xml(frame, canvas):
    rows, cols = parse_xml()
    # scroll_canvas = Canvas(frame)
    # scroll_canvas = Canvas(frame)
    # scroll_canvas.place(relx=0.01, rely=0.01, relwidth = 1, relheight = 1)
    # vsb = Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)
    # vsb.place(relx=0.98, rely=0.006, relheight=1, width=100)
    
    # hsb = Scrollbar(frame, orient="horizontal", command=scroll_canvas.xview)
    # hsb.place(relx=0.005, rely=0.95, height=400, width=500)
    # scroll_canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    

    
    # # set column headings
    # for col in cols:
    #     listBox.column(col, anchor = CENTER, stretch= YES)
    #     listBox.heading(col, text=col)    
    

    # #insert data to rows in table
    # for i, (PMID, 
    #         JournalISSN,
    #         JournalTitle,
    #         ISOAbbreviation,
    #         ArticleTitle,
    #         Language,
    #         AbstractList,          
    #         AuthorList,
    #         KeywordList,
    #         PublicationTypeList,
    #         JournalCountry,
    #         ) in enumerate(rows, start = 1):
    #             listBox.insert("", "end", values=(PMID, JournalISSN, JournalTitle, ISOAbbreviation, ArticleTitle, Language, ', '.join([item.text for item in AbstractList]),
    #             ', '.join(['{0} {1}'.format(item.findall('ForeName')[0].text, item.findall('LastName')[0].text) for item in AuthorList]),
    #             ', '.join([item.text for item in KeywordList]),
    #             ', '.join([item.text for item in PublicationTypeList]),
    #             JournalCountry, 
    #             ))
    #             print(item.text for item in KeywordList)
    for i, (PMID, 
            JournalISSN,
            JournalTitle,
            ISOAbbreviation,
            ArticleTitle,
            Language,
            AbstractList,          
            AuthorList,
            KeywordList,
            PublicationTypeList,
            JournalCountry,
            ) in enumerate(rows, start = 1):
                Label(frame, text=ArticleTitle, wraplength=1050, font=("RobotoRoman Bold", 12, 'bold')).pack(side='top', fill='x')
                Label(frame, text=(', '.join(['{0} {1}'.format(item.findall('ForeName')[0].text, item.findall('LastName')[0].text) for item in AuthorList])), wraplength=1050, font=("RobotoRoman Regular", 10, 'italic')).pack(side='top', fill='x')
                Label(frame, text=(''.join('{0} {1} {2} {3}'.format("PMID: ", PMID, "       ISO Abbreviation: ", ISOAbbreviation)) ), wraplength=1050, font=("RobotoRoman Regular", 8), anchor = 'w', justify = LEFT).pack(side='top', fill='x')
                Label(frame, text='ABSTRACT', wraplength=1050, font=("RobotoRoman Bold", 10, 'bold')).pack(side='top', fill='x')
                Label(frame, text=(' '.join([item.text for item in AbstractList])), wraplength=1050,font=("RobotoRoman Regular", 10), anchor = 'w', justify= LEFT).pack(side='top', fill='x')
                Label(frame, text="Keywords", wraplength=1050,font=("RobotoRoman Regular", 10, 'bold'), anchor = 'w', justify= LEFT).pack(side='top', pady = 15)
                Label(frame, text=('; '.join([item.text for item in KeywordList])), wraplength=1050,font=("RobotoRoman Regular", 10), anchor = 'w', justify= LEFT).pack(side='top')
    # Number of sentences
    canvas.create_text(
        33,
        440.0,
        anchor="nw",
        text= count_sentences_xml(rows),
        fill="#EE6983",
        font=("RobotoCondensed Bold", 30 * -1),
        
    )
    
def display_json(frame, canvas):
    data = open_json() 

     #Create rows and columns for adding data
    cols = ["PMID", "Title",  "Authors", "Citation", 
    "Journal/Book", "Publication Year", "Create Date"]
    rows = []

    #Create scroll bar
    listBox = ttk.Treeview(frame, columns=cols, show='headings', selectmode = 'browse')
    listBox.place(relx=0.01, rely=0.01, relwidth = 1, relheight = 1)
    
    vsb = Scrollbar(frame, orient="vertical", command=listBox.yview)
    vsb.place(relx=0.98, rely=0.006, relheight=1, width=100)

    hsb = Scrollbar(frame, orient="horizontal", command=listBox.xview)
    hsb.place(relx=0.005, rely=0.95, height=400, width=500)

    listBox.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # set column headings
    for col in cols:
        listBox.column(col, anchor = CENTER, stretch= YES)
        listBox.heading(col, text=col)    
    

    #insert data to rows in table
    for item in data:
        listBox.insert("", "end", values=(
            item['PMID'], 
            item['Title'],
            item['Authors'],
            item['Citation'],
            item['Journal/Book'],
            item['Publication Year'],
            item['Create Date'],))
     
    return data