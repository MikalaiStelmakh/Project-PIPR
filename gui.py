import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from ui_logomocja import UI


class MainWindow(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.ui = UI(master)
        self.initialValues()
        self.createImage()
        self.ui.entry.bind("<Return>", self.main)

    def createImage(self):
        self.image = Image.open('turtle.png')
        size = (self.image_height, self.image_width)
        self.ui.canvas_for_image.image = ImageTk.PhotoImage(
            self.image.resize(size),
            Image.ANTIALIAS)
        self.imagesprite = self.ui.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor='s',
            image=self.ui.canvas_for_image.image)

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
        size = (self.canvas_width, self.canvas_height)
        self.pil_image = Image.new('RGB', size, color='white')
        self.draw = ImageDraw.Draw(self.pil_image)
        self.commands_data = []

    def main(self, event):
        self.text = self.ui.entry.get()
        self.ui.label.config(text=self.text)
        self.ui.entry.delete(0, 'end')


def guiMain():
    root = tk.Tk()
    MainWindow(root)
    root.wm_title('Logomocja')
    root.mainloop()


if __name__ == "__main__":
    guiMain()
