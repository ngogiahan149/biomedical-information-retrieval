from nltk.stem import PorterStemmer
import re, collections, nltk, heapq
from nltk.tokenize import  sent_tokenize
import nltk, json, math
nltk.download('punkt')
nltk.download('stopwords')
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from word2vec import InputPreprocess
from tkinter import *

def TermPreprocess(text):
    result = []
    word = InputPreprocess(text)
    porter = PorterStemmer()
    for term in word:
        stemmedWord = porter.stem(term)
        result.append(stemmedWord)
    return result

def find_keywordset(query, all_docs):
  word_set = []
  doc_set = []
  word_index = {}
  all_docs.insert(0, query)
  for doc in all_docs:
      words_sentence = []
      for sent in sent_tokenize(doc):
        words = TermPreprocess(sent)
        for word in words:
          words_sentence.append(word)
          if word not in word_set:
            word_set.append(word)
      doc_set.append(words_sentence)
  word_set = set(word_set)
  for i, word in enumerate(word_set):
        word_index[word] = i
  return word_set, doc_set, word_index

# Count max tf
def most_term_frequency(document):
  most_tf = 0
  for word in document:
    tf = term_frequency(document, word)
    if most_tf <= tf:
      most_tf = tf
  return most_tf

#Normal tf
def term_frequency(document, term):
    N = len(document)
    occurence = len([token for token in document if token == term])
    return occurence/N

#Logarithm tf
def logarithm_term_frequency(document, term):
    tf = term_frequency(document, term)
    return 1 + np.log(tf)

#Augmented tf
def augmented_term_frequency(document, term):
    tf = term_frequency(document, term)
    most_tf = most_term_frequency(document)
    return 0.5 + (0.5*tf)/most_tf

#Count number of documents contain each keyword
def count_dict(word_set, doc_set):
    count_dict = {}
    for word in word_set:
        count_dict[word] = 0
    for sent in doc_set:
        for word in sent:
            count_dict[word] += 1
    return count_dict

#IDF
def inverse_document_frequency(word, word_count, doc_set):
    """
    Calculate the inverse document frequency of each word in the corpus.
    """
    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    return np.log(len(doc_set) / word_occurance)

#TF-IDF
def tf_idf(word_set, word_index, document, doc_set, function_term_frequency):
    """
    Calculate the TF-IDF of each sentence in the corpus.
    """
    word_count = count_dict(word_set, doc_set)
    vec = np.zeros((len(word_set),))
    for word in document:
        tf = function_term_frequency(document, word)
        idf = inverse_document_frequency(word, word_count, doc_set)
        vec[word_index[word]] = tf * idf
    return vec

def all_tfidf_vectors(word_set, word_index, doc_set, function_term_frequency):
    all_vectors = []
    for index, doc in enumerate(doc_set):
        vec = tf_idf(word_set, word_index, doc, doc_set, function_term_frequency)
        all_vectors.append(vec)
    return all_vectors

