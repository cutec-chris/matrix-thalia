import plugin
def CheckSentence(s,User,ForceAnswer=False):
    words = plugin.analyse_sentence(s)
    if 'hi' in words:
        return {'text':'ok'}