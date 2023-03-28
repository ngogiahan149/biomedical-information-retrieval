import re, collections, nltk
import numpy as np
import matplotlib.pyplot as plt
# from scipy import special
s = "string string. With. Punctuation? hello \n hello, hello"
def removePunc(text):
    return re.sub(r'[^\w\s]','',text).lower()
def removeStopWords(text):
    # Remove stop words using stopwords from Spacy library
    text = text.split()
    # sp = spacy.load('en_core_web_lg')
    # all_stopwords = sp.Defaults.stop_words
    all_stopwords = nltk.corpus.stopwords.words('english')
    new_stopwords = ["1", "2", "3", "4", "5", "6", "7", "8"]
    all_stopwords.extend(new_stopwords)
    # print(stopwords)
    word_without_stopword = [word for word in text if word not in all_stopwords]
    return word_without_stopword
def topFrequencyWord(text, top):
    #Remove punctuation
    text = removePunc(text)
    
    word_without_stopword = removeStopWords(text)

    #Calculate top frequency word
    counts = collections.Counter(word_without_stopword)
    return counts.most_common(top)
def createZipfTable(top_frequency):
    zipf_table = []
    for index, (word, frequency) in enumerate(top_frequency, start = 1):
        if index == 1:
            top_count = frequency
        zipf_table.append({
            "rank": index,
            "word": word,
            "actual_frequency": frequency,
            "expected_frequency": top_count/index})
    return zipf_table
def createChart(plot, table, title):    # %% Python visualization with pyplot
    plot.set_ylabel("Frequency")
    plot.tick_params('x', labelrotation = 50, labelsize = 7)
    # plot.xticks(rotation=90)    #to rotate x-axis values
    plot.plot([item['word'] for item in table], [item['expected_frequency'] for item in table], 
        marker='o', markerfacecolor='blue', markersize = 6, color='skyblue', linewidth = 2, label = 'Expected frequency')
    plot.bar([item['word'] for item in table], [item['actual_frequency'] for item in table], color = 'olive', label = 'Actual frequency')
    plot.legend(fontsize = 5)
    plot.set_title(title)

