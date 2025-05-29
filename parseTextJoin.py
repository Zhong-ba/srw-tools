import json
import os

EXCEL_PATH = '../StarRailData-master/ExcelOutput_Fix'
MAPPED_EXCEL_PATH = 'OutputEN'

with open(f'{EXCEL_PATH}/TextJoinConfig.json', 'r', encoding='utf-8') as file:
    textjoinjson: dict = json.load(file)
    
with open(f'{EXCEL_PATH}/TextJoinItem.json', 'r', encoding='utf-8') as file:
    textjoinitemjson: dict = json.load(file)
    
with open(f'{EXCEL_PATH}/../TextMap/TextMapEN.json', 'r', encoding='utf-8') as file:
    textmap: dict = json.load(file)

mapped_textjoin = {}

for key, textjoin in textjoinjson.items():
    out_str = '('
    
    for item_id in textjoin['TextJoinItemList']:
        try:
            texthash = textjoinitemjson[str(item_id)]['TextJoinText']['Hash']
            text = textmap[str(texthash)]
            out_str = out_str + text + '/'
        except KeyError:
            continue
    
    out_str = out_str[:-1] + ')'
    
    mapped_textjoin[f'{{TEXTJOIN#{key}}}'] = out_str


def replace_in_dict(d: dict, find, repl):
    out = {}
    
    for key, value in d.items():
        if isinstance(value, dict):
            out[key] = replace_in_dict(value, find, repl) 
        elif isinstance(value, str):
            out[key] = value.replace(find, repl)
        else:
            out[key] = value
    
    return out

   
for filename in os.listdir(MAPPED_EXCEL_PATH):
    if filename.endswith('.json'):  # Check if the file is a JSON file
        file_path = os.path.join(MAPPED_EXCEL_PATH, filename)
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            
        for key, value in mapped_textjoin.items():
            data = replace_in_dict(data, key, value)
            
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent = 2)
        
        print(f'Saved to {file_path}')