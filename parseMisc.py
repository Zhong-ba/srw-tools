import json
import argparse
import shutil
import os
import re
import pyperclip

import utils.ol as ol
from utils.redirect import file_redirect
from utils.misc import parse_params, parse_reward_text, autoround, convertwhole, dict_to_table
from utils.target import parse_battle_target, parse_raid_target
from getConfig import CONFIG

TEXTMAP_PATH = f'{CONFIG.DATA_PATH}/TextMap'


def parse_rewards():
    file_write_path =f'{CONFIG.OUTPUT_PATH}/Rewards.txt'

    with open(f'{CONFIG.EXCEL_PATH}/QuestData.json', 'r', encoding = 'utf-8') as file:
        questjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    output = ''

    for quest in questjson:
        try:
            title = questjson[quest]['QuestTitle']['TextMapEN']
        except KeyError:
            title = ''
        try:
            display = questjson[quest]['QuestDisplay']['TextMapEN']
        except KeyError:
            display = ''

        if title:
            if display:
                objective_txt = f"'''{title}'''<br />{display}"
            else:
                objective_txt = title

            reward_id = str(questjson[quest]['RewardID'])
            reward_text = ''

            for n in range(9):
                try:
                    item_id = str(rewardjson[reward_id][f'ItemID_{n + 1}'])
                    item_name = itemjson[item_id]['ItemName']['TextMapEN']
                    count = rewardjson[reward_id][f'Count_{n + 1}']
                    if n == 0:
                        reward_text = reward_text + f'{item_name}*{count}'
                    else:
                        reward_text = reward_text + f',{item_name}*{count}'
                except KeyError:
                    continue

            output = output + f'\n|-\n| {objective_txt} || {{{{Card List|{reward_text}}}}}'

    with open(file_write_path, 'w') as file:
        file.write(output)
        print('Saved to ' + file_write_path + '.')


def parse_rogue_endless_rewards():
    file_write_path =f'{CONFIG.OUTPUT_PATH}/RogueEndlessRewards.txt'

    with open(f'{CONFIG.EXCEL_PATH}/ActivityRewardRogueEndless.json', 'r', encoding = 'utf-8') as file:
        rewardrogueendlessjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

    output = ''

    for quest in rewardrogueendlessjson:
        print(quest)
        name = rewardrogueendlessjson[quest]['RewardLevelName']['TextMapEN']
        point = rewardrogueendlessjson[quest]['RewardPoint']
        name = name.replace('#1', str(point))

        reward_id = str(rewardrogueendlessjson[quest]['RewardID'])
        reward_text = ''

        for n in range(9):
            try:
                item_id = str(rewardjson[reward_id][f'ItemID_{n + 1}'])
                item_name = itemjson[item_id]['ItemName']['TextMapEN']
                count = rewardjson[reward_id][f'Count_{n + 1}']
                if n == 0:
                    reward_text = reward_text + f'{item_name}*{count}'
                else:
                    reward_text = reward_text + f',{item_name}*{count}'
            except KeyError:
                print(reward_text)

        try:
            hcoin = str(rewardjson[reward_id]['Hcoin'])
        except KeyError:
            hcoin = ''

        if hcoin:
            reward_text = f'Stellar Jade*{hcoin}'

        output = output + f'\n|-\n| {name} || {{{{Card List|{reward_text}}}}}'

    with open(file_write_path, 'w') as file:
        file.write(output)
        print('Saved to ' + file_write_path + '.')


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


def copy_file(source_path, destination_path):
    if os.path.exists(source_path):
        dest_dir = destination_path.replace(destination_path.split('/')[-1], '')
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy(source_path, destination_path)
        print(f"File copied successfully from {source_path} to {destination_path}")
    else:
        print(f"The file {source_path} does not exist.")


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


def write_file(file_write_path, file_write):
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





