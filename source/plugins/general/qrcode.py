from importlib.resources import path
import qrcode,nlp,spacy.matcher,pathlib,tempfile
pattern = [{'LOWER': 'qrcode'},
           {'POS': 'ADP'},
           {'LIKE_URL': True}]
pattern1 = [{'LOWER': 'qr-code'},
           {'POS': 'ADP'},
           {'LIKE_URL': True}]
async def CheckSentence(words,User,ForceAnswer=False):
    matcher = spacy.matcher.Matcher(nlp.languages[words.lang_].vocab)
    matcher.add("match", [pattern])
    matcher.add("match1", [pattern1])
    matches = matcher(words)
    res = None 
    for match in matches:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(words[match[2]-1].text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        fileName = str(pathlib.Path(tempfile.gettempdir()) / 'qrcode.jpg')
        img.save(fileName)
        res = {'image': fileName}
        break
    return res