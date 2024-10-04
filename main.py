#!/usr/bin/env python3

from os.path import basename, splitext, isfile
import tkinter as tk
from tkinter import LEFT, RIGHT, TOP
from datetime import datetime
# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf:dict = None, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Color Mishmasher"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        self.copy_color = ""


        self.frameR = tk.Frame(self)
        self.frameG = tk.Frame(self)
        self.frameB = tk.Frame(self)

        self.memFrame = tk.Frame(self)


        self.lblR = tk.Label(self.frameR, text = "R")
        self.lblG = tk.Label(self.frameG, text = "G")
        self.lblB = tk.Label(self.frameB, text = "B")

        self.varTime = tk.StringVar()

        self.varTime = str(datetime.now())

        self.timeLabel = tk.Label(text ="")
        self.timeLabel.bind('<Button-1>', self.time_stop_handler)

        self.varR = tk.IntVar()
        self.varG = tk.IntVar()
        self.varB = tk.IntVar()

        self.scaleR = tk.Scale(self.frameR, from_=0, to=255, orient=tk.HORIZONTAL, length=255, command=self.update_color, variable=self.varR) 
        self.scaleG = tk.Scale(self.frameG, from_=0, to=255, orient=tk.HORIZONTAL, length=255, command=self.update_color, variable=self.varG) 
        self.scaleB = tk.Scale(self.frameB, from_=0, to=255, orient=tk.HORIZONTAL, length=255, command=self.update_color, variable=self.varB) 
        
        self.entryR = tk.Entry(self.frameR, width=3, textvariable=self.varR)
        self.entryG = tk.Entry(self.frameG, width=3, textvariable=self.varG)
        self.entryB = tk.Entry(self.frameB, width=3, textvariable=self.varB)

        self.canvas = tk.Canvas(self, background = "#000000", width=300)
        self.canvas.bind('<Button-1>', self.click_handler)
        
        self.loadBt = tk.Button(self, text="Nacist", command=self.color_load)
        self.qBt = tk.Button(self, text="Ukoncit", command=self.quit)

        self.timeLabel.pack()
        
        self.frameR.pack()
        self.frameG.pack()
        self.frameB.pack()
        
        self.lblR.pack(side=LEFT, anchor="s")
        self.scaleR.pack(side=RIGHT, anchor="s")
        self.entryR.pack(side=LEFT, anchor="s")
        self.lblG.pack(side=LEFT, anchor="s")
        self.scaleG.pack(side=RIGHT)
        self.entryG.pack(side=RIGHT, anchor="s")
        self.lblB.pack(side=LEFT, anchor="s")
        self.scaleB.pack(side=RIGHT)
        self.entryB.pack(side=RIGHT, anchor="s")   

        self.canvas.pack(fill="both")

        self.memFrame.pack (side=TOP, fill="both")

        self.loadBt.pack()
        self.qBt.pack()

        self.canvaslist=[]
        for row in range(3):
            for col in range(7):
                canvas = tk.Canvas(self.memFrame, width=50, height=50, bg="#12abc3")
                canvas.grid(row=row, column=col)
                canvas.bind("<Button-1>", self.click_handler)
                self.canvaslist.append(canvas)

        self.color_load()
        self.time_step()
 
    def click_handler(self, event):
        if self.cget('cursor') != 'pencil':
            self.config(cursor='pencil')
            self.copy_color = event.widget.cget('background')
        else:
            self.config(cursor='')
            if event.widget is self.canvas:
                self.varR.set(int(self.copy_color[1:3],16))
                self.varG.set(int(self.copy_color[3:5],16))
                self.varB.set(int(self.copy_color[5:],16))
                self.update_color()
            else:
                event.widget.config(background = self.copy_color)
        

    def about(self):
        window = About(self)
        window.grab_set()

    def time_step(self):
        current_time = str(datetime.now())
        self.varTime = current_time
        self.timeLabel.config(text=current_time)
        self.timeID = self.after(1000, self.time_step)

    def time_stop_handler(self, event):
        if self.timeID != None:
            self.timeID = None
            print("stop")
        else:
            print("run")
            self.timeID = self.after(1000, self.time_step)

    def update_color(self, event=None):
        red = self.scaleR.get()
        blue = self.scaleB.get()
        green = self.scaleG.get()
        self.canvas.config(background = f"#{red:02X}{green:02X}{blue:02X}")

    def color_load(self):
        if isfile("colors.txt"):
            with open('colors.txt', 'r') as file:
                for widgets in self.canvaslist:
                    widgets.config(background = file.readline()[:7])
                self.canvas.config(background = file.readline()[:7])

        else:
           print("No save found!") 

    def color_save(self):
        with open('colors.txt', 'w') as file:
            for widgets in self.canvaslist:
                file.write(widgets.cget('background') + "\n")
            file.write(self.canvas.cget('background'))
            file.close()
            print("OK")
    
    def quit(self, event=None):
        print("Konec")
        self.color_save()
        super().quit()
    def destroy(self) -> None:
        print("Saving progress...", end="")
        self.color_save()
        return super().destroy()


app = Application()
app.mainloop()

