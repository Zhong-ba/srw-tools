import json
import argparse
import shutil
import os
import re
import pyperclip

import utils.ol as ol
from utils.files import copy_file, write_file
from utils.misc import autoround, dict_to_table
from getConfig import CONFIG

TEXTMAP_PATH = f'{CONFIG.DATA_PATH}/TextMap'

def parse_tutorial(tut_id):
    with open(f'{CONFIG.EXCEL_PATH}/TutorialGuideGroup.json', 'r', encoding = 'utf-8') as file:
        groupjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/TutorialGuideData.json', 'r', encoding = 'utf-8') as file:
        datajson = json.load(file)

    title = groupjson[tut_id]['MessageText']['TextMapEN']
    guide_ids = groupjson[tut_id]['TutorialGuideIDList']
    output = ''
    index = 1

    for guide in guide_ids:
        desc = datajson[str(guide)]['Default']['DescText']['TextMapEN']
        output = output + f'\n|image{index} = Tutorial {title} {index}.png\n|text{index}  = {desc}'

        source_path = datajson[str(guide)]['Default']['ImagePath']
        source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
        title_clean = re.sub(r'[^\w\s]', '', groupjson[tut_id]['MessageText']['TextMapEN'])
        destination_path = f'{CONFIG.OUTPUT_PATH}/Tutorial_{tut_id}/Tutorial {title_clean} {index}.png'

        if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/Tutorial_{tut_id}'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/Tutorial_{tut_id}')

        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"File copied successfully from {source_path} to {destination_path}")
        else:
            print(f"The file {source_path} does not exist.")

        index = index + 1

    output = f'{{{{Tutorial{output}\n}}}}'

    print(output)
    

def parse_achiev_id():
    with open(f'{CONFIG.EXCEL_PATH}/AchievementData.json', 'r', encoding = 'utf-8') as file:
        achievementjson = json.load(file)

    file_write_path = f'{CONFIG.OUTPUT_PATH}/Achievments/Achiev_ID_Output.lua'

    achiev_dict = {}

    for item in achievementjson:
        name = achievementjson[item]['AchievementTitle']['TextMapEN']
        name = name.replace('<i>', '\'\'').replace('</i>', '\'\'')
        achiev_id = 10000 - achievementjson[item]['Priority']
        id_str = str(achiev_id)

        achiev_dict[name] = id_str

    file_write = (f"--[=[<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some "
                  f"important information of edit. This struct will be removed automatically after you push edits.#\n "
                  f"   pageTitle = #Module:Achievement ID/data#\n    pageID = ##\n    revisionID = ##\n    "
                  f"contentModel = #Scribunto#\n    contentFormat = #text/plain#\n[END_PAGE_INFO] --%>--]=]\n\nreturn "
                  f"{dict_to_table(achiev_dict)}")

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


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

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def parse_hard_level():
    with open(f'{CONFIG.EXCEL_PATH}/HardLevelGroup.json', 'r', encoding = 'utf-8') as file:
        hardleveljson = json.load(file)

    file_write_path = f'{CONFIG.OUTPUT_PATH}/Level_Scaling_Output.lua'

    dict_0 = {}
    dict_1 = {}
    dict_2 = {}
    dict_3 = {}

    for hl_type in hardleveljson:
        if hl_type in ['1', '2', '3']:
            for level in hardleveljson[hl_type]:
                hp_mult = autoround(hardleveljson[hl_type][level]['HPRatio']['Value'])
                atk_mult = autoround(hardleveljson[hl_type][level]['AttackRatio']['Value'])
                def_mult = autoround(hardleveljson[hl_type][level]['DefenceRatio']['Value'])

                if hl_type == '1':
                    if level not in dict_1:
                        dict_1[level] = {}
                    dict_1[level]['hp'] = hp_mult
                    dict_1[level]['atk'] = atk_mult
                    dict_1[level]['def'] = def_mult
                elif hl_type == '2':
                    if level not in dict_2:
                        dict_2[level] = {}
                    dict_2[level]['hp'] = hp_mult
                    dict_2[level]['atk'] = atk_mult
                    dict_2[level]['def'] = def_mult
                elif hl_type == '3':
                    if level not in dict_3:
                        dict_3[level] = {}
                    dict_3[level]['hp'] = hp_mult
                    dict_3[level]['atk'] = atk_mult
                    dict_3[level]['def'] = def_mult

    dict_0['1'] = dict_1
    dict_0['2'] = dict_2
    dict_0['3'] = dict_3

    file_write = dict_to_table(dict_0)

    write_file(file_write_path, file_write)


