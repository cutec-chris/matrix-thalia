import spacy
languages = {}
n_disable=[
    'tagger', 
    #'parser', 
    'ner', 
    #'lemmatizer', 
    'textcat'
]
def analyse_sentence(text,intendlanguage='de'):
    if not intendlanguage in languages:
        if intendlanguage == 'de': languages['de'] = spacy.load("de_core_news_sm",disable=n_disable)
        if intendlanguage == 'en': languages['en'] = spacy.load("en_core_web_sm",disable=n_disable)
    if not intendlanguage in languages: return None
    return languages[intendlanguage](text)
    
