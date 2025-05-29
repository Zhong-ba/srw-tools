import json
import argparse
import shutil
import os
import re
import pyperclip

import utils.ol as ol
from utils.redirect import file_redirect
from utils.misc import parse_params, parse_reward_text, autoround, convertwhole
from utils.target import parse_battle_target, parse_raid_target
from getConfig import CONFIG

TEXTMAP_PATH = f'{CONFIG.DATA_PATH}/TextMap'


def parse_monster_text(monster_list):
    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    monster_text = ''
    monster_index = 0
    for monster in monster_list:
        monster_id = str(monster)
        monster_name = monsterjson[monster_id]['MonsterName']['TextMapEN']
        if monster_index == 0:
            monster_text = monster_text + monster_name
        else:
            monster_text = monster_text + f',{monster_name}'
        monster_index = monster_index + 1

    return monster_text


def parse_curio():
    file_write_path =f'{CONFIG.OUTPUT_PATH}Curio_Output.txt'
    file_write = ''
    file_write_2_path =f'{CONFIG.OUTPUT_PATH}Curio_Output_2.txt'
    file_write_2 = ''

    with open(f'{CONFIG.EXCEL_PATH}/RogueTournMiracleDisplay.json', 'r', encoding = 'utf-8') as file:
        roguemiracleconfig = json.load(file)

    # get stage list
    for item in roguemiracleconfig:
        name = roguemiracleconfig[item]['MiracleName']['TextMapEN']
        print(name)
        try:
            desc = roguemiracleconfig[item]['MiracleDesc']['TextMapEN']
        except KeyError:
            desc = ''
        try:
            lore = roguemiracleconfig[item]['MiracleBGDesc']['TextMapEN']
        except KeyError:
            lore = ''
        
        params = roguemiracleconfig[item]['DescParamList']
        
        if params:
            desc = parse_params(desc, params)

        # file
        file_write = (file_write +
                      f'\n|-\n|[[File:Curio {name}.png|50px]]\n|\'\'\'{name}\'\'\'\n|{desc}\n|-\n|colspan="3" | {lore}')

        file_write_2 = file_write_2 + f'\n** {{{{Item|{name}|20|nobr=1|type=Curio|link=}}}}'

    with open(file_write_path, 'w') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')

    with open(file_write_2_path, 'w') as file:
        file.write(file_write_2)
        print('Saved to ' + file_write_2_path + '.')


def parse_aether_passive():
    ol.load_data()
    
    file_write_path =f'{CONFIG.OUTPUT_PATH}AetherPassive.txt'
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


def parse_rewards():
    file_write_path =f'{CONFIG.OUTPUT_PATH}Rewards.txt'

    with open(f'{CONFIG.EXCEL_PATH}/QuestData.json', 'r', encoding = 'utf-8') as file:
        questjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    output = ''

    for quest in questjson:
        try:
            title = questjson[quest]['QuestTitle']['TextMapEN']
        except KeyError:
            title = ''
        try:
            display = questjson[quest]['QuestDisplay']['TextMapEN']
        except KeyError:
            display = ''

        if title:
            if display:
                objective_txt = f"'''{title}'''<br />{display}"
            else:
                objective_txt = title

            reward_id = str(questjson[quest]['RewardID'])
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

            output = output + f'\n|-\n| {objective_txt} || {{{{Card List|{reward_text}}}}}'

    with open(file_write_path, 'w') as file:
        file.write(output)
        print('Saved to ' + file_write_path + '.')


def parse_rogue_endless_rewards():
    file_write_path =f'{CONFIG.OUTPUT_PATH}RogueEndlessRewards.txt'

    with open(f'{CONFIG.EXCEL_PATH}/ActivityRewardRogueEndless.json', 'r', encoding = 'utf-8') as file:
        rewardrogueendlessjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

    output = ''

    for quest in rewardrogueendlessjson:
        print(quest)
        name = rewardrogueendlessjson[quest]['RewardLevelName']['TextMapEN']
        point = rewardrogueendlessjson[quest]['RewardPoint']
        name = name.replace('#1', str(point))

        reward_id = str(rewardrogueendlessjson[quest]['RewardID'])
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
                print(reward_text)

        try:
            hcoin = str(rewardjson[reward_id]['Hcoin'])
        except KeyError:
            hcoin = ''

        if hcoin:
            reward_text = f'Stellar Jade*{hcoin}'

        output = output + f'\n|-\n| {name} || {{{{Card List|{reward_text}}}}}'

    with open(file_write_path, 'w') as file:
        file.write(output)
        print('Saved to ' + file_write_path + '.')


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


def parse_blessings():
    file_write_path =f'{CONFIG.OUTPUT_PATH}Blessings_Output.txt'
    file_write = ''

    with open(f'{CONFIG.EXCEL_PATH}/RogueMazeBuff.json', 'r', encoding = 'utf-8') as file:
        roguemazebuff = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RogueBuff.json', 'r', encoding = 'utf-8') as file:
        roguebuff = json.load(file)

    # get stage list
    for item in roguemazebuff:
        try:
            name = roguemazebuff[item]['1']['BuffName']['TextMapEN']
        except KeyError:
            name = ''

        try:
            rarity = str(roguebuff[item]['1']['RogueBuffRarity'])
        except KeyError:
            rarity = ''

        try:
            image = roguemazebuff[item]['1']['BuffIcon']
        except KeyError:
            image = ''

        if image[-6:-4] == '01':
            imagetype = 'Attack'
        elif image[-6:-4] == '02':
            imagetype = 'Defense'
        elif image[-6:-4] == '03':
            imagetype = 'Buff'
        elif image[-6:-4] == '04':
            imagetype = 'Debuff'
        elif image[-6:-4] == '05':
            imagetype = 'Support'
        else:
            imagetype = ''

        if 'Joy' in image:
            path = 'Elation'
        elif 'Knight' in image:
            path = 'Preservation'
        elif 'Memory' in image:
            path = 'Remembrance'
        elif 'Pirest' in image:
            path = 'Abundance'
        elif 'Priest' in image:
            path = 'Abundance'
        elif 'RogueRogue' in image:
            path = 'Hunt'
        elif 'Warlock' in image:
            path = 'Nihility'
        elif 'Warrior' in image:
            path = 'Destruction'
        elif 'Propagation' in image:
            path = 'Propagation'
        else:
            path = ''

        try:
            desc1 = roguemazebuff[item]['1']['BuffDesc']['TextMapEN']
        except KeyError:
            desc1 = ''

        params1 = [key["Value"] for key in roguemazebuff[item]['1']['ParamList']]

        for n in range(0, len(params1)):
            param1 = convertwhole(autoround(params1[n]))
            percent1 = autoround(convertwhole(param1 * 100))
            desc1 = desc1.replace(f'#{n + 1}[i]%', str(percent1) + '%')
            desc1 = desc1.replace(f'#{n + 1}[f1]%', str(percent1) + '%')
            desc1 = desc1.replace(f'#{n + 1}[f2]%', str(percent1) + '%')
            desc1 = desc1.replace(f'#{n + 1}[i]', str(params1[n]))
            desc1 = desc1.replace(f'#{n + 1}[f1]', str(params1[n]))
            desc1 = desc1.replace(f'#{n + 1}[f2]', str(params1[n]))

        try:
            desc2 = roguemazebuff[item]['2']['BuffDesc']['TextMapEN']
        except KeyError:
            desc2 = ''

        if desc2 != '':
            params2 = [key["Value"] for key in roguemazebuff[item]['2']['ParamList']]

            for n in range(0, len(params2)):
                param2 = convertwhole(autoround(params2[n]))
                percent2 = autoround(convertwhole(param2 * 100))
                desc2 = desc2.replace(f'#{n + 1}[i]%', str(percent2) + '%')
                desc2 = desc2.replace(f'#{n + 1}[f1]%', str(percent2) + '%')
                desc2 = desc2.replace(f'#{n + 1}[f2]%', str(percent2) + '%')
                desc2 = desc2.replace(f'#{n + 1}[i]', str(params2[n]))
                desc2 = desc2.replace(f'#{n + 1}[f1]', str(params2[n]))
                desc2 = desc2.replace(f'#{n + 1}[f2]', str(params2[n]))

        if 'Resonance Formation' in name or 'Resonance Interplay' in name or 'Path Resonance' in name:
            file_write = (file_write +
                          f"\n|-\n|{{{{SU Blessing Card|{path}|{imagetype}|{rarity}}}}}\n|'''{name}'''<br />{desc1}")
        else:
            file_write = (file_write +
                          f'\n|-\n|{{{{SU Blessing Card|{path}|{imagetype}|{rarity}}}}}\n|{name}\n|{desc1}\n|{desc2}')

    with open(file_write_path, 'w') as file:
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
    file_write_path =f'{CONFIG.OUTPUT_PATH}AetherChallenge.txt'

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