def parse_char_asc():
    out_dict = {}

    with open(f'{CONFIG.EXCEL_PATH}/AvatarPromotionConfig.json', 'r', encoding = 'utf-8') as file:
        promotejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/AvatarConfig.json', 'r', encoding = 'utf-8') as file:
        avatarjson = json.load(file)

    for key, value in promotejson.items():
        if key in ['8003', '8004']:
            name = 'Trailblazer (Preservation)'
        elif key in ['8001', '8002']:
            name = 'Trailblazer (Destruction)'
        elif key in ['8005', '8006']:
            name = 'Trailblazer (Harmony)'
        elif key in ['8007', '8008']:
            name = 'Trailblazer (Remembrance)'
        elif key == '1001':
            name = 'March 7th (Preservation)'
        elif key == '1224':
            name = 'March 7th (The Hunt)'
        else:
            name = avatarjson[key]['AvatarName']['TextMapEN']
        out_dict[name] = {}

        rarity = int(avatarjson[key]['Rarity'][-1:])
        out_dict[name]['rarity'] = rarity

        boss = value['3']['PromotionCostList'][2]['ItemName']['TextMapEN']
        out_dict[name]['boss'] = boss

        common = [
            value['1']['PromotionCostList'][1]['ItemName']['TextMapEN'],
            value['3']['PromotionCostList'][1]['ItemName']['TextMapEN'],
            value['5']['PromotionCostList'][1]['ItemName']['TextMapEN'],
        ]
        out_dict[name]['common'] = common

        out_dict[name]['hp'] = value['1']['HPBase']['Value']
        out_dict[name]['atk'] = value['1']['AttackBase']['Value']
        out_dict[name]['def'] = value['1']['DefenceBase']['Value']
        out_dict[name]['spd'] = value['1']['SpeedBase']['Value']

    file_write_path =f'{CONFIG.OUTPUT_PATH}/Character_Ascension_and_Stats_data.lua'
    file_write = (f"--[=[<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some "
                  f"important information of edit. This struct will be removed automatically after you push edits.#\n "
                  f"   pageTitle = #Module:Character Ascensions and Stats/data#\n    pageID = ##\n    revisionID = "
                  f"##\n    contentModel = #Scribunto#\n    contentFormat = #text/plain#\n[END_PAGE_INFO] "
                  f"--%>--]=]\n\nreturn {dict_to_table(out_dict)}")

    write_file(file_write_path, file_write)
    

def parse_trace_upgr():
    out_dict = {}

    with open(f'{CONFIG.EXCEL_PATH}/AvatarSkillTreeConfig-Mapped.json', 'r', encoding = 'utf-8') as file:
        skilltree = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/AvatarConfig.json', 'r', encoding = 'utf-8') as file:
        avatarjson = json.load(file)

    for key, value in avatarjson.items():
        if key in ['8003', '8004']:
            name = 'Trailblazer (Preservation)'
        elif key in ['8001', '8002']:
            name = 'Trailblazer (Destruction)'
        elif key in ['8005', '8006']:
            name = 'Trailblazer (Harmony)'
        elif key in ['8007', '8008']:
            name = 'Trailblazer (Remembrance)'
        elif key == '1001':
            name = 'March 7th (Preservation)'
        elif key == '1224':
            name = 'March 7th (The Hunt)'
        else:
            name = value['AvatarName']['TextMapEN']
        out_dict[name] = {}

        rarity = int(value['Rarity'][-1:])
        out_dict[name]['rarity'] = rarity

        trace1 = key + '101'
        trace2 = key + '102'
        trace3 = key + '103'
        ult = key + '003'
        
        common = [
            skilltree[ult]['2']['MaterialList'][1]['ItemName']['TextMapEN'],
            skilltree[ult]['4']['MaterialList'][2]['ItemName']['TextMapEN'],
            skilltree[ult]['7']['MaterialList'][2]['ItemName']['TextMapEN'],
        ]
        
        out_dict[name]['common'] = common
        
        trace = [
            skilltree[trace1]['1']['MaterialList'][1]['ItemName']['TextMapEN'],
            skilltree[trace2]['1']['MaterialList'][1]['ItemName']['TextMapEN'],
            skilltree[trace3]['1']['MaterialList'][1]['ItemName']['TextMapEN'],
        ]
        
        out_dict[name]['trace'] = trace
        
        boss = skilltree[trace1]['1']['MaterialList'][2]['ItemName']['TextMapEN']
        out_dict[name]['boss'] = boss

    file_write_path =f'{CONFIG.OUTPUT_PATH}/Trace_Upgrades_data.lua'
    file_write = (f"--[=[<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some "
                  f"important information of edit. This struct will be removed automatically after you push edits.#\n "
                  f"   pageTitle = #Module:Trace Upgrades/data#\n    pageID = ##\n    revisionID = "
                  f"##\n    contentModel = #Scribunto#\n    contentFormat = #text/plain#\n[END_PAGE_INFO] "
                  f"--%>--]=]\n\nreturn {dict_to_table(out_dict)}")

    write_file(file_write_path, file_write)


