from tkinter import *
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo
import xml.etree.ElementTree as ET
import pandas as pd
import json
from textSummarize import *
import math
rows_result = []
counter_content = True

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
    return fileName
def parse_xml():
    filename = open_xml()
    tree = ET.parse(filename)

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
        rows_result.append([
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
        print(rows_result)
    return rows, cols

def display_xml(frame, canvas):
    global counter_content

    if (counter_content == True):
        width_content = 999
        counter_content = FALSE
    else:
        width_content = 1000
        counter_content = True
    for widget in frame.winfo_children():
        widget.destroy()

    mycanvas = Canvas(
        frame,
        bg="#FFF5E4",
        height=600,
        width=width_content,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    mycanvas.pack(side="left", fill="both", expand=True)
    # ADDING A SCROLLBAR
    myscrollbar = Scrollbar(frame, orient="vertical", command=mycanvas.yview)
    myscrollbar.pack(side="right", fill="y")

    mycanvas.configure(yscrollcommand=myscrollbar.set)
    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

    second_frame = Frame(mycanvas)
    mycanvas.create_window((0, 0), window=second_frame, anchor="nw")

    rows, cols = parse_xml()
    # scroll_canvas = Canvas(frame)
    # scroll_canvas = Canvas(frame)
    # scroll_canvas.place(relx=0.01, rely=0.01, relwidth = 1, relheight = 1)
    # vsb = Scrollbar(frame, orient="vertical", command=scroll_canvas.yview)
    # vsb.place(relx=0.98, rely=0.006, relheight=1, width=100)
    
    # hsb = Scrollbar(frame, orient="horizontal", command=scroll_canvas.xview)
    # hsb.place(relx=0.005, rely=0.95, height=400, width=500)
    # scroll_canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
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
            ) in enumerate(rows_result, start = 1):
                # Label(frame, text=ArticleTitle, wraplength=1050, font=("RobotoCondensed Bold", 12, 'bold'), background = 'white').pack(side='top', fill='x')
                # Label(frame, text=(', '.join(['{0} {1}'.format(item.findall('ForeName')[0].text, item.findall('LastName')[0].text) for item in AuthorList])), background = 'white', wraplength=1050, font=("RobotoRoman Regular", 10, 'italic')).pack(side='top', fill='x')
                # Label(frame, text=(''.join('{0} {1} {2} {3}'.format("PMID: ", PMID, "       ISO Abbreviation: ", ISOAbbreviation)) ), background = 'white', wraplength=1050, font=("RobotoRoman Regular", 8), anchor = 'w', justify = LEFT).pack(side='top', fill='x')
                # Label(frame, text=(''.join('{0} {1}'.format("Country: ", JournalCountry))), wraplength=1050,font=("RobotoRoman Regular", 8), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill = 'x')
                # Label(frame, text='ABSTRACT', wraplength=1050, font=("RobotoCondensed Bold", 10, 'bold'), background = 'white').pack(side='top', fill='x')
                # Label(frame, text=(' '.join([item.text for item in AbstractList])), wraplength=1050,font=("RobotoRoman Regular", 10), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill='x')
                # Label(frame, text=(''.join('{} {}'.format("Keywords: ", ', '.join([item.text for item in KeywordList])))), wraplength=1050,font=("RobotoRoman Regular", 10), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill = 'x')
                
                #Create Journal title
                journalTitleText = CreateTextbox(second_frame, 130, JournalTitle, 'center')
                journalTitleText.pack()
                journalTitleText.configure(font=("RobotoCondensed Bold", 12, 'underline bold'), background = 'white')
                
                #Create Article title
                articleTitleText = CreateTextbox(second_frame, 130, ArticleTitle, 'center')
                articleTitleText.pack()
                articleTitleText.configure(font=("RobotoCondensed Bold", 12, 'bold'), background = 'white')

                #Create Author
                authorName = ', '.join(['{0} {1}'.format(item.findall('ForeName')[0].text, item.findall('LastName')[0].text) for item in AuthorList])
                authorText = CreateTextbox(second_frame, 130, authorName, 'center')
                authorText.pack(fill='x')
                authorText.configure(font=("RobotoRoman Regular", 10, 'italic'), background = 'white')

                #Create PMID, ISO
                PMID = (''.join('{0} {1} {2} {3}'.format("PMID: ", PMID, "       ISO Abbreviation: ", ISOAbbreviation)) )
                pmidText = CreateTextbox(second_frame, 130, PMID, 'left')
                pmidText.pack(fill='x')
                pmidText.configure(font=("RobotoRoman Regular", 8), background = 'white')

                #Create Journal Country
                countryText = CreateTextbox(second_frame, 130, JournalCountry, 'left')
                countryText.pack(fill='x')
                countryText.configure(font=("RobotoRoman Regular", 8), background = 'white')


                #Create Abstract
                Label(second_frame, text='ABSTRACT', wraplength=1050, font=("RobotoCondensed Bold", 10, 'bold'), background = 'white').pack(side='top', fill='x')
                abstractContent= (' '.join([item.text for item in AbstractList]))
                abstractText = CreateTextbox(second_frame, 130, abstractContent, 'left')
                abstractText.pack(fill='x')
                abstractText.configure(font=("RobotoRoman Regular", 10), background = 'white')

                #Create Keyword
                keyword = (''.join('{} {}'.format("Keywords: ", ', '.join([item.text for item in KeywordList]))))
                keywordText = CreateTextbox(second_frame, 130, keyword, 'left')
                keywordText.pack(fill='x')
                keywordText.configure(font=("RobotoRoman Regular", 10), background = 'white')

                # Table of character, word, sentence count
                analysisFrame = LabelFrame(second_frame,  background='#850E35', foreground ='white')
                analysisFrame.pack(fill="both", expand="yes", pady = 10)

                # journalTitleNumOfChar, journalTitleNumOfWord, journalTitleNumOfSentence, journalTitleSummary = summarize(JournalTitle)
                # articleTitleNumOfChar, articleTitleNumOfWord, articleTitleNumOfSentence, articleTitleSummary = summarize(ArticleTitle)
                # abstractNumOfChar,abstractNumOfWord,abstractNumOfSentence, abstractSummary = summarize(' '.join([item.text for item in AbstractList]))
                # keywordNumOfChar, keywordNumOfWord, keywordNumOfSentence, keywordSummary = summarize(' '.join([item.text for item in KeywordList]))
                # authorNum = len(AuthorList)
                #
                # #Total analysis
                # total = ''.join('{} {} {} {}.'.format(JournalTitle, ArticleTitle, abstractContent, keyword))
                # totalNumOfChar, totalNumOfWord, totalNumOfSentence, totalSummary = summarize(total)
                #
                # ttk.Label(analysisFrame, text = ('Num of'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold'), anchor = 'w', justify=LEFT).grid(row=0, column=0, padx = 2, pady =5)
                # ttk.Label(analysisFrame, text = ('Characters'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=1, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = ('Words'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=2, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = ('Sentences'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=3, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = ('Summary'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=4, padx =2, pady =5, columnspan= 4)
                #
                # #Journal title analysis
                # ttk.Label(analysisFrame, text = 'Journal Title:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=1, column=0, padx =5, pady =5)
                # ttk.Label(analysisFrame, text = journalTitleNumOfChar, background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=1, column=1, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = journalTitleNumOfWord, background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=1, column=2, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = journalTitleNumOfSentence, background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=1, column=3, padx =2, pady =5)
                #
                # #Article title analysis
                # ttk.Label(analysisFrame, text = 'Artile Title:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=2, column=0, padx =5, pady =5)
                # ttk.Label(analysisFrame, text = articleTitleNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=2, column=1, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = articleTitleNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=2, column=2, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = articleTitleNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=2, column=3, padx =2, pady =5)
                #
                # #Abstract analysis
                # ttk.Label(analysisFrame, text = 'Abstract:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=3, column=0, padx =5, pady =5)
                # ttk.Label(analysisFrame, text = abstractNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=1, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = abstractNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=2, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = abstractNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=3, padx =2, pady =5)
                #
                # #Keyword analysis
                # ttk.Label(analysisFrame, text = 'Keyword:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=4, column=0, padx =5, pady =5)
                # ttk.Label(analysisFrame, text = keywordNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=4, column=1, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = keywordNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=4, column=2, padx =2, pady =5)
                # ttk.Label(analysisFrame, text = keywordNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=4, column=3, padx =2, pady =5)
                #
                # #Author analysis
                # ttk.Label(analysisFrame, text = 'Author:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=5, column=0, padx =5, pady =5)
                # ttk.Label(analysisFrame, text = '{} authors'.format(authorNum),background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=5, column=1, padx =2, pady =5, columnspan = 3)
                #
                # # #Total analysis
                # # ttk.Label(analysisFrame, text = 'Total', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=6, column=0, padx =5, pady =5)
                # # ttk.Label(analysisFrame, text = totalNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=6, column=1, padx =2, pady =5)
                # # ttk.Label(analysisFrame, text = totalNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=6, column=2, padx =2, pady =5)
                # # ttk.Label(analysisFrame, text = totalNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=6, column=3, padx =2, pady =5)
                #
                # #Summary content
                # ttk.Label(analysisFrame, text = totalSummary,  wraplength=700,background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=1, column=4, padx =5, pady =5, columnspan = 1, rowspan=5)

    # ttk.Label(analysisFrame, text = 'Article Title:', background='#454545', foreground ='white', font=("Courier", 10, 'underline italic')).grid(row=0, column=2, padx =5, pady =5)
    # ttk.Label(analysisFrame, text = '{} chars, {} words, {} sentences'.format(articleTitleNumOfChar,articleTitleNumOfWord,articleTitleNumOfSentence),background='#454545', foreground ='white').grid(row=0, column=3, padx =2, pady =5)

    # ttk.Label(analysisFrame, text = 'Abstract Text:', background='#454545', foreground ='white', font=("Courier", 10, 'underline italic')).grid(row=0, column=4, padx =5, pady =5)
    # ttk.Label(analysisFrame, text = '{} chars, {} words, {} sentences'.format(abstractTextNumOfChar,abstractTextNumOfWord,abstractTextNumOfSentence),background='#454545', foreground ='white').grid(row=0, column=5, padx =2, pady =5)

    # ttk.Label(analysisFrame, text = 'Author:', background='#454545', foreground ='white', font=("Courier", 10, 'underline italic')).grid(row=0, column=6, padx =5, pady =5)
    # ttk.Label(analysisFrame, text = len(AuthorList),background='#454545', foreground ='white').grid(row=0, column=7, padx =2, pady =5)

def display_json(frame):
    fileName = open_json()     
     #Open JSON file
    f = open(fileName.name, 'r', encoding="utf8")    

    #Return JSON file as a dictionary
    data = json.load(f)     
    for item in data:
        ArticleTitle = item['Title']
        AuthorList = item['Authors']
        AbstractList = item['Abstract']
        print(ArticleTitle)
        # pmid = item['PMID']
        # doi = item['DOI']
        # Citation = item['Citation']
        # Journal_Book = item['Journal/Book']
        # Publication_Year = item['Publication Year']
        # Create_Date = item['Create Date']

        #Create Article title
        articleTitleText = CreateTextbox(frame, 130, ArticleTitle, 'center')
        articleTitleText.pack()
        articleTitleText.configure(font=("RobotoCondensed Bold", 12, 'bold'), background = 'white')

        #Create Article title
        authorText = CreateTextbox(frame, 130, AuthorList, 'center')
        authorText.pack(fill='x')
        authorText.configure(font=("RobotoRoman Regular", 10, 'italic'), background = 'white')

        #Create Abstract
        Label(frame, text='ABSTRACT', wraplength=1050, font=("RobotoCondensed Bold", 10, 'bold'), background = 'white').pack(side='top', fill='x')
        abstractText = CreateTextbox(frame, 130, AbstractList, 'left')
        abstractText.pack(fill='x')
        abstractText.configure(font=("RobotoRoman Regular", 10), background = 'white')
        
        # Label(frame, text= AuthorList, background = 'white', wraplength=1050, font=("RobotoRoman Regular", 10, 'italic')).pack(side='top', fill='x')
        # Label(frame, text=(''.join('{0} {1} {2} {3}'.format("PMID: ", pmid, "       DOI: ", doi)) ), background = 'white', wraplength=1050, font=("RobotoRoman Regular", 10), anchor = 'w', justify = LEFT).pack(side='top', fill='x')
        # Label(frame, text=('Publication Year: {}'.format(Publication_Year)), wraplength=1050,font=("RobotoRoman Regular", 10), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill = 'x')
        # Label(frame, text=('Create Date: {}'.format(Create_Date)), wraplength=1050,font=("RobotoRoman Regular", 8), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill = 'x')
        # Label(frame, text='Citation', wraplength=1050, font=("RobotoCondensed Bold", 10, 'bold'), background = 'white').pack(side='top', fill='x')
        # Label(frame, text= Citation, wraplength=1050,font=("RobotoRoman Regular", 10), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill='x')
        # # Label(frame, text=(''.join('{} {}'.format("Keywords: ", ', '.join([item.text for item in KeywordList])))), wraplength=1050,font=("RobotoRoman Regular", 10), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill = 'x')
        # Label(frame, text=('Journal/Book: {}'.format(Journal_Book)), wraplength=1050,font=("RobotoRoman Regular", 10), background = 'white', anchor = 'w', justify= LEFT).pack(side='top', fill = 'x')

        # Table of character, word, sentence count
        analysisFrame = LabelFrame(frame,  background='#850E35', foreground ='white')
        analysisFrame.pack(fill="y", expand="yes", pady = 10, anchor = 's')
        articleTitleNumOfChar, articleTitleNumOfWord, articleTitleNumOfSentence, articleTitleSummary = summarize(ArticleTitle)
        abstractNumOfChar,abstractNumOfWord,abstractNumOfSentence, abstractSummary = summarize(AbstractList)
        authorNum = len(AuthorList.split(','))

        #Total analysis
        total = ''.join('{}. {}'.format(ArticleTitle, AbstractList))
        print(total)
        totalNumOfChar, totalNumOfWord, totalNumOfSentence, totalSummary = summarize(total)

        #Column name
        ttk.Label(analysisFrame, text = ('Num of'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold'), anchor = 'w', justify=LEFT).grid(row=0, column=0, padx = 2, pady =5)
        ttk.Label(analysisFrame, text = ('Characters'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=1, padx =2, pady =5)
        ttk.Label(analysisFrame, text = ('Words'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=2, padx =2, pady =5)
        ttk.Label(analysisFrame, text = ('Sentences'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=3, padx =2, pady =5)
        ttk.Label(analysisFrame, text = ('Summary'),background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=0, column=4, padx =2, pady =5, columnspan= 4)

        #Article analysis
        ttk.Label(analysisFrame, text = 'Artile Title:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=1, column=0, padx =5, pady =5)
        ttk.Label(analysisFrame, text = articleTitleNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=1, column=1, padx =2, pady =5)
        ttk.Label(analysisFrame, text = articleTitleNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=1, column=2, padx =2, pady =5)
        ttk.Label(analysisFrame, text = articleTitleNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=1, column=3, padx =2, pady =5)
        
        #Abstract analysis
        ttk.Label(analysisFrame, text = 'Abstract:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=2, column=0, padx =5, pady =5)
        ttk.Label(analysisFrame, text = abstractNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=2, column=1, padx =2, pady =5)
        ttk.Label(analysisFrame, text = abstractNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=2, column=2, padx =2, pady =5)
        ttk.Label(analysisFrame, text = abstractNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=2, column=3, padx =2, pady =5)
        # ttk.Label(analysisFrame, text = 'Keyword:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=3, column=0, padx =5, pady =5)
        # ttk.Label(analysisFrame, text = keywordNumOfChar,background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=1, padx =2, pady =5)
        # ttk.Label(analysisFrame, text = keywordNumOfWord,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=2, padx =2, pady =5)
        # ttk.Label(analysisFrame, text = keywordNumOfSentence,background='#850E35', foreground ='white',  font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=3, padx =2, pady =5)
        
        #Author analysis
        ttk.Label(analysisFrame, text = 'Author:', background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=3, column=0, padx =5, pady =5)
        ttk.Label(analysisFrame, text = '{} authors'.format(authorNum),background='#850E35', foreground ='white', font=("RobotoCondensed Bold", 11, 'bold')).grid(row=3, column=1, padx =2, pady =5, columnspan = 3)
        
        #Summary content
        ttk.Label(analysisFrame, text = totalSummary,  wraplength=700,background='#850E35', foreground ='white', font=("RobotoRoman Bold", 10, 'bold')).grid(row=1, column=4, padx =5, pady =5, columnspan = 1, rowspan=5)
    
        separator = Frame(frame, bd=10, relief='sunken', height=4, bg = "#EE6983")
        separator.pack(side='top', fill='x')

    # #insert data to rows in table
    # for item in data:
    #     listBox.insert("", "end", values=(
    #         item['PMID'], 
    #         item['Title'],
    #         item['Authors'],
    #         item['Citation'],
    #         item['Journal/Book'],
    #         item['Publication Year'],
    #         item['Create Date'],))
def CreateTextbox(parentWid, iWidth, textString, justify):
    lineCount = int(math.ceil(len(textString)/iWidth))
    newtextbox = Text(parentWid, height = lineCount, width=iWidth - 15, wrap = WORD, bg ='white', bd =0, padx = 15)
    newtextbox.tag_configure("tag_name", justify=justify)
    newtextbox.insert(INSERT, textString)
    newtextbox.tag_add("tag_name", "1.0", "end")
    newtextbox.config(state=DISABLED)
    return newtextbox