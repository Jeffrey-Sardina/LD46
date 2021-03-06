from PIL import Image, ImageTk, ImageSequence
import random
import glob
import os
import re
import json

#Constants
text_path = os.path.join('assets', 'text')
json_path = os.path.join('assets', 'json')
image_path = os.path.join('assets', 'images')

#JSON functions
def load_json_text_asset(file_name):
    '''
    Load JSON from disk
    '''
    path = os.path.join(json_path, file_name)
    if os.path.exists(path):
        with open(path, 'r') as input_file:
            data = json.load(input_file) 
        return data
    else:
        print('WARNING: file ' + path + ' does not exist')
        return None

#TXT functions
def tome_texts():
    tome_pages = []
    time_files = tome_text_files()
    for file_name in time_files:
        text, _ = load_text_asset(file_name)
        tome_pages.append(text)
    return tome_pages

def tome_text_files():
    '''
    Returns all text files holding tome data
    '''
    path = os.path.join(text_path, 'tome_entry_*.txt')
    return [os.path.basename(file_name) for file_name in glob.glob(path)]

def description_text_files():
    '''
    Gets all text files in the form name.txt, but not name.<number>.txt
    .txt extension is not returned
    '''
    path = os.path.join(text_path, '*.txt')
    files = glob.glob(path)
    return [os.path.basename(file_name).split('.')[0] for file_name in files if file_name.count('.') == 1]

def load_text_asset(file_name):
    '''
    Get all text in a file
    '''
    path = os.path.join(text_path, file_name)
    if os.path.exists(path):
        with open(path, 'r') as data:
            text = data.readlines()
        if len(text) == 0:
            return None, None
        if '.txt' in text[-1]:
            description = ''.join(line for line in text[:-1])
            file_name = text[-1].strip().split('.')[0]
            return description, file_name
        else:
            description = ''.join(line for line in text)
            return description, None
    else:
        return None, None

#Image functions
def load_image_asset(file_name, width, height):
    '''
    Loads a single static image
    '''
    path = os.path.join(image_path, file_name)
    if os.path.exists(path):
        image = Image.open(path)
        img_width, img_height = dimensions_to_fill_space(image, width, height)
        image = image.resize((int(img_width), int(img_height)))
        imgtk = ImageTk.PhotoImage(image=image)
        return imgtk
    else:
        return None

def load_gif_asset(file_name, width, height):
    '''
    Loads all frames in a gif and returns them as a list
    '''
    path = os.path.join(image_path, file_name)
    if os.path.exists(path):
        gif = Image.open("animation.gif")
        image_frames = []
        for image_frame in ImageSequence.Iterator(gif):
            img_width, img_height = dimensions_to_fill_space(image_frame, width, height)
            image_frame = image_frame.resize((int(img_width), int(img_height)))
            imgtk = ImageTk.PhotoImage(image=image_frame)
            image_frames.append(imgtk)
        return image_frame
    else:
        return None


def dimensions_to_fill_space(img, width, height):
    '''
    This method gets the largest-area resize of an image to be displayed onthe given dimensions
    image to overflow off-screen. It maintains the image aspect ratio.
    '''

    #Get image dimensions
    original_width = img.width
    original_height = img.height

    #Get the scalars that transform the original size into the fullscreen dize
    width_scalar = width / original_width
    height_scalar = height / original_height

    #Make the image as large as possible without going over the screen size.
    width_based_scaling_height = original_height * width_scalar
    width_based_scaling_valid = True
    if width_based_scaling_height > height:
        width_based_scaling_valid = False
    height_based_scaling_width = original_width * height_scalar
    height_based_scaling_valid = True
    if height_based_scaling_width > width:
        height_based_scaling_valid = False

    #Return the calculated dimensions
    if width_based_scaling_valid and not height_based_scaling_valid:
        return width, width_based_scaling_height
    else:
        return height_based_scaling_width, height

#Misc.
def roll(num, d):
    total = 0
    for i in range(num):
        total += random.randint(1, d)
    return total