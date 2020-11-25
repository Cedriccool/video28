import vlc
import sys
import RPi.GPIO as GPIO
import os
import pathlib
from threading import Timer, Thread, Event
import time
import platform
import dist

print(' globals.minDistance')
print(dist.minDistance)

global minDistance, distance, currentVideo
distance = 1000000
minDistance = 30


if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename


GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


GPIO_TRIGGER = 7
GPIO_ECHO = 11

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


video = "/home/pi/Python/video28/movie1.mp4"
video2 = "/home/pi/Python/video28/jingle.mp4"
video_temp = "/home/pi/Python/video28/temp.mp4"

currentVideo = ''


class ttkTimer(Thread):

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters


class Player(Tk.Frame):
    global minDistance, distance, currentVideo, isCached, cachePosx

    distance = 10000000
    isCached = True

    cachePosx = 2000  # root.winfo_screenwidth()  # 450

    def pressedRight(self, event):
        print("pressedRight")
        _quit()

    def pressedOne(self, event):
        print("pressedOne")
        self.blackFrame.place(x=0)
        self.OnOpenB()

    def pressedTwo(self, event):
        print("pressedTwo")
        _quit()

    def __init__(self, parent, title=None):
        global minDistance, isCached

        isCached = True

        self.lastValue = ''
        Tk.Frame.__init__(self, parent)

        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="white", background="white")

        self.player = None
        self.videopanel = ttk.Frame(self.parent, style="BW.TLabel")

        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        self.videopanel.bind("<Button-1>", self.pressedOne)
        self.videopanel.bind("<Button-3>", self.pressedRight)
        self.videopanel.bind("<Double-Button-1>", self.pressedTwo)

        ctrlpanel = ttk.Frame(self.parent, style="BW.TLabel")
        loadB = ttk.Button(ctrlpanel, text="LoadTemp", command=self.OnLoadB)

        self.blackFrame = ttk.Frame(self.parent, style="BW.TLabel")
        self.blackFrame.place(
            x=0, y=0, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        # temp
        # self.blackFrame.place(x=6000)

        self.blackFrame.bind("<Button-1>", self.pressedOne)
        self.blackFrame.bind("<Button-3>", self.pressedRight)

        loadB.pack(side=Tk.LEFT)

        ctrlpanel2 = ttk.Frame(self.parent, style="BW.TLabel")
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
        self.timeslider_last_update = time.time()

        # VLC player controls
#        self.Instance = vlc.Instance('--no-xlib --verbose=0')
        self.Instance = vlc.Instance('--verbose=0')
        self.player = self.Instance.media_player_new()
        self.player.audio_set_volume(100)
        self.player.video_set_scale(0)
        # self.player.toggle_fullscreen()
        self.player.set_fullscreen(True)
        self.player.video_set_aspect_ratio('16:9')

        # var mediaOptions = new string[] {"input-repeat=-1"};

        # self.player.SetMedia(new FileInfo(MediaFile), mediaOptions);

        # self.player.video_set_deinterlace('on')

        # below is a test, now use the File->Open file menu
        media = self.Instance.media_new(video)
        self.player.set_media(media)

        self.timer = ttkTimer(self.OnTimer, 1)
        self.timer.start()
        self.parent.update()

    def OnExit(self, evt):
        self.Close()

    def getDistance(self):
        # return 500

        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance

    def checkDistance(self):
        global distance
        distance = self.getDistance()

        #root.after(500, self.checkDistance)

    def OnOpenB(self):
        global currentVideo, isCached
        isCached = True
        self.OnStop()

        fullname = video2  # == jingle
        currentVideo = fullname

        if os.path.isfile(fullname):
            print(fullname)
            splt = os.path.split(fullname)
            dirname = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            # Creation
            self.Media = self.Instance.media_new(
                str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)

            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                # this line messes up windows
                self.player.set_xwindow(self.GetHandle())
            # FIXME: this should be made cross-platform
            self.OnPlay()

            # self.volslider.set(self.player.audio_get_volume())

    def OnOpen(self):
        global currentVideo, isCached
        isCached = True
        self.OnStop()

        fullname = video_temp
        currentVideo = fullname

        if os.path.isfile(fullname):
            print(fullname)
            splt = os.path.split(fullname)
            dirname = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            # Creation
            self.Media = self.Instance.media_new(
                str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)

            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                # this line messes up windows
                self.player.set_xwindow(self.GetHandle())
            # FIXME: this should be made cross-platform
            self.OnPlay()

            # self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):

        if not self.player.get_media():
            self.OnOpen()
        else:
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    # def OnPause(self, evt):
    def OnPause(self):
        self.player.pause()

    def OnStop(self):
        self.player.stop()
        # reset the time slider
        self.timeslider.set(0)

    def OnTimer(self):
        global isCached

        if self.player == None:
            return

        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"

        self.checkDistance()

        #print(str(distance) + " / " + str(minDistance))
        print(tyme)

        if(tyme > 11000 and currentVideo == '/home/pi/Python/video28/temp.mp4' and isCached == False):
            isCached = True
            self.blackFrame.place(x=0)
            # self.OnLoad()

        # if(tyme > 900 and isCached == True and tyme < 6000):
        if(tyme > 740 and tyme < 6000):
            isCached = False
            self.blackFrame.place(x=cachePosx)

        print("distance: " + str(distance) + " / " + str(dist.minDistance))

        if(distance < dist.minDistance and currentVideo == '/home/pi/Python/video28/temp.mp4'):
            print("NEW PLAY DISTANCE")
            isCached = True
            self.blackFrame.place(x=0)
            self.OnLoadB()

        # if(tyme > 700 and isCached == True):
        #    print("NEW PLAY")
        #    isCached = True
        #    self.blackFrame.place(x=0)
        #    self.OnLoad()

        if(tyme == self.lastValue):
            print("NEW PLAY")
            #isCached == True
            isCached = True
            self.blackFrame.place(x=0)
            self.OnLoad()
        # if(tyme == self.lastValue):
        #    print("NEW PLAY")
        #    isCached = True
        #    self.blackFrame.place(x=0)
        #    # self.blackFrame.place(x=6000)
        #    self.OnLoad()

        self.lastValue = tyme

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:

            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval))  # expects milliseconds

    def OnLoad(self):
        self.OnOpen()
        return

    def OnLoadB(self):
        self.OnOpenB()
        return

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = Tk.messageBox.showerror(self, 'Error', errormessage)


def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):  # (1)
        Tk_get_root.root = Tk.Tk()  # initialization call is inside the function
    return Tk_get_root.root


def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)


def onKeyPress(event):
    print('You pressed %s\n' % (event.char, ))


if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.protocol("WM_DELETE_WINDOW", _quit)
    root.configure(background='#000000')
    root. attributes('-type', 'dock')

    height = round(9 * screen_width / 16)

    top = round(screen_height - height / 2)
    print('TOP: ' + str(top))
    #root.attributes("-fullscreen", True)
    root.geometry(str(screen_width)+"x"+str(height)+"+0+0")

    root.bind('<KeyPress>', onKeyPress)

    root.configure(bg='white')

    player = Player(root, title="tkinter vlc")
    # show the player window centwhite and run the application

    #root.after(1000, player.checkDistance)
    root.mainloop()
