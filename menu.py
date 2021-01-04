from tkinter import filedialog
from InputProcessing import InputProcessing

# TODO: save commands as txt


class Menu:
    def __init__(self, ui):
        self.ui = ui

    def cleanUp(self):
        self.ui.canvas_for_image.delete('all')
        self.ui.canvas_for_image.delete(self.ui.imagesprite)
        self.ui.initialOptions()
        self.ui.label.config(text='Hello')

    def openFile(self):
        self.cleanUp()
        file = filedialog.askopenfilename()
        with open(file, 'r') as file_handle:
            for line in file_handle:
                line = line.rstrip()
                self.ui.result = line
                InputProcessing(self.ui)
        self.ui.label.config(text=file)

    def saveImage(self):
        filename = filedialog.asksaveasfilename(
            filetypes=(
                ('jpeg files', '*.jpg'),
                ('png files', '*.png'),
                ('gif files', '*.gif')
            )
        )
        self.ui.pil_image.save(filename)

    def exit(self):
        self.ui.master.destroy()
        self.ui.pil_image.close()