def rank_corpus(fileName, query, modelframe):
    for widget in modelframe.winfo_children():
            widget.destroy()
    #Open json file
    f = open(fileName, 'r', encoding="utf8")  
    data = json.load(f)  
    data_after_join = []
    #Get all total text for eact document   
    for index, item in enumerate(data):
        ArticleTitle = item["Title"]
        Abstract = item["Abstract"]
        total = ''.join('{}. {}'.format(ArticleTitle, Abstract))
        data_after_join.insert(index, total)
    normal_tfidf_title = CreateTextbox(modelframe, 80, "Normal TF-IDF", 'center')
    normal_tfidf_title.grid(row = 0, column = 0)
    normal_tfidf_title.configure(font = ("RobotoCondensed Bold", 10, 'bold'), fg = 'red')

    logarithm_tfidf_title = CreateTextbox(modelframe, 80, "Logarithm TF-IDF", 'center')
    logarithm_tfidf_title.grid(row = 0, column = 1)
    logarithm_tfidf_title.configure(font = ("RobotoCondensed Bold", 10, 'bold'), fg = 'red')

    augmented_tfidf_title = CreateTextbox(modelframe, 80, "Augmented TF-IDF", 'center')
    augmented_tfidf_title.grid(row = 0, column = 2)
    augmented_tfidf_title.configure(font = ("RobotoCondensed Bold", 10, 'bold'), fg = 'red')


    #Add query to data and find word_set, doc_set, # of word existed in all documents
    word_set, doc_set, word_index = find_keywordset(query, data_after_join)
    set_function_tf = [term_frequency, logarithm_term_frequency, augmented_term_frequency]
    j = 0
    for function_tf in set_function_tf:
        print(function_tf)
        i = 1
        #Create TF-IDF vectors of all words
        all_vectors = all_tfidf_vectors(word_set, word_index, doc_set, function_tf)
        all_vectors = np.array(all_vectors)

        #Reshape query to calculate cosine similarity
        query = np.array(all_vectors[0]).reshape(1, -1)

        #Calculate cosine similarity
        initial_cosine_vector = cosine_similarity(query, all_vectors)
        
        #Remove the score of comparing query to query
        initial_cosine_vector_1D = np.delete(initial_cosine_vector[0], 0)

        #Add index to the list of cosine
        sorted_cosine_vector = [(index, item) for index, item in enumerate(initial_cosine_vector_1D)]

        #Sorted the cosine list
        sorted_cosine_vector = heapq.nlargest(10, sorted_cosine_vector, key = lambda list: list[1])
        for index, item in sorted_cosine_vector:
            ArticleTitle = data[index]["Title"]
            Abstract = data[index]["Abstract"]
            
            articleTitleText = CreateTextbox(modelframe, 80, ArticleTitle, 'center')
            articleTitleText.grid(row = i, column = j)
            articleTitleText.configure(font = ("RobotoCondensed Bold", 9, 'bold'))
            
            abstractText = CreateTextbox(modelframe, 80, Abstract, 'left')
            abstractText.grid(row = i+1, column = j)
            abstractText.configure(font = ("RobotoCondensed Bold", 8))

            # similarityScore = CreateTextbox(modelframe, 80, "Similarity: {}".format(item), 'left')
            # similarityScore.grid(row = i+2, column = j)
            # similarityScore.configure(font = ("RobotoCondensed Bold", 8))
            print(data[index]["Title"])
            i += 2
        j += 1

