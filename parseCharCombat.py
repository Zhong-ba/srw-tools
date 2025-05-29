import json
import argparse
import os
import re

import utils.ol as ol
from utils.files import write_file
from utils.misc import autoround, convertwhole, copy_icon, parse_extraeffect
from utils.pageinfo import pageinfo
from getConfig import CONFIG

BUFFED_PREFIX = 'buffed_'

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=int)
parser.add_argument('--ver', type=float)
"""parser.add_argument('--sid', type=int)
parser.add_argument('--stype', type=str)
parser.add_argument('--sname', type=str)"""
parser.add_argument('--files', type=bool)
parser.add_argument('--enhanced', type=bool)

args = parser.parse_args()

char_id = str(args.id)
ver = str(args.ver)
"""specify_id = str(args.sid)
specify_type = str(args.stype)
specify_name = str(args.sname)"""
files = str(args.files)
ability_list = [['01', 'Basic_ATK_1'], ['02', 'Skill'], ['03', 'Ultimate'], ['04', 'Talent'], ['07', 'Technique'], ['08', 'Basic_ATK_2'], ['09', 'Skill_2'], ['11', 'Skill_3'], ['18', 'Path_Resonance']]
trace_list = [['101', 'A2'], ['102', 'A4'], ['103', 'A6']]
eidolon_list = [['01', 'E1'], ['02', 'E2'], ['03', 'E3'], ['04', 'E4'], ['05', 'E5'], ['06', 'E6']]

character = ''

ol.load_data()


