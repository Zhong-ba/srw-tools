import json
import argparse
import re
import os
import shutil
from config import CONFIG
from parseMisc import parse_extraeffect

IMAGE_PATH = f'{CONFIG["ImgPath"]}/assets/asbres/'
EXCEL_PATH = f'{CONFIG["DataPath"]}/MappedExcelOutput_EN'
OLD_PATH = f'{CONFIG["DataPathOld"]}/MappedExcelOutput_EN'
OUT_PATH = CONFIG["OutputPath"]

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=int)
parser.add_argument('--ver', type=float)
parser.add_argument('--files', type=bool)
parser.add_argument('--ids', nargs='+')
parser.add_argument('--new', type=bool)
args = parser.parse_args()

mons_id = str(args.id) if args.id else None
id_list: list = args.ids or []
ver = str(args.ver)
files = args.files


def copy_file(source_path, destination_path):
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f"File copied successfully from {source_path} to {destination_path}")
    else:
        print(f"The file {source_path} does not exist.")
        
        
def write_file(file_write_path, file_write):
    if os.path.exists(file_write_path):
        print(f'The file {file_write_path} already exists. Skipping.')
        return
    
    with open(file_write_path, 'w', encoding='utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')    


def file_redirect(target, source):
    if not os.path.exists(f'{OUT_PATH}/Redirects'):
            os.makedirs(f'{OUT_PATH}/Redirects')
    
    file_write_path = f'{OUT_PATH}/Redirects/{source}.wikitext'
    file_write = f"<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some important information of edit. This struct will be removed automatically after you push edits.#\n    pageTitle = #File:{target}#\n    pageID = ##\n    revisionID = ##\n    contentModel = ##\n    contentFormat = ##\n[END_PAGE_INFO] --%>\n\n#REDIRECT [[File:{source}]]\n[[Category:Redirect Pages]]"
    
    write_file(file_write_path, file_write)
    

def copy_icon(source, name, folder):
    file_name_clean = name.replace(":", "").replace("/", "").replace("\"", "")
    
    if file_name_clean != name:
        file_redirect(name, file_name_clean)
        
    src = IMAGE_PATH + source.lower()
    
    dest = f'{OUT_PATH}/Images/{folder}/{file_name_clean}'
    
    if not os.path.exists(f'{OUT_PATH}/Images/{folder}'):
            os.makedirs(f'{OUT_PATH}/Images/{folder}')
    
    copy_file(src, dest)
        

def autoround(value):
    s_value = str(value)

    patterns = ['999', '998', '000', '001']

    for pattern in patterns:
        position = s_value.find(pattern)
        if position != -1:
            # Position of the pattern minus position of the dot gives the number of decimal places
            return round(value, position - s_value.find('.'))

    return value


