from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
text = "This is my can't text. It icludes commas, question marks? and other stuff. Also ."
tokens = tokenizer.tokenize(text)
print(tokens)
print(len(tokens))