def parseSkill(id, ver):
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarSkillConfig.json', 'r', encoding='utf-8') as file:
        avatarskillconfig = json.load(file)
    character = avatarconfig[str(args.id)[:4]]['AvatarName']['TextMapEN']
    levels = len(avatarskillconfig[id])
    name = avatarskillconfig[id]['1']['SkillName']['TextMapEN']
    type = avatarskillconfig[id]['1']['SkillTypeDesc']['TextMapEN']
    
    # rappa
    if type == "Path Resonance":
        type = "Basic ATK"
    
    try:
        tag = avatarskillconfig[id]['1']['SkillTag']['TextMapEN']
    except KeyError:
        tag = ''
    desc = avatarskillconfig[id]['1']['SkillDesc']['TextMapEN']
    
    if args.enhanced:
        original_id = id[1:]
        original_desc = avatarskillconfig[original_id]['1']['SkillDesc']['TextMapEN']
        if original_desc == desc:
            print(f'Enhanced skill {id} has the same description as original skill {original_id}. Skipping.')
            return
    
    if files:
        icon = avatarskillconfig[id]['1']['UltraSkillIcon']
        if not icon:
            icon = avatarskillconfig[id]['1']['SkillIcon']
        copy_icon(icon, f'Ability {name}.png', f'{character} Ability Icons')
      
    params = [key["Value"] for key in avatarskillconfig[id]['1']['ParamList']]
    if type == 'Basic ATK':
        level_possible = 8
    elif type == 'Technique':
        level_possible = 2
    else:
        level_possible = 13
    
    table_rows = ''
    
    for i in range(0, len(params)):
        levels = []
        for level in range(1, level_possible):
            if f'{i + 1}[i]%' in desc or f'{i + 1}[f1]%' in desc:
                levels.append(str(autoround(avatarskillconfig[id][str(level)]['ParamList'][i]['Value'] * 100)) + '%')
            else:
                levels.append(str(avatarskillconfig[id][str(level)]['ParamList'][i]['Value']))
        
        if type != 'Technique' and levels[0] != levels[1]:
            table_rows = table_rows + f'|{";".join(levels)}\n'
            pattern = re.compile(rf'#{i + 1}\[i\]%|#{i + 1}\[f1\]%|#{i + 1}\[i\]|#{i + 1}\[f1\]')
            desc = pattern.sub(f'{levels[0]}—{levels[-1]}', desc)
        else:
            pattern = re.compile(rf'#{i + 1}\[i\]%|#{i + 1}\[f1\]%|#{i + 1}\[i\]|#{i + 1}\[f1\]')
            desc = pattern.sub(f'{levels[0]}', desc)
    
    if type == 'Technique':
        param_table = ''
    elif type == 'Basic ATK':
        param_table = f'\n==Scaling==\n{{{{Skill Scaling|basicatk=1\n{table_rows}}}}}\n'
    else:
        param_table = f'\n==Scaling==\n{{{{Skill Scaling\n{table_rows}}}}}\n'
    
    toughdmg_main = int(avatarskillconfig[id]['1']['ShowStanceList'][0]['Value'] / 3)
    toughdmg_all = int(avatarskillconfig[id]['1']['ShowStanceList'][1]['Value'] / 3)
    toughdmg_adjacent = int(avatarskillconfig[id]['1']['ShowStanceList'][2]['Value'] / 3)
    
    if toughdmg_main != 0 and toughdmg_all == 0 and toughdmg_adjacent == 0:
        toughdmg_output = str(toughdmg_main)
    elif toughdmg_main != 0 and toughdmg_adjacent != 0:
        toughdmg_output = f'{toughdmg_main} (Main)<br />{toughdmg_adjacent} (Adjacent)'
    elif toughdmg_all != 0:
        toughdmg_output = str(toughdmg_all)
    else:
        toughdmg_output = ''
        
    try:
        energyGen = avatarskillconfig[id]['1']['SPBase']['Value']
    except KeyError:
        energyGen = ''
        
    try:
        energyCost = avatarskillconfig[id]['1']['SPNeed']['Value']
    except KeyError:
        energyCost = ''
    
    OLtext = ol.gen_ol(name)
    
    # parse extra effect
    extraeffect_idlist = avatarskillconfig[id]['1']['ExtraEffectIDList']
    if extraeffect_idlist:
        desc = parse_extraeffect(desc, extraeffect_idlist)
    
    page_content = (f"{pageinfo(name)}\n{{{{Ability Infobox\n|title      = {name}\n|image"
                    f"      = Ability {name}.png\n|character  = {character}\n|type       = {type}\n|tag        "
                    f"= {tag}\n|toughdmg   = {toughdmg_output}\n|energyGen  = {energyGen}\n|energyCost = {energyCost}"
                    f"\n|duration   = \n|desc       = {desc}\n|utility1   = \n|scale_att1 = \n}}}}\n'''{name}''' is"
                    f" [[{character}]]'s [[{type}]].\n<!--\n==Gameplay Notes==\n--><!--\n==Preview==\n{{{{Preview\n"
                    f"|file = {name} Preview\n}}}}\n-->{param_table}"
                    f"\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{ver}}}}}\n\n"
                    f"==Navigation==\n{{{{Ability Navbox}}}}")
    
    if args.enhanced:
        page_content = (f"|{BUFFED_PREFIX}type       = {type}\n|{BUFFED_PREFIX}tag        "
                        f"= {tag}\n|{BUFFED_PREFIX}toughdmg   = {toughdmg_output}\n|{BUFFED_PREFIX}energyGen  = {energyGen}\n|{BUFFED_PREFIX}energyCost = {energyCost}"
                        f"\n|{BUFFED_PREFIX}duration   = \n|{BUFFED_PREFIX}desc       = {desc}\n|{BUFFED_PREFIX}utility1   = \n|{BUFFED_PREFIX}scale_att1 = \n"
                        f"\n{param_table}")
    
    return(page_content)


