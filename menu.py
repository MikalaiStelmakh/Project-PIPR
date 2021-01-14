from tkinter import filedialog, messagebox
from InputProcessing import InputProcessing

# TODO: save commands as txt, open file has 2 options: open as new file and open as an addition to already existing file


class Menu:
    def __init__(self, ui, gui):
        self.ui = ui
        self.gui = gui

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
                    InputProcessing(self.ui, self.gui)
            errors = self.gui.errors
            if errors > 0:
                message = f'{errors} {"errors" if errors > 1 else "error"} occured while opening the file'
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
        self.gui.pil_image.close()
