from PIL import Image, ImageTk
import tkinter as tk
from logomocja_choice import Choice, Turn


"""
TODO:
1) Split main function into class functions,
2) In logomocja_choice split choice's turnCommand function into new class functions
3) In logomocja_choice split choice's moveCommand function into new class functions
"""


class UI(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, height=700, width=800)
        self.canvas.pack()

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
        self.image_x = self.canvas_width*0.5
        self.image_y = self.canvas_height*0.5 + self.image_height/2

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
        self.entry_frame.place(rely=0.97, relwidth=1, relheight=0.03)
        self.entry = tk.Entry(self.entry_frame, bg='white', fg='black')
        self.x = 0
        self.simple_angle = 0
        self.direction = 'N'
        self.previous_angle = 0
        self.is_up = False
        self.new_image_x, self.new_image_y = self.image_x, self.image_y
        self.entry.bind("<Return>", self.main)
        self.entry.place(relwidth=1)

        self.image = Image.open('turtle.png')
        self.canvas_for_image.image = ImageTk.PhotoImage(
            self.image.resize((self.image_height, self.image_width)),
            Image.ANTIALIAS)
        self.imagesprite = self.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor='s',
            image=self.canvas_for_image.image)

    def main(self, event):
        self.result = self.entry.get()
        if self.result == 'podnies':
            self.is_up = True
        elif self.result == 'opusc':
            self.is_up = False
        try:
            choice = Choice(self)
            self.command = choice.command
            self.units = choice.units
            if self.command == 'obrot':
                text = self.result
                self.turnCommand()
            elif self.command == 'naprzod':
                text = self.result
                choice.moveCommand()
                self.image_x = choice.image_x
                self.image_y = choice.image_y
                self.new_image_x = choice.new_image_x
                self.new_image_y = choice.new_image_y
            elif choice.command == 'podnies' or choice.command == 'opusc':
                text = ('ValueError\n'
                        'Example of a correct entry: podnies')
            else:
                text = (f'Undefined command: {self.result}\n'
                        'Example of a correct entry: obrot 90')
        except IndexError:
            if self.result == 'podnies' or self.result == 'opusc':
                text = self.result
            else:
                text = (f'Undefined command: {self.result}\n'
                        'Example of a correct entry: obrot 90')
        except ValueError:
            text = ('ValueError\n'
                    'Example of a correct entry: move 100')
        self.label.config(text=text)
        self.entry.delete(0, 'end')

    def turnCommand(self):
        turn = Turn(self)
        self.previous_angle = turn.angle
        self.simple_angle = turn.simplifyAngle()
        self.direction = turn.direction
        self.anchor = turn.setImageAnchor()
        turn.setRotateValue(self.units)
        turn.setResizeValue()
        self.canvas_for_image.image = turn.createImage()
        self.imagesprite = turn.drawImage()


root = tk.Tk()
ui = UI(root)
root.mainloop()
