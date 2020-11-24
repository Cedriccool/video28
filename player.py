# pip3 install python-vlc
import RPi.GPIO as GPIO
import io
import sys
import os
import subprocess
from subprocess import Popen
import time
import vlc

minDistance = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 20
GPIO_ECHO = 21

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

movie1 = ("/home/pi/Python/video28/movie1.mp4")
movie2 = ("/home/pi/Python/video28/movie2.mp4")


#Instance = vlc.Instance('--fullscreen')
Instance = vlc.Instance()
player = Instance.media_player_new()
player.toggle_fullscreen()
Media = Instance.media_new(movie2)
Media.get_mrl()
player.set_media(Media)


last_state1 = True
last_state2 = True

input_state1 = True
input_state2 = True
quit_video = True

isPlaying = False


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance


while True:
    dist = distance()
    print("Measured Distance = %.1f cm" % dist)

    if(dist < minDistance and isPlaying == False):  # we play video
        #os.system('killall omxplayer.bin')
        #omxc = Popen(['omxplayer', '-b', movie1])
        print('OK PLAY')
        # player.play()

        subprocess.call(['vlc', movie2, '--play-and-exit', '--fullscreen'])

        isPlaying = True
        # time.sleep(51)
        time.sleep(2)
        while player.is_playing():
            time.sleep(1)

    time.sleep(0.4)

'''
while True:
    #Read states of inputs
    input_state1 = GPIO.input(17)
    input_state2 = GPIO.input(18)
    quit_video = GPIO.input(24)

    #If GPIO(17) is shorted to Ground
    if input_state1 != last_state1:
        if (player and not input_state1):
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', movie1])
            player = True
        elif not input_state1:
            omxc = Popen(['omxplayer', '-b', movie1])
            player = True

    #If GPIO(18) is shorted to Ground
    elif input_state2 != last_state2:
        if (player and not input_state2):
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', movie2])
            player = True
        elif not input_state2:
            omxc = Popen(['omxplayer', '-b', movie2])
            player = True

    #If omxplayer is running and GIOP(17) and GPIO(18) are not shorted to Ground
    elif (player and input_state1 and input_state2):
        os.system('killall omxplayer.bin')
        player = False

    #GPIO(24) to close omxplayer manually - used during debug
    if quit_video == False:
        os.system('killall omxplayer.bin')
        player = False

    #Set last_input states
    last_state1 = input_state1
    last_state2 = input_state2

'''
