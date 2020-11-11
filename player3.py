#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# zip -P password file.zip file
import os
import shutil
import vlc
import zipfile
import sys
from PIL import Image, ImageTk
from datetime import datetime
import pyudev
from tkinter import simpledialog, Tk, BOTH, IntVar, LEFT, messagebox
import tkinter.font as font
from tkinter.ttk import Frame, Label, Scale, Style
import threading
import usb.core
from glob import glob
from subprocess import check_output, CalledProcessError
from tkinter.filedialog import askopenfilename


if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


def quit_prog():
    sys.exit(0)


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def vp_start_gui():
    global val, w, root
    root = tk.Tk()
    # root.attributes("-fullscreen", True)
    top = Toplevel1(root)
    root.wm_attributes("-topmost", True)

    root.mainloop()


# w = None
def create_Toplevel1(rt, *args, **kwargs):
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    main_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


def restart():
    os.system("sudo shutdown -r now")


class Toplevel1(tk.Frame):
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'
        _fgcolor = '#000000'
        _compcolor = '#d9d9d9'
        _ana1color = '#d9d9d9'
        _ana2color = '#ececec'

        top.geometry("480x320")

        top.resizable(0, 0)
        top.title("AgriMusic, Give Music & Love")
        top.configure(background="#8bae52")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.video_source = "/home/pi/Python/video28/movie1.mp4"

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Canvas
        image = Image.open('/home/pi/Python/AgriMusic/assets/bg_update.png')
        image = image.resize((480, 320), Image.ANTIALIAS)
        background_image = ImageTk.PhotoImage(image)

        canvas = tk.Canvas(top, width=480, height=320,
                           bg="#333333", bd=0, highlightthickness=0)
        canvas.place(x=0, y=0, width=480, height=320)

        root.background_image = background_image
        canvas.create_image(0, 0, image=background_image, anchor="nw")

        canvas.update()

        def GetHandle(self):
            # Getting frame ID
            return self.winfo_id()

        def play(self, _source):
            # Function to start player from given source
            Media = self.instance.media_new(_source)
            Media.get_mrl()
            self.player.set_media(Media)

            # self.player.play()
            # self.player.set_hwnd(self.GetHandle())
            self.player.play()

        play(self, self.video_source)

        print("End creating the GUi\n")


if __name__ == '__main__':
    vp_start_gui()
