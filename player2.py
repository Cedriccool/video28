# pip3 install python-vlc
import RPi.GPIO as GPIO
import io
import sys
import os
import subprocess
from subprocess import Popen
import time
import vlc


def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, bg='black')
    self.settings = {  # Inizialazing dictionary settings
        "width": 1024,
        "height": 576
    }
    self.settings.update(kwargs)  # Changing the default settings
    # Open the video source |temporary
    self.video_source = _path_+'asd.mp4'

    # Canvas where to draw video output
    self.canvas = Canvas(
        self, width=self.settings['width'], height=self.settings['height'], bg="black", highlightthickness=0)
    self.canvas.pack()

    # Creating VLC player
    self.instance = vlc.Instance()
    self.player = self.instance.media_player_new()


def GetHandle(self):
    # Getting frame ID
    return self.winfo_id()


def play(self, _source):
    # Function to start player from given source
    Media = self.instance.media_new(_source)
    Media.get_mrl()
    self.player.set_media(Media)

    # self.player.play()
    self.player.set_hwnd(self.GetHandle())
    self.player.play()
