import json

from utils.files import write_file
from utils.misc import dict_to_table
from getConfig import CONFIG


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