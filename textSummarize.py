from openFile import *
import nltk, re, heapq, string
from nltk.tokenize import sent_tokenize
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer
#nltk.download('stopwords')
text = "in can't . i? ? in"
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

def preprocessing(text):
    # Removing Square Brackets and Extra Spaces
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', text)
    formatted_article_text = re.sub(r'\s+', ' ', text)
    return formatted_article_text, text

def summarize(string):
    formatted_article_text, text = preprocessing(string)
    #Convert text to sentence list
    sentence_list = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    #Find word scores
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word.lower() not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    #Find character total
    charNum = sum(len(word) for word in nltk.word_tokenize(formatted_article_text))

    #Find word total
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    wordNum = len(tokens)

    # #Find weighted frequency
    # maximum_frequncy = max(word_frequencies.values())
    # word_weighted = {}
    # for word in word_frequencies.keys():
    #     word_weighted[word] = (word_frequencies[word]/maximum_frequncy)
    
    #Find total sentence
    sentenceNum = len(sentence_list)

    #Find sentence scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    # print("Total sentences", sum(len(sent for sent in sentence_scores)))
    #Select just 30% for summary
    select_length = int(len(sentence_scores)*0.3) 
    summary_sentences = heapq.nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    return charNum, wordNum, sentenceNum, summary
