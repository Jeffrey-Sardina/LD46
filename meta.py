import re
from utils import *

def determine_hp_change(text):
    result = re.search('lose [1-9] HP', text)
    hp_mod = 0
    if result:
        hp_mod = -int(result.group().split(' ')[1])
    else:
        result = re.search('gain [1-9] HP', text)
        if result:
            hp_mod = int(result.group().split(' ')[1])
    return hp_mod

def calc_hp_changes():
    hp_dict = {}
    screens = description_text_files()
    for screen_name in screens:
        text, _ = load_text_asset(screen_name + '.txt')
        hp_dict[screen_name] = determine_hp_change(text)
    return hp_dict

def main():
    hp_dict = calc_hp_changes()
    print(hp_dict)

if __name__ == '__main__':
    main()