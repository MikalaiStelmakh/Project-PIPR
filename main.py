from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from InputProcessing import InputProcessing
from menu import Menu


class UI(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, height=700, width=800)
        self.canvas.pack()

        self.createMenu(self.master)

        self.canvas_for_image = tk.Canvas(master, bg='white')
        self.canvas_for_image.place(
            relx=0.5,
            rely=0.5,
            width=700,
            height=525,
            anchor='center')
        self.canvas_for_image.update()
        self.canvas_width = self.canvas_for_image.winfo_width()
        self.canvas_height = self.canvas_for_image.winfo_height()

        self.image_width = int(self.canvas_width*0.05)
        self.image_height = int(self.canvas_height*0.05)

        self.image = Image.open('turtle.png')

        self.initialValues()

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
        self.new_image_x, self.new_image_y = self.image_x, self.image_y
        self.entry.bind("<Return>", self.main)
        self.entry.place(relwidth=1)

    def initialValues(self):
        self.image_x = self.canvas_width*0.5
        self.image_y = self.canvas_height*0.5 + self.image_height/2
        self.simple_angle = 0
        self.direction = 'N'
        self.previous_angle = 0
        self.is_up = False
        self.canvas_for_image.image = ImageTk.PhotoImage(
            self.image.resize((self.image_height, self.image_width)),
            Image.ANTIALIAS)
        self.imagesprite = self.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor='s',
            image=self.canvas_for_image.image)
        size = (self.canvas_width, self.canvas_height)
        self.pil_image = Image.new('RGB', size, color='white')
        self.draw = ImageDraw.Draw(self.pil_image)
        self.commands_data = []

    def createMenu(self, master):
        menu_command = Menu(self)
        menu = tk.Menu(master)
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

    def main(self, event):
        self.result = self.entry.get()
        self.commands_data.append(self.result)
        InputProcessing(self)


root = tk.Tk()
ui = UI(root)
root.wm_title('Logomocja')
root.mainloop()