def All(query, modelframe):
    for widget in modelframe.winfo_children():
            widget.destroy()
    #Open json file
    all_path = [r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_LungCancer.json",
    r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_BrainCancer.json",
    r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_GastricCancer.json",
    r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_Alzheimer.json",
    r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_Diabetes.json"]
    data_after_join = []
    data_before_join = []
    i = 0
    for path in all_path:
        f = open(path, 'r', encoding="utf8")  
        data = json.load(f)  
        #Get all total text for eact document   
        for index, item in enumerate(data):
            ArticleTitle = item["Title"]
            Abstract = item["Abstract"]
            total = ''.join('{}. {}'.format(ArticleTitle, Abstract))
            data_after_join.insert(i, total)
            i += 1
        data_before_join.append(data)
    normal_tfidf_title = CreateTextbox(modelframe, 80, "Normal TF-IDF", 'center')
    normal_tfidf_title.grid(row = 0, column = 0)
    normal_tfidf_title.configure(font = ("RobotoCondensed Bold", 10, 'bold'), fg = 'red')

    logarithm_tfidf_title = CreateTextbox(modelframe, 80, "Logarithm TF-IDF", 'center')
    logarithm_tfidf_title.grid(row = 0, column = 1)
    logarithm_tfidf_title.configure(font = ("RobotoCondensed Bold", 10, 'bold'), fg = 'red')

    augmented_tfidf_title = CreateTextbox(modelframe, 80, "Augmented TF-IDF", 'center')
    augmented_tfidf_title.grid(row = 0, column = 2)
    augmented_tfidf_title.configure(font = ("RobotoCondensed Bold", 10, 'bold'), fg = 'red')


    #Add query to data and find word_set, doc_set, # of word existed in all documents
    word_set, doc_set, word_index = find_keywordset(query, data_after_join)
    set_function_tf = [term_frequency, logarithm_term_frequency, augmented_term_frequency]
    j = 0
    for function_tf in set_function_tf:
        print(function_tf)
        i = 1
        #Create TF-IDF vectors of all words
        all_vectors = all_tfidf_vectors(word_set, word_index, doc_set, function_tf)
        all_vectors = np.array(all_vectors)

        #Reshape query to calculate cosine similarity
        query = np.array(all_vectors[0]).reshape(1, -1)

        #Calculate cosine similarity
        initial_cosine_vector = cosine_similarity(query, all_vectors)
        
        #Remove the score of comparing query to query
        initial_cosine_vector_1D = np.delete(initial_cosine_vector[0], 0)

        #Add index to the list of cosine
        sorted_cosine_vector = [(index, item) for index, item in enumerate(initial_cosine_vector_1D)]

        #Sorted the cosine list
        sorted_cosine_vector = heapq.nlargest(10, sorted_cosine_vector, key = lambda list: list[1])
        for index, item in sorted_cosine_vector:
            ArticleTitle = data_before_join[index]["Title"]
            Abstract = data_before_join[index]["Abstract"]
            
            articleTitleText = CreateTextbox(modelframe, 80, ArticleTitle, 'center')
            articleTitleText.grid(row = i, column = j)
            articleTitleText.configure(font = ("RobotoCondensed Bold", 9, 'bold'))
            
            abstractText = CreateTextbox(modelframe, 80, Abstract, 'left')
            abstractText.grid(row = i+1, column = j)
            abstractText.configure(font = ("RobotoCondensed Bold", 8))

            # similarityScore = CreateTextbox(modelframe, 80, "Similarity: {}".format(item), 'left')
            # similarityScore.grid(row = i+2, column = j)
            # similarityScore.configure(font = ("RobotoCondensed Bold", 8))
            print(data[index]["Title"])
            i += 2
        j += 1
# word_set, doc_set, word_index = find_keywordset(query, rank_corpus(r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_LungCancer.json"))
# all_vectors = all_tfidf_vectors(word_set, word_index, doc_set, term_frequency)
# all_vectors = np.array(all_vectors)
# query = np.array(all_vectors[0]).reshape(1, -1)
# #Calculate cosine similarity
# initial_cosine_vector = cosine_similarity(query, all_vectors)
# initial_cosine_vector_1D = np.delete(initial_cosine_vector[0], 0)
# print(initial_cosine_vector[0])
# sorted_cosine_vector = [(index, item) for index, item in enumerate(initial_cosine_vector_1D)]
# sorted_cosine_vector.sort(key = lambda list: list[1], reverse = True)
# for index, item in sorted_cosine_vector:
#     print(index)
#Sort cosine_vector with descending item
# sorted_cosine_vector.sort(key = lambda list: list[[1]])
# path = r"D:\NCKU\Biomedical Information Retrieval\Homework\HW4\Data\Pubmed_LungCancer.json"
# rank_corpus(path, query, logarithm_term_frequency)
def CreateTextbox(parentWid, iWidth, textString, justify):
    lineCount = int(math.ceil(len(textString)/iWidth))
    newtextbox = Text(parentWid, height = lineCount, width=iWidth - 30, wrap = WORD, bd =0, padx = 15)
    newtextbox.tag_configure("tag_name", justify=justify)
    newtextbox.insert(INSERT, textString)
    newtextbox.tag_add("tag_name", "1.0", "end")
    newtextbox.config(state=DISABLED)
    return newtextbox

