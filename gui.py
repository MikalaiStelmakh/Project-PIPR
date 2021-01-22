import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
from ui import UI
from inputProcessing import InputProcessing


class MainWindow(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.ui = UI()
        self.ui.setupUi(master)
        self.createMenu()
        self.initialValues()
        self.createImage()
        # When the enter is pressed, the main function is called.
        self.ui.entry.bind("<Return>", self.main)

    # Creates an image at its original location.
    def createImage(self):
        size = (self.image_height, self.image_width)
        self.ui.image = Image.open('docs/turtle.png')
        self.ui.canvas_for_image.image = ImageTk.PhotoImage(
            self.ui.image.rotate(0, expand=True).resize(size),
            Image.ANTIALIAS)
        self.ui.imagesprite = self.ui.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor='s',
            image=self.ui.canvas_for_image.image)
        canvas_size = (self.canvas_width, self.canvas_height)
        # Creates an invisible image, which is needed to save the created image
        self.ui.pil_image = Image.new('RGB', canvas_size, color='white')
        self.ui.draw = ImageDraw.Draw(self.ui.pil_image)

    def createMenu(self):
        menu_command = Menu(self.ui, self)
        self.ui.fileMenu.add_command(label='New',
                                     command=menu_command.cleanUp)
        self.ui.fileMenu.add_command(label='Open',
                                     command=menu_command.openFile)
        self.ui.fileMenu.add_command(label='Save image as...',
                                     command=menu_command.saveImage)
        self.ui.fileMenu.add_command(label='Save txt',
                                     command=menu_command.saveTxt)
        self.ui.fileMenu.add_separator()
        self.ui.fileMenu.add_command(label='Exit', command=menu_command.exit)
        self.master.config(menu=self.ui.menu)

    # Values set at program start.
    def initialValues(self):
        self.canvas_width = self.ui.canvas_for_image.winfo_width()
        self.canvas_height = self.ui.canvas_for_image.winfo_height()
        self.image_width = int(self.canvas_width*0.05)
        self.image_height = int(self.canvas_height*0.05)
        # Sets the size of the picture relative to the size of the canvas.
        self.image_x = self.canvas_width*0.5
        self.image_y = self.canvas_height*0.5 + self.image_height/2
        self.new_image_x, self.new_image_y = self.image_x, self.image_y
        self.simple_angle = 0
        self.direction = 'N'
        self.previous_angle = 0
        self.is_up = False
        # List necessary to save the file in txt format from the menu.
        self.commands_data = []
        # Changes the value when opening a file from the menu.
        self.errors = 0

    def getInput(self):
        text = self.ui.entry.get()
        return text

    def main(self, event):
        self.text = self.getInput()
        self.commands_data.append(self.text)
        InputProcessing(self.ui, self, self.text)


class Menu:
    def __init__(self, ui, gui):
        self.ui = ui
        self.gui = gui

    # Clears the canvas, variables return to their original values.
    def cleanUp(self):
        self.ui.canvas_for_image.delete('all')
        self.ui.canvas_for_image.delete(self.ui.imagesprite)
        self.gui.initialValues()
        self.gui.createImage()
        self.ui.label.config(text='Hello')

    def openFile(self):
        file = filedialog.askopenfilename(filetypes=[('txt files', '*.txt')])
        if file:
            self.cleanUp()
            with open(file, 'r') as file_handle:
                for line in file_handle:
                    line = line.rstrip()
                    self.gui.text = line
                    self.gui.commands_data.append(self.gui.text)
                    InputProcessing(self.ui, self.gui, self.gui.text)
            errors = self.gui.errors
            # shows warning message if errors were found in the opened file
            if errors > 0:
                message = (
                    f'{errors} {"errors" if errors > 1 else "error"} '
                    'occured while opening the file'
                    )
                messagebox.showwarning('Warning', message)
            self.ui.label.config(text=file)

    def saveImage(self):
        filename = filedialog.asksaveasfilename(
            filetypes=(
                ('jpeg files', '*.jpg'),
                ('png files', '*.png'),
                ('gif files', '*.gif'),
                ('all types', '*.*')
            )
        )
        if filename:
            self.ui.pil_image.save(filename)

    def saveTxt(self):
        filename = filedialog.asksaveasfilename(
            filetypes=[('txt files', '*.txt')])
        if filename:
            with open(filename, 'w') as file_text:
                for command in self.gui.commands_data:
                    file_text.write(command + '\n')

    def exit(self):
        self.ui.master.destroy()
        self.ui.pil_image.close()


def guiMain():
    root = tk.Tk()
    MainWindow(root)
    root.wm_title('Logomocja')
    root.mainloop()


if __name__ == "__main__":
    guiMain()
