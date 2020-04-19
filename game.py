import cv2
import tkinter as tk
from PIL import Image, ImageTk
import random
import sys
from utils import *
from player import Player

pages = {}
back_color = '#000000'
fore_color = '#00ff00'
screen_width = 0
screen_height = 0
title_font_name = 'Old English Text MT'
common_font_name = 'Courier'

class Video_Displayer():
    def __init__(self, video_name, display_area, width, height, is_training):
        self.cap = load_video_asset(video_name)
        self.display_area = display_area
        self.width = width
        self.height = height
        self.is_training = is_training

    def display(self):
        is_reading, frame = self.cap.read()

        if is_reading:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)

            img_width, img_height = dimensions_to_fill_space(img, self.width, self.height)
            img = img.resize((int(img_width), int(img_height)))

            imgtk = ImageTk.PhotoImage(image=img)
            self.display_area.imgtk = imgtk
            self.display_area.configure(image=imgtk)
            self.display_area.after(10, self.display)
        else:
            self.cap.release()

    def update(self, video_name):
        self.cap = cv2.VideoCapture(video_name)

def main():
    global ui_lang, screen_width, screen_height

    #Create Outermost Window
    window = tk.Tk()
    window.title('Game')

    #Create a container (that would contain all frames)
    container = tk.Frame()
    container.pack(side="top", fill="both", expand=True)

    #Set to fullscreen
    screen_width  = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (screen_width, screen_height))

    #Create pages
    pages['splash'] = create_splash_page(container, width=screen_width, height=screen_height)
    pages['howto'] = create_howto_page(container, width=screen_width, height=screen_height)
    pages['game_intro'] = create_game_intro_page(container, width=screen_width, height=screen_height)

    #Place pages in container such that all have the same relative size (ie, none show out from under others)
    for page_id in pages:
        pages[page_id].place(in_=container, relwidth=1, relheight=1)

    #Start on the consent page
    show_page('splash')

    #Start GUI Loop--control now in the hands of the UI
    window.mainloop()

def show_page(to_show):
    for page_id in pages:
        pages[page_id].lower()
    pages[to_show].lift()

def create_splash_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('splash.jpeg')
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Title
    title = tk.Label(background, text='Our Game', background=back_color, foreground=fore_color, font=(title_font_name, 42))
    width = screen_width // 7
    title.place(in_=background, x = screen_width // 2 - width // 2, y = screen_height // 10, width = width)

    #Start
    start = tk.Button(background, text='Begin Quest!', command=on_start, background=back_color, foreground=fore_color, font=(title_font_name, 23))
    width = screen_width // 7
    start.place(in_=background, x = screen_width // 3 - width // 2, y = 3 * screen_height // 4, width = width)

    #How to Play
    howto = tk.Button(background, text='Training Grounds', command=on_howto, background=back_color, foreground=fore_color, font=(title_font_name, 23))
    width = screen_width // 7
    howto.place(in_=background, x = screen_width // 2 - width // 2, y = 2 * screen_height // 3, width = width)

    #Exit
    leave = tk.Button(background, text="Cowards' Way Out", command=on_leave, background=back_color, foreground=fore_color, font=(title_font_name, 23))
    width = screen_width // 7
    leave.place(in_=background, x = 2 * screen_width // 3 - width // 2, y = 3 * screen_height // 4, width = width)

    return page

def create_howto_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    return page

def create_game_intro_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('splash.jpeg')
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Text
    src = 'opening.txt'
    text = load_text_asset(src)
    width = 4 * screen_width // 5
    label = tk.Label(background, text=text, wraplength=width, background=back_color, foreground = fore_color, anchor='w', font=(common_font_name, 17))
    label.place(in_=background, x = screen_width // 2 - width // 2, y = 5 * screen_height // 10, width = width, height = 3 * screen_height // 10)
    
    more = True
    width = screen_width // 10
    file_base_name = src.split('.')[0]
    try:
        text, file_name = load_text_options_asset(file_base_name + '.1.txt')
        btn1 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(common_font_name, 17))
        btn1.place(in_=background, x = screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
    except:
            more = False

    if more:
        try:
            text, file_name = load_text_options_asset(file_base_name + '.2.txt')
            btn2 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(common_font_name, 17))
            btn2.place(in_=background, x = 2 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        except:
            more = False

    if more:
        try:
            text, file_name = load_text_options_asset(file_base_name + '.3.txt')
            btn3 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(common_font_name, 17))
            btn3.place(in_=background, x = 3 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        except:
            more = False

    if more:
        try:
            text, file_name = load_text_options_asset(file_base_name + '.4.txt')
            btn2 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(common_font_name, 17))
            btn2.place(in_=background, x = 2 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        except:
            more = False
    
    
    text = load_text_asset('temp.1.txt')
    btn4 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(common_font_name, 17))
    btn4.place(in_=background, x = 4 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)

    return page

def on_start():
    show_page('game_intro')

def on_howto():
    show_page('howto')

def on_leave():
    sys.exit(0)

if __name__ == '__main__':
    main()