from tkinter import *
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo
import xml.etree.ElementTree as ET
import pandas as pd
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
    return filename
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
    return filename
def parse_xml():
    filename = open_xml()
    tree = ET.parse(filename)

    root = tree.getroot()
    cols = ["PMID", "Journal ISSN",  "Journal Title", "ISO Abbreviation", 
    "Article Title", "Language", "Abstract", "Author", "Publication Type", "Journal Country", "Keyword List"]
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
            PublicationTypeList,
            JournalCountry,
            KeywordList,
        ])
    return rows, cols
def display_xml(frame):
    rows, cols = parse_xml()
    # for y in range(len(rows)+1):
    #         for x in range(len(cols)):
    #             if y==0:
    #                 e=Label(frame, font=("RobotoRoman Regular", 9 * -1),bg='light blue',justify='center', text = cols[x])
    #                 e.grid(column=x, row=y)
    #                 e.insert(0,cols[x])
    #             else:
    #                 e=Label(frame, text = rows[y-1][x], height = 3, width = 7, padx = 2, pady = 2)
                  
    #                 e.grid(column=x, row=y)
    
    listBox = ttk.Treeview(frame, columns=cols, show='headings', selectmode = 'browse')
    listBox.place(relx=0.01, rely=0.01, width = 430, height = 700)
    
    vsb = Scrollbar(frame, orient="vertical", command=listBox.yview)
    vsb.place(relx=0.98, rely=0.006, height=500, width=100)

    hsb = Scrollbar(frame, orient="horizontal", command=listBox.xview)
    hsb.place(relx=0.005, rely=0.95, height=400, width=500)

    listBox.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    # set column headings
    for col in cols:
        listBox.column(col, anchor = CENTER, stretch= YES)
        listBox.heading(col, text=col)    
    

    #set rows data
    for i, (PMID, 
            JournalISSN,
            JournalTitle,
            ISOAbbreviation,
            ArticleTitle,
            Language,
            AbstractList,
            AuthorList,
            PublicationTypeList,
            JournalCountry,
            KeywordList) in enumerate(rows, start = 1):
                listBox.insert("", "end", values=(PMID, JournalISSN, JournalTitle, ISOAbbreviation, ArticleTitle, Language, ', '.join([item.text for item in AbstractList]),
                ', '.join(['{0} {1}'.format(item.findall('ForeName')[0].text, item.findall('LastName')[0].text) for item in AuthorList]),
                ', '.join([item.text for item in PublicationTypeList]),
                JournalCountry, ', '.join([item.text for item in KeywordList]),
                ))
                print(item.text for item in KeywordList)
                # journalissn = listBox.insert("", "end", text= JournalISSN)
                # isoabbreviation = listBox.insert("", "end", text= ISOAbbreviation)
                # articletitle = listBox.insert("", "end", text=ArticleTitle)
                # language = listBox.insert("", "end", text=Language)
                # abstractlist = listBox.insert("", "end", values = 'abstract_list', open = True)
                # authorlist = listBox.insert("", "end", values = 'author_list', open = True)
                # publicationtypelist = listBox.insert("", "end", values = '', open = True)
                # for item in AbstractList:
                #     print(item.text)
                #     print('day la lan', i)
                #     abstract = listBox.insert(abstractlist, "end", text = item.text)
                # for item in AuthorList:
                #     print(item.text)
                #     name = '{0}.{1}'.format(item.findall('ForeName')[0].text, item.findall('LastName')[0].text)
                #     authorname = listBox.insert(authorlist, "end", values = name)
                # for item in PublicationTypeList:
                #     print(item.text)
                #     publicationtype = listBox.insert(publicationtypelist, "end", values = item.text)
                # listBox.insert("", 6, text = "Abstract_list", values="stract", open = True)  
                # for item in AbstractList:
                #     print(item.text)
                #     listBox.insert("Abstract List", "end", text = "Abstract", values=item.text, open = True)
    
