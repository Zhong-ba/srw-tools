import json

from getConfig import CONFIG

langs = []
data = {}


def load_data():
    global langs, data
    langs = ['CHS','CHT','DE','EN','ES','FR','ID','JP','KR','PT','RU','TH','VI']
    data = {}
    for lang in langs:
        with open(f'{CONFIG.DATA_PATH}/TextMap/TextMap{lang}.json', 'r', encoding='utf-8') as file:
            data[lang] = json.load(file)


def gen_ol(text):
    textdata = {}
    textId_list = []
        
    for item in data['EN']:
        if (data['EN'][item]) == text:
            textId_list.append(item)
    textId = textId_list[0]
    
    for lang in langs:
        textdata[lang] = data[lang].get(textId, '')
        
    output = f"{{{{Other Languages\n|en   = {text}\n|zhs  = {textdata['CHS']}\n|zht  = {textdata['CHT']}\n|ja   = {textdata['JP']}\n|ko   = {textdata['KR']}\n|es   = {textdata['ES']}\n|fr   = {textdata['FR']}\n|ru   = {textdata['RU']}\n|th   = {textdata['TH']}\n|vi   = {textdata['VI']}\n|de   = {textdata['DE']}\n|id   = {textdata['ID']}\n|pt   = {textdata['PT']}\n}}}}\n"
    
    return output