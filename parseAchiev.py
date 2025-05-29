import json
import os
import re
import argparse
from config import CONFIG

MAPPED_EXCEL_PATH = f'{CONFIG["DataPath"]}/MappedExcelOutput_EN'
OLD_MAPPED_EXCEL_PATH = f'{CONFIG["DataPathOld"]}/MappedExcelOutput_EN'
OUT_PATH = CONFIG['OutputPath']
TEXTMAP_PATH = f'{CONFIG["DataPath"]}/TextMap'

parser = argparse.ArgumentParser()
parser.add_argument('--ver', type = str)

args = parser.parse_args()
version = args.ver

with open(f'{MAPPED_EXCEL_PATH}/AchievementData.json', 'r', encoding='utf-8') as file:
    achievementjson = json.load(file)
    
with open(f'{OLD_MAPPED_EXCEL_PATH}/AchievementData.json', 'r', encoding='utf-8') as file:
    old_achievementjson = json.load(file)
    
with open(f'{MAPPED_EXCEL_PATH}/AchievementSeries.json', 'r', encoding='utf-8') as file:
    achievementseriesjson = json.load(file)


langs = ['CHS','CHT','DE','EN','ES','FR','ID','JP','KR','PT','RU','TH','VI']
data = {}
for lang in langs:
    with open(f'{TEXTMAP_PATH}/TextMap{lang}.json', 'r', encoding='utf-8') as file:
        data[lang] = json.load(file)


def genOL(text):        
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

for item in achievementjson:
    name = achievementjson[item]['AchievementTitle']['TextMapEN']
    
    if old_achievementjson.get(item) or name == '...':
        print(f'Skipped {name}.')
        continue
    
    OLtext = genOL(name)
    desc = achievementjson[item]['AchievementDesc']['TextMapEN']
    rarity = achievementjson[item]['Rarity']
    priority = str(achievementjson[item]['Priority'])
    
    try:
        hidedesc = achievementjson[item]['HideAchievementDesc']['TextMapEN']
    except KeyError:
        hidedesc = ''
    
    if hidedesc != '':
        extradesc = desc.split('<br />※')[1].strip()
        desc = hidedesc
    else:
        extradesc = ''
    
    params = [key["Value"] for key in achievementjson[item]['ParamList']]
    
    for n in range(0, len(params)):
        percent = params[n] * 100
        desc = desc.replace(f'#{n + 1}[i]%', str(percent) + '%')
        desc = desc.replace(f'#{n + 1}[i]', str(params[n]))
        desc = desc.replace(f'#{n + 1}', str(params[n]))
        
    for n in range(0, len(params)):
        percent = params[n] * 100
        extradesc = extradesc.replace(f'#{n + 1}[i]%', str(percent) + '%')
        extradesc = extradesc.replace(f'#{n + 1}[i]', str(params[n]))
        extradesc = extradesc.replace(f'#{n + 1}', str(params[n]))
    
    if hidedesc != '':
        lowerdesc = extradesc[0].lower() + extradesc[1:] + '.'
    else:
        lowerdesc = desc[0].lower() + desc[1:] + '.'
    
    if lowerdesc.endswith('".'):
        lowerdesc = lowerdesc[:-2] + '."'
        
    try:
        if achievementjson[item]['ShowType'] == 'ShowAfterFinish':
            hidden = '1'
        else:
            hidden = ''
    except KeyError:
        hidden = ''
        
    seriesId = str(achievementjson[item]['SeriesID'])
    series = achievementseriesjson[seriesId]['SeriesTitle']['TextMapEN']
    
    clean_name = re.sub(r'[:*?"<>|]', ' ', name)
    
    file_write_path = f"{OUT_PATH}/Achievements/{series}/{clean_name}.wikitext"
    directory_path = f'{OUT_PATH}/Achievements/{series}'
    #file_write_path = re.sub(r'[:*?"<>|]', ' ', file_write_path)
    #directory_path = re.sub(r'[:*?"<>|]', ' ', directory_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    file_write = f"<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some important information of edit. This struct will be removed automatically after you push edits.#\n    pageTitle = #{name}#\n    pageID = ##\n    revisionID = ##\n    contentModel = ##\n    contentFormat = ##\n[END_PAGE_INFO] --%>\n\n{{{{Achievement Infobox\n|rarity           = {rarity}\n|title            = {{{{subst:#titleparts:{{{{subst:PAGENAME}}}}}}}}\n|category         = {series}\n|description      = {desc}\n|extraDescription = {extradesc}\n|hidden           = {hidden}\n|mission          = \n|topic            = \n}}}}\n'''{{{{subst:#titleparts:{{{{subst:PAGENAME}}}}}}}}''' is an [[Achievement]] in the category [[{series}]].\n\nTo unlock this achievement, the player must {lowerdesc}\n<!--\n==Gameplay Notes==\n\n==Trivia==\n*\n-->\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{version}}}}}\n\n==Navigation==\n{{{{Achievement Navbox}}}}\n"

    with open(file_write_path, 'w', encoding='utf-8') as file:
       file.write(file_write)
       print('Saved to ' + file_write_path + '.')    



