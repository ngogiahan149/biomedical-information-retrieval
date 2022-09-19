from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import PhraseMatcher
from scipy import spatial
import enchant
documents = "I enjoy watching movies when it's cold outside. Because of you, I died. I'm good"
#  "Toy Story is the best animation movie ever",
#  "Watching horror movies alone at night is really scary",
#  "He loves films filled with suspense and unexpected plot twists ",
#  "This is one of the most overrated movies I've ever seen"]

# spacy english model (large)
# Run 'py -m spacy download en_core_web_lg' in terminal after 'run pip install spacy'
nlp = spacy.load('en_core_web_lg')

# customer sentence segmenter for creating spacy document object
# def setCustomBoundaries(doc):
#     # traversing through tokens in document object
#     for token in doc:
     

# create spacy document object from pdf text
def getSpacyDocument(text, nlp):
    main_doc = nlp(text)  # create spacy document object
    return main_doc

# # adding setCusotmeBoundaries to the pipeline
# nlp.add_pipe(setCustomBoundaries(documents), before='parser')
# convert keywords to vector
def createKeywordsVectors(keyword, nlp):
    doc = nlp(keyword)  # convert to document object
    return doc.vector


# method to find cosine similarity
def cosineSimilarity(vect1, vect2):
    # return cosine distance
    return 1 - spatial.distance.cosine(vect1, vect2)


# method to find similar words
def getSimilarWords(keyword, nlp):
    similarity_list = []

    keyword_vector = createKeywordsVectors(keyword, nlp)
    
    for tokens in nlp.vocab:
        print(tokens)
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
    print(top_similar_words)
    # top_similar_words = [item[0].text for item in similarity_list]
    top_similar_words = top_similar_words[:3]
    top_similar_words.append(keyword)

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
    return top_similar_words
# method for searching keyword from the text
def search_for_keyword(keyword, document, nlp):
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
        matched_text.append(span.sent.text)
    print(matched_text)
    return matched_text
 
 
search_keyword = 'Best die'
 
search_for_keyword(search_keyword, documents, nlp)