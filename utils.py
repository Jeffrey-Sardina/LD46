from PIL import Image, ImageTk
import random
import glob
import os
import re

#Constants
text_path = os.path.join('assets', 'text')
image_path = os.path.join('assets', 'images')

def tome_texts():
    tome_pages = []
    for file_name in tome_text_files():
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

def load_image_asset(file_name, width, height):
    path = os.path.join(image_path, file_name)
    if os.path.exists(path):
        image = Image.open(path)
        img_width, img_height = dimensions_to_fill_space(image, width, height)
        image = image.resize((int(img_width), int(img_height)))
        imgtk = ImageTk.PhotoImage(image=image)
        return imgtk
    else:
        return None

def roll(num, d):
    total = 0
    for i in range(num):
        total += random.randint(1, d)
    return total

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