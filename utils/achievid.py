import json

from utils.misc import dict_to_table
from getConfig import CONFIG


def parse_achiev_id():
    with open(f'{CONFIG.EXCEL_PATH}/AchievementData.json', 'r', encoding = 'utf-8') as file:
        achievementjson = json.load(file)

    file_write_path = f'{CONFIG.OUTPUT_PATH}/Achievments/Achiev_ID_Output.lua'

    achiev_dict = {}

    for item in achievementjson:
        name = achievementjson[item]['AchievementTitle']['TextMapEN']
        name = name.replace('<i>', '\'\'').replace('</i>', '\'\'')
        achiev_id = 10000 - achievementjson[item]['Priority']
        id_str = str(achiev_id)

        achiev_dict[name] = id_str

    file_write = (f"--[=[<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some "
                  f"important information of edit. This struct will be removed automatically after you push edits.#\n "
                  f"   pageTitle = #Module:Achievement ID/data#\n    pageID = ##\n    revisionID = ##\n    "
                  f"contentModel = #Scribunto#\n    contentFormat = #text/plain#\n[END_PAGE_INFO] --%>--]=]\n\nreturn "
                  f"{dict_to_table(achiev_dict)}")

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')