import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from ui_logomocja import UI
from menu import Menu
from InputProcessing import InputProcessing


class MainWindow(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.ui = UI()
        self.ui.setupUi(master)
        self.createMenu()
        self.initialValues()
        self.createImage()
        self.ui.entry.bind("<Return>", self.main)

    def createImage(self):
        size = (self.image_height, self.image_width)
        self.ui.image = Image.open('turtle.png')
        self.ui.canvas_for_image.image = ImageTk.PhotoImage(
            self.ui.image.resize(size),
            Image.ANTIALIAS)
        self.ui.imagesprite = self.ui.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor='s',
            image=self.ui.canvas_for_image.image)
        canvas_size = (self.canvas_width, self.canvas_height)
        self.ui.pil_image = Image.new('RGB', canvas_size, color='white')
        self.ui.draw = ImageDraw.Draw(self.ui.pil_image)

    def createMenu(self):
        menu_command = Menu(self.ui, self)
        self.ui.fileMenu.add_command(label='New', command=menu_command.cleanUp)
        self.ui.fileMenu.add_command(label='Open', command=menu_command.openFile)
        self.ui.fileMenu.add_command(label='Save image as...',
                                     command=menu_command.saveImage)
        self.ui.fileMenu.add_command(label='Save txt', command=menu_command.saveTxt)
        self.ui.fileMenu.add_separator()
        self.ui.fileMenu.add_command(label='Exit', command=menu_command.exit)
        self.master.config(menu=self.ui.menu)

    def initialValues(self):
        self.canvas_width = self.ui.canvas_for_image.winfo_width()
        self.canvas_height = self.ui.canvas_for_image.winfo_height()
        self.image_width = int(self.canvas_width*0.05)
        self.image_height = int(self.canvas_height*0.05)
        self.image_x = self.canvas_width*0.5
        self.image_y = self.canvas_height*0.5 + self.image_height/2
        self.new_image_x, self.new_image_y = self.image_x, self.image_y
        self.simple_angle = 0
        self.direction = 'N'
        self.previous_angle = 0
        self.is_up = False
        self.commands_data = []
        self.errors = 0

    def main(self, event):
        self.text = self.ui.entry.get()
        self.commands_data.append(self.text)
        InputProcessing(self.ui, self)


def guiMain():
    root = tk.Tk()
    MainWindow(root)
    root.wm_title('Logomocja')
    root.mainloop()


if __name__ == "__main__":
    guiMain()
