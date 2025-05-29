import argparse
import os
import pyperclip

import utils.ol as ol
from getConfig import CONFIG


def copy_ol(input):
    ol.load_data()
    pyperclip.copy(ol.gen_ol(input))
    

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
        from utils.su_old import parse_curio
        parse_curio()
        
    if args.blessings:
        from utils.su_old import parse_blessings
        parse_blessings()

    if args.aetherpassive:
        from utils.events.aether import parse_aether_passive
        parse_aether_passive()
        
    if args.aetherchallenge:
        from utils.events.aether import parse_aether_divide_challenge
        parse_aether_divide_challenge()

    if args.rewards:
        from utils.rewards import parse_rewards
        parse_rewards()
        
    if args.rogueendlessrewards:
        from utils.rewards import parse_rogue_endless_rewards
        parse_rogue_endless_rewards()

    if args.tutorial:
        from utils.tutorial import parse_tutorial
        parse_tutorial(str(args.tutorial))

    if args.heliobuschallenge:
        from utils.events.heliobus import parse_heliobus_challenge
        parse_heliobus_challenge()

    if args.heliobusraid:
        from utils.events.heliobus import parse_heliobus_raid
        parse_heliobus_raid(args.heliobusraid)

    if args.heliobususer:
        from utils.events.heliobus import parse_heliobus_user
        parse_heliobus_user()

    if args.heliobuspost:
        from utils.events.heliobus import parse_heliobus_post
        parse_heliobus_post()

    if args.heliobustemplate:
        from utils.events.heliobus import parse_heliobus_template
        parse_heliobus_template()

    if args.achievid:
        from utils.achievid import parse_achiev_id
        parse_achiev_id()

    if args.nousdicefaceicons:
        from utils.su_old import parse_nous_dice_face
        parse_nous_dice_face()

    if args.hardlevel:
        from utils.hardlevel import parse_hard_level
        parse_hard_level()

    if args.purefiction:
        from utils.endgame import parse_pure_fiction_main
        parse_pure_fiction_main(args.purefiction)
        
    if args.purefictionv2:
        from utils.endgame import parse_pure_fiction_main_v2
        parse_pure_fiction_main_v2(args.purefictionv2)

    if args.fh:
        from utils.endgame import parse_pure_fiction_main
        parse_pure_fiction_main(args.fh, fh = True)

    if args.charasc:
        from utils.leveling import parse_char_asc
        parse_char_asc()
        
    if args.traceupgr:
        from utils.leveling import parse_trace_upgr
        parse_trace_upgr()

    if args.lcasc:
        from utils.leveling import parse_lc_asc
        parse_lc_asc()

    if args.text:
        from utils.text import parse_char_text
        parse_char_text(args.text)

    if args.techniquestatus:
        from utils.status import parse_technique_status
        parse_technique_status()
        
    if args.avatarstatus:
        from utils.status import parse_avatar_status
        parse_avatar_status()
        
    if args.monsterstatus:
        from utils.status import parse_monster_status
        parse_monster_status()
        
    if args.ol:
        copy_ol(args.ol)
        
    if args.apocshadow:
        from utils.endgame import parse_apoc_shadow
        parse_apoc_shadow(args.apocshadow)
        
    if args.redirectfromstr:
        from utils.redirect import redirects_from_str
        redirects_from_str(args.redirectfromstr)
