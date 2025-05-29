import json
import os

from utils.misc import parse_params, convertwhole, autoround
from utils.files import copy_file, write_file
from getConfig import CONFIG


def parse_curio():
    file_write_path =f'{CONFIG.OUTPUT_PATH}/Curio_Output.txt'
    file_write = ''
    file_write_2_path =f'{CONFIG.OUTPUT_PATH}/Curio_Output_2.txt'
    file_write_2 = ''

    with open(f'{CONFIG.EXCEL_PATH}/RogueTournMiracleDisplay.json', 'r', encoding = 'utf-8') as file:
        roguemiracleconfig = json.load(file)

    # get stage list
    for item in roguemiracleconfig:
        name = roguemiracleconfig[item]['MiracleName']['TextMapEN']
        print(name)
        try:
            desc = roguemiracleconfig[item]['MiracleDesc']['TextMapEN']
        except KeyError:
            desc = ''
        try:
            lore = roguemiracleconfig[item]['MiracleBGDesc']['TextMapEN']
        except KeyError:
            lore = ''
        
        params = roguemiracleconfig[item]['DescParamList']
        
        if params:
            desc = parse_params(desc, params)

        # file
        file_write = (file_write +
                      f'\n|-\n|[[File:Curio {name}.png|50px]]\n|\'\'\'{name}\'\'\'\n|{desc}\n|-\n|colspan="3" | {lore}')

        file_write_2 = file_write_2 + f'\n** {{{{Item|{name}|20|nobr=1|type=Curio|link=}}}}'
        
    write_file(file_write_path, file_write)
    write_file(file_write_2_path, file_write_2)
        

def parse_blessings():
    file_write_path =f'{CONFIG.OUTPUT_PATH}/Blessings_Output.txt'
    file_write = ''

    with open(f'{CONFIG.EXCEL_PATH}/RogueMazeBuff.json', 'r', encoding = 'utf-8') as file:
        roguemazebuff = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RogueBuff.json', 'r', encoding = 'utf-8') as file:
        roguebuff = json.load(file)

    # get stage list
    for item in roguemazebuff:
        try:
            name = roguemazebuff[item]['1']['BuffName']['TextMapEN']
        except KeyError:
            name = ''

        try:
            rarity = str(roguebuff[item]['1']['RogueBuffRarity'])
        except KeyError:
            rarity = ''

        try:
            image = roguemazebuff[item]['1']['BuffIcon']
        except KeyError:
            image = ''

        if image[-6:-4] == '01':
            imagetype = 'Attack'
        elif image[-6:-4] == '02':
            imagetype = 'Defense'
        elif image[-6:-4] == '03':
            imagetype = 'Buff'
        elif image[-6:-4] == '04':
            imagetype = 'Debuff'
        elif image[-6:-4] == '05':
            imagetype = 'Support'
        else:
            imagetype = ''

        if 'Joy' in image:
            path = 'Elation'
        elif 'Knight' in image:
            path = 'Preservation'
        elif 'Memory' in image:
            path = 'Remembrance'
        elif 'Pirest' in image:
            path = 'Abundance'
        elif 'Priest' in image:
            path = 'Abundance'
        elif 'RogueRogue' in image:
            path = 'Hunt'
        elif 'Warlock' in image:
            path = 'Nihility'
        elif 'Warrior' in image:
            path = 'Destruction'
        elif 'Propagation' in image:
            path = 'Propagation'
        else:
            path = ''

        try:
            desc1 = roguemazebuff[item]['1']['BuffDesc']['TextMapEN']
        except KeyError:
            desc1 = ''

        params1 = [key["Value"] for key in roguemazebuff[item]['1']['ParamList']]

        for n in range(0, len(params1)):
            param1 = convertwhole(autoround(params1[n]))
            percent1 = autoround(convertwhole(param1 * 100))
            desc1 = desc1.replace(f'#{n + 1}[i]%', str(percent1) + '%')
            desc1 = desc1.replace(f'#{n + 1}[f1]%', str(percent1) + '%')
            desc1 = desc1.replace(f'#{n + 1}[f2]%', str(percent1) + '%')
            desc1 = desc1.replace(f'#{n + 1}[i]', str(params1[n]))
            desc1 = desc1.replace(f'#{n + 1}[f1]', str(params1[n]))
            desc1 = desc1.replace(f'#{n + 1}[f2]', str(params1[n]))

        try:
            desc2 = roguemazebuff[item]['2']['BuffDesc']['TextMapEN']
        except KeyError:
            desc2 = ''

        if desc2 != '':
            params2 = [key["Value"] for key in roguemazebuff[item]['2']['ParamList']]

            for n in range(0, len(params2)):
                param2 = convertwhole(autoround(params2[n]))
                percent2 = autoround(convertwhole(param2 * 100))
                desc2 = desc2.replace(f'#{n + 1}[i]%', str(percent2) + '%')
                desc2 = desc2.replace(f'#{n + 1}[f1]%', str(percent2) + '%')
                desc2 = desc2.replace(f'#{n + 1}[f2]%', str(percent2) + '%')
                desc2 = desc2.replace(f'#{n + 1}[i]', str(params2[n]))
                desc2 = desc2.replace(f'#{n + 1}[f1]', str(params2[n]))
                desc2 = desc2.replace(f'#{n + 1}[f2]', str(params2[n]))

        if 'Resonance Formation' in name or 'Resonance Interplay' in name or 'Path Resonance' in name:
            file_write = (file_write +
                          f"\n|-\n|{{{{SU Blessing Card|{path}|{imagetype}|{rarity}}}}}\n|'''{name}'''<br />{desc1}")
        else:
            file_write = (file_write +
                          f'\n|-\n|{{{{SU Blessing Card|{path}|{imagetype}|{rarity}}}}}\n|{name}\n|{desc1}\n|{desc2}')

    write_file(file_write_path, file_write)
        
    
def parse_nous_dice_face():
    with open(f'{CONFIG.EXCEL_PATH}/RogueNousDiceSurface.json', 'r', encoding = 'utf-8') as file:
        dicesurfacejson = json.load(file)

    file_write_path = f'{CONFIG.OUTPUT_PATH}/Dice_Face_Output.lua'
    file_write = ''

    dice_dict = {}

    for item in dicesurfacejson:
        name = dicesurfacejson[item]['SurfaceName']['TextMapEN']
        rarity = str(dicesurfacejson[item]['Rarity'] + 2)

        dice_dict[name] = rarity

        file_name_clean = f'Dice Face {name.replace(":", "")}'

        source_path = dicesurfacejson[item]['Icon']
        source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
        destination_path = f'{CONFIG.OUTPUT_PATH}/DiceFaces/{file_name_clean}.png'

        if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/DiceFaces'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/DiceFaces')

        copy_file(source_path, destination_path)

    sorted_dict = {key: dice_dict[key] for key in sorted(dice_dict)}

    sorted_dict_2 = {k: v for k, v in sorted(sorted_dict.items(), key = lambda dict_item: dict_item[1], reverse = True)}

    for name, rarity in sorted_dict_2.items():
        file_write = file_write + f'\n	[\'{name}\'] = {{ rarity = \'{rarity}\' }},'

    write_file(file_write_path, file_write)