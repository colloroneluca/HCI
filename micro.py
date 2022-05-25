from tkinter import *
from PIL import Image, ImageTk


class MyLabel(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)



class microphone():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("+1400+200")
        self.root.overrideredirect(1)
        anim = MyLabel(self.root, 'micro.gif')
        anim.pack()
        self.root.after(100, self.check)
        self.root.mainloop()

    def check(self):
        f = open("thread_control.txt", "r")
        num = f.read()
        if num == "1":
            self.destroier()
        self.root.after(100, self.check)
    def destroier(self):
        print("destroing")
        try:
            self.root.destroy()
        except:
            print("destroying again")
            self.destroier()


if __name__ == "__main__":
    m = microphone()