def parse_lc_asc():
    out_dict = {}

    with open(f'{CONFIG.EXCEL_PATH}/EquipmentPromotionConfig.json', 'r', encoding = 'utf-8') as file:
        promotejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/EquipmentConfig.json', 'r', encoding = 'utf-8') as file:
        equipjson = json.load(file)

    for key, value in promotejson.items():
        name = equipjson[key]['EquipmentName']['TextMapEN']
        out_dict[name] = {}

        rarity = int(equipjson[key]['Rarity'][-1:])
        out_dict[name]['rarity'] = rarity

        cone = [
            value['2']['PromotionCostList'][1]['ItemName']['TextMapEN'],
            value['3']['PromotionCostList'][1]['ItemName']['TextMapEN'],
            value['5']['PromotionCostList'][1]['ItemName']['TextMapEN'],
        ]
        out_dict[name]['cone'] = cone

        common = [
            value['1']['PromotionCostList'][1]['ItemName']['TextMapEN'],
            value['3']['PromotionCostList'][2]['ItemName']['TextMapEN'],
            value['5']['PromotionCostList'][2]['ItemName']['TextMapEN'],
        ]
        out_dict[name]['common'] = common

        out_dict[name]['hp'] = value['1']['BaseHP']['Value']
        out_dict[name]['atk'] = value['1']['BaseAttack']['Value']
        out_dict[name]['def'] = value['1']['BaseDefence']['Value']

    file_write_path =f'{CONFIG.OUTPUT_PATH}/Light_Cone_Ascension_and_Stats_data.lua'
    file_write = (f"--[=[<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some "
                  f"important information of edit. This struct will be removed automatically after you push edits.#\n "
                  f"   pageTitle = #Module:Light Cone Ascensions and Stats/data#\n    pageID = ##\n    revisionID = "
                  f"##\n    contentModel = #Scribunto#\n    contentFormat = #text/plain#\n[END_PAGE_INFO] "
                  f"--%>--]=]\n\nreturn {dict_to_table(out_dict)}")

    write_file(file_write_path, file_write)


def preprocess_text(sec_id: int) -> list:
    print(f'PREPROCESSING {sec_id}')
    out = []
    msgitem_ls = []
    allnext_ls = []
    start_ls = []
    end_ls = []

    with open(f'{CONFIG.EXCEL_PATH}/MessageItemConfig.json', 'r', encoding = 'utf-8') as file:
        msgitemjson = json.load(file)

    for msgitem in msgitemjson.values():
        if msgitem.get('SectionID') == sec_id:
            msgitem_ls.append(msgitem['ID'])

    # convergence points
    for msgitem in msgitem_ls:
        next_ls = msgitemjson[str(msgitem)]['NextItemIDList']
        if len(next_ls) > 0:
            if next_ls[0] in allnext_ls and next_ls[0] not in end_ls:
                end_ls.append(next_ls[0])
            allnext_ls = allnext_ls + next_ls

        if len(next_ls) > 1:
            start_ls.append(msgitem)

    out = [[start, end] for start, end in zip(start_ls, end_ls)]
    return out


