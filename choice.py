from PIL import Image, ImageTk
import math
from bordersCrossing import BorderCrossed


class Turn:
    def __init__(self, ui, gui, units):
        self.ui = ui
        self.gui = gui
        self.units = units
        self.angle = self.units + self.gui.previous_angle
        while self.angle > 360:
            self.angle -= 360
        while self.angle < 0:
            self.angle += 360

    def simplifyAngle(self):
        if self.angle == 0 or self.angle == 360:
            self.direction = 'N'
        elif self.angle == 90:
            self.direction = 'E'
        elif self.angle == 180:
            self.direction = 'S'
        elif self.angle == 270:
            self.direction = 'W'
        elif self.angle < 90:
            self.angle = 90 - self.angle
            self.direction = 'NE'
        elif self.angle < 180:
            self.angle = 90 - (180 - self.angle)
            self.direction = 'SE'
        elif self.angle < 270:
            self.angle = 270 - self.angle
            self.direction = 'SW'
        elif self.angle < 360:
            self.angle = 90 - (360 - self.angle)
            self.direction = 'NW'
        self.gui.simple_angle = self.angle

    def setImageAnchor(self):
        if self.direction == 'E':
            self.anchor = 'w'
        elif self.direction == 'S':
            self.anchor = 'n'
        elif self.direction == 'W':
            self.anchor = 'e'
        elif self.direction == 'N':
            self.anchor = 's'
        elif self.direction == 'NE':
            self.anchor = 'sw'
        elif self.direction == 'SE':
            self.anchor = 'nw'
        elif self.direction == 'SW':
            self.anchor = 'ne'
        elif self.direction == 'NW':
            self.anchor = 'se'
        self.gui.direction = self.direction
        self.gui.anchor = self.anchor

    def setRotateValue(self, angle):
        rotate_value = -(angle + self.gui.previous_angle)
        self.gui.previous_angle = -rotate_value
        return rotate_value

    def setResizeValue(self):
        if self.angle == 0 or self.angle == 360 or self.angle == 180:
            resize_value = (self.gui.image_height, self.gui.image_width)
        elif self.angle == 90 or self.angle == 270:
            resize_value = (self.gui.image_width, self.gui.image_height)
        else:
            sinus = math.sin(math.radians(self.angle))
            cosinus = math.cos(math.radians(self.angle))
            height = self.gui.image_height
            width = self.gui.image_width
            image_width = height * cosinus + width * sinus
            image_height = height * sinus + width * cosinus
            resize_value = (int(image_height), int(image_width))
        return resize_value

    def createImage(self):
        rotate_value = self.setRotateValue(self.units)
        resize_value = self.setResizeValue()
        self.ui.canvas_for_image.image = ImageTk.PhotoImage(
            self.ui.image.rotate(rotate_value, expand=True).resize(resize_value),
            Image.ANTIALIAS
            )

    def drawImage(self):
        self.ui.imagesprite = self.ui.canvas_for_image.create_image(
            self.gui.image_x,
            self.gui.image_y,
            anchor=self.anchor,
            image=self.ui.canvas_for_image.image
            )


class Move:
    def __init__(self, ui, gui, units):
        self.ui = ui
        self.gui = gui
        self.units = units
        self.start_x = self.gui.image_x
        self.start_y = self.gui.image_y
        self.setNewCoordinates()
        self.drawIfDown(self.gui.image_x, self.gui.image_y,
                        self.new_image_x, self.new_image_y)
        self.gui.image_x = self.new_image_x
        self.gui.image_y = self.new_image_y
        self.moveImage()

    def moveValue(self):
        units = self.units
        direction = self.gui.direction
        x = units * math.cos(math.radians(self.gui.simple_angle))
        y = units * math.sin(math.radians(self.gui.simple_angle))
        if direction == 'N':
            x, y = (0, -units)
        elif direction == 'E':
            x, y = (units, 0)
        elif direction == 'S':
            x, y = (0, units)
        elif direction == 'W':
            x, y = (-units, 0)
        if direction == 'SW':
            x = -x
        elif direction == 'NW':
            x = -x
            y = -y
        elif direction == 'NE':
            y = -y
        return x, y

    def drawIfDown(self, x0, y0, x1, y1):
        if self.gui.is_up is False:
            self.ui.canvas_for_image.create_line(x0, y0, x1, y1)
            self.ui.draw.line([x0, y0, x1, y1], fill='black')

    def setNewCoordinates(self):
        self.move_x, self.move_y = self.moveValue()
        self.new_image_x = self.gui.image_x + self.move_x
        self.new_image_y = self.gui.image_y + self.move_y
        if self.isBorderCrossed() is True:
            crossed_border = BorderCrossed(
                self.ui, self.gui,
                self.new_image_x, self.new_image_y,
                self.move_x, self.move_y)
            self.gui.image_x = crossed_border.image_x
            self.gui.image_y = crossed_border.image_y
            self.new_image_x = crossed_border.new_image_x
            self.new_image_y = crossed_border.new_image_y

    def isBorderCrossed(self):
        return (self.new_image_x < 0 or
                self.new_image_x > self.gui.canvas_width or
                self.new_image_y < 0 or
                self.new_image_y > self.gui.canvas_height)

    def moveImage(self):
        move_img_x = self.new_image_x - self.start_x
        move_img_y = self.new_image_y - self.start_y
        imagesprite = self.ui.imagesprite
        self.ui.canvas_for_image.move(imagesprite, move_img_x, move_img_y)
