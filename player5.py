# import external libraries
'''
mv ~/.config/pulse ~/.config/pulse.old
pulseaudio --start
'''
import vlc
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

# import standard libraries
import os
import pathlib
from threading import Timer, Thread, Event
import time
import platform

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


video = "/home/pi/Python/video28/movie1.mp4"
video2 = "/home/pi/Python/video28/jingle.mp4"
video_temp = "/home/pi/Python/video28/temp.mp4"

currentVideo = ''


class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        #print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            #print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

# def doit():
#    print("hey dude")

# code to demo ttkTimer
#t = ttkTimer(doit, 1.0)
# t.start()
# time.sleep(5)
#print("t.get= ", t.get())
# t.stop()
#print("timer should be stopped now")


class Player(Tk.Frame):

    def pressedOne(self, event):
        print("pressedOne")
        self.OnOpenB()

    def pressedTwo(self, event):
        print("pressedTwo")
        # exit()
        _quit()

    def __init__(self, parent, title=None):
        self.lastValue = ''
        Tk.Frame.__init__(self, parent)

        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")

        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent, style="BW.TLabel")
        # self.videopanel.config(bg="black")
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        #frame = ttk.Frame(root, width=1000, height=1000)

        self.videopanel.bind("<Button-1>", self.pressedOne)
        self.videopanel.bind("<Double-Button-1>", self.pressedTwo)

        ctrlpanel = ttk.Frame(self.parent, style="BW.TLabel")
        pause = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
        play = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
        stop = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
        load = ttk.Button(ctrlpanel, text="LoadMain", command=self.OnLoad)
        loadB = ttk.Button(ctrlpanel, text="LoadTemp", command=self.OnLoadB)

        # pause.pack(side=Tk.LEFT)
        # play.pack(side=Tk.LEFT)
        # stop.pack(side=Tk.LEFT)
        # load.pack(side=Tk.LEFT)
        loadB.pack(side=Tk.LEFT)

        ctrlpanel2 = ttk.Frame(self.parent, style="BW.TLabel")
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
        self.timeslider_last_update = time.time()

        # ctrlpanel.pack(side=Tk.BOTTOM)
        #ctrlpanel2.pack(side=Tk.BOTTOM, fill=Tk.X)

        # VLC player controls
        self.Instance = vlc.Instance('--no-xlib --verbose=0')
        self.player = self.Instance.media_player_new()
        self.player.audio_set_volume(100)
        self.player.video_set_scale(0)
        self.player.video_set_aspect_ratio('16:9')
        self.player.video_set_deinterlace('on')

        # self.player.set_fullscreen(True)

        # below is a test, now use the File->Open file menu
        media = self.Instance.media_new(video)
        self.player.set_media(media)
        # self.player.play()  # hit the player button
        # self.player.video_set_deinterlace(str_to_bytes('yadif'))

        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()

        # self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this

    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def OnOpenB(self):

        self.OnStop()

        fullname = video2
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
        """Update the time slider according to the current movie time.
        """
        if self.player == None:
            return

        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"

        print(str(tyme) + " / " + str(self.lastValue) + " : " + str(length))

        if(tyme == self.lastValue):
            print("NEW PLAY")
            self.OnLoad()

        self.lastValue = tyme

        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

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

    root.configure(bg='black')

    player = Player(root, title="tkinter vlc")
    # show the player window centred and run the application
    root.mainloop()
