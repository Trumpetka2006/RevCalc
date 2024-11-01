#!/usr/bin/env python3


from operator import index
from os.path import basename, splitext, isfile
import tkinter as tk
from tkinter import LEFT, RIGHT, TOP, END
from datetime import datetime
import token
from operations import operation2
# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        
        font_settings = ("Helvetica", 14)
        self.option_add("*Font", font_settings)

        if not "textvariable" in kw:
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

class MyListbox(tk.Listbox):
    def pop(self):
        if self.size() > 0:
            x = self.get(END)
            self.delete(END)
            return x
        else:
            raise IndexError

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
    name = "RPNCalc"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.lbl = tk.Label(master=self,text="Reverzní Kalkukačka")
        self.listbox = MyListbox(master=self)
        self.btn = tk.Button(self, text="Destroy", command=self.destroy)
        self.entry = MyEntry(self)
        self.entry.bind("<Return>",func=self.enterHandler)
        
        self.lbl.pack()
        self.listbox.pack()
        self.entry.pack()
        self.btn.pack()

    def enterHandler(self, event):
        for toke in self.entry.value.split():
            try:
                self.listbox.insert(END,float(toke))
            except ValueError:
                self.tokenProcess(str(toke))
        self.listbox.see(END)
        #print(self.listbox.pop())
        self.entry.value = ""
        pass
    
    def tokenProcess(self,token):
        token = token.strip()
        print(token)
        if token in operation2 and self.listbox.size()>1:
            x = float(operation2[token](self.listbox.pop(), self.listbox.pop()))
            self.listbox.insert(END, x)
        match token:
            case "del" if self.listbox.size()>0:
                self.listbox.delete(END)
    def addition(self):
        self.listbox.insert(END,float(self.listbox.pop()+self.listbox.pop()))
    def subtraction(self):
        self.listbox.insert(END, float(self.listbox.pop() - self.listbox.pop()))
    def multiplication(self):
        self.listbox.insert(END, float(self.listbox.pop() * self.listbox.pop()))
    def division(self):
        try:
            self.listbox.insert(END, float(self.listbox.pop() / self.listbox.pop()))
        except ValueError:
            pass
app = Application()
app.mainloop()

