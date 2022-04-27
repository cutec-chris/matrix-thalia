async def CheckSentence(words,User,ForceAnswer=False):
    res = words.lang_+'\ntext vector pos tag lemma tag label\n'
    for token in words:
        res += token.text+' '+str(token.vector_norm)+' '+token.pos_+' '+token.tag_+' '+token.lemma_+' '+token.tag_+' '+token.ent_type_+'\n'
    return {'text':res}