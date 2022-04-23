import spacy
languages = {}
n_disable=[
    'tagger', 
    #'parser', 
    #'ner', 
    #'lemmatizer', 
    #'textcat'
]
gpu_activated = spacy.prefer_gpu()
def analyse_sentence(text,intendlanguage='de'):
    if len(languages)==0:
        try: 
            languages['de'] = spacy.load("de_core_news_md",disable=n_disable)
            languages['de'].add_pipe("merge_noun_chunks")
        except: pass
        try: 
            languages['en'] = spacy.load("en_core_web_md",disable=n_disable)
            languages['en'].add_pipe("merge_noun_chunks")
        except: pass
    if not intendlanguage in languages: return None
    res = languages[intendlanguage](text)
    return res
    
