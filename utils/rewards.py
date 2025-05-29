import json

from getConfig import CONFIG


def parse_rewards():
    file_write_path =f'{CONFIG.OUTPUT_PATH}/Rewards.txt'

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
    file_write_path =f'{CONFIG.OUTPUT_PATH}/RogueEndlessRewards.txt'

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