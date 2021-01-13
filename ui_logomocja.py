import tkinter as tk
from menu import Menu


class UI(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, height=700, width=800)
        self.canvas.pack()
        self.createMenu()
        self.canvas_for_image = tk.Canvas(master, bg='white')
        self.canvas_for_image.place(
            relx=0.5,
            rely=0.5,
            width=700,
            height=525,
            anchor='center')
        self.canvas_for_image.update()
        self.label_frame = tk.Frame(master, borderwidth=2, relief="sunken")
        self.label_frame.place(rely=0.9, relwidth=1, relheight=0.07)
        self.label = tk.Label(
            self.label_frame,
            text='Hello\n',
            fg='black',
            font=("Modern", 10),
            justify='left',
            bd=4)
        self.label.pack(side='top', anchor='w')
        self.entry_frame = tk.Frame(master)
        self.entry_frame.place(rely=0.97, relwidth=1.1, relheight=0.03)
        self.entry = tk.Entry(self.entry_frame, bg='white', fg='black')
        self.entry.place(relwidth=1)

    def createMenu(self):
        menu_command = Menu(self)
        menu = tk.Menu(self.master)
        fileMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='New', command=menu_command.cleanUp)
        fileMenu.add_command(label='Open', command=menu_command.openFile)
        fileMenu.add_command(label='Save image as...',
                             command=menu_command.saveImage)
        fileMenu.add_command(label='Save txt', command=menu_command.saveTxt)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=menu_command.exit)
        self.master.config(menu=menu)
