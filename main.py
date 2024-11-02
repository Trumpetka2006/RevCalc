#!/usr/bin/env python3

from doctest import master
from os.path import basename, splitext, isfile
import tkinter as tk
from tkinter import LEFT, RIGHT, TOP, END, X, W
from datetime import datetime
from turtle import back
from operations import operation2
# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        font_settings = ("Helvetica", 20)
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

        self.history = []
        self.history_pos = 0

        self.title(self.name)
        self.lbl = tk.Label(
            master=self, text="Reverzní Kalkukačka", font="Helvetica 15", pady=10
        )
        self.listbox = MyListbox(master=self, font="Helvetica 22")
        self.btn = tk.Button(self, text="Destroy", command=self.destroy)
        self.entry = MyEntry(self)
        self.stateframe = tk.Frame(master=self, height=10)
        self.state = tk.Label(
            self,
            text="STATUS",
            background="green",
            anchor=W,
            justify=LEFT,
            padx=5,
            pady=5,
            font="Helvetica 12",
        )
        self.entry.bind("<Return>", func=self.enterHandler)
        self.entry.bind("<Up>", func=self.historyBack)
        self.entry.bind("<Down>", func=self.historyForward)

        self.lbl.pack()
        self.listbox.pack()
        self.entry.pack(fill=X)
        self.btn.pack()
        self.stateframe.pack(fill=X)
        self.state.pack(fill=X, anchor=W)
        self.stateHandler("ok")

    def stateHandler(self, state, message=""):
        match state:
            case "ok":
                self.state.configure(bg="cyan", text=f"OK: {message}")
            case "warn":
                self.state.configure(bg="yellow", text=f"WARNING: {message}")
            case "error":
                self.state.configure(bg="red", text=f"ERROR: {message}")

    def historyBack(self, event):
        print(self.history)
        print(self.history_pos)
        lenght = self.history.__len__() - 1
        if lenght + self.history_pos > 0:
            self.history_pos -= 1
            self.stateHandler("ok")
        else:
            self.stateHandler("warn", "Historie neexistuje.")
        self.entry.value = self.history[lenght + self.history_pos]

    def historyForward(self, event):
        print(self.history)
        print(self.history_pos, end="  ")
        lenght = self.history.__len__() - 1
        print(lenght + self.history_pos)
        self.entry.value = self.history[lenght + self.history_pos]
        if self.history_pos < 0:
            self.history_pos += 1
            self.stateHandler("ok")
        else:
            self.stateHandler("warn", "Historie neexistuje.")
        self.entry.value = self.history[lenght + self.history_pos]

    def enterHandler(self, event):
        self.stateHandler("ok")
        for toke in self.entry.value.split():
            try:
                self.listbox.insert(END, float(toke))
            except ValueError:
                self.tokenProcess(str(toke))
        self.listbox.see(END)
        if self.history.__len__() > 0:
            self.history.pop()

        self.history.append(self.entry.value)
        self.history.append("")
        self.entry.value = ""
        pass

    def tokenProcess(self, token):
        token = token.strip()
        print(token)
        if token in operation2 and self.listbox.size() > 1:
            b = self.listbox.pop()
            a = self.listbox.pop()
            try:
                x = float(operation2[token](a, b))
                self.listbox.insert(END, x)
                self.stateHandler("ok", f"{a} {token} {b}")
            except ZeroDivisionError:
                self.listbox.insert(END, a)
                self.listbox.insert(END, b)
                self.stateHandler("error", "Dělení nulou!")
            return
        elif token in operation2 and self.listbox.size() < 2:
            self.stateHandler("error", "Nedostatek čisel v zásobníku!")
            return
        match token:
            case "del":
                if self.listbox.size() > 0:
                    self.listbox.delete(END)
                    self.stateHandler("ok", "Zásobník smazán.")
                else:
                    self.stateHandler("error", "Nic nelze smazat!")
        if token not in ["del"]:
            self.stateHandler("error", "Neplatný token!")


app = Application()
app.mainloop()
