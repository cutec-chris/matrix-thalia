import logging
from math import *
async def CheckSentence(words,User,ForceAnswer=False):
    res = None
    formula = ''
    count = 0
    for word in words:
        if word.pos_ == 'NUM'\
        or word.pos_ == 'SYM'\
        or word.pos_ == 'PROPN'\
        or word.pos_ == 'ADV'\
        or word.pos_ == 'X'\
        or word.pos_ == 'NOUN':
            formula += ' '+word.text
            count += 1
        else:
            formula = ''
            count = 0
    try: 
        if ForceAnswer:
            r = eval(formula)
            if not r is None:
                res = {'text': str(r)}
    except BaseException as e:
        logging.debug(str(e))
    return res