def parseTrace(id, ver):
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarSkillTreeConfig-Mapped.json', 'r', encoding='utf-8') as file:
        skilltreeconfig = json.load(file)
    character = avatarconfig[str(args.id)[:4]]['AvatarName']['TextMapEN']
    name = skilltreeconfig[id]['1']['PointName']
    ascension = skilltreeconfig[id]['1']['AvatarPromotionLimit']
    desc = skilltreeconfig[id]['1']['PointDesc']
    
    if args.enhanced:
        original_id = id[1:]
        original_desc = skilltreeconfig[original_id]['1']['PointDesc']
        if original_desc == desc:
            print(f'Enhanced trace {id} has the same description as original trace {original_id}. Skipping.')
            return
    
    if files:
        icon = skilltreeconfig[id]['1']['IconPath']
        copy_icon(icon, f'Trace {name}.png', f'{character} Trace Icons')
      
    params = [key["Value"] for key in skilltreeconfig[id]['1']['ParamList']]
    
    for n in range(0, len(params)):
        param = convertwhole(autoround(params[n]))
        percent = convertwhole(autoround(param * 100))
        desc = desc.replace(f'#{n + 1}[i]%', f'{str(percent)}%')
        desc = desc.replace(f'#{n + 1}[f1]%', f'{str(percent)}%')
        desc = desc.replace(f'#{n + 1}[i]', f'{str(param)}')
        desc = desc.replace(f'#{n + 1}[f1]', f'{str(param)}')
    
    OLtext = ol.gen_ol(name)
    
    # parse extra effect
    extraeffect_idlist = skilltreeconfig[id]['1']['ExtraEffectIDList']
    if extraeffect_idlist:
        desc = parse_extraeffect(desc, extraeffect_idlist)
    
    page_content = f"{pageinfo(name)}\n{{{{Ability Infobox\n|title      = {name}\n|image      = Trace {name}.png\n|character  = {character}\n|type       = Bonus Ability\n|reqAsc     = {ascension}\n|duration   = \n|desc       = {desc}\n|scale_att1 = \n|utility1   = \n}}}}\n'''{{{{subst:PAGENAME}}}}''' is one of [[{character}]]'s [[Bonus Abilities]].\n<!--\n==Gameplay Notes==\n--><!--\n==Preview==\n-->\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{ver}}}}}\n\n==Navigation==\n{{{{Ability Navbox}}}}"
    
    if args.enhanced:
        page_content = (f"|{BUFFED_PREFIX}type       = Bonus Ability\n|{BUFFED_PREFIX}reqAsc     = {ascension}\n"
                        f"|{BUFFED_PREFIX}duration   = \n|{BUFFED_PREFIX}desc       = {desc}\n|{BUFFED_PREFIX}utility1   = \n|{BUFFED_PREFIX}scale_att1 = \n")
    
    return(page_content)

def parseEidolon(id, ver):
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarRankConfig-Mapped.json', 'r', encoding='utf-8') as file:
        rankconfig = json.load(file)
    character = avatarconfig[str(args.id)[:4]]['AvatarName']['TextMapEN']
    name = rankconfig[id]['Name']
    rank = rankconfig[id]['Rank']
    desc = rankconfig[id]['Desc']
    
    if args.enhanced:
        original_id = id[1:]
        original_desc = rankconfig[original_id]['Desc']
        if original_desc == desc:
            print(f'Enhanced eidolon {id} has the same description as original eidolon {original_id}. Skipping.')
            return
    
    if files:
        icon = rankconfig[id]['IconPath']
        copy_icon(icon, f'Eidolon {name}.png', f'{character} Eidolon Icons')
    
    try:  
        params = [key["Value"] for key in rankconfig[id]['Param']]
    except KeyError:
        params = []
    
    for n in range(0, len(params)):
        param = convertwhole(autoround(params[n]))
        percent = convertwhole(autoround(param * 100))
        desc = desc.replace(f'#{n + 1}[i]%', f'{str(percent)}%')
        desc = desc.replace(f'#{n + 1}[f1]%', f'{str(percent)}%')
        desc = desc.replace(f'#{n + 1}[i]', f'{str(param)}')
        desc = desc.replace(f'#{n + 1}[f1]', f'{str(param)}')
    
    OLtext = ol.gen_ol(name)
    
    utility = []
    
    if 'Ultimate Lv. +2' in desc:
        utility.append('Ultimate Level Increase')
    
    if 'Talent Lv. +2' in desc:
        utility.append('Talent Level Increase')
        
    if 'Skill Lv. +2' in desc:
        utility.append('Skill Level Increase')
        
    if 'Basic ATK Lv. +1' in desc:
        utility.append('Basic ATK Level Increase')
        
    if not utility:
        utility = ['', '']
        
    # parse extra effect
    extraeffect_idlist = rankconfig[id]['ExtraEffectIDList']
    if extraeffect_idlist:
        desc = parse_extraeffect(desc, extraeffect_idlist)
    
    page_content = f"{pageinfo(name)}\n{{{{Eidolon Infobox\n|title      = {name}\n|image      = Eidolon {name}.png\n|character  = {character}\n|level      = {rank}\n|duration   = \n|desc       = {desc}\n|scale_att1 = \n|utility1   = {utility[0]}\n|utility2   = {utility[1]}\n}}}}\n'''{name}''' is [[{character}]]'s Level {rank} Eidolon.\n<!--\n==Gameplay Notes==\n--><!--\n==Preview==\n-->\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{ver}}}}}\n\n==Navigation==\n{{{{Ability Navbox}}}}"
    
    if args.enhanced:
        page_content = (f"|{BUFFED_PREFIX}level      = {rank}\n|{BUFFED_PREFIX}duration   = \n|{BUFFED_PREFIX}desc       = {desc}\n"
                        f"|{BUFFED_PREFIX}utility1   = {utility[0]}\n|{BUFFED_PREFIX}utility2   = {utility[1]}\n")
    
    return(page_content)


