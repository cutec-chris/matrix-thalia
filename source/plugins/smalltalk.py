import plugin
async def CheckSentence(s,User,ForceAnswer=False):
    if s[:3]=='en ':
        words = plugin.analyse_sentence(s[3:])
    else:
        words = plugin.analyse_sentence(s)
    if words:
        res = ''
        for token in words:
            res += token.text+' '+str(token.vector_norm)+' '+token.pos_+' '+token.tag_+'\n'
        return {'text':res}