def parse_heliobus_challenge():
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusChallengeStage.json', 'r', encoding = 'utf-8') as file:
        heliobuschallengejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/ItemConfig.json', 'r', encoding = 'utf-8') as file:
        itemjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/StageConfig.json', 'r', encoding = 'utf-8') as file:
        stagejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/RewardData.json', 'r', encoding = 'utf-8') as file:
        rewardjson = json.load(file)

    file_write = ''
    file_write_path =f'{CONFIG.OUTPUT_PATH}HeliobusChallenge.txt'

    for item in heliobuschallengejson:
        try:
            diff = heliobuschallengejson[item]['HeliobusChallengeHard']
            diff_text = ''

            if diff == 1:
                diff_text = 'I'
            elif diff == 2:
                diff_text = 'II'
            elif diff == 3:
                diff_text = 'III'
            elif diff == 4:
                diff_text = 'IV'

            target_list = heliobuschallengejson[item]['BattleTargetList']
            target_1, target_2, target_3 = [parse_battle_target(str(target_list[0])),
                                            parse_battle_target(str(target_list[1])),
                                            parse_battle_target(str(target_list[2]))]

            stage_id = str(heliobuschallengejson[item]['EventID']) + '0'
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

            reward_id = str(heliobuschallengejson[item]['RewardID'])
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

            file_write = (f"{file_write}\n{{| class=\"wikitable\"\n! Difficulty {diff_text}\n|-\n| '''Objectives'''"
                          f"<ul><!--\n--><li>{target_1}</li><!--\n--><li>{target_2}</li><!--\n--><li>"
                          f"{target_3}</li><!--\n--><ul>\n|-\n| '''Enemy Lineup'''<br /><!--\n-->{{{{Card "
                          f"List|type=Enemy|caption=1|{monster_list}}}}}\n|-\n| '''First-Time Clearance Rewards'''<br "
                          f"/><!--\n-->{{{{Card List|caption=1|{reward_text}}}}}\n|}}\n</div><!--\n--><div>")
        except KeyError:
            print(f'Skipped {item}.')

    with open(file_write_path, 'w') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def parse_heliobus_raid(raid_id):
    with open(f'{CONFIG.EXCEL_PATH}/RaidConfig.json', 'r', encoding = 'utf-8') as file:
        raidjson = json.load(file)

    id_str = str(raid_id)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/HeliobusRaid_{id_str}.txt'

    name = raidjson[id_str]['0']['RaidName']['TextMapEN']

    target_list = raidjson[id_str]['0']['RaidTargetID']
    target_1, target_2, target_3 = [parse_raid_target(str(target_list[0])), parse_raid_target(str(target_list[1])),
                                    parse_raid_target(str(target_list[2]))]

    monster_list = raidjson[id_str]['0']['MonsterList']
    monster_text = parse_monster_text(monster_list)

    reward_id = str(raidjson[id_str]['0']['RewardList'][0])
    reward_text = parse_reward_text(reward_id)

    buff_desc = raidjson[id_str]['0']['BuffDesc']['TextMapEN']
    buff_params = raidjson[id_str]['0']['BuffParamList']
    buff_desc = parse_params(buff_desc, buff_params)

    file_write = (file_write +
                  f"\n{{| class=\"wikitable\"\n! {name}\n|-\n| '''Anomaly'''<br /><!--\n-->{buff_desc}\n|-\n| " +
                  f"''''Objectives'''<ul><!--\n--><li>{target_1}</li><!--\n--><li>{target_2}</li><!--\n-->" +
                  f"<li>{target_3}</li><!--\n--><ul>\n|-\n| '''May Encounter'''<br /><!--\n-->{{{{Card List|type=" +
                  f"Enemy|caption=1|{monster_text}}}}}\n|-\n| '''First-Time Clearance Rewards'''<br /><!--\n-->" +
                  f"{{{{Card List|caption=1|{reward_text}}}}}\n|}}\n</div><!--\n--><div>")

    with open(file_write_path, 'w') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def parse_heliobus_user():
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusUser.json', 'r', encoding = 'utf-8') as file:
        heliobususerjson = json.load(file)

    for item in heliobususerjson:
        name = heliobususerjson[item]['HeliobusUserName']['TextMapEN']
        file_name = f'A Foxian Tale of the Haunted User {name}'
        file_name_clean = re.sub(r'[^\w\s]', '', file_name)

        if file_name != file_name_clean:
            redirect_write = (f"<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record "
                              f"contains some important information of edit. This struct will be removed "
                              f"automatically after you push edits.#\n    pageTitle = #File:{file_name}.png#\n    "
                              f"pageID = ##\n    revisionID = ##\n    contentModel = ##\n    contentFormat = ##\n["
                              f"END_PAGE_INFO] --%>\n\n#REDIRECT [[File:{file_name_clean}.png]]\n[[Category:Redirect "
                              f"Pages]]")
            redirect_write_path = f'{CONFIG.OUTPUT_PATH}/HeliobusUserIcons/{file_name_clean}.wikitext'
            with open(redirect_write_path, 'w') as file:
                file.write(redirect_write)
                print('Saved redirect page to ' + redirect_write_path + '.')

        source_path = heliobususerjson[item]['UserIconPath']
        source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
        destination_path = f'{CONFIG.OUTPUT_PATH}/HeliobusUserIcons/{file_name_clean}.png'

        if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/HeliobusUserIcons'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/HeliobusUserIcons')

        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"File copied successfully from {source_path} to {destination_path}")
        else:
            print(f"The file {source_path} does not exist.")


def get_heliobus_post_img(img_id):
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusPostImg.json', 'r', encoding = 'utf-8') as file:
        heliobuspostimgjson = json.load(file)

    path = heliobuspostimgjson[str(img_id)]['PostImgPath']

    return path


def get_heliobus_user(user_id):
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusUser.json', 'r', encoding = 'utf-8') as file:
        heliobususerjson = json.load(file)

    username = heliobususerjson[str(user_id)]['HeliobusUserName']['TextMapEN']
    username = username.replace('|', '{{!}}')

    return username


