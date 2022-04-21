import spacy
n_disable=[
    'tagger', 
    #'parser', 
    'ner', 
    #'lemmatizer', 
    'textcat'
]
eng = spacy.load("en_core_web_sm",disable=n_disable)
ger = spacy.load("de_core_news_sm",disable=n_disable)

def tokenizer_eng(text):
    res = eng(text)
    for word in res:
        print(word,word.vector.shape,word.lemma_.lower().strip())
    return [tok for tok in eng.tokenizer(text)]

def tokenizer_ger(text):
    return [tok.text for tok in ger.tokenizer(text)]

print(tokenizer_eng('hello how are you'))