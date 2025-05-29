import json
import os
import glob

from getConfig import CONFIG

IN_PATH = f'{CONFIG.DATA_PATH}/ExcelOutput'
OUT_PATH = f'{CONFIG.DATA_PATH}/ExcelOutput_Fix'

if not os.path.exists(OUT_PATH):
    os.makedirs(OUT_PATH)

excels = glob.glob(os.path.join(IN_PATH, '*.json'))


def process_excel(raw_excel, is_leveled = False):
    if not isinstance(raw_excel, list):
        return raw_excel

    processed_excel = {}
    for item in raw_excel:
        if item is None:
            return processed_excel
        if not isinstance(item, dict):
            return raw_excel

        # Find the first key that ends with 'ID'
        id_key = next((k for k in item.keys() if k.endswith('ID')), None)
        if id_key is None:
            return raw_excel

        new_key = item[id_key]
        if not isinstance(new_key, int):
            return raw_excel

        if processed_excel.get(str(new_key)):
            if not processed_excel.get(str(new_key)).get('1'):
                processed_excel[str(new_key)] = {
                    '1': processed_excel[str(new_key)]
                }
            i = 1
            while processed_excel.get(str(new_key)).get(str(i)):
                i = i + 1
            processed_excel[str(new_key)][str(i)] = item
            is_leveled = True
        elif is_leveled:
            processed_excel[str(new_key)] = {
                '1': item
            }
        else:
            processed_excel[str(new_key)] = item

    return processed_excel
            

for excel in excels:
    with open(excel, 'r', encoding = 'utf-8') as file:
        raw_excel = json.load(file)
    
    out_file = f'{OUT_PATH}/{os.path.basename(excel)}'
    is_leveled = False
    for match in ['AvatarSkillTree', 'AvatarMazeBuff']:
        if match in excel:
            is_leveled = True
    with open(out_file, 'w', encoding = 'utf-8') as file:
        json.dump(process_excel(raw_excel, is_leveled), file, indent = 2)
        
    print(f'Saved to {out_file}.')