def parse_heliobus_comments(post_id, template = False):
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusComment.json', 'r', encoding = 'utf-8') as file:
        heliobuscommentjson = json.load(file)

    comment_output = ''

    for lv1_index in range(0, 9):
        try:
            if template:
                lv1_comment_id = f'{post_id}{lv1_index}'
            else:
                lv1_comment_id = f'{post_id}{lv1_index:02}'
            lv1_comment_content = heliobuscommentjson[lv1_comment_id]['HeliobusCommentTextID']['TextMapEN']
            lv1_comment_user = get_heliobus_user(heliobuscommentjson[lv1_comment_id]['HeliobusUserID'])
            comment_output = (f"{comment_output}\n:'''{{{{Icon/FTH|{lv1_comment_user}}}}}"
                              f" {lv1_comment_user.replace('{{!}}', '')}:''' {lv1_comment_content}")
            player_comment_list = heliobuscommentjson[lv1_comment_id]['PlayerCommentIDList']

            # if player_comment_list:
            for comment in player_comment_list:
                comment_text = heliobuscommentjson[str(comment)]['HeliobusCommentTextID']['TextMapEN']
                comment_output = (f"{comment_output}\n::'''{{{{DIcon}}}} {{{{Icon/FTH|LilGuiGuinevere}}}} "
                                  f"LilGuiGuinevere:''' {comment_text}")

            for lv2_index in range(0, 9):
                try:
                    lv2_comment_id = f'{lv1_comment_id}{lv2_index}'
                    lv2_comment_content = heliobuscommentjson[lv2_comment_id]['HeliobusCommentTextID']['TextMapEN']
                    lv2_comment_user = get_heliobus_user(heliobuscommentjson[lv2_comment_id]['HeliobusUserID'])
                    comment_output = (f"{comment_output}\n::'''{{{{Icon/FTH|{lv2_comment_user.replace('{{!}}', '')}}}}}"
                                      f" {lv2_comment_user}:''' {lv2_comment_content}")
                except KeyError:
                    continue
        except KeyError:
            continue

    return comment_output


def parse_heliobus_post():
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusPost.json', 'r', encoding = 'utf-8') as file:
        heliobuspostjson = json.load(file)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/HeliobusPost/HeliobusPostOutput.wikitext'

    for post in heliobuspostjson:
        # if post != '703':
        #    continue

        title = heliobuspostjson[post]['HeliobusPostTitle']['TextMapEN']
        user = get_heliobus_user(heliobuspostjson[post]['HeliobusUserID'])
        content = heliobuspostjson[post]['HeliobusPostContent']['TextMapEN']
        comments = parse_heliobus_comments(post)

        file_name = f'A Foxian Tale of the Haunted Post {title}'
        file_name_clean = re.sub(r'[^\w\s]', '', file_name)

        try:
            source_path = get_heliobus_post_img(heliobuspostjson[post]['PostImgID'])
            source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
            destination_path = f'{CONFIG.OUTPUT_PATH}/HeliobusPost/{file_name_clean}.png'

            if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/HeliobusPost'):
                os.makedirs(f'{CONFIG.OUTPUT_PATH}/HeliobusPost')

            if os.path.exists(source_path):
                shutil.copy(source_path, destination_path)
                print(f"File copied successfully from {source_path} to {destination_path}")
            else:
                print(f"The file {source_path} does not exist.")

            format_txt = (f"{{| class=\"wikitable\"\n! colspan=\"2\" | {title}\n|-\n| [[File:{file_name_clean}.png"
                          f"|250px]]\n| {{{{Icon/FTH|{user.replace('{{!}}', '')}|30}}}} '''{user}'''<br />{content}"
                          f"\n|-\n| colspan=\"2\" | {{{{Dialogue Start}}}}{comments}\n{{{{Dialogue End}}}}\n|}}")
        except KeyError:
            format_txt = (f"{{| class=\"wikitable\"\n! {title}\n|-\n| {{{{Icon/FTH|{user}|30}}}}"
                          f" '''{user.replace('{{!}}', '')}'''<br />{content}\n|-\n| {{{{Dialogue Start}}}}{comments}"
                          f"\n{{{{Dialogue End}}}}\n|}}")

        file_write = file_write + f'{format_txt}\n'

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def parse_heliobus_template():
    with open(f'{CONFIG.EXCEL_PATH}/HeliobusTemplate.json', 'r', encoding = 'utf-8') as file:
        heliobustemplatejson = json.load(file)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/HeliobusTemplate/HeliobusTemplateOutput.wikitext'

    for post in heliobustemplatejson:
        # if post != '703':
        #    continue

        title = heliobustemplatejson[post]['HeliobusTemplateTitle']['TextMapEN']
        content = heliobustemplatejson[post]['HeliobusTemplateContent']['TextMapEN']

        tendency = 0
        if heliobustemplatejson[post]['TemplateTendency'] == 'Tendency1':
            tendency = 1
        elif heliobustemplatejson[post]['TemplateTendency'] == 'Tendency2':
            tendency = 2
        elif heliobustemplatejson[post]['TemplateTendency'] == 'Tendency3':
            tendency = 3
        elif heliobustemplatejson[post]['TemplateTendency'] == 'Tendency4':
            tendency = 1

        comments = parse_heliobus_comments(post[:4] + str(tendency), template = True)

        file_name = f'A Foxian Tale of the Haunted Post {title}'
        file_name_clean = re.sub(r'[^\w\s]', '', file_name)

        source_path = get_heliobus_post_img(heliobustemplatejson[post]['PostImgID'])
        source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
        destination_path = f'{CONFIG.OUTPUT_PATH}/HeliobusTemplate/{file_name_clean}.png'

        if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/HeliobusTemplate'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/HeliobusTemplate')

        if os.path.exists(source_path):
            shutil.copy(source_path, destination_path)
            print(f"File copied successfully from {source_path} to {destination_path}")
        else:
            print(f"The file {source_path} does not exist.")

        format_txt = (f"{{| class=\"wikitable\"\n! colspan=\"2\" | {title}\n|-\n| [[File:{file_name_clean}.png|250px]]"
                      f"\n| {{{{Icon/FTH|LilGuiGuinevere}}}} '''LilGuiGuinevere'''<br />{content}\n|-\n| colspan=\"2\""
                      f" | {{{{Dialogue Start}}}}{comments}\n{{{{Dialogue End}}}}\n|}}")

        file_write = file_write + f'{format_txt}\n'

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def fix_str(str_input):
    return str_input.replace('"', r'\"')


def python_dict_to_lua_table(python_dict, indent = 0):
    indent_str = '\t' * indent  # indentation string
    lua_table = "{\n"
    for key, value in python_dict.items():
        # Assuming keys are strings
        lua_key = f'{indent_str}\t["{fix_str(key)}"]'
        if isinstance(value, str):
            lua_value = f'"{fix_str(value)}"'
        elif isinstance(value, dict):
            # recursive call for nested dictionaries with increased indent
            lua_value = python_dict_to_lua_table(value, indent + 1)
        elif isinstance(value, list):
            # Process list to Lua table format
            list_values = ", ".join([f'"{fix_str(item)}"' if isinstance(item, str) else str(item) for item in value])
            lua_value = "{" + list_values + "}"
        else:
            lua_value = str(value)
        lua_table += f"{lua_key} = {lua_value},\n"
    lua_table += f"{indent_str}}}"

    return lua_table


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
                  f"{python_dict_to_lua_table(achiev_dict)}")

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def copy_file(source_path, destination_path):
    if os.path.exists(source_path):
        dest_dir = destination_path.replace(destination_path.split('/')[-1], '')
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy(source_path, destination_path)
        print(f"File copied successfully from {source_path} to {destination_path}")
    else:
        print(f"The file {source_path} does not exist.")