def parseServantSkill(id, ver):
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarServantSkillConfig.json', 'r', encoding='utf-8') as file:
        servantskillconfig = json.load(file)
    character = avatarconfig[str(args.id)[:4]]['AvatarName']['TextMapEN']
    levels = len(servantskillconfig[id])
    name = servantskillconfig[id]['1']['SkillName']['TextMapEN']
    type = servantskillconfig[id]['1']['SkillTypeDesc']['TextMapEN']
    
    try:
        tag = servantskillconfig[id]['1']['SkillTag']['TextMapEN']
    except KeyError:
        tag = ''
    desc = servantskillconfig[id]['1']['SkillDesc']['TextMapEN']
    
    if files:
        icon = servantskillconfig[id]['1']['UltraSkillIcon']
        if not icon:
            icon = servantskillconfig[id]['1']['SkillIcon']
        copy_icon(icon, f'Ability {name}.png', f'{character} Ability Icons')
      
    params = [key["Value"] for key in servantskillconfig[id]['1']['ParamList']]
    level_possible = 8
    
    table_rows = ''

    for i in range(0, len(params)):
        levels = []
        for level in range(1, level_possible):
            if f'{i + 1}[i]%' in desc or f'{i + 1}[f1]%' in desc:
                levels.append(str(autoround(servantskillconfig[id][str(level)]['ParamList'][i]['Value'] * 100)) + '%')
            else:
                levels.append(str(servantskillconfig[id][str(level)]['ParamList'][i]['Value']))
        
        if levels[0] != levels[1]:
            table_rows = table_rows + f'|{";".join(levels)}\n'
            pattern = re.compile(rf'#{i + 1}\[i\]%|#{i + 1}\[f1\]%|#{i + 1}\[i\]|#{i + 1}\[f1\]')
            desc = pattern.sub(f'{levels[0]}—{levels[-1]}', desc)
        else:
            pattern = re.compile(rf'#{i + 1}\[i\]%|#{i + 1}\[f1\]%|#{i + 1}\[i\]|#{i + 1}\[f1\]')
            desc = pattern.sub(f'{levels[0]}', desc)          
    
    if table_rows:
        param_table = f'\n==Scaling==\n{{{{Skill Scaling|basicatk=1\n{table_rows}}}}}\n'
    else:
        param_table = ''
    
    toughdmg_main = int(servantskillconfig[id]['1']['ShowStanceList'][0]['Value'] / 3)
    toughdmg_all = int(servantskillconfig[id]['1']['ShowStanceList'][1]['Value'] / 3)
    toughdmg_adjacent = int(servantskillconfig[id]['1']['ShowStanceList'][2]['Value'] / 3)
    
    if toughdmg_main != 0 and toughdmg_all == 0 and toughdmg_adjacent == 0:
        toughdmg_output = str(toughdmg_main)
    elif toughdmg_main != 0 and toughdmg_adjacent != 0:
        toughdmg_output = f'{toughdmg_main} (Main)<br />{toughdmg_adjacent} (Adjacent)'
    elif toughdmg_all != 0:
        toughdmg_output = str(toughdmg_all)
    else:
        toughdmg_output = ''
        
    try:
        energyGen = servantskillconfig[id]['1']['SPBase']['Value']
    except KeyError:
        energyGen = ''
        
    try:
        energyCost = servantskillconfig[id]['1']['SPNeed']['Value']
    except KeyError:
        energyCost = ''
        
    # parse extra effect
    extraeffect_idlist = servantskillconfig[id]['1']['ExtraEffectIDList']
    if extraeffect_idlist:
        desc = parse_extraeffect(desc, extraeffect_idlist)
    
    OLtext = ol.gen_ol(name)
    
    page_content = (f"{pageinfo(name)}\n{{{{Ability Infobox\n|title      = {name}\n|image"
                    f"      = Ability {name}.png\n|character  = {character}\n|type       = {type}\n|tag        "
                    f"= {tag}\n|toughdmg   = {toughdmg_output}\n|energyGen  = {energyGen}\n|energyCost = {energyCost}"
                    f"\n|duration   = \n|desc       = {desc}\n|utility1   = \n|scale_att1 = \n}}}}\n'''{name}''' is"
                    f" [[{character}]]'s [[{type}]].\n<!--\n==Gameplay Notes==\n--><!--\n==Preview==\n{{{{Preview\n"
                    f"|file = {name} Preview\n}}}}\n-->{param_table}"
                    f"\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{ver}}}}}\n\n"
                    f"==Navigation==\n{{{{Ability Navbox}}}}")
    
    return(page_content)


