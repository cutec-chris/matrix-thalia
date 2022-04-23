import plugin
async def CheckSentence(s,User,ForceAnswer=False):
    if s[:3]=='en ':
        words = plugin.analyse_sentence(s[3:],'en')
    else:
        words = plugin.analyse_sentence(s)
    if words:
        res = 'text vector pos tag lemma tag label\n'
        for token in words:
            res += token.text+' '+str(token.vector_norm)+' '+token.pos_+' '+token.tag_+' '+token.lemma_+' '+token.tag_+' '+token.ent_type_+'\n'
        return {'text':res}