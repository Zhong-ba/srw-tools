import os
import json

import utils.ol as ol
from utils.misc import convertwhole, autoround
from getConfig import CONFIG


def parse_aether_passive():
    ol.load_data()
    
    file_write_path =f'{CONFIG.OUTPUT_PATH}/AetherPassive.txt'
    file_write = ''

    with open(f'{CONFIG.EXCEL_PATH}/AetherDividePassiveSkill-Mapped.json', 'r', encoding = 'utf-8') as file:
        aetherpassivejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/AetherPassive/Items'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}/AetherPassive/Items')

    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/AetherPassive/Redirects'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}/AetherPassive/Redirects')

    for item in aetherpassivejson:
        try:
            name = aetherpassivejson[item]['ItemName']['TextMapEN']
            item_id = str(aetherpassivejson[item]['ItemID'])
            icon = itemjson[item_id]['ItemIconPath']
            icon = f'Icon Expansion Chip {icon[-6:-4]}.png'
            if itemjson[item_id]['Rarity'] == 'VeryRare':
                rarity = 4
            else:
                rarity = 3
            simpledesc = aetherpassivejson[item]['ItemDescription']
            desc = aetherpassivejson[item]['PassiveSkillDescription']
            params = [key["Value"] for key in aetherpassivejson[item]['ParamList']]
            for n in range(0, len(params)):
                param = convertwhole(autoround(params[n]))
                percent = convertwhole(param * 100)
                desc = desc.replace(f'#{n + 1}[i]%', f'{str(percent)}%')
                desc = desc.replace(f'#{n + 1}[f1]%', f'{str(percent)}%')
                desc = desc.replace(f'#{n + 1}[i]', f'{str(param)}')
                desc = desc.replace(f'#{n + 1}[f1]', f'{str(param)}')
            
            ol_text = ol.gen_ol(name)
            file_write = file_write + f"\n|-\n| [[File:{icon}|50px]] || '''{name}'''<br />{desc}"

            item_file_write_path = f'{CONFIG.OUTPUT_PATH}/AetherPassive/Items/{name}.wikitext'
            item_file_write = (f"<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record "
                               f"contains some important information of edit. This struct will be removed "
                               f"automatically after you push edits.#\n    pageTitle = #{name}#\n    pageID = ##\n    "
                               f"revisionID = ##\n    contentModel = ##\n    contentFormat = ##\n[END_PAGE_INFO] "
                               f"--%>\n\n{{{{Item Infobox\n|id          = {item_id}\n|image       = {icon}\n|type     "
                               f"   = Expansion Chip\n|rarity      = {rarity}\n|effect      = "
                               f"{simpledesc}\n|description = A game item in Aetherium Wars. Aether Spirits will gain "
                               f"a special enhanced ability after equipping it.\n|source1     = \n}}}}\n'''{name}''' "
                               f"is a [[Aetherium Wars/Expansion Chip|Expansion Chip]] in the [[Aetherium Wars]] "
                               f"event.\n\n==Other Languages==\n{ol_text}\n==Change History==\n{{{{Change "
                               f"History|1.4}}}}\n")
            with open(item_file_write_path, 'w', encoding = 'utf-8') as file:
                file.write(item_file_write)
                print('Saved to ' + item_file_write_path + '.')

            redirect_file_write_path = f'{CONFIG.OUTPUT_PATH}/AetherPassive/Redirects/{name}.wikitext'
            redirect_file_write = (f"<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record "
                                   f"contains some important information of edit. This struct will be removed "
                                   f"automatically after you push edits.#\n    pageTitle = #File:Item {name}.png#\n   "
                                   f" pageID = ##\n    revisionID = ##\n    contentModel = ##\n    contentFormat = "
                                   f"##\n[END_PAGE_INFO] --%>\n\n#REDIRECT [[File:{icon}]]\n[[Category:Redirect "
                                   f"Pages]]")
            with open(redirect_file_write_path, 'w', encoding = 'utf-8') as file:
                file.write(redirect_file_write)
                print('Saved to ' + redirect_file_write_path + '.')
        except KeyError:
            print(f'Skipped {item}.')

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')
        

def parse_aether_divide_challenge():
    with open(f'{CONFIG.EXCEL_PATH}/AetherDivideChallengeList.json', 'r', encoding = 'utf-8') as file:
        aetherchallengjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/StageConfig.json', 'r', encoding = 'utf-8') as file:
        stagejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

    file_write = ''
    file_write_path =f'{CONFIG.OUTPUT_PATH}/AetherChallenge.txt'

    for item in aetherchallengjson:
        try:
            name = aetherchallengjson[item]['OpponentName']['TextMapEN']

            rank = aetherchallengjson[item]['Rank']
            rank_text = '[[File:Icon Aetherium Wars Difficulty.png|30px]]' * rank

            stage_id = str(aetherchallengjson[item]['EventID'])
            monster_list = ''
            monster_index = 0
            for monster in (stagejson[stage_id]['MonsterList'])[0]:
                monster_id = str((stagejson[stage_id]['MonsterList'])[0][monster])
                monster_name = monsterjson[monster_id]['MonsterName']['TextMapEN']
                if monster_index == 0:
                    monster_list = monster_list + monster_name
                else:
                    monster_list = monster_list + f',{monster_name}'
                monster_index = monster_index + 1

            reward_id = str(aetherchallengjson[item]['RewardID'])
            reward_text = ''
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

            file_write = (f"{file_write}\n{{| class=\"wikitable\"\n! [[{name}]] {rank_text}\n|-\n| '''Enemy Lineup'''"
                          "<br /><!--\n-->{{{{Card List|type=Aether Enemy|caption=1|{monster_list}}}}}\n|-\n| "
                          "'''Victory Rewards'''<br /><!--\n-->{{{{Card List|caption=1|{reward_text}}}}}\n|}}")
        except KeyError:
            print(f'Skipped {item}.')

    with open(file_write_path, 'w') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')