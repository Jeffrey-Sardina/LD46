from PIL import Image, ImageTk
import random
import glob
import os

#Constants
text_path = os.path.join('assets', 'text')
image_path = os.path.join('assets', 'images')

def description_text_files():
    '''
    Gets all text files in the form name.txt, but not name.<number>.txt
    '''
    path = os.path.join(text_path, '*.txt')
    files = glob.glob(path)
    return [os.path.basename(file_name).split('.')[0] for file_name in files if file_name.count('.') == 1]


def load_text_asset(file_name):
    '''
    Get all text in a file
    '''
    path = os.path.join(text_path, file_name)
    with open(path, 'r') as data:
        text = data.read()
    return text

def load_text_options_asset(file_name):
    '''
    Get 2 strings
        1) option description
        2) next file
    '''
    path = os.path.join(text_path, file_name)
    with open(path, 'r') as data:
        text = data.readlines()

    description = ''.join(line for line in text[:-1])
    file_name = text[-1].strip().split('.')[0]
    return description, file_name

def load_language_module(file_name):
    mapping = {}
    path = os.path.join(text_path, file_name)
    with open(path, 'r') as data:
        for line in data:
            for data_id, text in line.strip().split(','):
                mapping[data_id] = text
    return mapping

def load_image_asset(file_name):
    path = os.path.join(image_path, file_name)
    return ImageTk.PhotoImage(file=path)

def roll(num, d):
    total = 0
    for i in range(num):
        total += random.randint(1, d)
    return total

def edit_distance(v, w):
    n = len(v) + 1
    m = len(w) + 1

    s = [[float('-inf') for _ in range(m)] for _ in range(n)]
    s[0][0] = 0
    for i in range(1,n):
        s[i][0] = s[i-1][0] + 1
    for j in range(1,m):
        s[0][j] = s[0][j-1] + 1

    for i in range(1, n):
        for j in range(1, m):
            deletion_event = s[i-1][j] + 1
            insertion_event = s[i][j-1] + 1
            if v[i-1] != w[j-1]:
                substitution_event = s[i-1][j-1] + 1
                s[i][j] = min(deletion_event, insertion_event, substitution_event)
            else:
                match_event = s[i-1][j-1]
                s[i][j] = min(deletion_event, insertion_event, match_event)

    return s[i][j]