import cv2
from PIL import Image, ImageTk
import random

#Constants
text_path = 'assets/text/'
image_path = 'assets/images/'
video_path = 'assets/videos/'

def load_text_asset(file_name):
    with open(text_path + file_name, 'r') as data:
        text = data.read()
    return text

def load_image_asset(file_name):
    return ImageTk.PhotoImage(file=image_path + file_name)

def load_video_asset(file_name):
    return cv2.VideoCapture(video_path + file_name)

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