import json
import os
import shutil
import re

from getConfig import CONFIG
from utils.target import parse_battle_target, parse_raid_target
from utils.misc import parse_params, parse_monster_text, parse_reward_text


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
    file_write_path =f'{CONFIG.OUTPUT_PATH}/HeliobusChallenge.txt'

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