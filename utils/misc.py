import os
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