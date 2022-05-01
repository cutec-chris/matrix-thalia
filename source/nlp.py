import spacy,logging
request_headers = {'User-Agent': 'Thalia/0.1 (https://github.com/cutec-chris/matrix-thalia; thalia@chris.ullihome.de)'}
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
def is_question(sentence_doc):
    res = {}
    for token in sentence_doc:
        if token.tag_ in ['PWS','PWAV','WP','WRB']\
        and token.pos_ in ['PRON','ADV','SCONJ']:
            if token.lemma_ in ['wer','who']:
                res['label'] = ['PERSON','PER']
            elif token.lemma_ in ['wann','when']:
                res['label'] = ['DATE']
            elif token.lemma_ in ['was','what']:
                res['label'] = ['ORG']
        if token.tag_ in ['VAFIN','VBZ','VVPP']\
        and token.dep_ != 'ROOT':
            res['verb'] = token.lemma_
    if not 'verb' in res:
        for token in sentence_doc:
            if token.tag_ in ['VAFIN','VBZ','VVPP']:
                res['verb'] = token.lemma_
    if 'verb' in res:
        for token in sentence_doc:
            if token.dep_ == 'ROOT':
                for child in token.children:
                    if child.lemma_ != res['verb']\
                    and child.pos_  != 'PUNCT':
                        res['object'] = ''
                        for obj_token in sentence_doc:
                            if obj_token == child\
                            or obj_token in child.children:
                                res['object'] += ' '+obj_token.text
                        res['object'] = res['object'][1:]
    if not 'label' in res:
        res = None
    return res
def is_futuristic(sentence_doc):
    if any((token.morph.get('Tense') == [] and
            token.morph.get('VerbForm') == ['Fin'] and 
            token.morph.get('Mood') == [])
           or
           (token.morph.get('Tense') == ['Pres'] and
            token.morph.get('VerbForm') == ['Fin'] and
            token.morph.get('Mood') != ['Ind'])
           for token in sentence_doc):

        return True
    else:
        return False