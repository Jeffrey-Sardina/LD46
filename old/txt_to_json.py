import os
import glob
from utils import *

health_changes = {'afterdruidcommands': 0, 'atbaseoftree': 0, 'BASEstory': -1, 'beforethirdpuzzle': 0, 'branchtoentrance': 0, 'chantwords': 0, 'chaseafterdruid': 0, 'climbtree': 0, 'decaytome': 0, 'dodobarrel': 0, 'dodoburnt': 0, 'dododoor': 0, 'dodotunnel': 0, 'entermaindoor': 0, 'falltodeath': 0, 'findtree': 0, 'finishthirdpuzzle': 0, 'firstpuzzle': 0, 'firstpuzzleright': 0, 'firstpuzzleutter': 0, 'firstpuzzlewrong': -1, 'flamestrap': -2, 'fourthpuzzle': 0, 'hackbarrel': 0, 'haifnix': 0, 'hiketotree': 0, 'introduction': 0, 'magai': 0, 'maindooropen': 0, 'maindooropensforreal': 0, 'mouthdrop': 0, 'nobudge': 0, 'openbarrel': 1, 'opening': 0, 'opentome': 0, 'raisechalice': 0, 'scrapeblood': 0, 'secondpuzzle': 0, 'secondpuzzletokenright': 0, 'secondpuzzletokens': 0, 'secondpuzzletokenwrong': -1, 'secondpuzzleutter': 0, 'secondpuzzleutterall': 0, 'shexgozh': 0, 'silentdoor': 0, 'slide': 0, 'standbarrel': 0, 'thirdpuzzle': 0, 'thirdpuzzlefirsttileright': 0, 'thirdpuzzlefirsttilewrong': -1, 'thirdpuzzlefourthtile': 0, 'thirdpuzzlesecondtile': 0, 'thirdpuzzlesecondtileright': 0, 'thirdpuzzlesecondtilewrong': -2, 'thirdpuzzlethirdtile': 0, 'thirdpuzzlethirdtileright': 0, 'thirdpuzzlethirdtilewrong': -3, 'tome': 0, 'tome_entry_01': 0, 'tome_entry_02': 0, 'tome_entry_03': 0, 'tome_entry_04': 0, 'tome_entry_05': 0, 'tome_entry_06': 0, 'tome_entry_07': 0, 'tome_entry_08': 0, 'tome_entry_09': 0, 'tome_entry_10': 0, 'training': 0, 'waitfordeath': 0, 'whattowalkto': 0, 'wingame': 0, 'wingame2': 0, 'wordsondoor': 0, 'wormstome': 0}


def main():
    text_path = os.path.join('assets', 'text')
    files = glob.glob(os.path.join(text_path, '*.txt'))

    out_path = os.path.join('assets', 'json')
    for file_name in files:
        base_name = '.'.join(x for x in os.path.basename(file_name).split('.')[:-1])
        text, next_file = load_text_asset(base_name + '.txt')
        if base_name in health_changes:
            data_dict = {'text':text, 'next_file':next_file, 'health_change':health_changes[base_name]}
        else:
            data_dict = {'text':text, 'next_file':next_file, 'health_change':0}
        with open(os.path.join(out_path, base_name + '.json' ), 'w') as out:
            json.dump(data_dict, out)

if __name__ == '__main__':
    main()