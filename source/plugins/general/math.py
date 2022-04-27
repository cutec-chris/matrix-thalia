import logging
from math import *
async def CheckSentence(words,User,ForceAnswer=False):
    res = None
    formula = ''
    for word in words:
        if word.pos_ == 'NUM'\
        or word.pos_ == 'SYM'\
        or word.pos_ == 'PROPN'\
        or word.pos_ == 'ADV'\
        or word.pos_ == 'X'\
        or word.pos_ == 'NOUN':
            formula += word.text
        else:
            formula = ''
        try: 
            r = eval(formula)
            if r:
            #    print(str(r))
                res = {'text': str(r)}
        except BaseException as e:
            logging.debug(str(e))
    return res