def parse_nous_dice_face():
    with open(f'{CONFIG.EXCEL_PATH}/RogueNousDiceSurface.json', 'r', encoding = 'utf-8') as file:
        dicesurfacejson = json.load(file)

    file_write_path = f'{CONFIG.OUTPUT_PATH}/Dice_Face_Output.lua'
    file_write = ''

    dice_dict = {}

    for item in dicesurfacejson:
        name = dicesurfacejson[item]['SurfaceName']['TextMapEN']
        rarity = str(dicesurfacejson[item]['Rarity'] + 2)

        dice_dict[name] = rarity

        file_name_clean = f'Dice Face {name.replace(":", "")}'

        source_path = dicesurfacejson[item]['Icon']
        source_path = f'{CONFIG.IMAGE_PATH}/{source_path.lower()}'
        destination_path = f'{CONFIG.OUTPUT_PATH}/DiceFaces/{file_name_clean}.png'

        if not os.path.exists(f'{CONFIG.OUTPUT_PATH}/DiceFaces'):
            os.makedirs(f'{CONFIG.OUTPUT_PATH}/DiceFaces')

        copy_file(source_path, destination_path)

    sorted_dict = {key: dice_dict[key] for key in sorted(dice_dict)}

    sorted_dict_2 = {k: v for k, v in sorted(sorted_dict.items(), key = lambda dict_item: dict_item[1], reverse = True)}

    for name, rarity in sorted_dict_2.items():
        file_write = file_write + f'\n	[\'{name}\'] = {{ rarity = \'{rarity}\' }},'

    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


def write_file(file_write_path, file_write):
    with open(file_write_path, 'w', encoding = 'utf-8') as file:
        file.write(file_write)
        print('Saved to ' + file_write_path + '.')


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

    file_write = python_dict_to_lua_table(dict_0)

    write_file(file_write_path, file_write)


def parse_pure_fiction_main(pf_id, fh = False):
    ol.load_data()
    
    if fh:
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeMazeConfig.json', 'r', encoding = 'utf-8') as file:
            challengestoryjson = json.load(file)
    else:
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryMazeConfig.json', 'r', encoding = 'utf-8') as file:
            challengestoryjson = json.load(file)
            
    with open(f'{CONFIG.EXCEL_PATH}/MazeBuff.json', 'r', encoding = 'utf-8') as file:
            mazebuffjson = json.load(file)

    stage_list = []

    for maze in challengestoryjson:
        if challengestoryjson[maze]['GroupID'] == pf_id:
            stage_list.append(maze)

    file_write = ''
    if fh:
        file_write_path = f'{CONFIG.OUTPUT_PATH}/Forgotten_Hall_Output.wikitext'
    else:
        file_write_path = f'{CONFIG.OUTPUT_PATH}/Pure_Fiction_Output.wikitext'

    for n, stage in enumerate(stage_list):
        if n == len(stage_list) - 1:
            end_text = ''
        else:
            end_text = '\n</div><!--\n--><div>\n'

        if fh:
            template = parse_fh_stage(stage)
        else:
            template = parse_pure_fiction(stage)

        file_write = file_write + "====Stage " + str(n + 1) + "====\n" + template + end_text

    file_write = (f'<div style="display:flex; column-gap: 15px; flex-direction:'
                  f'row; flex-wrap: wrap;"><div>\n{file_write}\n</div></div>')
    
    if fh:
        with open(f'{CONFIG.EXCEL_PATH}/ScheduleDataChallengeMaze.json', 'r', encoding = 'utf-8') as file:
            schedulejson = json.load(file)
        
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeGroupConfig.json', 'r', encoding = 'utf-8') as file:
            challengegroupjson = json.load(file)        
            
        challengegroup = challengegroupjson[str(pf_id)]
        
        periodname = challengegroup['GroupName']['TextMapEN']
        scheduleid = challengegroup['ScheduleDataID']
        mazebuffid = challengegroup['MazeBuffID']
        mazebuff = mazebuffjson[str(mazebuffid)]
        
        buffdesc = mazebuff['1']['BuffDesc']['TextMapEN']
        buffparams = mazebuff['1']['ParamList']
        
        buffdesc = parse_params(buffdesc, buffparams)
        
        starttime = schedulejson[str(scheduleid)]['BeginTime'].replace('-', '/')
        endtime = schedulejson[str(scheduleid)]['EndTime'].replace('-', '/')
        
        ol_text = ol.gen_ol(periodname)
        
        file_write = f'''{{{{Forgotten Hall Version
|time_start        = {starttime}
|time_end          = {endtime}
|prev              = 
|next              = 
}}}}

==Memory of Chaos==
===Memory Turbulence===
{{{{Memory Turbulence
|name1       = {periodname}
|time_start1 = {starttime}
|time_end1   = {endtime}
|effect1     = {buffdesc}

|no2 = 1

|no3 = 1
}}}}

=={periodname}==
{file_write}
<noinclude>
==Other Languages==
{ol_text}<!--
==Notes==
{{{{Reflist|note=1}}}}
-->
==Navigation==
{{{{Endgame Navbox}}}}
</noinclude>
'''        
    else:
        with open(f'{CONFIG.EXCEL_PATH}/ScheduleDataChallengeStory.json', 'r', encoding = 'utf-8') as file:
            schedulejson = json.load(file)
        
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryGroupConfig.json', 'r', encoding = 'utf-8') as file:
            challengegroupjson = json.load(file) 
            
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryGroupExtra.json', 'r', encoding = 'utf-8') as file:
            extrajson = json.load(file)
            
        challengegroup = challengegroupjson[str(pf_id)]
        
        periodname = challengegroup['GroupName']['TextMapEN']
        mazebuffid = str(challengegroup['MazeBuffID'])
        
        main_buff = parse_mazebuff(mazebuffid)

        sub_buff_1 = parse_mazebuff(str(extrajson[str(pf_id)]['BuffList'][0]))
        sub_buff_2 = parse_mazebuff(str(extrajson[str(pf_id)]['BuffList'][1]))
        sub_buff_3 = parse_mazebuff(str(extrajson[str(pf_id)]['BuffList'][2]))
        
        begin, end = parse_schedule(str(challengegroupjson[str(pf_id)]['ScheduleDataID']), schedulejson)
        
        ol_text = ol.gen_ol(periodname)
        
        # phase icon
        icon = extrajson[str(pf_id)].get('ThemeIconPicPath')
        
        if icon:
            copy_file(f'{CONFIG.IMAGE_PATH}/{icon}', f'{CONFIG.OUTPUT_PATH}/Images/{periodname}.png')
        
        file_write = f'''<noinclude>
{{{{Pure Fiction Version
|image             = {periodname}.png
|time_start        = {begin}
|time_end          = {end}
|prev              = 
|next              = 
}}}}
</noinclude>
=={periodname}==
{{{{Clr}}}}
{{{{Whimsicality
|time_start        = {begin}
|time_end          = {end}
|whim_name         = {main_buff[0]}
|whim_eff          = {main_buff[1]}
|caco_name1        = {sub_buff_1[0]}
|caco_eff1         = {sub_buff_1[1]}
|caco_name2        = {sub_buff_2[0]}
|caco_eff2         = {sub_buff_2[1]}
|caco_name3        = {sub_buff_3[0]}
|caco_eff3         = {sub_buff_3[1]}
}}}}
{file_write}
<noinclude>
==Other Languages==
{ol_text}
==Navigation==
{{{{Endgame Navbox}}}}
</noinclude>
'''
        

    write_file(file_write_path, file_write)
    
    
