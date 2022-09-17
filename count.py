from openFile import *
import nltk
from nltk.tokenize import sent_tokenize

def count_sentences_xml(rows):

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
        sentences = (' '.join([item.text for item in AbstractList]))
        number_of_sentences = sent_tokenize(sentences)
    return len(number_of_sentences)

