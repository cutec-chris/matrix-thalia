from wsgiref import headers
import nlp,urllib.request,urllib.parse,json
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
            content = article
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
