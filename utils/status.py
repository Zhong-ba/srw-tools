import json
import re

from getConfig import CONFIG
from utils.files import write_file, copy_file
from utils.redirect import file_redirect
from utils.misc import parse_params


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