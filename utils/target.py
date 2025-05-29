import json

from getConfig import CONFIG


def parse_challenge_target(target_id):
    with open(f'{CONFIG.EXCEL_PATH}/ChallengeTargetConfig.json', 'r', encoding = 'utf-8') as file:
        targetconfig = json.load(file)

    target_string = targetconfig[target_id]['ChallengeTargetName']['TextMapEN']
    try:
        target_param = targetconfig[target_id]['ChallengeTargetParam1']
    except KeyError:
        target_param = 0

    target_string = target_string.replace(r'#1[i]', str(target_param))

    return target_string


def parse_battle_target(target_id):
    with open(f'{CONFIG.EXCEL_PATH}/BattleTargetConfig.json', 'r', encoding = 'utf-8') as file:
        targetconfig = json.load(file)

    target_string = targetconfig[target_id]['TargetName']['TextMapEN']
    try:
        target_param = targetconfig[target_id]['TargetParam']
    except KeyError:
        target_param = 0

    target_string = target_string.replace(r'#1[i]', str(target_param))

    return target_string


def parse_raid_target(target_id):
    with open(f'{CONFIG.EXCEL_PATH}/RaidTargetConfig.json', 'r', encoding = 'utf-8') as file:
        targetconfig = json.load(file)

    target_string = targetconfig[target_id]['TargetName']['TextMapEN']
    try:
        target_param = targetconfig[target_id]['TargetParam1']
    except KeyError:
        target_param = 0

    target_string = target_string.replace(r'#1[i]', str(target_param)).replace(r'#1', str(target_param))

    return target_string