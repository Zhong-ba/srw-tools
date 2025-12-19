import json
import pyperclip

import utils.ol as ol
from utils.files import write_file, copy_file
from utils.misc import parse_params, dict_to_template, parse_mazebuff
from getConfig import CONFIG


def parse_schedule(id, schedulejson: dict = None):
    if not schedulejson:
        with open(f'{CONFIG.EXCEL_PATH}/ScheduleDataChallengeBoss.json', 'r', encoding = 'utf-8') as file:
            schedulejson = json.load(file)
            
    return schedulejson[id]['BeginTime'].replace('-', '/'), schedulejson[id]['EndTime'].replace('-', '/')


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
|image             = Event Memory of Chaos {periodname}.png
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
|image             = <gallery>
Event Pure Fiction {periodname}.png|Banner
{periodname}.png|Icon
</gallery>
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
|image             = <gallery>
Event Apocalyptic Shadow {name}.png|Banner
{name}.png|Icon
</gallery>
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
    # Feixiao
    if mons_id == 203501201:
        mons_id = 203302201
    
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