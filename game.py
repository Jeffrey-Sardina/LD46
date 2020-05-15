import tkinter as tk
from tkinter import font
import sys
from utils import *

#General global variable
pages = {}
back_color = '#000000'
fore_color = '#00ff00'
tome_text_color = '#000000'
screen_width = 0
screen_height = 0
container = None
start_file = 'opening'
title_font_name = 'Old English Text MT'
common_font_name = 'Georgia'
tome_created = False
sub_window = None #Window for time
tome_text = None
tome_idx = 0
tome_pages = None

#Player dadta
hp_tk = None
hp_prefix = 'Health: '
hp_val = 10
starting_hp = 10

#Precompute this using meta.py before each build
hp_change_pages = {'afterdruidcommands': 0, 'atbaseoftree': 0, 'BASEstory': -1, 'beforethirdpuzzle': 0, 'branchtoentrance': 0, 'chantwords': 0, 'chaseafterdruid': 0, 'climbtree': 0, 'decaytome': 0, 'dodobarrel': 0, 'dodoburnt': 0, 'dododoor': 0, 'dodotunnel': 0, 'entermaindoor': 0, 'falltodeath': 0, 'findtree': 0, 'finishthirdpuzzle': 0, 'firstpuzzle': 0, 'firstpuzzleright': 0, 'firstpuzzleutter': 0, 'firstpuzzlewrong': -1, 'flamestrap': -2, 'fourthpuzzle': 0, 'hackbarrel': 0, 'haifnix': 0, 'hiketotree': 0, 'introduction': 0, 'magai': 0, 'maindooropen': 0, 'maindooropensforreal': 0, 'mouthdrop': 0, 'nobudge': 0, 'openbarrel': 1, 'opening': 0, 'opentome': 0, 'raisechalice': 0, 'scrapeblood': 0, 'secondpuzzle': 0, 'secondpuzzletokenright': 0, 'secondpuzzletokens': 0, 'secondpuzzletokenwrong': -1, 'secondpuzzleutter': 0, 'secondpuzzleutterall': 0, 'shexgozh': 0, 'silentdoor': 0, 'slide': 0, 'standbarrel': 0, 'thirdpuzzle': 0, 'thirdpuzzlefirsttileright': 0, 'thirdpuzzlefirsttilewrong': -1, 'thirdpuzzlefourthtile': 0, 'thirdpuzzlesecondtile': 0, 'thirdpuzzlesecondtileright': 0, 'thirdpuzzlesecondtilewrong': -2, 'thirdpuzzlethirdtile': 0, 'thirdpuzzlethirdtileright': 0, 'thirdpuzzlethirdtilewrong': -3, 'tome': 0, 'tome_entry_01': 0, 'tome_entry_02': 0, 'tome_entry_03': 0, 'tome_entry_04': 0, 'tome_entry_05': 0, 'tome_entry_06': 0, 'tome_entry_07': 0, 'tome_entry_08': 0, 'tome_entry_09': 0, 'tome_entry_10': 0, 'training': 0, 'waitfordeath': 0, 'whattowalkto': 0, 'wingame': 0, 'wingame2': 0, 'wordsondoor': 0, 'wormstome': 0}

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

    #Start on the splash page
    show_page('splash')

    #Start GUI Loop--control now in the hands of the UI
    window.mainloop()