def parse_pure_fiction_main_v2(pf_id, fh = False):
    ol.load_data()
    
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryMazeConfig.json', 'r', encoding = 'utf-8') as file:
        challengestoryjson = json.load(file)

    stage_list = []

    for maze in challengestoryjson:
        if challengestoryjson[maze]['GroupID'] == pf_id:
            stage_list.append(maze)

    file_write = ''
    file_write_path = f'{CONFIG.OUTPUT_PATH}/Pure_Fiction_Output.wikitext'

    for n, stage in enumerate(stage_list):
        if n == len(stage_list) - 1:
            end_text = ''
        else:
            end_text = '\n</div><!--\n--><div>\n'

        template = parse_pure_fiction(stage)

        file_write = file_write + "====Stage " + str(n + 1) + "====\n" + template + end_text

    file_write = (f'<div style="display:flex; column-gap: 15px; flex-direction:'
                  f'row; flex-wrap: wrap;"><div>\n{file_write}\n</div></div>')
    
    
    with open(f'{CONFIG.EXCEL_PATH}/ScheduleDataChallengeStory.json', 'r', encoding = 'utf-8') as file:
        schedulejson = json.load(file)
    
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryGroupConfig.json', 'r', encoding = 'utf-8') as file:
        challengegroupjson = json.load(file) 
        
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryGroupExtra.json', 'r', encoding = 'utf-8') as file:
        extrajson = json.load(file)
        
    challengegroup = challengegroupjson[str(pf_id)]
    
    periodname = challengegroup['GroupName']['TextMapEN']
    
    main_buff = parse_mazebuff(str(extrajson[str(pf_id)]['SubMazeBuffList'][0]))
    main_buff_2 = parse_mazebuff(str(extrajson[str(pf_id)]['SubMazeBuffList'][1]))
    main_buff_3 = parse_mazebuff(str(extrajson[str(pf_id)]['SubMazeBuffList'][2]))

    sub_buff_1 = parse_mazebuff(str(extrajson[str(pf_id)]['BuffList'][0]))
    sub_buff_2 = parse_mazebuff(str(extrajson[str(pf_id)]['BuffList'][1]))
    sub_buff_3 = parse_mazebuff(str(extrajson[str(pf_id)]['BuffList'][2]))
    
    begin, end = parse_schedule(str(challengegroupjson[str(pf_id)]['ScheduleDataID']), schedulejson)
    
    ol_text = ol.gen_ol(periodname)
    
    # phase icon
    icon = extrajson[str(pf_id)].get('ThemeIconPicPath')
    
    if icon:
        copy_file(f'{CONFIG.IMAGE_PATH}/{icon}', f'{CONFIG.OUTPUT_PATH}/Images/{periodname}.png')
    
    file_write = f'''<noinclude>
{{{{Pure Fiction Version
|image             = {periodname}.png
|time_start        = {begin}
|time_end          = {end}
|prev              = 
|next              = 
}}}}
</noinclude>
=={periodname}==
{{{{Clr}}}}
{{{{Whimsicality
|time_start        = {begin}
|time_end          = {end}
|whim_name         = {main_buff[0]}
|whim_eff          = {main_buff[1]}
|whim_name2        = {main_buff_2[0]}
|whim_eff2         = {main_buff_2[1]}
|whim_name3        = {main_buff_3[0]}
|whim_eff3         = {main_buff_3[1]}
|caco_name1        = {sub_buff_1[0]}
|caco_eff1         = {sub_buff_1[1]}
|caco_name2        = {sub_buff_2[0]}
|caco_eff2         = {sub_buff_2[1]}
|caco_name3        = {sub_buff_3[0]}
|caco_eff3         = {sub_buff_3[1]}
}}}}
{file_write}
<noinclude>
==Other Languages==
{ol_text}
==Navigation==
{{{{Endgame Navbox}}}}
</noinclude>
'''
        

    write_file(file_write_path, file_write)


def parse_pure_fiction(pf_id):
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryMazeConfig.json', 'r', encoding = 'utf-8') as file:
        challengestoryjson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/StageConfig.json', 'r', encoding = 'utf-8') as file:
        stagejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/StageInfiniteGroup.json', 'r', encoding = 'utf-8') as file:
        stageinfinitegroup = json.load(file)

    main = challengestoryjson[str(pf_id)]

    # rtypes
    rec_types_1 = main['DamageType1']
    rec_types_1_str = ''
    rec_types_2 = main['DamageType2']
    rec_types_2_str = ''
    for x in range(0, len(rec_types_1)):
        if rec_types_1[x] == 'Thunder':
            rec_types_1[x] = 'Lightning'
        if x == 0:
            rec_types_1_str = rec_types_1[x]
        else:
            rec_types_1_str = rec_types_1_str + "," + rec_types_1[x]
    for x in range(0, len(rec_types_2)):
        if rec_types_2[x] == 'Thunder':
            rec_types_2[x] = 'Lightning'
        if x == 0:
            rec_types_2_str = rec_types_2[x]
        else:
            rec_types_2_str = rec_types_2_str + "," + rec_types_2[x]

    # stages
    stage1 = stagejson[str(main['EventIDList1'][0])]
    level = stage1['Level']

    stageinfinitegroup1 = stageinfinitegroup[str(main['EventIDList1'][0])]
    s1w1 = parse_stage_infinite_group(stageinfinitegroup1['WaveIDList'][0])
    s1w2 = parse_stage_infinite_group(stageinfinitegroup1['WaveIDList'][1])
    s1w3 = parse_stage_infinite_group(stageinfinitegroup1['WaveIDList'][2])

    stageinfinitegroup2 = stageinfinitegroup[str(main['EventIDList2'][0])]
    s2w1 = parse_stage_infinite_group(stageinfinitegroup2['WaveIDList'][0])
    s2w2 = parse_stage_infinite_group(stageinfinitegroup2['WaveIDList'][1])
    s2w3 = parse_stage_infinite_group(stageinfinitegroup2['WaveIDList'][2])

    # targets
    target_ids = main['ChallengeTargetID']
    for i in range(len(target_ids)):
        target_ids[i] = str(target_ids[i])
    target_1 = parse_target(target_ids[0], story = True)
    target_2 = parse_target(target_ids[1], story = True)
    target_3 = parse_target(target_ids[2], story = True)

    format_dict = {
        'maxcycle': '5 + 5',
        'enemylv ': level,
        'rtype1  ': rec_types_1_str,
        'rtype2  ': rec_types_2_str,
        'obj     ': f'{target_1};{target_2};{target_3}',
        't1w1    ': s1w1['mons'],
        't1w1max ': s1w1['max'],
        't1w2    ': s1w2['mons'],
        't1w2max ': s1w2['max'],
        't1w3    ': s1w3['mons'],
        't1w3max ': s1w3['max'],
        't2w1    ': s2w1['mons'],
        't2w1max ': s2w1['max'],
        't2w2    ': s2w2['mons'],
        't2w2max ': s2w2['max'],
        't2w3    ': s2w3['mons'],
        't2w3max ': s2w3['max'],
    }

    out = dict_to_template(format_dict, 'Pure Fiction Stage')

    return out


def dict_to_template(dictionary, template):
    out = ''
    for key, value in dictionary.items():
        out = f'{out}|{key} = {value}\n'

    out = f'{{{{{template}\n{out}}}}}'

    return out


def parse_target(target_id, story = False, boss = False):
    if story:
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeStoryTargetConfig.json', 'r', encoding = 'utf-8') as file:
            targetconfig = json.load(file)
    elif boss:
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeBossTargetConfig.json', 'r', encoding = 'utf-8') as file:
            targetconfig = json.load(file)
    else:
        with open(f'{CONFIG.EXCEL_PATH}/ChallengeTargetConfig.json', 'r', encoding = 'utf-8') as file:
            targetconfig = json.load(file)

    target_string = targetconfig[target_id]['ChallengeTargetName']['TextMapEN']
    try:
        target_param = targetconfig[target_id]['ChallengeTargetParam1']
    except KeyError:
        target_param = 0

    target_string = target_string.replace(r'#1[i]', str(target_param))
    target_string = target_string.replace(r'#1', str(target_param))

    return target_string


