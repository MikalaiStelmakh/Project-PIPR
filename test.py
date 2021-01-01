from PIL import Image, ImageTk
import tkinter as tk
import math


def returnEntry(arg=None):
    global is_up, previous_angle, simple_angle, image_x, image_y, direction
    global new_image_x, new_image_y, imagesprite
    result = entry.get()
    choice = Choice(
        result=result,
        previous_angle=previous_angle,
        simple_angle=simple_angle,
        direction=direction,
        imagesprite=imagesprite,
        image_x=image_x,
        image_y=image_y,
        new_image_x=new_image_x,
        new_image_y=new_image_y
        )
    if choice.command == 'turn':
        label.config(text=result)
        choice.turnCommand()
        previous_angle = choice.previous_angle
        simple_angle = choice.simple_angle
        direction = choice.direction
        imagesprite = choice.imagesprite
    elif choice.command == 'move':
        label.config(text=result)
        choice.moveCommand()
        image_x = choice.image_x
        image_y = choice.image_y
        new_image_x = choice.new_image_x
        new_image_y = choice.new_image_y
    entry.delete(0, 'end')


class Choice:
    def __init__(
            self,
            result,
            previous_angle,
            simple_angle,
            direction,
            imagesprite,
            image_x,
            image_y,
            new_image_x,
            new_image_y):
        self.result = result
        self.previous_angle = previous_angle
        self.simple_angle = simple_angle
        self.direction = direction
        self.imagesprite = imagesprite
        self.image_x = image_x
        self.image_y = image_y
        self.new_image_x = new_image_x
        self.new_image_y = new_image_y
        self.command, self.units = self.splitInput()

    def splitInput(self):
        splitted_result = self.result.split()
        return (splitted_result[0], float(splitted_result[1]))

    def drawIfNotUp(self, x0, y0, x, y):
        if is_up is False:
            canvas_for_image.create_line(
                x0, y0,
                x, y)

    def simplifyAngle(self, angle):
        if angle == 0 or angle == 360:
            self.direction = 'N'
        elif angle == 90:
            self.direction = 'E'
        elif angle == 180:
            self.direction = 'S'
        elif angle == 270:
            self.direction = 'W'
        elif angle < 90:
            angle = 90 - angle
            self.direction = 'NE'
        elif angle < 180:
            angle = 90 - (180 - angle)
            self.direction = 'SE'
        elif angle < 270:
            angle = 270 - angle
            self.direction = 'SW'
        elif angle < 360:
            angle = 90 - (360 - angle)
            self.direction = 'NW'
        return angle

    def moveValue(self):
        # new_angle, self.direction = self.simplifyAngle(angle)
        x = self.units * math.cos(math.radians(self.simple_angle))
        y = self.units * math.sin(math.radians(self.simple_angle))
        if self.direction == 'N':
            x, y = (0, -self.units)
        elif self.direction == 'E':
            x, y = (self.units, 0)
        elif self.direction == 'S':
            x, y = (0, self.units)
        elif self.direction == 'W':
            x, y = (-self.units, 0)
        if self.direction == 'SW':
            x = -x
        elif self.direction == 'NW':
            x = -x
            y = -y
        elif self.direction == 'NE':
            y = -y
        return (float(x), float(y))

    def turnCommand(self):
        # global new_image_x, new_image_y, imagesprite, previous_angle, simple_angle, x
        angle = self.units
        while angle/360 > 1:
            angle -= 360
        image_rotate = -(angle + self.previous_angle)
        image_resize = (image_height, image_width)
        canvas_for_image.image = ImageTk.PhotoImage(
            image.rotate(image_rotate).resize(image_resize),
            Image.ANTIALIAS)
        self.previous_angle += angle
        angle = self.previous_angle
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        self.simple_angle = self.simplifyAngle(angle)
        if angle == 90:
            anchor = 'w'
        elif angle == 180:
            anchor = 'n'
        elif angle == 270:
            anchor = 'e'
        elif angle == 0 or angle == 360:
            anchor = 's'
        elif angle < 90:
            anchor = 'sw'
        elif angle < 180:
            anchor = 'nw'
        elif angle < 270:
            anchor = 'ne'
        elif angle < 360:
            anchor = 'se'
        self.imagesprite = canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor=anchor,
            image=canvas_for_image.image)

    def moveCommand(self):
        self.move_x = self.moveValue()[0]
        self.move_y = self.moveValue()[1]
        self.new_image_x = self.image_x + self.move_x
        self.new_image_y = self.image_y + self.move_y
        if self.new_image_y < 0:
            crossed_border = upperBorderCrossing(self)
        elif self.new_image_y > canvas_height:
            crossed_border = bottomBorderCrossing(self)
        # elif new_image_x > canvas_width:
        #     crossed_border = rightBorderCrossing(self)
        # elif new_image_x < 0:
        #     crossed_border = leftBorderCrossing(self)
        else:
            crossed_border = self
            canvas_for_image.move(imagesprite, self.move_x, self.move_y)
            self.drawIfNotUp(
                self.image_x, self.image_y,
                self.new_image_x, self.new_image_y
            )
        self.new_image_x = crossed_border.new_image_x
        self.new_image_y = crossed_border.new_image_y
        self.image_x = self.new_image_x
        self.image_y = self.new_image_y


