import json

from getConfig import CONFIG

langs = ['CHS','CHT','DE','EN','ES','FR','ID','JP','KR','PT','RU','TH','VI']
data = {}


def print_progress_bar(iteration, total, length = 50):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\rLoading OL: |{bar}| {percent}%', end='\r')
    if iteration == total: 
        print()
        

def load_data(progress_callback = None):
    global langs, data
    
    if data:
        return
    
    for index, lang in enumerate(langs):
        with open(f'{CONFIG.DATA_PATH}/TextMap/TextMap{lang}.json', 'r', encoding='utf-8') as file:
            data[lang] = json.load(file)
        if progress_callback:
            progress_callback(index + 1, len(langs))
        print_progress_bar(index + 1, len(langs))


def gen_ol(text):
    textdata = {}
    textId_list = []
        
    for item in data['EN']:
        if (data['EN'][item]) == text:
            textId_list.append(item)
    try:
        textId = textId_list[0]
    except Exception as e:
        print(f"Error while generating OL for text: {text}. Error: {str(e)}")
        return

    for lang in langs:
        textdata[lang] = data[lang].get(textId, '')
        
    output = f"{{{{Other Languages\n|en   = {text}\n|zhs  = {textdata['CHS']}\n|zht  = {textdata['CHT']}\n|ja   = {textdata['JP']}\n|ko   = {textdata['KR']}\n|es   = {textdata['ES']}\n|fr   = {textdata['FR']}\n|ru   = {textdata['RU']}\n|th   = {textdata['TH']}\n|vi   = {textdata['VI']}\n|de   = {textdata['DE']}\n|id   = {textdata['ID']}\n|pt   = {textdata['PT']}\n}}}}\n"
    
    return output