def parseGlobal(id, ver):
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarGlobalBuffConfig.json', 'r', encoding='utf-8') as file:
        avatarglobalconfig = json.load(file)
    
    if not avatarglobalconfig.get(id):
        print(f"No global passive found for {id}.")
        return
    
    character = avatarconfig[str(args.id)[:4]]['AvatarName']['TextMapEN']
    name = avatarglobalconfig[id]['Name']['TextMapEN']
    type = 'Unique'
    
    try:
        tag = avatarglobalconfig[id]['SkillTag']['TextMapEN']
    except KeyError:
        tag = ''
    desc = avatarglobalconfig[id]['Desc']['TextMapEN']
    
    if files:
        icon = f"spriteoutput/skillicons/avatar/{id}/SkillIcon_{id}_Passive.png"
        copy_icon(icon, f'Ability {name}.png', f'{character} Ability Icons')
      
    params = [key["Value"] for key in avatarglobalconfig[id]['ParamList']]
    level_possible = 2
    
    for n in range(0, len(params)):
        param = convertwhole(autoround(params[n]))
        percent = convertwhole(autoround(param * 100))
        desc = desc.replace(f'#{n + 1}[i]%', f'{str(percent)}%')
        desc = desc.replace(f'#{n + 1}[f1]%', f'{str(percent)}%')
        desc = desc.replace(f'#{n + 1}[i]', f'{str(param)}')
        desc = desc.replace(f'#{n + 1}[f1]', f'{str(param)}')
    
    param_table = ''
    
    toughdmg_output = ''
    if avatarglobalconfig[id].get('ShowStanceList'):
        toughdmg_main = int(avatarglobalconfig[id]['ShowStanceList'][0]['Value'] / 3)
        toughdmg_all = int(avatarglobalconfig[id]['ShowStanceList'][1]['Value'] / 3)
        toughdmg_adjacent = int(avatarglobalconfig[id]['ShowStanceList'][2]['Value'] / 3)
        
        if toughdmg_main != 0 and toughdmg_all == 0 and toughdmg_adjacent == 0:
            toughdmg_output = str(toughdmg_main)
        elif toughdmg_main != 0 and toughdmg_adjacent != 0:
            toughdmg_output = f'{toughdmg_main} (Main)<br />{toughdmg_adjacent} (Adjacent)'
        elif toughdmg_all != 0:
            toughdmg_output = str(toughdmg_all)
        
    try:
        energyGen = avatarglobalconfig[id]['SPBase']['Value']
    except KeyError:
        energyGen = ''
        
    try:
        energyCost = avatarglobalconfig[id]['SPNeed']['Value']
    except KeyError:
        energyCost = ''
    
    OLtext = ol.gen_ol(name)
    
    # parse extra effect
    extraeffect_idlist = avatarglobalconfig[id]['ExtraEffectIDList']
    if extraeffect_idlist:
        desc = parse_extraeffect(desc, extraeffect_idlist)
    
    page_content = (f"{pageinfo(name)}\n{{{{Ability Infobox\n|title      = {name}\n|image"
                    f"      = Ability {name}.png\n|character  = {character}\n|type       = {type}\n|tag        "
                    f"= {tag}\n|toughdmg   = {toughdmg_output}\n|energyGen  = {energyGen}\n|energyCost = {energyCost}"
                    f"\n|duration   = \n|desc       = {desc}\n|utility1   = \n|scale_att1 = \n}}}}\n'''{name}''' is"
                    f" [[{character}]]'s [[{type}]].\n<!--\n==Gameplay Notes==\n--><!--\n==Preview==\n{{{{Preview\n"
                    f"|file = {name} Preview\n}}}}\n-->{param_table}"
                    f"\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{ver}}}}}\n\n"
                    f"==Navigation==\n{{{{Ability Navbox}}}}")
    
    return(page_content)


