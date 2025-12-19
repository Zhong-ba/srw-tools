import json
import os
import re
import argparse

import utils.ol as ol
from utils.files import write_file
from utils.pageinfo import pageinfo
from getConfig import CONFIG

TEXTMAP_PATH = f'{CONFIG.DATA_PATH}/TextMap'

parser = argparse.ArgumentParser()
parser.add_argument('--ver', type = str)

args = parser.parse_args()
version = args.ver

with open(f'{CONFIG.EXCEL_PATH}/AchievementData.json', 'r', encoding='utf-8') as file:
    achievementjson = json.load(file)
    
with open(f'{CONFIG.EXCEL_PATH_OLD}/AchievementData.json', 'r', encoding='utf-8') as file:
    old_achievementjson = json.load(file)
    
with open(f'{CONFIG.EXCEL_PATH}/AchievementSeries.json', 'r', encoding='utf-8') as file:
    achievementseriesjson = json.load(file)

ol.load_data()

for item in achievementjson:
    name = achievementjson[item]['AchievementTitle']['TextMapEN']
    
    if old_achievementjson.get(item) or name == '...':
        print(f'Skipped {name}.')
        continue
    
    OLtext = ol.gen_ol(name)
    desc = achievementjson[item]['AchievementDesc']['TextMapEN']
    rarity = achievementjson[item]['Rarity']
    priority = str(achievementjson[item]['Priority'])
    
    try:
        hidedesc = achievementjson[item]['HideAchievementDesc']['TextMapEN']
    except KeyError:
        hidedesc = ''
    
    if hidedesc != '':
        if '<br />※' in desc:
            extradesc = desc.split('<br />※')[1].strip()
        elif '<br />' in desc:
            extradesc = desc.split('<br />')[1].strip()
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
    
    file_write_path = f"{CONFIG.OUTPUT_PATH}/Achievements/{series}/{clean_name}.wikitext"
    directory_path = f'{CONFIG.OUTPUT_PATH}/Achievements/{series}'
    #file_write_path = re.sub(r'[:*?"<>|]', ' ', file_write_path)
    #directory_path = re.sub(r'[:*?"<>|]', ' ', directory_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    file_write = f"{pageinfo(name)}\n{{{{Achievement Infobox\n|rarity           = {rarity}\n|title            = {name}\n|category         = {series}\n|description      = {desc}\n|extraDescription = {extradesc}\n|hidden           = {hidden}\n|mission          = \n|topic            = \n}}}}\n'''{name}''' is an [[Achievement]] in the category [[{series}]].\n\nTo unlock this achievement, the player must {lowerdesc}\n<!--\n==Gameplay Notes==\n\n==Trivia==\n*\n-->\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{version}}}}}\n\n==Navigation==\n{{{{Achievement Navbox}}}}\n"

    write_file(file_write_path, file_write)



