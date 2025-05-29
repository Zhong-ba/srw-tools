import json
import os
import shutil


import ctypes
import sys

"""def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the script with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    # Your code here that needs admin rights
    print("I am running as admin!")"""


MASTER_DIR = '..'
JSON = {}
    
with open(f'{MASTER_DIR}/StarRailExcelMap/OutputEN/AvatarSkillConfig.json', 'r') as file:
    JSON['skill'] = json.load(file)
    
with open(f'{MASTER_DIR}/StarRailExcelMap/OutputEN/AvatarSkillTreeConfig-Mapped.json', 'r') as file:
    JSON['skilltree']  = json.load(file)
    
with open(f'{MASTER_DIR}/StarRailExcelMap/OutputEN/AvatarRankConfig.json', 'r') as file:
    JSON['rank']  = json.load(file)


def simplify_list(items):
    if not isinstance(items, list):
        return items
    
    if not items:  # Check if the list is empty
        return None  # Return None or any appropriate value to signify an empty list
    
    if all(item == items[0] for item in items):  # Check if all items are the same as the first item
        return items[0]  # Return only the first item
    else:
        return items


def replace_hashes(d, hash_map):
    if isinstance(d, dict):
        for key, value in list(d.items()):
            if key == "DynamicHashes" and isinstance(value, list):
                # Replace list with a dictionary of mapped values
                d[key] = {str(v): hash_map.get(str(v), None) for v in value}
            else:
                replace_hashes(value, hash_map)
    elif isinstance(d, list):
        for item in d:
            replace_hashes(item, hash_map)
            

def save_json(dict, dir):
    if not os.path.exists(dir.replace(dir.split('/')[-1], '')):
        os.makedirs(dir.replace(dir.split('/')[-1], ''))
    
    with open(dir, 'w') as f:
        json.dump(dict, f, indent = 2)
        
    print(f'Saved to {dir}')


def parse_avatar_dynamic_hashes(abilityjson, configjson, id, output_path):
    print(f'============================{id}============================')
    
    mapped_hashes = {}
    
    id_dict = {
        # batk
        'Skill01': JSON['skill'].get(f'{id}01', None),
        # enhanced batk
        'Skill11': JSON['skill'].get(f'{id}08', None),
        'Skill12': JSON['skill'].get(f'{id}10', None),
        'Skill13': JSON['skill'].get(f'{id}12', None),
        # skill
        'Skill02': JSON['skill'].get(f'{id}02', None),
        'Skill21': JSON['skill'].get(f'{id}09', None),
        # ult
        'Skill03': JSON['skill'].get(f'{id}03', None),
        'Skill31': JSON['skill'].get(f'{id}14', None),
        # talent
        'SkillP01': JSON['skill'].get(f'{id}04', None),
        # technique
        'SkillMaze': JSON['skill'].get(f'{id}07', None),
        # eidolon
        'Rank01': JSON['rank'].get(f'{id}01', None),
        'Rank02': JSON['rank'].get(f'{id}02', None),
        'Rank03': JSON['rank'].get(f'{id}03', None),
        'Rank04': JSON['rank'].get(f'{id}04', None),
        'Rank05': JSON['rank'].get(f'{id}05', None),
        'Rank06': JSON['rank'].get(f'{id}06', None),
        # trace
        'PointB1': JSON['skilltree'].get(f'{id}101', None),
        'PointB2': JSON['skilltree'].get(f'{id}102', None),
        'PointB3': JSON['skilltree'].get(f'{id}103', None),
    }
    
    paramlist_index = 0
    
    for key, value in configjson.get('DynamicValues').get('Values').items():
        if not value:
            continue
        
        skilltype = value['ReadInfo']['Str']
        
        if skilltype not in id_dict.keys():
            continue
        
        # When Type = None for that skill, that hash is a reference to the 1st/0th item in the ParamList. If it is not the Type = None, then you want to count how many away you are from that None type which will be your position in the ParamList
        if value['ReadInfo']['Type'] == 'None':
            paramlist_index = 0
        else:
            paramlist_index = paramlist_index + 1
            
        # out = None
        if skilltype in ['Skill01', 'Skill02', 'Skill03', 'SkillP01', 'Skill11', 'Skill12', 'Skill13', 'Skill21', 'Skill31']:
            out = []
            for _, value2 in id_dict[skilltype].items():
                try:
                    out.append(value2['ParamList'][paramlist_index]['Value'])
                except IndexError:
                    out.append(value2['ParamList'][0]['Value'])
        elif skilltype == 'SkillMaze':
            try:
                out = id_dict[skilltype]['1']['ParamList'][paramlist_index]['Value']
            except IndexError:
                out = id_dict[skilltype]['1']['ParamList'][0]['Value']
        elif skilltype in ['Rank01', 'Rank02', 'Rank03', 'Rank04', 'Rank05', 'Rank06']:
            try:
                out = id_dict[skilltype]['Param'][paramlist_index]['Value']
            except IndexError:
                out = id_dict[skilltype]['Param'][0]['Value']
        elif skilltype in ['PointB1', 'PointB2', 'PointB3']:
            try:
                out = id_dict[skilltype]['1']['ParamList'][paramlist_index]['Value']
            except IndexError:
                out = id_dict[skilltype]['1']['ParamList'][0]['Value']
                
        mapped_hashes[key] = simplify_list(out)
        
        
    replace_hashes(abilityjson, mapped_hashes)
    
    save_json(abilityjson, output_path)
               

def load_char_files():
    with open(f'{MASTER_DIR}/StarRailExcelMap/OutputEN/AvatarConfig.json', 'r') as file:
        avatarjson = json.load(file)
        
    for key, value in avatarjson.items():
        id = key
        configjson_path = value.get('JsonPath')
        abilityjson_path = configjson_path.replace('Config.json', 'Ability.json').replace('ConfigCharacter', 'ConfigAbility')
        output_path = f"{MASTER_DIR}/StarRailData-master/{abilityjson_path.replace('/Avatar', '/Avatar_Mapped')}"
    
        with open(f'{MASTER_DIR}/StarRailData-master/{configjson_path}', 'r') as file:
            configjson = json.load(file)
            
        with open(f'{MASTER_DIR}/StarRailData-master/{abilityjson_path}', 'r') as file:
            abilityjson = json.load(file)
            
        parse_avatar_dynamic_hashes(abilityjson, configjson, id, output_path)


def main():
    load_char_files()


if __name__ == '__main__':
    main()