with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarConfig.json', 'r', encoding='utf-8') as file:
    avatarconfig = json.load(file)
        
if not char_id == "None":
    character = avatarconfig[char_id]['AvatarName']['TextMapEN']

    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/{character}/Abilities'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}/{character}/Abilities')
    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/{character}/Traces'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}/{character}/Traces')
    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/{character}/Eidolons'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}/{character}/Eidolons')

    for ability in ability_list:
        file_write_path = f'{CONFIG.OUTPUT_PATH}/{character}/Abilities/{ability[1]}.wikitext'
        id = f'{char_id}{ability[0]}'
        if args.enhanced:
            id = f'1{id}'
        try:
            write = parseSkill(id, ver)
            if write:
                write_file(file_write_path, write)
        except KeyError as err:
            print(f'Skipped {id}. ({err})')
        
    for trace in trace_list:
        file_write_path = f'{CONFIG.OUTPUT_PATH}/{character}/Traces/{trace[1]}.wikitext'
        id = f'{char_id}{trace[0]}'
        if args.enhanced:
            id = f'1{id}'
        
        write = parseTrace(id, ver)
        if write:
            write_file(file_write_path, write)
        
    for eidolon in eidolon_list:
        file_write_path = f'{CONFIG.OUTPUT_PATH}/{character}/Eidolons/{eidolon[1]}.wikitext'
        id = f'{char_id}{eidolon[0]}'
        if args.enhanced:
            id = f'1{id}'
            
        write = parseEidolon(id, ver)
        if write:
            write_file(file_write_path, write)
    
    # global passive
    global_file_write_path = f'{CONFIG.OUTPUT_PATH}/{character}/Abilities/Global Passive.wikitext'
    global_content = parseGlobal(char_id, ver)
    if global_content:
        write_file(global_file_write_path, global_content)
        
    # servants    
    if avatarconfig[char_id]['AvatarBaseType'] == 'Memory':
        print('==========Memosprite Skills==========')
        
        servant_id = f'1{char_id}'
        
        with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/AvatarServantConfig.json', 'r', encoding='utf-8') as file:
            servantconfig = json.load(file)

        servant = servantconfig[servant_id]
        servant_skills = [str(servant_skill) for servant_skill in servant['SkillIDList']]
        
        for servant_skill in servant_skills:
            file_write_path = f'{CONFIG.OUTPUT_PATH}/{character}/Abilities/Servant {servant_skill}.wikitext'
            write_file(file_write_path, parseServantSkill(servant_skill, ver))
        
        
        
"""if specify_id != "None" and specify_type != "None" and specify_name != "None":
    if specify_type == "skill":
        file_write_path = f'{specify_name}.wikitext'
        with open(file_write_path, 'w', encoding='utf-8') as file:
            file.write(parseSkill(specify_id, ver))
        print('Saved to ' + file_write_path + '.')
        
    elif specify_type == "trace":
        file_write_path = f'{specify_name}.wikitext'
        with open(file_write_path, 'w', encoding='utf-8') as file:
            file.write(parseTrace(specify_id, ver))
        print('Saved to ' + file_write_path + '.')
        
    elif specify_type == "eidolon":
        file_write_path = f'{specify_name}.wikitext'
        with open(file_write_path, 'w', encoding='utf-8') as file:
            file.write(parseEidolon(specify_id, ver))
        print('Saved to ' + file_write_path + '.')"""