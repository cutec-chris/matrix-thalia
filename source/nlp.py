import spacy,logging
languages = {}
n_disable=[
    #'tagger', 
    #'parser', 
    #'ner', 
    #'lemmatizer', 
    #'textcat'
]
gpu_activated = spacy.prefer_gpu()
def analyse_sentence(text,intendlanguage='de'):
    model_size='md'
    if len(languages)==0:
        logging.debug('loading languages...')
        try: 
            languages['de'] = spacy.load("de_core_news_"+model_size,disable=n_disable)
            #languages['de'].add_pipe("merge_entities")
        except: pass
        try: 
            languages['en'] = spacy.load("en_core_web_"+model_size,disable=n_disable)
            #languages['en'].add_pipe("merge_entities")
        except: pass
        logging.debug('...done')
    if not intendlanguage in languages:
        logging.warning('language not found: %s' % intendlanguage) 
        return None
    res = languages[intendlanguage](text)
    return res
