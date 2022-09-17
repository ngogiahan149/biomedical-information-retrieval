from openFile import *
import nltk, re, heapq, string
from nltk.tokenize import sent_tokenize
 
#nltk.download('stopwords')
text = "In late, summer 1945. i, was you and me a child. Hi; I can't. I'm"
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
    
    print('-------------------\n', formatted_article_text)
    #Convert text to sentence list
    sentence_list = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    #Find word scores
    word_frequencies = {}
    print(stopwords)
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    format_word_frequencies = list(filter(lambda token: token not in string.punctuation, word_frequencies))
    print("Word frquency: ", format_word_frequencies)
    print("Total Word", len(format_word_frequencies))
    #Find character scores and total
    char_frequencies = {}
    for char in format_word_frequencies:
        if char not in char_frequencies.keys():
            char_frequencies[char] = 1
        else:
            char_frequencies[char] += 1
    print("Character frquency: ", char_frequencies)
    print("Total characters", len(char_frequencies))
    #Find weighted frequency
    maximum_frequncy = max(word_frequencies.values())

    word_weighted = {}
    for word in word_frequencies.keys():
        word_weighted[word] = (word_frequencies[word]/maximum_frequncy)
    print("Word weighted: ", word_weighted)

    

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
    print("sentence scores ", sentence_scores)
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    print(summary)
    return word_frequencies, 
preprocessing(text)                        