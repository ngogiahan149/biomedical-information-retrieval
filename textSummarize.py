from openFile import *
import nltk, re
from nltk.tokenize import sent_tokenize
from gensim.similarities import 
#nltk.download('stopwords')
text = "In late summer 1945, guests are gathered for the wedding reception of Don Vito Corleones " + \
       "daughter Connie (Talia Shire) and Carlo Rizzi (Gianni Russo). Vito (Marlon Brando),"  + \
       "the head of the Corleone Mafia family, is known to friends and associates as Godfather. "  + \
       "He and Tom Hagen (Robert Duvall), the Corleone family lawyer, are hearing requests for favors "  + \
       "because, according to Italian tradition, no Sicilian can refuse a request on his daughter's wedding " + \
       " day. One of the men who asks the Don for a favor is Amerigo Bonasera, a successful mortician "  + \
       "and acquaintance of the Don, whose daughter was brutally beaten by two young men because she"  + \
       "refused their advances; the men received minimal punishment from the presiding judge. " + \
       "The Don is disappointed in Bonasera, who'd avoided most contact with the Don due to Corleone's" + \
       "nefarious business dealings. The Don's wife is godmother to Bonasera's shamed daughter, " + \
       "a relationship the Don uses to extract new loyalty from the undertaker. The Don agrees " + \
       "to have his men punish the young men responsible (in a non-lethal manner) in return for " + \
        "future service if necessary."
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
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    print("Word frquency: ", word_frequencies)
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
    print summarize(text)
preprocessing(text)                        