class upperBorderCrossing(Choice):
    def __init__(self, choice):
        self.move_x = choice.move_x
        self.move_y = choice.move_y
        self.image_x = choice.image_x
        self.image_y = choice.image_y
        self.new_image_x = choice.new_image_x
        self.simple_angle = choice.simple_angle
        self.imagesprite = choice.imagesprite
        self.passed_y = image_y
        self.new_image_y = canvas_height + choice.move_y + self.passed_y
        if simple_angle == 0 or simple_angle == 360:
            self.crossingAtRightAngle()
        else:
            self.crossingAtNotRightAngle()
        self.move_x = self.new_image_x - self.image_x
        self.move_y = self.new_image_y - self.image_y
        canvas_for_image.move(self.imagesprite, self.move_x, self.move_y)

    def crossingAtRightAngle(self):
        super().drawIfNotUp(
            self.image_x, self.image_y,
            self.new_image_x, 0
        )
        while self.new_image_y < 0:
            self.passed_y += canvas_height
            self.new_image_y = self.move_y + self.passed_y
        super().drawIfNotUp(
            self.image_x, canvas_height,
            self.new_image_x, self.new_image_y
        )

    def crossingAtNotRightAngle(self):
        radians = math.radians(self.simple_angle)
        self.passed_x = self.passed_y/math.tan(radians)
        if self.move_x > 0:
            top_x = self.image_x + self.passed_x
        else:
            top_x = self.image_x - self.passed_x
        self.new_image_x = top_x
        super().drawIfNotUp(
            self.image_x, self.image_y,
            top_x, 0
        )
        while self.new_image_y < 0:
            self.passed_y += canvas_height
            self.new_image_y = self.move_y + self.passed_y
            self.passed_x += canvas_height/math.tan(radians)
            self.new_image_x = top_x
            if self.move_x > 0:
                top_x = self.image_x + self.passed_x
            else:
                top_x = self.image_x - self.passed_x
            super().drawIfNotUp(
                self.new_image_x, canvas_height,
                top_x, 0
            )
        self.new_image_x = top_x
        self.passed_y += canvas_height - self.new_image_y
        self.passed_x += (canvas_height - self.new_image_y)/math.tan(radians)
        if self.move_x > 0:
            top_x = self.image_x + self.passed_x
        else:
            top_x = self.image_x - self.passed_x
        super().drawIfNotUp(
            self.new_image_x, canvas_height,
            top_x, self.new_image_y
        )
        self.new_image_x, top_x = top_x, self.new_image_x


class bottomBorderCrossing(Choice):
    def __init__(self, choice):
        self.move_x = choice.move_x
        self.move_y = choice.move_y
        self.image_x = choice.image_x
        self.image_y = choice.image_y
        self.new_image_x = choice.new_image_x
        self.simple_angle = choice.simple_angle
        self.imagesprite = choice.imagesprite
        self.passed_y = canvas_height - choice.image_y
        self.new_image_y = choice.move_y - self.passed_y
        if simple_angle == 180:
            self.crossingAtRightAngle()
        else:
            self.crossingAtNotRightAngle()
        self.move_x = self.new_image_x - self.image_x
        self.move_y = self.new_image_y - self.image_y
        canvas_for_image.move(self.imagesprite, self.move_x, self.move_y)

    def crossingAtRightAngle(self):
        super().drawIfNotUp(
            self.image_x, self.image_y,
            self.new_image_x, canvas_height
        )
        while self.new_image_y > canvas_height:
            self.passed_y += canvas_height
            self.new_image_y = self.move_y - self.passed_y
        super().drawIfNotUp(
            self.image_x, 0,
            self.new_image_x, self.new_image_y
        )

    def crossingAtNotRightAngle(self):
        radians = math.radians(self.simple_angle)
        self.passed_x = self.passed_y/math.tan(radians)
        if self.move_x > 0:
            bot_x = self.image_x + self.passed_x
        else:
            bot_x = self.image_x - self.passed_x
        self.new_image_x = bot_x
        super().drawIfNotUp(
            self.image_x, self.image_y,
            bot_x, canvas_height
        )
        while self.new_image_y > canvas_height:
            self.passed_y += canvas_height
            self.new_image_y = self.move_y - self.passed_y
            self.passed_x += canvas_height/math.tan(radians)
            self.new_image_x = bot_x
            if self.move_x > 0:
                bot_x = self.image_x + self.passed_x
            else:
                bot_x = self.image_x - self.passed_x
            super().drawIfNotUp(
                self.new_image_x, 0,
                bot_x, canvas_height
            )
        self.new_image_x = bot_x
        self.passed_y += self.new_image_y
        self.passed_x += self.new_image_y/math.tan(radians)
        if self.move_x > 0:
            bot_x = self.image_x + self.passed_x
        else:
            bot_x = self.image_x - self.passed_x
        super().drawIfNotUp(
            self.new_image_x, 0,
            bot_x, self.new_image_y
        )
        self.new_image_x, bot_x = bot_x, self.new_image_x


