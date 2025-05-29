import json

from getConfig import CONFIG


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