def copy_ol(input):
    ol.load_data()
    pyperclip.copy(ol.gen_ol(input))


#########################################################################

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--curio', type = bool)
    parser.add_argument('--aetherpassive', type = bool)
    parser.add_argument('--rewards', type = bool)
    parser.add_argument('--tutorial', type = int)
    parser.add_argument('--blessings', type = bool)
    parser.add_argument('--aetherchallenge', type = bool)
    parser.add_argument('--rogueendlessrewards', type = bool)
    parser.add_argument('--heliobuschallenge', type = bool)
    parser.add_argument('--heliobusraid', type = int)
    parser.add_argument('--heliobususer', type = bool)
    parser.add_argument('--heliobuspost', type = bool)
    parser.add_argument('--heliobustemplate', type = bool)
    parser.add_argument('--achievid', type = bool)
    parser.add_argument('--nousdicefaceicons', type = bool)
    parser.add_argument('--hardlevel', type = bool)
    parser.add_argument('--purefiction', type = int)
    parser.add_argument('--purefictionv2', type = int)
    parser.add_argument('--fh', type = int)
    parser.add_argument('--charasc', type = bool)
    parser.add_argument('--traceupgr', type = bool)
    parser.add_argument('--lcasc', type = bool)
    parser.add_argument('--text', type = str)
    parser.add_argument('--techniquestatus', type = str)
    parser.add_argument('--avatarstatus', type = str)
    parser.add_argument('--monsterstatus', type = str)
    parser.add_argument('--ol', type = str)
    parser.add_argument('--apocshadow', type = str)
    parser.add_argument('--redirectfromstr', type = str)

    args = parser.parse_args()

    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}')

    if args.curio:
        from utils.su_old import parse_curio
        parse_curio()
        
    if args.blessings:
        from utils.su_old import parse_blessings
        parse_blessings()

    if args.aetherpassive:
        from utils.events.aether import parse_aether_passive
        parse_aether_passive()
        
    if args.aetherchallenge:
        from utils.events.aether import parse_aether_divide_challenge
        parse_aether_divide_challenge()

    if args.rewards:
        from utils.rewards import parse_rewards
        parse_rewards()
        
    if args.rogueendlessrewards:
        from utils.rewards import parse_rogue_endless_rewards
        parse_rogue_endless_rewards()

    if args.tutorial:
        parse_tutorial(str(args.tutorial))

    if args.heliobuschallenge:
        from utils.events.heliobus import parse_heliobus_challenge
        parse_heliobus_challenge()

    if args.heliobusraid:
        from utils.events.heliobus import parse_heliobus_raid
        parse_heliobus_raid(args.heliobusraid)

    if args.heliobususer:
        from utils.events.heliobus import parse_heliobus_user
        parse_heliobus_user()

    if args.heliobuspost:
        from utils.events.heliobus import parse_heliobus_post
        parse_heliobus_post()

    if args.heliobustemplate:
        from utils.events.heliobus import parse_heliobus_template
        parse_heliobus_template()

    if args.achievid:
        parse_achiev_id()

    if args.nousdicefaceicons:
        parse_nous_dice_face()

    if args.hardlevel:
        parse_hard_level()

    if args.purefiction:
        from utils.endgame import parse_pure_fiction_main
        parse_pure_fiction_main(args.purefiction)
        
    if args.purefictionv2:
        from utils.endgame import parse_pure_fiction_main_v2
        parse_pure_fiction_main_v2(args.purefictionv2)

    if args.fh:
        from utils.endgame import parse_pure_fiction_main
        parse_pure_fiction_main(args.fh, fh = True)

    if args.charasc:
        from utils.leveling import parse_char_asc
        parse_char_asc()
        
    if args.traceupgr:
        from utils.leveling import parse_trace_upgr
        parse_trace_upgr()

    if args.lcasc:
        from utils.leveling import parse_lc_asc
        parse_lc_asc()

    if args.text:
        from utils.text import parse_char_text
        parse_char_text(args.text)

    if args.techniquestatus:
        from utils.status import parse_technique_status
        parse_technique_status()
        
    if args.avatarstatus:
        from utils.status import parse_avatar_status
        parse_avatar_status()
        
    if args.monsterstatus:
        from utils.status import parse_monster_status
        parse_monster_status()
        
    if args.ol:
        copy_ol(args.ol)
        
    if args.apocshadow:
        from utils.endgame import parse_apoc_shadow
        parse_apoc_shadow(args.apocshadow)
        
    if args.redirectfromstr:
        from utils.redirect import redirects_from_str
        redirects_from_str(args.redirectfromstr)
