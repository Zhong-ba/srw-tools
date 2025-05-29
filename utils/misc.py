import os
import re
import json

from utils.redirect import file_redirect
from utils.files import copy_file
from getConfig import CONFIG


def copy_icon(source, name, folder):
    file_name_clean = name.replace(":", "").replace("/", "").replace("\"", "")
    
    if file_name_clean != name:
        file_redirect(name, file_name_clean)
        
    src = f'{CONFIG.IMAGE_PATH}/{source.lower()}'
    
    dest = f'{CONFIG.OUTPUT_PATH}/Images/{folder}/{file_name_clean}'
    
    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/Images/{folder}'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/Images/{folder}')
    
    copy_file(src, dest)
        

def autoround(value):
    s_value = str(value)

    patterns = ['999', '998', '000', '001']

    for pattern in patterns:
        position = s_value.find(pattern)
        if position != -1:
            return round(value, position - s_value.find('.'))

    return value


def convertwhole(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    else:
        return value
    
    
def dict_to_template(dictionary, template):
    out = ''
    for key, value in dictionary.items():
        out = f'{out}|{key} = {value}\n'

    out = f'{{{{{template}\n{out}}}}}'

    return out


def fix_str(str_input):
    return str_input.replace('"', r'\"')


def dict_to_table(python_dict, indent = 0):
    indent_str = '\t' * indent
    lua_table = "{\n"
    
    for key, value in python_dict.items():
        lua_key = f'{indent_str}\t["{fix_str(key)}"]'
        
        if isinstance(value, str):
            lua_value = f'"{fix_str(value)}"'
        elif isinstance(value, dict):
            lua_value = dict_to_table(value, indent + 1)
        elif isinstance(value, list):
            list_values = ", ".join([f'"{fix_str(item)}"' if isinstance(item, str) else str(item) for item in value])
            lua_value = "{" + list_values + "}"
        else:
            lua_value = str(value)
            
        lua_table += f"{lua_key} = {lua_value},\n"
        
    lua_table += f"{indent_str}}}"

    return lua_table
    

def parse_extraeffect(desc, idlist):
    underline_tags = re.findall(r'<u>(.*?)</u>', desc)
    seen = set()
    unique_tags = []
    for tag in underline_tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    if len(unique_tags) != len(idlist):
        # Fallback replacement without IDs, with warning
        print("Warning: mismatched tag and ID count.")
        print("Found tags:", unique_tags)
        print("Provided IDs:", idlist)
        return re.sub(r'<u>(.*?)</u>', r'{{Extra Effect|\1}}', desc)

    # Map tags to IDs
    effect_dict = dict(zip(unique_tags, idlist))

    # Replace tags with ID-injected format
    def replacer(match):
        text = match.group(1)
        return f"{{{{Extra Effect|{text}|{effect_dict[text]}}}}}"

    return re.sub(r'<u>(.*?)</u>', replacer, desc)


def parse_params(desc, params):
    try:
        if isinstance(params[0], dict):
            params = [key["Value"] for key in params]

        for n in range(0, len(params)):
            percent = autoround(params[n] * 100)
            desc = desc.replace(f'#{n + 1}[i]%', str(int(percent)) + '%')
            desc = desc.replace(f'#{n + 1}[i]', str(autoround(params[n])))
            desc = desc.replace(f'#{n + 1}', str(autoround(params[n])))
    except IndexError as err:
        print(f'Param mapping failed. ({err})')

    return desc


def parse_reward_text(reward_id):
    reward_text = ''

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

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

    return reward_text


def parse_mazebuff(id):
    with open(f'{CONFIG.EXCEL_PATH}/MazeBuff.json', 'r', encoding = 'utf-8') as file:
        mazebuffjson = json.load(file)
        
    desc = mazebuffjson[id]['1']['BuffDesc']['TextMapEN']
    params = mazebuffjson[id]['1']['ParamList']
    
    name = mazebuffjson[id]['1']['BuffName']['TextMapEN']
    
    icon = mazebuffjson[id]['1'].get('BuffIcon')
    
    if icon and icon != 'SpriteOutput/BuffIcon/Inlevel/IconBuffCommon.png':
        copy_file(f'{CONFIG.IMAGE_PATH}/{icon}', f'{CONFIG.OUTPUT_PATH}/Images/Icon {name}.png')
        
    
    return name, parse_params(desc, params)


def parse_monster_text(monster_list):
    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    monster_text = ''
    monster_index = 0
    for monster in monster_list:
        monster_id = str(monster)
        monster_name = monsterjson[monster_id]['MonsterName']['TextMapEN']
        if monster_index == 0:
            monster_text = monster_text + monster_name
        else:
            monster_text = monster_text + f',{monster_name}'
        monster_index = monster_index + 1

    return monster_text