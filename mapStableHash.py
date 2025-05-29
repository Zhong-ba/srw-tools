import json
# import ctypes
import xxhash
from getConfig import CONFIG

JSON_NAMES = [
    'AvatarSkillTreeConfig',
    'AvatarRankConfig',
]

def get_stable_hash(s: str):
    return xxhash.xxh64(s).intdigest()

"""
OUTDATED AS OF 3.1

def get_stable_hash(str: str):
    hash1 = 5381
    hash2 = 5381

    for i in range(0, len(str), 2):
        hash1 = ((hash1 << 5) + hash1) ^ ord(str[i])
        if i + 1 < len(str):
            hash2 = ((hash2 << 5) + hash2) ^ ord(str[i + 1])
    return ctypes.c_int32(hash1 + (hash2 * 1566083941)).value
"""

with open(f'{CONFIG.DATA_PATH}/TextMap/TextMapEN.json', encoding='utf-8') as f:
    hash_dict = json.load(f)

def replace_hashes(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ['Hash', 'Name', 'PointName', 'Desc', 'PointDesc']:
                if key == 'Hash':
                    hash_val = value
                else:
                    hash_val = get_stable_hash(str(value))
                if str(hash_val) in hash_dict:
                    obj[key] = hash_dict[str(hash_val)]
            else:
                replace_hashes(value)
    elif isinstance(obj, list):
        for item in obj:
            replace_hashes(item)
            
            
for JSON_NAME in JSON_NAMES:
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/{JSON_NAME}.json', encoding='utf-8') as f:
        input_data = json.load(f)
        
    replace_hashes(input_data)
    
    with open(f'{CONFIG.DATA_PATH}/MappedExcelOutput_EN/{JSON_NAME}-Mapped.json', 'w', encoding='utf-8') as f:
        json.dump(input_data, f, indent=2, ensure_ascii=False)
        
    print(f'{JSON_NAME} done.')