def rightBorderCrossing(move_x, move_y):
    passed_x = canvas_width - image_x
    new_image_x = move_x - passed_x
    while new_image_x > canvas_width:
        passed_x += canvas_width
        new_image_x = move_x - passed_x
    move_x = image_x - new_image_x
    if simple_angle[0] == 90:
        canvas_for_image.move(imagesprite, move_x, move_y)
        if is_up is False:
            canvas_for_image.create_line(
                image_x,
                image_y,
                canvas_width,
                new_image_y)
            canvas_for_image.create_line(
                0,
                new_image_y,
                new_image_x,
                new_image_y)
    else:
        passed_y = passed_x * math.tan(math.radians(simple_angle[0]))
        right_y = image_y - passed_y if move_y > 0 else image_y + passed_y
        canvas_for_image.move(imagesprite, -move_x, -move_y)
        if is_up is False:
            canvas_for_image.create_line(
                image_x,
                image_y,
                canvas_width,
                right_y
            )
            canvas_for_image.create_line(
                0,
                right_y,
                new_image_x,
                new_image_y
            )
    return (new_image_x, new_image_y)


def leftBorderCrossing(move_x, move_y):
    passed_x = image_x
    new_image_x = canvas_width + move_x + passed_x
    while new_image_x < 0:
        passed_x += canvas_width
        new_image_x = canvas_width + move_x + passed_x
    move_x = new_image_x - image_x
    if simple_angle[0] == 270:
        canvas_for_image.move(imagesprite, move_x, move_y)
        if is_up is False:
            canvas_for_image.create_line(
                image_x,
                image_y,
                0,
                new_image_y)
            canvas_for_image.create_line(
                canvas_width,
                new_image_y,
                new_image_x,
                new_image_y)
    else:
        passed_y = passed_x * math.tan(math.radians(simple_angle[0]))
        left_y = image_y - passed_y if move_y > 0 else image_y - passed_y
        canvas_for_image.move(imagesprite, move_x, -move_y)
        if is_up is False:
            canvas_for_image.create_line(
                image_x,
                image_y,
                0,
                left_y
            )
            canvas_for_image.create_line(
                canvas_width,
                left_y,
                new_image_x,
                new_image_y
            )
    return (new_image_x, new_image_y)


root = tk.Tk()
global simple_angle, previous_angle, image_x, image_y, new_image_x, is_up, x
global new_image_y, image_width, image_height, canvas_width, canvas_height, direction

canvas = tk.Canvas(root, height=700, width=800)
canvas.pack()

canvas_for_image = tk.Canvas(root, bg='white')
canvas_for_image.place(
    relx=0.5,
    rely=0.5,
    width=640,
    height=490,
    anchor='center')
canvas_for_image.update()
canvas_width = canvas_for_image.winfo_width()
canvas_height = canvas_for_image.winfo_height()

image_width = int(canvas_width*0.05)
image_height = int(canvas_height*0.05)
image_x = canvas_width*0.5
image_y = canvas_height*0.5 + image_height/2

label_frame = tk.Frame(root, borderwidth=2, relief="sunken")
label_frame.place(rely=0.9, relwidth=1, relheight=0.07)
label = tk.Label(
    label_frame,
    text='Hello\n',
    fg='black',
    font=("Modern", 10),
    justify='left',
    bd=4)
label.pack(side='top', anchor='w')

entry_frame = tk.Frame(root)
entry_frame.place(rely=0.97, relwidth=1, relheight=0.03)
entry = tk.Entry(entry_frame, bg='white', fg='black')
x = 0
simple_angle = 0
direction = 'N'
previous_angle = 0
is_up = False
new_image_x, new_image_y = image_x, image_y
entry.bind("<Return>", returnEntry)
entry.place(relwidth=1)

image = Image.open('turtle.png')
canvas_for_image.image = ImageTk.PhotoImage(
    image.resize((image_height, image_width)),
    Image.ANTIALIAS)
imagesprite = canvas_for_image.create_image(
    image_x,
    image_y,
    anchor='s',
    image=canvas_for_image.image)

root.mainloop()
