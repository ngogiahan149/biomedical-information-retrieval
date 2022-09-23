from tkinter import *
import nltk
from nltk.stem import LancasterStemmer, SnowballStemmer
from nltk.tokenize import RegexpTokenizer
import spacy
from spacy.matcher import PhraseMatcher
from scipy import spatial
import enchant
from textSummarize import preprocessing
def simpleSearch(text, keyword, foreground ='red'):
    text.tag_remove('found', '1.0', END)
    if keyword:
        idx = '1.0'
        idx = text.search(keyword, idx, nocase=1,
                        stopindex=END)
        if not idx: 
            return
        lastidx = '%s+%dc' % (idx, len(keyword))
        
        text.tag_add('found', idx, lastidx)
        idx = lastidx
        text.tag_config('found', foreground = foreground)
def simpleSearch2(text, keyword, foreground ='red'):
    #text.tag_remove('found', '0.0', END)
    if keyword:
        idx = '1.0'
        idx = text.search(keyword, idx, nocase=1,
                        stopindex=END)
        if not idx: 
            return
        lastidx = '%s+%dc' % (idx, len(keyword))
        
        text.tag_add('found', idx, lastidx)
        idx = lastidx
        text.tag_config('found', foreground = foreground)
def searchFunc(frame, keyword):
    for widget in frame.winfo_children():
        if widget.winfo_class() == 'Text':
            simpleSearch(widget, keyword, foreground = 'red')
def SnowwballStemming(text):
    snowball = SnowballStemmer(language = 'English')
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    listStem = []
    for word in tokens:
        stemmedWord = snowball.stem(word)
        listStem.append(stemmedWord)
    return ' '.join(listStem)
def LancasterStemming(text):
    lancaster = LancasterStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    listStem = []
    for word in tokens:
        stemmedWord = lancaster.stem(word)
        listStem.append(stemmedWord)
    return ' '.join(listStem)

# customer sentence segmenter for creating spacy document object
# def setCustomBoundaries(doc):
#     # traversing through tokens in document object
#     for token in doc:
     

# create spacy document object from pdf text
def getSpacyDocument(text, nlp):
    main_doc = nlp(text)  # create spacy document object
    return main_doc


# convert keywords to vector
def createKeywordsVectors(keyword, nlp):
      # convert to document object
    return getSpacyDocument(keyword, nlp).vector


# method to find cosine similarity
def cosineSimilarity(vect1, vect2):
    # return cosine distance
    return 1 - spatial.distance.cosine(vect1, vect2)


# method to find similar words
def getSimilarWords(keyword, nlp):
    similarity_list = []
    keyword_vector = createKeywordsVectors(keyword, nlp)
    
    for tokens in nlp.vocab:
        if (tokens.has_vector):
            if (tokens.is_lower):
                if (tokens.is_alpha):
                    similarity_list.append((tokens, cosineSimilarity(keyword_vector, tokens.vector)))

    similarity_list = sorted(similarity_list, key=lambda item: -item[1])
    similarity_list = similarity_list[:30]

    #Create top similar word list
    used = set()
    mylist = [item[0].text for item in similarity_list]
    top_similar_words = [x for x in mylist if x not in used and (used.add(x) or True)]
    # top_similar_words = [item[0].text for item in similarity_list]
    top_similar_words = top_similar_words[:10]

    for token in nlp(keyword):
        if not token.is_stop and not token.is_punct:
            lemmaWord = token.lemma_
            if lemmaWord not in top_similar_words:
                top_similar_words.insert(0, lemmaWord)
    for words in top_similar_words:
        if words.endswith("s"):
            top_similar_words.append(words[0:len(words)-1])

    top_similar_words = list(set(top_similar_words))
    check_spell = enchant.Dict('en_US')
    top_similar_words = [words for words in top_similar_words if check_spell.check(words) == True]
    top_similar_words.append(keyword)
    print(top_similar_words)
    return top_similar_words
# method for searching keyword from the text
def search_for_keyword(keyword, document, nlp):
    keyword.lower()
    document.lower()
    doc_obj = getSpacyDocument(document, nlp)
    phrase_matcher = PhraseMatcher(nlp.vocab)
    similar_keywords = getSimilarWords(keyword, nlp)
    phrase_list = [nlp(word) for word in similar_keywords]
    phrase_matcher.add(keyword, None, *phrase_list)
    matched_items = phrase_matcher(doc_obj)
    matched_text = []
    for match_id, start, end in matched_items:
        text = nlp.vocab.strings[match_id]
        span = doc_obj[start: end]
        print(span.text)
        matched_text.append(span.text)
    return matched_text
def advancedSearch(frame, keyword, nlp):
    for widget in frame.winfo_children():
        if widget.winfo_class() == 'Text':
            widget.tag_remove('found', '1.0', END)
    for widget in frame.winfo_children():
        if widget.winfo_class() == 'Text':
            #To get input from widget for passing into search_for_keyword()
            matched_text = search_for_keyword(keyword, widget.get("1.0",'end-1c'), nlp)
            for item in matched_text:
                print(item)
                simpleSearch2(widget, item, foreground = 'red')  