from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import PhraseMatcher
from scipy import spatial
import enchant, collections
sp = spacy.load('en_core_web_lg')

all_stopwords = sp.Defaults.stop_words
print(all_stopwords)