import spacy
from spacy.matcher import PhraseMatcher
from scipy import spatial
import enchant
from nltk.tokenize import RegexpTokenizer
documents = "I enjoy watching movies when it's cold outside"
import re
# spacy english model (large)
# Run 'py -m spacy download en_core_web_lg' in terminal after 'run pip install spacy'
def preprocessing(text):
    # Removing Square Brackets and Extra Spaces
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', text)
    formatted_article_text = re.sub(r'\s+', ' ', text)
    return formatted_article_text.lower(), text
print(preprocessing("Best Friend!"))