def convertwhole(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    else:
        return value
    

langs = ['CHS','CHT','DE','EN','ES','FR','ID','JP','KR','PT','RU','TH','VI']
data = {}
for lang in langs:
    with open(f'{CONFIG["DataPath"]}/TextMap/TextMap{lang}.json', 'r', encoding='utf-8') as file:
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


with open(f'{EXCEL_PATH}/MonsterConfig.json', 'r', encoding='utf-8') as file:
    monsterconfig = json.load(file)
    
with open(f'{OLD_PATH}/MonsterConfig.json', 'r', encoding='utf-8') as file:
    monsterconfig_old = json.load(file)
    
with open(f'{EXCEL_PATH}/MonsterTemplateConfig.json', 'r', encoding='utf-8') as file:
    monstertemplateconfig = json.load(file)
    
with open(f'{EXCEL_PATH}/MonsterSkillConfig.json', 'r', encoding='utf-8') as file:
    monsterskillconfig = json.load(file)

with open(f'{EXCEL_PATH}/MonsterCamp.json', 'r', encoding='utf-8') as file:
    monstercamp = json.load(file)


def parseMonster(id, ver):        
    name = monsterconfig[id]['MonsterName']['TextMapEN']
    print(f'=========={name}==========')
    
    filename = name.replace(' (Bug)', '').replace(' (Complete)', '').replace(' (Error)', '')
    template_id = str(monsterconfig[id]['MonsterTemplateID'])
    intro = monsterconfig[id]['MonsterIntroduction']['TextMapEN']
    skill_list = monsterconfig[id]['SkillList']
    
    #tier
    if monstertemplateconfig[template_id]['Rank'] == 'BigBoss':
        tier = 'Echo of War'
    elif monstertemplateconfig[template_id]['Rank'] == 'LittleBoss':
        tier = 'Boss'
    elif monstertemplateconfig[template_id]['Rank'] == 'Elite':
        tier = 'Elite'
    else:
        tier = 'Normal'
        
    
    #files
    if files:
        largeimage = monstertemplateconfig[template_id]['ImagePath']
        copy_icon(largeimage, f'Enemy {name}.png', f'Enemy Images')
        
        icon = monstertemplateconfig[template_id]['RoundIconPath']
        copy_icon(icon, f'Icon Enemy {name}.png', f'Enemy Icons')
    
    
    #stat modifiers
    atkratio = autoround(monsterconfig[id]['AttackModifyRatio']['Value'])
    defratio = autoround(monsterconfig[id]['DefenceModifyRatio']['Value'])
    hpratio = autoround(monsterconfig[id]['HPModifyRatio']['Value'])
    spdratio = autoround(monsterconfig[id]['SpeedModifyRatio']['Value'])
    stanceratio = autoround(monsterconfig[id]['StanceModifyRatio']['Value'])
    try:
        speedadd = autoround(monsterconfig[id]['SpeedModifyValue']['Value'])
    except KeyError:
        speedadd = 0
    try:
        stanceadd = autoround(monsterconfig[id]['StanceModifyValue']['Value'])
    except KeyError:
        stanceadd = 0
        
    #stats
    atk = autoround(monstertemplateconfig[template_id]['AttackBase']['Value']) * atkratio
    if atk != 18:
        atk_text = f'|atk  = {atk}\n'
    else:
        atk_text = ''
    try:
        defence = autoround(monstertemplateconfig[template_id]['DefenceBase']['Value']) * defratio
    except KeyError:
        defence = 0 * defratio
    if defence != 210:
        def_text = f'|def  = {defence}\n'
    else:
        def_text = ''
    hp = autoround(monstertemplateconfig[template_id]['HPBase']['Value']) * hpratio
    hp_text = f'|hp   = {hp}\n'
    try:
        spd = autoround(monstertemplateconfig[template_id]['SpeedBase']['Value']) * spdratio + speedadd
    except KeyError:
        spd = 0
    spd_text = f'|spd  = {spd}\n'
    try:
        stance = int((autoround(monstertemplateconfig[template_id]['StanceBase']['Value']) * stanceratio + stanceadd) / 3)
    except KeyError:
        stance = 0
    try:
        eres = autoround(monstertemplateconfig[template_id]['StatusResistanceBase']['Value'])
    except KeyError:
        eres = 0.1
    eres_text = f'|eres = {eres}\n'
    
    #weakness
    weak_list = monsterconfig[id]['StanceWeakList']
    weak_list = list(map(lambda x: x.replace('Thunder', 'Lightning'), weak_list))
    weak_text = ''
    for weak in weak_list:
        if weak == weak_list[-1]:
            weak_end = ''
        else:
            weak_end = ';'
        weak_text = weak_text + f'{weak}{weak_end}'
        
    #res
    damage_res_text = ''
    for item in monsterconfig[id]['DamageTypeResistance']:
        dmgtype = item['DamageType'].replace('Physical', '|physical_res  = ').replace('Fire', '|fire_res      = ').replace('Ice', '|ice_res       = ').replace('Wind', '|wind_res      = ').replace('Thunder', '|lightning_res = ').replace('Imaginary', '|imaginary_res = ').replace('Quantum', '|quantum_res   = ')
        dmgres = autoround(item['Value']['Value'])
        damage_res_text = damage_res_text + f'{dmgtype}{dmgres}\n'
    
    debuff_res_text = ''
    for item in monsterconfig[id]['DebuffResist']:
        debufftype = item['Key'].replace('STAT_CTRL_Frozen', '|frozen_res       = ').replace('STAT_Entangle', '|entanglement_res = ').replace('STAT_Confine', '|imprisonment_res = ').replace('STAT_DOT_Burn', '|burn_res         = ').replace('STAT_DOT_Electric', '|shock_res        = ').replace('STAT_DOT_Poison', '|windsheer_res    = ').replace('STAT_CTRL', '|ctrleff_res      = ')
        debuffres = autoround(item['Value']['Value'])
        debuff_res_text = debuff_res_text + f'{debufftype}{debuffres}\n'
    
    #skills
    skill_text = ''
    type_list = []
    phase_show = False
    number = 1
    for n in range(len(skill_list)):        
        skill = skill_list[n]
        try:
            skill_name = monsterskillconfig[str(skill)]['SkillName']['TextMapEN']
        except KeyError:
            skill_name = ''
        
        try:
            skill_desc = monsterskillconfig[str(skill)]['SkillDesc']['TextMapEN']
        except KeyError:
            skill_desc = ''
            
        try:
            skill_type = monsterskillconfig[str(skill)]['SkillTag']['TextMapEN']
        except KeyError:
            skill_type = ''

        if monsterskillconfig[str(skill)].get('PhaseList'):            
            # damage type list
            for dmgtype in ['Physical', 'Fire', 'Ice', 'Lightning', 'Wind', 'Quantum', 'Imaginary']:
                if f'{dmgtype} DMG' in skill_desc:
                    if not dmgtype in type_list:
                        type_list.append(dmgtype)
            
            # energy
            try:
                energy_value = autoround(monsterskillconfig[str(skill)]['SPHitBase']['Value'])
                skill_energy = f'|energy{number} = {energy_value}\n'
            except KeyError:
                skill_energy = ''
                
            # danger
            try:
                if monsterskillconfig[str(skill)]['IsThreat'] == True:
                    skill_danger = f'|danger{number} = 1\n'
                else:
                    skill_danger = ''
            except KeyError:
                skill_danger = ''
                
            # phases
            phase_text = f'|phase{number}  = '
            phase_list = monsterskillconfig[str(skill)]['PhaseList']
            for phase in phase_list:
                if phase == phase_list[-1]:
                    phase_end = ''
                else:
                    phase_end = ','
                if phase != 1:
                    phase_show = True
                phase_text = phase_text + f'{phase}{phase_end}'
                
            # parse extra effect
            extraeffect_idlist = monsterskillconfig[str(skill)]['ExtraEffectIDList']
            if extraeffect_idlist:
                skill_desc = parse_extraeffect(skill_desc, extraeffect_idlist)
                
            skill_text = skill_text + f'\n|name{number}   = {skill_name}\n|type{number}   = {skill_type}\n|desc{number}   = {skill_desc}\n{skill_energy}{skill_danger}{phase_text}\n'
            
            number = number + 1
        
    #remove phase if no phase
    if phase_show == False:
        skill_text = re.sub(r'\|phase.*\n', '', skill_text)
        
    #dmg types
    type_text = ''
    if type_list:
        for dmgtype in type_list:
            if dmgtype == type_list[-1]:
                type_end = ''
            else:
                type_end = ';'
            type_text = type_text + f'{dmgtype}{type_end}'
            
    #faction
    try:
        camp_id = str(monstertemplateconfig[template_id]['MonsterCampID'])
        camp_name = monstercamp[camp_id]['Name']['TextMapEN']
        if camp_name in ['Jarilo-VI', 
                        'The Xianzhou Luofu', 
                        'Simulated Universe', 
                        'Stellaron Hunters', 
                        'Antimatter Legion',
                        'The Swarm']:
            camp_link = f'{camp_name} (Enemy Faction)|{camp_name}'
        else:
            camp_link = camp_name
    except KeyError:
        camp_name = ''
        camp_link = ''
    
    OLtext = genOL(name)
    
    page_content = f"<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some important information of edit. This struct will be removed automatically after you push edits.#\n    pageTitle = #{name}#\n    pageID = ##\n    revisionID = ##\n    contentModel = ##\n    contentFormat = ##\n[END_PAGE_INFO] --%>\n\n{{{{Enemy Infobox\n|image    = Enemy {filename}.png\n|tier     = {tier}\n|type     = {type_text}\n|weakness = {weak_text}\n|tough    = {stance}\n|faction  = {camp_name}\n|location = \n}}}}\n'''{name}''' is a [[{tier} Enemy]] part of the [[{camp_link}]] faction.\n\n==Enemy Info==\n{{{{Description|{intro}}}}}\n\n==Stats==\n{{{{Enemy Stats\n{damage_res_text}\n{debuff_res_text}\n{atk_text}{def_text}{hp_text}{spd_text}{eres_text}}}}}\n\n==Skills==\n{{{{Enemy Skills{skill_text}}}}}\n\n==Other Languages==\n{OLtext}\n==Change History==\n{{{{Change History|{ver}}}}}\n\n==Navigation==\n{{{{Enemy Navbox|{tier}}}}}\n"

    return([page_content, name])


def output_mons(id):
    output = parseMonster(id, ver)

    if not os.path.exists(f'{OUT_PATH}/Monsters'):
        os.makedirs(f'{OUT_PATH}/Monsters')

    file_name = output[1].replace(' ', '_').replace(':', '').replace('"', '')
    file_write_path = f'{OUT_PATH}/Monsters/{file_name}.wikitext'

    write_file(file_write_path, output[0])


if mons_id:
    output_mons(mons_id)


if args.new:
    old_names = [value.get('MonsterName').get('TextMapEN') for value in monsterconfig_old.values()]    
    for id, value in monsterconfig.items():
        if value.get('MonsterName').get('TextMapEN') not in old_names:
            id_list.append(id)
        """if id not in list(monsterconfig_old.keys()):
            id_list.append(id)"""


if id_list:
    for id in id_list:
        output_mons(id)