def parse_stage_infinite_group(wave):
    with open(f'{CONFIG.EXCEL_PATH}/StageInfiniteWaveConfig.json', 'r', encoding = 'utf-8') as file:
        stageinfinitewave = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/StageInfiniteMonsterGroup.json', 'r', encoding = 'utf-8') as file:
        stageinfinitemonster = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    mons_list = stageinfinitemonster[str(wave)]['MonsterList']
    mons_dict = {}

    for mons in mons_list:
        mons_name = monsterjson[str(mons)]['MonsterName']['TextMapEN']

        if mons_name == 'Sequence Trotter':
            weaknesses = get_mons_weak(mons)
            try:
                mons_dict[(mons_name, weaknesses)] = mons_dict[(mons_name, weaknesses)] + 1
            except KeyError:
                mons_dict[(mons_name, weaknesses)] = 1
        elif mons_name == 'Fictional Ensemble':
            continue
        else:
            try:
                mons_dict[mons_name] = mons_dict[mons_name] + 1
            except KeyError:
                mons_dict[mons_name] = 1

    mons_format = ''

    for key, value in mons_dict.items():
        if isinstance(key, tuple):
            mons_format = f'{mons_format}{key[0]}{{ text = {value} $ weakness = {key[1]} }},'
        else:
            mons_format = f'{mons_format}{key}{{ text = {value} }},'

    mons_format = mons_format[:-1]

    max_count = stageinfinitewave[str(wave)]['MaxTeammateCount']

    output = {
        'max': max_count,
        'mons': mons_format
    }

    return output


def get_mons_weak(mons_id):
    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    out = ''

    for weak in monsterjson[str(mons_id)]['StanceWeakList']:
        if weak == 'Thunder':
            out = f'{out}Lightning;'
        else:
            out = f'{out}{weak};'

    out = out[:-1]

    return out


def parse_fh_stage(stage_id):
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeMazeConfig.json', 'r', encoding = 'utf-8') as file:
        challengemazejson = json.load(file)

    with open(f'{CONFIG.EXCEL_PATH}/StageConfig.json', 'r', encoding = 'utf-8') as file:
        stagejson = json.load(file)

    main = challengemazejson[str(stage_id)]

    # rtypes
    rec_types_1 = main['DamageType1']
    rec_types_1_str = ''
    for x in range(0, len(rec_types_1)):
        if rec_types_1[x] == 'Thunder':
            rec_types_1[x] = 'Lightning'
        if x == 0:
            rec_types_1_str = rec_types_1[x]
        else:
            rec_types_1_str = rec_types_1_str + "," + rec_types_1[x]

    rec_types_2_str = ''
    if main['DamageType2']:
        rec_types_2 = main['DamageType2']
        for x in range(0, len(rec_types_2)):
            if rec_types_2[x] == 'Thunder':
                rec_types_2[x] = 'Lightning'
            if x == 0:
                rec_types_2_str = rec_types_2[x]
            else:
                rec_types_2_str = rec_types_2_str + "," + rec_types_2[x]
    else:
        rec_types_2_str = ''

    # mons
    mons_dict1 = {
        'b1w1': '',
        'b1w2': '',
        'b1w3': '',
        'b2w1': '',
        'b2w2': '',
        'b2w3': ''
    }

    mons_dict2 = mons_dict1

    eventidlist1 = main['EventIDList1']
    mons_dict1 = parse_fh_event_id_list(eventidlist1)

    eventidlist2 = main['EventIDList2']
    if eventidlist2:
        mons_dict2 = parse_fh_event_id_list(eventidlist2)

    # targets
    target_ids = main['ChallengeTargetID']
    for i in range(len(target_ids)):
        target_ids[i] = str(target_ids[i])
    target_1 = parse_target(target_ids[0])
    target_2 = parse_target(target_ids[1])
    target_3 = parse_target(target_ids[2])

    # misc
    stage = stagejson[str(eventidlist1[0])]
    level = stage['Level']
    maxcycle = main['ChallengeCountDown']

    # templatize
    format_dict = {
        'maxcycle': maxcycle,
        'enemylv ': level,
        'rtype1  ': rec_types_1_str,
        'rtype2  ': rec_types_2_str,
        'obj     ': f'{target_1};{target_2};{target_3}',
        't1w1    ': mons_dict1['b1w1'],
        't1w2    ': mons_dict1['b1w2'],
        't1w3    ': mons_dict1['b1w3'],
        't2w1    ': mons_dict2['b1w1'],
        't2w2    ': mons_dict2['b1w2'],
        't2w3    ': mons_dict2['b1w3'],
        'delim   ': ';'
    }

    if mons_dict1['b2w1']:
        format_dict['battle  '] = '1'
        format_dict['t2w1    '] = mons_dict1['b2w1']
        format_dict['t2w2    '] = mons_dict1['b2w2']
        format_dict['t2w3    '] = mons_dict1['b2w3']

    out = dict_to_template(format_dict, 'Forgotten Hall Stage')

    return out


def parse_fh_event_id_list(idlist):
    with open(f'{CONFIG.EXCEL_PATH}/StageConfig.json', 'r', encoding = 'utf-8') as file:
        stagejson = json.load(file)

    b1w2 = ''
    b1w3 = ''
    b2w1 = ''
    b2w2 = ''
    b2w3 = ''

    b1 = stagejson[str(idlist[0])]['MonsterList']
    b1w1 = parse_monster_dict(b1[0])

    if len(b1) >= 2:
        b1w2 = parse_monster_dict(b1[1])

    if len(b1) == 3:
        b1w3 = parse_monster_dict(b1[2])

    if len(idlist) == 2:
        b2 = stagejson[str(idlist[1])]['MonsterList']
        b2w1 = parse_monster_dict(b2[0])

        if len(b2) >= 2:
            b2w2 = parse_monster_dict(b2[1])

        if len(b2) >= 3:
            b2w3 = parse_monster_dict(b2[2])

    return {
        'b1w1': b1w1[:-1],
        'b1w2': b1w2[:-1],
        'b1w3': b1w3[:-1],
        'b2w1': b2w1[:-1],
        'b2w2': b2w2[:-1],
        'b2w3': b2w3[:-1]
    }


def parse_monster_dict(monster_dict):
    with open(f'{CONFIG.EXCEL_PATH}/MonsterConfig.json', 'r', encoding = 'utf-8') as file:
        monsterjson = json.load(file)

    out = ''

    for mons in monster_dict.values():
        mons_name = monsterjson[str(mons)]['MonsterName']['TextMapEN']
        out = f'{out}{mons_name};'

    return out


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
                  f"--%>--]=]\n\nreturn {python_dict_to_lua_table(out_dict)}")

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
                  f"--%>--]=]\n\nreturn {python_dict_to_lua_table(out_dict)}")

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

    file_write_path =f'{CONFIG.OUTPUT_PATH}Light_Cone_Ascension_and_Stats_data.lua'
    file_write = (f"--[=[<%-- [PAGE_INFO]\n    comment = #Please do not remove this struct. It's record contains some "
                  f"important information of edit. This struct will be removed automatically after you push edits.#\n "
                  f"   pageTitle = #Module:Light Cone Ascensions and Stats/data#\n    pageID = ##\n    revisionID = "
                  f"##\n    contentModel = #Scribunto#\n    contentFormat = #text/plain#\n[END_PAGE_INFO] "
                  f"--%>--]=]\n\nreturn {python_dict_to_lua_table(out_dict)}")

    write_file(file_write_path, file_write)