def parse_text_sec(sec_id, char_name):
    out = ''

    with open(f'{CONFIG.EXCEL_PATH}/MessageItemConfig.json', 'r', encoding = 'utf-8') as file:
        msgitemjson = json.load(file)

    msgitem_id = str(sec_id) + '00'
    complete = False

    branch_ls = preprocess_text(sec_id)

    """while not complete:
        sender = '(Trailblazer)' if msgitemjson[msgitem_id]['Sender'] == 'Player' else char_name
        text = msgitemjson[msgitem_id]['MainText']['TextMapEN']
        try:
            option_text = msgitemjson[msgitem_id]['OptionText']['TextMapEN']
        except KeyError:
            option_text = ''

        if option_text:
            out = f"{out}\n{indent[:-1]}{{{{DIcon}}}} {option_text}\n{indent}'''{sender}:''' {text}"
        else:
            out = f"{out}\n{indent}'''{sender}:''' {text}\n"

        if msgitemjson[msgitem_id]['NextItemIDList']:
            if msgitemjson[msgitem_id]['NextItemIDList'] == end_point:"""


def parse_char_text(char_name):
    with open(f'{CONFIG.EXCEL_PATH}/MessageContactsConfig.json', 'r', encoding = 'utf-8') as file:
        contactjson = json.load(file)

    char_id = ''
    for contact in contactjson.values():
        if contact['Name'].get('TextMapEN') == char_name:
            char_id = contact['ID']
            signature = contact['SignatureText']['TextMapEN']

    # message groups
    message_sec_ids = []

    with open(f'{CONFIG.EXCEL_PATH}/MessageGroupConfig.json', 'r', encoding = 'utf-8') as file:
        msggrpjson = json.load(file)

    for msggrp in msggrpjson.values():
        if msggrp['MessageContactsID'] == char_id:
            message_sec_ids.append(msggrp['MessageSectionIDList'][0])

    for sec_id in message_sec_ids:
        parse_text_sec(sec_id, char_name)


def parse_technique_status():
    with open(f'{CONFIG.EXCEL_PATH}/AvatarMazeBuff.json', 'r', encoding = 'utf-8') as file:
        mazebuffjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/AvatarSkillConfig.json', 'r', encoding = 'utf-8') as file:
        avatarskilljson = json.load(file)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/Technique_Status_Output.wikitext'

    for entry_id in mazebuffjson.values():
        entry = entry_id['1']
        
        name = entry.get('BuffName').get('TextMapEN')
        if not name:
            continue
        print(name)

        # desc
        desc = entry.get('BuffDesc').get('TextMapEN')
        params_id = str(entry.get('BuffDescParamByAvatarSkillID'))

        skill_name = str(entry.get('id'))
        if params_id != 'None':
            params = avatarskilljson[params_id]['1']['ParamList']
            desc = parse_params(desc, params)
            skill_name = avatarskilljson[params_id]['1']['SkillName']['TextMapEN'].replace(' ', '_')

        # file
        image = CONFIG.IMAGE_PATH + '/spriteoutput/bufficon/inlevel/avatar/' + entry.get('BuffIcon').split('/')[-1]
        image_2 = CONFIG.IMAGE_PATH + '/spriteoutput/bufficon/inlevel/' + entry.get('BuffIcon').split('/')[-1]
        image_name = f'Icon {name}.png'
        image_name_clean = image_name.replace(':', '')
        dest_path = f'{CONFIG.OUTPUT_PATH}/Technique_Status_Icons/{image_name_clean}'

        if image_name != image_name_clean:
            file_redirect(image_name, image_name_clean)

        copy_file(image, dest_path)
        copy_file(image_2, dest_path)

        # output
        type1 = entry.get('MazeBuffIconType')
        if type1 in ['Buff', 'Debuff']:
            type2 = type1
        else:
            type2 = 'Status Effect'

        

        out = f'''
<!-------------- {skill_name} --------------->

==Unique Status Effects==
;{type1}s
{{{{Unique {type2}
|name1 = {name}
|desc1 = {desc}
}}}}
'''

        file_write = file_write + out

    write_file(file_write_path, file_write)
    

