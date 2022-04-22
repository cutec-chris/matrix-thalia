import spacy
languages = {}
n_disable=[
    'tagger', 
    #'parser', 
    'ner', 
    #'lemmatizer', 
    'textcat'
]
gpu_activated = spacy.prefer_gpu()
def analyse_sentence(text,intendlanguage=None):
    if not intendlanguage in languages:
        if   intendlanguage == 'de': languages['de'] = spacy.load("de_core_news_md",disable=n_disable)
        elif intendlanguage == 'en': languages['en'] = spacy.load("en_core_web_md",disable=n_disable)
        #else:                        languages['xx'] = spacy.load("xx_ent_wiki_sm",disable=n_disable)
    if not intendlanguage in languages: return None
    return languages[intendlanguage](text)
    
