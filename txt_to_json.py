import os
import glob
from utils import *

def main():
    text_path = os.path.join('assets', 'text')
    files = glob.glob(os.path.join(text_path, '*.txt'))

    out_path = os.path.join('assets', 'json')
    for file_name in files:
        base_name = os.path.basename(file_name).split('.')[0]
        text, next_file = load_text_asset(base_name + '.txt')
        data_dict = {'text':text, 'next_file':next_file}
        with open(os.path.join(out_path, base_name + '.json' ), 'w') as out:
            json.dump(data_dict, out)

if __name__ == '__main__':
    main()