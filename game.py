import tkinter as tk
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
container = None

def main():
    global screen_width, screen_height, container

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
    load_pages()

    #Place pages in container such that all have the same relative size (ie, none show out from under others)
    for page_id in pages:
        pages[page_id].place(in_=container, relwidth=1, relheight=1)

    #Start on the consent page
    show_page('splash')

    #Start GUI Loop--control now in the hands of the UI
    window.mainloop()

def load_pages():
    #One-offs
    pages['splash'] = create_splash_page(container, width=screen_width, height=screen_height)
    pages['howto'] = create_howto_page(container, width=screen_width, height=screen_height)
    pages['end'] = create_end_page(container, width=screen_width, height=screen_height)

    #All screens in game
    screens = description_text_files()
    for screen_name in screens:
        pages[screen_name] = create_game_text_page(container, screen_name, width=screen_width, height=screen_height)

def show_page(to_show):
    for page_id in pages:
        pages[page_id].lower()
    pages[to_show].lift()
    print(to_show)

def create_splash_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('splash.jpg')
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

def create_game_text_page(container, file_base_name, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    try:
        background_image = load_image_asset(file_base_name + '.jpg')
    except:
        background_image = load_image_asset('temp.jpg')
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Text
    src = file_base_name + '.txt'
    text = load_text_asset(src)
    width = 4 * screen_width // 5
    label = tk.Label(background, text=text, wraplength=width, background=back_color, foreground = fore_color, anchor='w', font=(common_font_name, 17))
    label.place(in_=background, x = screen_width // 2 - width // 2, y = 5 * screen_height // 10, width = width, height = 3 * screen_height // 10)
    
    more = True
    width = .19 * screen_width
    file_base_name = src.split('.')[0]
    try:
        text1, file_name1 = load_text_options_asset(file_base_name + '.1.txt')
        btn1 = tk.Button(background, text=text1, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name1))
        btn1.place(in_=background, x = screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
    except:
        more = False

    if not more:
        show_page('end')

    if more:
        try:
            text2, file_name2 = load_text_options_asset(file_base_name + '.2.txt')
            btn2 = tk.Button(background, text=text2, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name2))
            btn2.place(in_=background, x = 2 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        except:
            more = False

    if more:
        try:
            text3, file_name3 = load_text_options_asset(file_base_name + '.3.txt')
            btn3 = tk.Button(background, text=text3, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name3))
            btn3.place(in_=background, x = 3 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        except:
            more = False

    if more:
        try:
            text4, file_name4 = load_text_options_asset(file_base_name + '.4.txt')
            btn4 = tk.Button(background, text=text4, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name4))
            btn4.place(in_=background, x = 4 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        except:
            more = False

    return page

def create_end_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    return page

def on_start():
    show_page('zz_temp')

def on_howto():
    show_page('howto')

def on_leave():
    sys.exit(0)

def on_option(file_name):
    pages[file_name] = create_game_text_page(container, file_name, width=screen_width, height=screen_height)
    show_page('howto')

if __name__ == '__main__':
    main()