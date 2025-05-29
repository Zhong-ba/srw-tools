import json

from utils.misc import autoround, dict_to_table
from utils.files import write_file
from getConfig import CONFIG


def parse_hard_level():
    with open(f'{CONFIG.EXCEL_PATH}/HardLevelGroup.json', 'r', encoding = 'utf-8') as file:
        hardleveljson = json.load(file)

    file_write_path = f'{CONFIG.OUTPUT_PATH}/Level_Scaling_Output.lua'

    dict_0 = {}
    dict_1 = {}
    dict_2 = {}
    dict_3 = {}

    for hl_type in hardleveljson:
        if hl_type in ['1', '2', '3']:
            for level in hardleveljson[hl_type]:
                hp_mult = autoround(hardleveljson[hl_type][level]['HPRatio']['Value'])
                atk_mult = autoround(hardleveljson[hl_type][level]['AttackRatio']['Value'])
                def_mult = autoround(hardleveljson[hl_type][level]['DefenceRatio']['Value'])

                if hl_type == '1':
                    if level not in dict_1:
                        dict_1[level] = {}
                    dict_1[level]['hp'] = hp_mult
                    dict_1[level]['atk'] = atk_mult
                    dict_1[level]['def'] = def_mult
                elif hl_type == '2':
                    if level not in dict_2:
                        dict_2[level] = {}
                    dict_2[level]['hp'] = hp_mult
                    dict_2[level]['atk'] = atk_mult
                    dict_2[level]['def'] = def_mult
                elif hl_type == '3':
                    if level not in dict_3:
                        dict_3[level] = {}
                    dict_3[level]['hp'] = hp_mult
                    dict_3[level]['atk'] = atk_mult
                    dict_3[level]['def'] = def_mult

    dict_0['1'] = dict_1
    dict_0['2'] = dict_2
    dict_0['3'] = dict_3

    file_write = dict_to_table(dict_0)

    write_file(file_write_path, file_write)