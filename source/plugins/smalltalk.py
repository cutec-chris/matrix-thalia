import plugin
async def CheckSentence(s,User,ForceAnswer=False):
    words = plugin.analyse_sentence(s)
    for token in words:
        if token.text in ['hi','hallo']:
            return {'text':'hallo'}