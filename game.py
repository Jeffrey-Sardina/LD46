import cv2
import tkinter as tk
from PIL import Image, ImageTk
import random
from utils import *
from player import Player

pages = {}

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
    pages['game'] = None

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
    consent_page = tk.Frame(container, *args, **kwargs)

    consent_text = load_text_asset('assets/consent.txt')

    consent_message = tk.Text(consent_page, width = 110, height = 20)
    consent_message.insert(tk.INSERT, consent_text)
    consent_message.config(state = 'disabled')
    consent_message.grid(row=0, column=0)

    consent_button = tk.Button(consent_page, text='I consent', command=on_consent)
    consent_button.grid(row=1, column=0)

    return consent_page

def main():
    pass

if __name__ == '__main__':
    main()