def load_pages():
    #One-offs
    pages['splash'] = create_splash_page(container, width=screen_width, height=screen_height)
    pages['howto'] = create_howto_page(container, 'training', width=screen_width, height=screen_height)
    pages['die'] = create_die_page(container, width=screen_width, height=screen_height)

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
    title = tk.Label(background, text='The Tome of the Ccaizhdi', background=back_color, foreground=fore_color, font=(title_font_name, 42))
    width = screen_width // 3
    title.place(in_=background, x = screen_width // 2 - width // 2, y = screen_height // 10, width = width)

    #Start Button
    start_command = lambda:on_option(start_file)
    start = tk.Button(background, text='Begin Quest!', command=start_command, background=back_color, foreground=fore_color, font=(title_font_name, 23))
    width = screen_width // 7
    start.place(in_=background, x = screen_width // 3 - width // 2, y = 3 * screen_height // 4, width = width)

    #How to Play Button
    howto = tk.Button(background, text='Training Grounds', command=on_howto, background=back_color, foreground=fore_color, font=(title_font_name, 23))
    width = screen_width // 7
    howto.place(in_=background, x = screen_width // 2 - width // 2, y = 2 * screen_height // 3, width = width)

    #Exit Button
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
    src = file_base_name + '.json'
    text = load_json_text_asset(src)['text']
    width = 4 * screen_width // 5
    label = tk.Label(background, text=text, wraplength=width, background=back_color, foreground = fore_color, anchor='w', font=(common_font_name, 17))
    label.place(in_=background, x = screen_width // 2 - width // 2, y = 6 * screen_height // 10, width = width, height = 3 * screen_height // 10)

    #Back
    width = screen_width // 15
    text = 'Back'
    btn1 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(title_font_name, 17), wraplength=width, command=lambda:on_option('splash'))
    btn1.place(in_=background, x = 0, y = 9 * screen_height // 10, width=width, height = screen_height // 15)

    return page

def create_game_text_page(container, file_base_name, data = None, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset(file_base_name + '.jpg', screen_width, screen_height)
    if not background_image:
        background_image = load_image_asset('temp.jpg', screen_width, screen_height)
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Text
    src = file_base_name + '.json'
    if not data:
        data = load_json_text_asset(src)
        text = data['text']
        next_file = data['next_file']

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
    data1 = load_json_text_asset(file_base_name + '.1.json')
    if data1:
        text1 = data1['text']
        file_name1 = data1['next_file']
        command = lambda:on_option(file_name1)
    else:
        text1 = 'End Game'
        more = False
        command = lambda:show_page('splash')

    btn1 = tk.Button(background, text=text1, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=command)
    btn1.place(in_=background, x = screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
    
    #Make the other buttons as long as there are options
    if more:
        data2 = load_json_text_asset(file_base_name + '.2.json')
        if data2:
            text2 = data2['text']
            file_name2 = data2['next_file']
            btn2 = tk.Button(background, text=text2, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name2))
            btn2.place(in_=background, x = 2 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        else:
            more = False

    if more:
        data3 = load_json_text_asset(file_base_name + '.3.json')
        if data3:
            text3 = data3['text']
            file_name3 = data3['next_file']
            btn3 = tk.Button(background, text=text3, background=back_color, foreground = fore_color, font=(common_font_name, 17), wraplength=width, command=lambda:on_option(file_name3))
            btn3.place(in_=background, x = 3 * screen_width // 5 - width // 2, y = 8 * screen_height // 10, width = width, height = 1 * screen_height // 10)
        else:
            more = False

    if more:
        data4 = load_json_text_asset(file_base_name + '.4.json')
        if data4:
            text4 = data4['text']
            file_name4 = data4['next_file']
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

def create_die_page(container, *args, **kwargs):
    page = tk.Frame(container, *args, **kwargs)

    #Background
    background_image = load_image_asset('die.jpg', screen_width, screen_height)
    background = tk.Label(page, image=background_image, background=back_color)
    background.image = background_image #Just to save the reference
    background.place(in_=page, x=0, y=0, relwidth=1, relheight=1)

    #Title
    title = tk.Label(background, text='You lose', background=back_color, foreground=fore_color, font=(title_font_name, 42))
    width = 2 * screen_width // 7
    title.place(in_=background, x = screen_width // 2 - width // 2, y = screen_height // 10, width = width)

    #Back
    width = screen_width // 15
    text = 'Quit'
    btn1 = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(title_font_name, 17), wraplength=width, command=lambda:on_option('splash'))
    btn1.place(in_=background, x = 0, y = 9 * screen_height // 10, width=width, height = screen_height // 15)

    return page

def on_howto():
    show_page('howto')

def on_leave():
    sys.exit(0)

def on_option(file_name):
    '''
    Called when the user pressed one of the options buttons.
    Loads the screen corresponding to that options and displays it

    file name: (str) the name of the new page, which is the same as its associated file
    '''
    global hp_val
    page_data = load_json_text_asset(file_name + '.json')
    alive = True
    if page_data:
        alive = change_health(page_data['health_change'])
    if alive:
        if not file_name in pages:
            pages[file_name] = create_game_text_page(container, file_name, width=screen_width, height=screen_height)
            pages[file_name].place(in_=container)
        show_page(file_name)
    else:
        show_page('die')

def change_health(health_change):
    '''
    Change health by the given amount
    Reutrn True if h > 0, else False
    '''
    global hp_val
    hp_val += health_change
    hp_val = min(hp_val, starting_hp)
    hp_val = max(hp_val, 0)
    hp_tk.set(hp_prefix + str(hp_val))

    if hp_val == 0:
        return False
    return True

def on_tome_button():
    global tome_created, sub_window, tome_text, tome_pages
    if not tome_created:
        sub_window = tk.Toplevel()
        sub_window.wm_title("Druidic Tome")

        sub_window.geometry("%dx%d+0+0" % (screen_width // 3, screen_height // 3))

        tome_pages = tome_texts()
        tome_text = tk.StringVar()
        tome_text.set(tome_pages[tome_idx])

        #Background image
        background_image = load_image_asset('paper.jpg', screen_width, screen_height)
        background = tk.Label(sub_window, textvariable=tome_text, wraplength=screen_width // 3, image=background_image, compound=tk.CENTER, background=back_color, foreground = tome_text_color, font=(title_font_name, 27))
        background.image = background_image #Just to save the reference
        background.place(in_=sub_window, x=0, y=0, relwidth=1, relheight=1)

        #Arrows
        gen_left_arrow(background)
        gen_right_arrow(background)

        #Handle closing event:
        sub_window.protocol("WM_DELETE_WINDOW", on_tome_closing)

        tome_created = True
    else:
        sub_window.lift()

def on_tome_closing():
    global tome_created, sub_window
    tome_created = False
    sub_window.destroy()
    sub_window = None

def gen_left_arrow(background):
    text = '<'
    width = screen_width // 15
    height = screen_height // 15
    tome_left_arrow = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(title_font_name, 27), command=lambda:show_tome_page(tome_idx-1))
    tome_left_arrow.pack(side=tk.LEFT)

def gen_right_arrow(background):
    text = '>'
    width = screen_width // 15
    height = screen_height // 15
    tome_right_arrow = tk.Button(background, text=text, background=back_color, foreground = fore_color, font=(title_font_name, 27), command=lambda:show_tome_page(tome_idx+1))
    tome_right_arrow.pack(side=tk.RIGHT)

def show_tome_page(number):
    global tome_idx
    if number >= 0 and number < len(tome_pages):
        tome_idx = number
        tome_text.set(tome_pages[tome_idx])
    else:
        print('err: ', number)

if __name__ == '__main__':
    main()