def parse_avatar_status():
    with open(f'{CONFIG.EXCEL_PATH}/AvatarStatusConfig.json', 'r', encoding = 'utf-8') as file:
        mazebuffjson = json.load(file)
        
    with open(f'{CONFIG.EXCEL_PATH_OLD}/AvatarStatusConfig.json', 'r', encoding = 'utf-8') as file:
        old_mazebuffjson = json.load(file)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/Avatar_Status_Output.wikitext'

    for key, entry in mazebuffjson.items():
        has_name = entry.get('StatusName')
        if not has_name:
            continue
        
        name = has_name.get('TextMapEN')
        
        if old_mazebuffjson.get(key):
            print(f'Skipped {name}.')
            continue

        # desc
        desc = entry.get('StatusDesc').get('TextMapEN')

        # file
        image = CONFIG.IMAGE_PATH + '/spriteoutput/bufficon/inlevel/avatar/' + entry.get('StatusIconPath').split('/')[-1]
        
        if not re.findall(r'Icon\d\d\d\d', image):
            print(f'Skipped {name}. (No Unique Icon)')
            continue
        
        image_name = f'Icon {name}.png'
        image_name_clean = image_name.replace(':', '').replace('?', '')
        dest_path = f'{CONFIG.OUTPUT_PATH}/Avatar_Status_Icons/{image_name_clean}'

        if image_name != image_name_clean:
            file_redirect(image_name, image_name_clean)

        copy_file(image, dest_path)

        # output
        type1 = entry.get('StatusType')
        if type1 in ['Buff', 'Debuff']:
            type2 = type1
        else:
            type2 = 'Status Effect'

        out = f'''
<!-------------- {entry.get('ModifierName')} --------------->

==Unique Status Effects==
;{type1}s
{{{{Unique {type2}
|name1 = {name}
|desc1 = {desc}
}}}}
'''

        file_write = file_write + out

    write_file(file_write_path, file_write)
    
    
def parse_monster_status():
    with open(f'{CONFIG.EXCEL_PATH}/MonsterStatusConfig.json', 'r', encoding = 'utf-8') as file:
        mazebuffjson = json.load(file)
        
    with open(f'{CONFIG.EXCEL_PATH_OLD}/MonsterStatusConfig.json', 'r', encoding = 'utf-8') as file:
        old_mazebuffjson = json.load(file)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/Monster_Status_Output.wikitext'

    for key, entry in mazebuffjson.items():
        name = entry.get('StatusName').get('TextMapEN')
        if not name:
            continue
        
        if old_mazebuffjson.get(key):
            print(f'Skipped {name}.')
            continue

        # desc
        desc = entry.get('StatusDesc').get('TextMapEN')

        # file
        image = CONFIG.IMAGE_PATH + '/spriteoutput/bufficon/inlevel/' + entry.get('StatusIconPath').split('/')[-1]
        
        image_name = f'Icon {name}.png'
        image_name_clean = image_name.replace(':', '').replace('?', '')
        dest_path = f'{CONFIG.OUTPUT_PATH}/Monster_Status_Icons/{image_name_clean}'

        if image_name != image_name_clean:
            file_redirect(image_name, image_name_clean)

        copy_file(image, dest_path)

        # output
        type1 = entry.get('StatusType')
        if type1 in ['Buff', 'Debuff']:
            type2 = type1
        else:
            type2 = 'Status Effect'

        out = f'''
<!-------------- {entry.get('ModifierName')} --------------->

==Unique Status Effects==
;{type1}s
{{{{Unique {type2}
|name1 = {name}
|desc1 = {desc}
}}}}
'''

        file_write = file_write + out

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
        parse_rewards()
        
    if args.rogueendlessrewards:
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
        parse_char_asc()
        
    if args.traceupgr:
        parse_trace_upgr()

    if args.lcasc:
        parse_lc_asc()

    if args.text:
        parse_char_text(args.text)

    if args.techniquestatus:
        parse_technique_status()
        
    if args.avatarstatus:
        parse_avatar_status()
        
    if args.monsterstatus:
        parse_monster_status()
        
    if args.ol:
        copy_ol(args.ol)
        
    if args.apocshadow:
        from utils.endgame import parse_apoc_shadow
        parse_apoc_shadow(args.apocshadow)
        
    if args.redirectfromstr:
        from utils.redirect import redirects_from_str
        redirects_from_str(args.redirectfromstr)
