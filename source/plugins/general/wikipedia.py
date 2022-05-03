import nlp,urllib.request,urllib.parse,json,re
url_article = 'https://{lang}.wikipedia.org/w/api.php?action=parse&page={page}&prop=wikitext&format=json';
url_search = 'https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={object}&utf8=&format=json'
async def CheckSentence(words,User,ForceAnswer=False):
    res = None
    quest = nlp.is_question(words)
    if quest and not nlp.is_futuristic(words):
        article = get_article(words.lang_,quest['object'])
        if not article:
            sr = search(words.lang_,quest['object'])
            if len(sr)>0:
                article = get_article(words.lang_,sr[0]['title'])
        if article:
            cleaned_article = clean_article(article) 
            sentences = nlp.analyse_sentence(cleaned_article)
            if quest['verb'] == 'be'\
            or quest['verb'] == 'sein': 
                count = 0
                res = {'markdown':[]}
                for sentence in sentences.sents:
                    if count>0 and '\n' in sentence.text.strip():
                        break
                    if sentence.text.strip() != '':
                        res['markdown'].append(sentence.text.strip())
                        count +=1
                    if count>=3: break
            else:
                res = {'markdown':[]}
                for sentence in sentences.sents:
                    for token in sentence:
                        if token.lemma_ == quest['verb']:
                            res['markdown'].append(sentence.text)
                            break
            pass
    return res
def search(lang,object):
    try:
        nurl = url_search.format(lang=lang,object=urllib.parse.quote(object))
        req = urllib.request.Request(nurl, headers=nlp.request_headers)
        response = urllib.request.urlopen(req)
        sr = response.read()
        sr = json.loads(sr)
        sr = sr['query']['search']
        return sr
    except BaseException as e:
        return None
def get_article(lang,page):
    try:
        nurl = url_article.format(lang=lang,page=urllib.parse.quote(page))
        req = urllib.request.Request(nurl, headers=nlp.request_headers)
        response = urllib.request.urlopen(req)
        sr = response.read()
        sr = json.loads(sr)
        if 'error' in sr:
            sr = None
        sr = sr['parse']['wikitext']['*']
        return sr
    except BaseException as e:
        return None
def clean_article(article):
    res = re.sub(r'\{\{(.*)\}\}','',article)
    res = re.sub(r'<!--(.*)-->','',res)
    res = re.sub(r'<ref(.*)</ref>','',res)
    res = re.sub(r'\[\[(.*):(.*)\]\]','',res)
    res = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]',r'\1',res)
    res = re.sub(r'\[\[(.*)\]\]','',res)
    res = res.replace('\'','')
    res = res.replace('&nbsp;',' ')
    res = re.sub(r'====(.*)====',r'\n\1\n',res)
    res = re.sub(r'===(.*)===',r'\n\1\n',res)
    res = re.sub(r'==(.*)==',r'\n\1\n',res)
    res = re.sub(r'=(.*)=',r'\n\1\n',res)
    return res