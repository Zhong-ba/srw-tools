import json
import os
import re
import shutil

from getConfig import CONFIG


def parse_tutorial(tut_id):
    with open(f'{CONFIG.EXCEL_PATH}/TutorialGuideGroup.json', 'r', encoding = 'utf-8') as file:
        groupjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/TutorialGuideData.json', 'r', encoding = 'utf-8') as file:
        datajson = json.load(file)

    title = groupjson[tut_id]['MessageText']['TextMapEN']
    guide_ids = groupjson[tut_id]['TutorialGuideIDList']
    output = ''
    index = 1

    for guide in guide_ids:
        desc = datajson[str(guide)]['Default']['DescText']['TextMapEN']
        output = output + f'\n|image{index} = Tutorial {title} {index}.png\n|text{index}  = {desc}'

        source_path = datajson[str(guide)]['Default']['ImagePath']
        source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
        title_clean = re.sub(r'[^\w\s]', '', groupjson[tut_id]['MessageText']['TextMapEN'])
        destination_path = f'{CONFIG.OUTPUT_PATH}/Tutorial_{tut_id}/Tutorial {title_clean} {index}.png'

        if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/Tutorial_{tut_id}'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/Tutorial_{tut_id}')

        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"File copied successfully from {source_path} to {destination_path}")
        else:
            print(f"The file {source_path} does not exist.")

        index = index + 1

    output = f'{{{{Tutorial{output}\n}}}}'

    print(output)