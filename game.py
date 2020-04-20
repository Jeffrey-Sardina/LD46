import tkinter as tk
from tkinter import font
import sys
from utils import *

#General global variable
pages = {}
tome = []
back_color = '#000000'
fore_color = '#00ff00'
tome_text_color = '#000000'
screen_width = 0
screen_height = 0
container = None
start_file = 'opening'
title_font_name = 'Old English Text MT'
common_font_name = 'Georgia'

#Player dadta
hp_tk = None
hp_prefix = 'Health: '
hp_val = 10

#Precompute this using meta.py before each build
hp_change_pages = {'afterdruidcommands': 0, 'atbaseoftree': 0, 'BASEstory': -1, 'beforethirdpuzzle': 0, 'branchtoentrance': 0, 'chaseafterdruid': 0, 'climbtree': 0, 'decaytome': 0, 'entermaindoor': 0, 'findtree': 0, 'firstpuzzle': 0, 'firstpuzzleright': 0, 'firstpuzzleutter': 0, 'firstpuzzlewrong': -1, 'hiketotree': 0, 'introduction': 0, 'maindooropen': 0, 'maindooropensforreal': 0, 'mouthdrop': 0, 'nobudge': 0, 'opening': 0, 'opentome': 0, 'scrapeblood': 0, 'secondpuzzle': 0, 'secondpuzzletokenright': 0, 'secondpuzzletokens': 0, 'secondpuzzleutter': 0, 'secondpuzzleutterall': 0, 'silentdoor': 0, 'thirdpuzzle': 0, 'thirdpuzzlefirsttileright': 0, 'thirdpuzzlefirsttilewrong': -1, 'tome': 0, 'training': 0, 'waitfordeath': 0, 'wordsondoor': 0, 'wormstome': 0}

def main():
    global screen_width, screen_height, container, hp_tk

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

    #Player data
    hp_tk = tk.StringVar()
    hp_tk.set(hp_prefix + str(hp_val))

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
    pages['howto'] = create_howto_page(container, 'training', width=screen_width, height=screen_height)
    pages['end'] = create_end_page(container, width=screen_width, height=screen_height)

    #All screens in game
    screens = description_text_files()
    for screen_name in screens:
        pages[screen_name] = create_game_text_page(container, screen_name, width=screen_width, height=screen_height)

def show_page(to_show):
    print(to_show)
    for page_id in pages:
        pages[page_id].lower()
    pages[to_show].lift()

def create_splash_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('splash.jpg', screen_width, screen_height)
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