def preprocess_text(sec_id: int) -> list:
    print(f'PREPROCESSING {sec_id}')
    out = []
    msgitem_ls = []
    allnext_ls = []
    start_ls = []
    end_ls = []

    with open(f'{CONFIG.EXCEL_PATH}/MessageItemConfig.json', 'r', encoding = 'utf-8') as file:
        msgitemjson = json.load(file)

    for msgitem in msgitemjson.values():
        if msgitem.get('SectionID') == sec_id:
            msgitem_ls.append(msgitem['ID'])

    # convergence points
    for msgitem in msgitem_ls:
        next_ls = msgitemjson[str(msgitem)]['NextItemIDList']
        if len(next_ls) > 0:
            if next_ls[0] in allnext_ls and next_ls[0] not in end_ls:
                end_ls.append(next_ls[0])
            allnext_ls = allnext_ls + next_ls

        if len(next_ls) > 1:
            start_ls.append(msgitem)

    out = [[start, end] for start, end in zip(start_ls, end_ls)]
    return out


def parse_text_sec(sec_id, char_name):
    out = ''

    with open(f'{CONFIG.EXCEL_PATH}/MessageItemConfig.json', 'r', encoding = 'utf-8') as file:
        msgitemjson = json.load(file)

    msgitem_id = str(sec_id) + '00'
    complete = False

    branch_ls = preprocess_text(sec_id)

    """while not complete:
        sender = '(Trailblazer)' if msgitemjson[msgitem_id]['Sender'] == 'Player' else char_name
        text = msgitemjson[msgitem_id]['MainText']['TextMapEN']
        try:
            option_text = msgitemjson[msgitem_id]['OptionText']['TextMapEN']
        except KeyError:
            option_text = ''

        if option_text:
            out = f"{out}\n{indent[:-1]}{{{{DIcon}}}} {option_text}\n{indent}'''{sender}:''' {text}"
        else:
            out = f"{out}\n{indent}'''{sender}:''' {text}\n"

        if msgitemjson[msgitem_id]['NextItemIDList']:
            if msgitemjson[msgitem_id]['NextItemIDList'] == end_point:"""


def parse_char_text(char_name):
    with open(f'{CONFIG.EXCEL_PATH}/MessageContactsConfig.json', 'r', encoding = 'utf-8') as file:
        contactjson = json.load(file)

    char_id = ''
    for contact in contactjson.values():
        if contact['Name'].get('TextMapEN') == char_name:
            char_id = contact['ID']
            signature = contact['SignatureText']['TextMapEN']

    # message groups
    message_sec_ids = []

    with open(f'{CONFIG.EXCEL_PATH}/MessageGroupConfig.json', 'r', encoding = 'utf-8') as file:
        msggrpjson = json.load(file)

    for msggrp in msggrpjson.values():
        if msggrp['MessageContactsID'] == char_id:
            message_sec_ids.append(msggrp['MessageSectionIDList'][0])

    for sec_id in message_sec_ids:
        parse_text_sec(sec_id, char_name)


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
        
    with open('D:/HSR/0 - Data/StarRailBetaData-master 2.3/StarRailExcelMap/OutputEN/MonsterStatusConfig.json', 'r', encoding = 'utf-8') as file:
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
    

def parse_apoc_shadow(id):
    ol.load_data()
    
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeBossGroupConfig.json', 'r', encoding = 'utf-8') as file:
        groupjson = json.load(file)
        
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeBossMazeConfig.json', 'r', encoding = 'utf-8') as file:
        mazejson = json.load(file)
        
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeBossGroupExtra.json', 'r', encoding = 'utf-8') as file:
        extrajson = json.load(file)

    name = groupjson[id]['GroupName']['TextMapEN']
    
    # rtypes
    rec_types_1 = mazejson[f'{id}1']['DamageType1']
    rec_types_1_str = ''
    for x in range(0, len(rec_types_1)):
        if rec_types_1[x] == 'Thunder':
            rec_types_1[x] = 'Lightning'
        if x == 0:
            rec_types_1_str = rec_types_1[x]
        else:
            rec_types_1_str = rec_types_1_str + "," + rec_types_1[x]

    rec_types_2_str = ''
    if mazejson[f'{id}1']['DamageType2']:
        rec_types_2 = mazejson[f'{id}1']['DamageType2']
        for x in range(0, len(rec_types_2)):
            if rec_types_2[x] == 'Thunder':
                rec_types_2[x] = 'Lightning'
            if x == 0:
                rec_types_2_str = rec_types_2[x]
            else:
                rec_types_2_str = rec_types_2_str + "," + rec_types_2[x]
    else:
        rec_types_2_str = ''
        
    # mons
    mons_dict1 = {
        'b1w1': '',
        'b1w2': '',
        'b1w3': '',
        'b2w1': '',
        'b2w2': '',
        'b2w3': ''
    }

    mons_dict2 = mons_dict1

    eventidlist1 = mazejson[f'{id}1']['EventIDList1']
    mons_dict1 = parse_fh_event_id_list(eventidlist1)
    mons_tags1 = monster_tags_from_stage(eventidlist1[0])

    eventidlist2 = mazejson[f'{id}1']['EventIDList2']
    if eventidlist2:
        mons_dict2 = parse_fh_event_id_list(eventidlist2)
        mons_tags2 = monster_tags_from_stage(eventidlist2[0])
        
    # targets
    target_ids = mazejson[f'{id}1']['ChallengeTargetID']
    for i in range(len(target_ids)):
        target_ids[i] = str(target_ids[i])
    target_1 = parse_target(target_ids[0], boss = True)
    target_2 = parse_target(target_ids[1], boss = True)
    target_3 = parse_target(target_ids[2], boss = True)
    
    # buffs
    main_buff = parse_mazebuff(str(mazejson[f'{id}1']['MazeBuffID']))
    
    sub_buff_1_1 = parse_mazebuff(str(extrajson[id]['BuffList1'][0]))
    sub_buff_1_2 = parse_mazebuff(str(extrajson[id]['BuffList1'][1]))
    sub_buff_1_3 = parse_mazebuff(str(extrajson[id]['BuffList1'][2]))
    
    sub_buff_2_1 = parse_mazebuff(str(extrajson[id]['BuffList2'][0]))
    sub_buff_2_2 = parse_mazebuff(str(extrajson[id]['BuffList2'][1]))
    sub_buff_2_3 = parse_mazebuff(str(extrajson[id]['BuffList2'][2]))
    
    # schedule
    begin, end = parse_schedule(str(groupjson[id]['ScheduleDataID']))
    
    # ol
    ol_text = ol.gen_ol(name)
    
    # phase icon
    icon = extrajson[str(id)].get('ThemeIconPicPath')
    
    if icon:
        copy_file(f'{CONFIG.IMAGE_PATH}/{icon}', f'{CONFIG.OUTPUT_PATH}/Images/{name}.png')
    
    # output
    out = f"""<noinclude>
{{{{Apocalyptic Shadow Version
|image             = {name}.png
|time_start        = {begin}
|time_end          = {end}
|prev              = 
|next              = 
}}}}
__TOC__
</noinclude>{{{{Clr}}}}
=={name}==
{{{{Apocalyptic Shadow
|levels            = 60;70;80;90
|rtype1            = {rec_types_1_str}
|rtype2            = {rec_types_2_str}
|obj               = {target_1};{target_2};{target_3}
|main_buff         = {main_buff[0]}
|main_buff_desc    = {main_buff[1]}
|sub_buff_1_1      = {sub_buff_1_1[0]}
|sub_buff_1_1_desc = {sub_buff_1_1[1]}
|sub_buff_1_2      = {sub_buff_1_2[0]}
|sub_buff_1_2_desc = {sub_buff_1_2[1]}
|sub_buff_1_3      = {sub_buff_1_3[0]}
|sub_buff_1_3_desc = {sub_buff_1_3[1]}
|sub_buff_2_1      = {sub_buff_2_1[0]}
|sub_buff_2_1_desc = {sub_buff_2_1[1]}
|sub_buff_2_2      = {sub_buff_2_2[0]}
|sub_buff_2_2_desc = {sub_buff_2_2[1]}
|sub_buff_2_3      = {sub_buff_2_3[0]}
|sub_buff_2_3_desc = {sub_buff_2_3[1]}
|enemies_1         = {mons_dict1['b1w1']}
|enemies_2         = {mons_dict2['b1w1']}
|trait_1_1         = {mons_tags1[0][0]}
|trait_1_1_desc    = {mons_tags1[0][1]}
|trait_1_2         = {mons_tags1[1][0]}
|trait_1_2_desc    = {mons_tags1[1][1]}
|trait_1_3         = {mons_tags1[2][0]}
|trait_1_3_desc    = {mons_tags1[2][1]}
|trait_1_4         = {mons_tags1[3][0]}
|trait_1_4_desc    = {mons_tags1[3][1]}
|trait_2_1         = {mons_tags2[0][0]}
|trait_2_1_desc    = {mons_tags2[0][1]}
|trait_2_2         = {mons_tags2[1][0]}
|trait_2_2_desc    = {mons_tags2[1][1]}
|trait_2_3         = {mons_tags2[2][0]}
|trait_2_3_desc    = {mons_tags2[2][1]}
|trait_2_4         = {mons_tags2[3][0]}
|trait_2_4_desc    = {mons_tags2[3][1]}
}}}}
<noinclude>
==Other Languages==
{ol_text}
==Navigation==
{{{{Endgame Navbox}}}}
</noinclude>"""

    pyperclip.copy(out)
    print(out)
    

def monster_tags_from_stage(id, monsindex = 0):
    with open(f'{CONFIG.EXCEL_PATH}/StageConfig.json', 'r', encoding = 'utf-8') as file:
        stagejson = json.load(file)
    
    with open(f'{CONFIG.EXCEL_PATH}/MonsterGuideConfig.json', 'r', encoding = 'utf-8') as file:
        guidejson = json.load(file)
        
    with open(f'{CONFIG.EXCEL_PATH}/MonsterGuideTag.json', 'r', encoding = 'utf-8') as file:
        tagjson = json.load(file)
        
    mons_id = stagejson[str(id)]['MonsterList'][0][f'Monster{monsindex}']
    tags = guidejson[str(mons_id)]['TagList']
    
    out = []
    
    for tag in tags:
        name = tagjson[str(tag)]['TagName']['TextMapEN']
        desc = tagjson[str(tag)]['TagBriefDescription']['TextMapEN']
        params = tagjson[str(tag)]['ParameterList']
        
        if params:
            desc = parse_params(desc, params)
        
        out.append([name, desc])
        
    return out
    

def parse_schedule(id, schedulejson: dict = None):
    if not schedulejson:
        with open(f'{CONFIG.EXCEL_PATH}/ScheduleDataChallengeBoss.json', 'r', encoding = 'utf-8') as file:
            schedulejson = json.load(file)
            
    return schedulejson[id]['BeginTime'].replace('-', '/'), schedulejson[id]['EndTime'].replace('-', '/')
    

def parse_mazebuff(id):
    with open(f'{CONFIG.EXCEL_PATH}/MazeBuff.json', 'r', encoding = 'utf-8') as file:
        mazebuffjson = json.load(file)
        
    desc = mazebuffjson[id]['1']['BuffDesc']['TextMapEN']
    params = mazebuffjson[id]['1']['ParamList']
    
    name = mazebuffjson[id]['1']['BuffName']['TextMapEN']
    
    icon = mazebuffjson[id]['1'].get('BuffIcon')
    
    if icon and icon != 'SpriteOutput/BuffIcon/Inlevel/IconBuffCommon.png':
        copy_file(f'{CONFIG.IMAGE_PATH}/{icon}', f'{CONFIG.OUTPUT_PATH}/Images/Icon {name}.png')
        
    
    return name, parse_params(desc, params)
 

def copy_ol(input):
    ol.load_data()
    pyperclip.copy(ol.gen_ol(input))


#########################################################################

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--curio', type = bool)
    parser.add_argument('--aetherpassive', type = bool)
    parser.add_argument('--rewards', type = bool)
    parser.add_argument('--tutorial', type = int)
    parser.add_argument('--blessings', type = bool)
    parser.add_argument('--aetherchallenge', type = bool)
    parser.add_argument('--rogueendlessrewards', type = bool)
    parser.add_argument('--heliobuschallenge', type = bool)
    parser.add_argument('--heliobusraid', type = int)
    parser.add_argument('--heliobususer', type = bool)
    parser.add_argument('--heliobuspost', type = bool)
    parser.add_argument('--heliobustemplate', type = bool)
    parser.add_argument('--achievid', type = bool)
    parser.add_argument('--nousdicefaceicons', type = bool)
    parser.add_argument('--hardlevel', type = bool)
    parser.add_argument('--purefiction', type = int)
    parser.add_argument('--purefictionv2', type = int)
    parser.add_argument('--fh', type = int)
    parser.add_argument('--charasc', type = bool)
    parser.add_argument('--traceupgr', type = bool)
    parser.add_argument('--lcasc', type = bool)
    parser.add_argument('--text', type = str)
    parser.add_argument('--techniquestatus', type = str)
    parser.add_argument('--avatarstatus', type = str)
    parser.add_argument('--monsterstatus', type = str)
    parser.add_argument('--ol', type = str)
    parser.add_argument('--apocshadow', type = str)
    parser.add_argument('--redirectfromstr', type = str)

    args = parser.parse_args()

    if not os.path.exists(f'{CONFIG.OUTPUT_PATH}'):
        os.makedirs(f'{CONFIG.OUTPUT_PATH}')

    if args.curio:
        parse_curio()

    if args.aetherpassive:
        parse_aether_passive()

    if args.rewards:
        parse_rewards()

    tutorial_id = args.tutorial
    if tutorial_id:
        parse_tutorial(str(tutorial_id))

    if args.blessings:
        parse_blessings()

    if args.aetherchallenge:
        parse_aether_divide_challenge()

    if args.rogueendlessrewards:
        parse_rogue_endless_rewards()

    if args.heliobuschallenge:
        parse_heliobus_challenge()

    heliobus_raid_id = args.heliobusraid
    if heliobus_raid_id:
        parse_heliobus_raid(heliobus_raid_id)

    if args.heliobususer:
        parse_heliobus_user()

    if args.heliobuspost:
        parse_heliobus_post()

    if args.heliobustemplate:
        parse_heliobus_template()

    if args.achievid:
        parse_achiev_id()

    if args.nousdicefaceicons:
        parse_nous_dice_face()

    if args.hardlevel:
        parse_hard_level()

    if args.purefiction:
        parse_pure_fiction_main(args.purefiction)
        
    if args.purefictionv2:
        parse_pure_fiction_main_v2(args.purefictionv2)

    if args.fh:
        parse_pure_fiction_main(args.fh, fh = True)

    if args.charasc:
        parse_char_asc()
        
    if args.traceupgr:
        parse_trace_upgr()

    if args.lcasc:
        parse_lc_asc()

    if args.text:
        parse_char_text(args.text)

    if args.techniquestatus:
        parse_technique_status()
        
    if args.avatarstatus:
        parse_avatar_status()
        
    if args.monsterstatus:
        parse_monster_status()
        
    if args.ol:
        copy_ol(args.ol)
        
    if args.apocshadow:
        parse_apoc_shadow(args.apocshadow)
        
    if args.redirectfromstr:
        from utils.redirect import redirects_from_str
        redirects_from_str(args.redirectfromstr)