def create_howto_page(container, file_base_name, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('training.jpg', screen_width, screen_height)
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Title
    title = tk.Label(background, text='Training Grounds', background=back_color, foreground=fore_color, font=(title_font_name, 42))
    width = 2 * screen_width // 7
    title.place(in_=background, x = screen_width // 2 - width // 2, y = screen_height // 10, width = width)

    #Main Text
    src = file_base_name + '.txt'
    text, _ = load_text_asset(src)
    width = 4 * screen_width // 5
    label = tk.Label(background, text=text, wraplength=width, background=back_color, foreground = fore_color, anchor='w', font=(common_font_name, 17))
    label.place(in_=background, x = screen_width // 2 - width // 2, y = 6 * screen_height // 10, width = width, height = 3 * screen_height // 10)

    #Back
    width = screen_width // 15
    text = 'Back'
    btn1 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(title_font_name, 17), wraplength=width, command=lambda:on_option('splash'))
    btn1.place(in_=background, x = 0, y = 9 * screen_height // 10, width=width, height = screen_height // 15)

    return page

def create_game_text_page(container, file_base_name, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset(file_base_name + '.jpg', screen_width, screen_height)
    if not background_image:
        background_image = load_image_asset('temp.jpg', screen_width, screen_height)
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Text
    src = file_base_name + '.txt'
    text, next_file = load_text_asset(src)
    width = 4 * screen_width // 5
    label = tk.Label(background, text=text, wraplength=width, background=back_color, foreground = fore_color, anchor='w', font=(common_font_name, 17))
    label.place(in_=background, x = screen_width // 2 - width // 2, y = 5 * screen_height // 10, width = width, height = 3 * screen_height // 10)

    #Player stats and UI (Health and Tome button)
    gen_player_controls(background)

    #Create button to move to a new page
    if next_file:
        gen_next_button(background, next_file)
    else:
        gen_game_buttons(page, background, src)

    return page

def gen_next_button(background, next_file):
    width = 0.19 * screen_width
    text = 'Continue'
    btn1 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(next_file))
    btn1.place(in_=background, x = screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)

def gen_game_buttons(page, background, src):
    #Fist button is a special case--we create it even if there are no options
    more = True
    width = 0.19 * screen_width
    file_base_name = src.split('.')[0]
    text1, file_name1 = load_text_asset(file_base_name + '.1.txt')
    command = lambda:on_option(file_name1)
    if not text1:
        text1 = 'End Game'
        more = False
        command = lambda:show_page('splash')

    btn1 = tk.Button(background, text=text1, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=command)
    btn1.place(in_=background, x = screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
    
    #Make the other buttons as long as there are options
    if more:
        text2, file_name2 = load_text_asset(file_base_name + '.2.txt')
        if text2:
            btn2 = tk.Button(background, text=text2, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name2))
            btn2.place(in_=background, x = 2 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        else:
            more = False

    if more:
        text3, file_name3 = load_text_asset(file_base_name + '.3.txt')
        if text3:
            btn3 = tk.Button(background, text=text3, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name3))
            btn3.place(in_=background, x = 3 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        else:
            more = False

    if more:
        text4, file_name4 = load_text_asset(file_base_name + '.4.txt')
        if text4:
            btn4 = tk.Button(background, text=text4, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name4))
            btn4.place(in_=background, x = 4 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        else:
            more = False

def gen_player_controls(background):
    #Health indicator
    health_width = screen_width // 15
    health_height = screen_height // 20
    label = tk.Label(background, textvariable=hp_tk, wraplength=health_width, background=back_color, foreground = fore_color, anchor='w', font=(common_font_name, 17))
    label.place(in_=background, x = 0, y = 0, width = health_width, height = health_height)

    #Tome button
    width = height = screen_width // 15
    image = load_image_asset('tome_icon.jpg', width, height)
    button = tk.Button(background, image=image, background=back_color, command=lambda:on_tome_button())
    button.image = image
    button.place(in_=background, x = 0, y=health_height, width=width, height=height)

def create_end_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('temp.jpg', screen_width, screen_height)
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    return page

def on_start():
    show_page(start_file)

def on_howto():
    show_page('howto')

def on_leave():
    sys.exit(0)

def on_option(file_name):
    global hp_val
    hp_val += hp_change_pages[file_name]
    hp_tk.set(hp_prefix + str(hp_val))
    show_page(file_name)

def on_tome_button():
    sub_window = tk.Toplevel()
    sub_window.wm_title("Druidic Tome")

    sub_container = tk.Frame(sub_window)
    sub_container.pack(side="top", fill="both", expand=True)

    tome_pages = tome_texts()
    for tome_page in sorted(tome_pages):
        tome.append(generate_tome_page(sub_container, tome_page))

    show_tome_page(0)

def generate_tome_page(sub_container, text, *args, **kwargs):
    page = tk.Frame(sub_container, *args, **kwargs)

    #Background image
    background_image = load_image_asset('paper.jpg', screen_width, screen_height)
    background = tk.Label(sub_container, text=text, image=background_image, compound=tk.CENTER, background=back_color, foreground = tome_text_color, font=(title_font_name, 27))
    background.image = background_image #Just to save the reference
    background.place(in_=sub_container, x=0, y=0, relwidth=1, relheight=1)

    return page

def show_tome_page(number):
    if number < len(tome):
        for tome_page in tome:
            tome_page.lower()
        tome[number].lift()

def on_tome_page_change():
    pass

if __name__ == '__main__':
    main()