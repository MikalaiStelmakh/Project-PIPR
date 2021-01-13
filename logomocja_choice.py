from PIL import Image, ImageTk
import math
from logomocja_borders_crossing import BorderCrossed


class Turn:
    def __init__(self, ui):
        self.ui = ui
        self.angle = self.ui.units + self.ui.previous_angle
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
        self.ui.simple_angle = self.angle

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
        self.ui.direction = self.direction
        self.ui.anchor = self.anchor

    def setRotateValue(self, angle):
        rotate_value = -(angle + self.ui.previous_angle)
        self.ui.previous_angle = -rotate_value
        return rotate_value

    # def setResizeValue(self):
    #     if self.angle == 0 or self.angle == 360 or self.angle == 180:
    #         resize_value = (self.ui.image_height, self.ui.image_width)
    #     elif self.angle == 90 or self.angle == 270:
    #         resize_value = (self.ui.image_width, self.ui.image_height)
    #     else:
    #         image_width = self.ui.image_height * math.cos(math.radians(self.angle)) + self.ui.image_width * math.sin(math.radians(self.angle))
    #         image_height = self.ui.image_height * math.sin(math.radians(self.angle)) + self.ui.image_width * math.cos(math.radians(self.angle))
    #         resize_value = (int(image_height), int(image_width))
    #     return resize_value

    def createImage(self):
        rotate_value = self.setRotateValue(self.ui.units)
        resize_value = (self.ui.image_height, self.ui.image_width)
        self.ui.canvas_for_image.image = ImageTk.PhotoImage(
            self.ui.image.rotate(rotate_value).resize(resize_value),
            Image.ANTIALIAS
            )

    def drawImage(self):
        self.ui.imagesprite = self.ui.canvas_for_image.create_image(
            self.ui.image_x,
            self.ui.image_y,
            anchor=self.anchor,
            image=self.ui.canvas_for_image.image
            )


class Move:
    def __init__(self, ui):
        self.ui = ui
        self.is_up = ui.is_up
        self.image_x = ui.image_x
        self.image_y = ui.image_y
        self.canvas_width = ui.canvas_width
        self.canvas_height = ui.canvas_height
        self.angle = ui.simple_angle
        self.imagesprite = ui.imagesprite
        self.start_x = self.image_x
        self.start_y = self.image_y

        self.setNewCoordinates()
        self.drawIfDown(self.image_x, self.image_y, self.new_image_x, self.new_image_y)
        self.moveImage()

    def moveValue(self):
        units = self.ui.units
        direction = self.ui.direction
        x = units * math.cos(math.radians(self.angle))
        y = units * math.sin(math.radians(self.angle))
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
        if self.is_up is False:
            self.ui.canvas_for_image.create_line(x0, y0, x1, y1)
            self.ui.draw.line([x0, y0, x1, y1], fill='black')

    def setNewCoordinates(self):
        self.move_x, self.move_y = self.moveValue()
        self.new_image_x = self.image_x + self.move_x
        self.new_image_y = self.image_y + self.move_y
        if self.isBorderCrossed() is True:
            crossed_border = BorderCrossed(self)
            self.image_x = crossed_border.image_x
            self.image_y = crossed_border.image_y
            self.new_image_x = crossed_border.new_image_x
            self.new_image_y = crossed_border.new_image_y
        self.ui.image_x = self.new_image_x
        self.ui.image_y = self.new_image_y

    def isBorderCrossed(self):
        return (self.new_image_x < 0 or
                self.new_image_x > self.canvas_width or
                self.new_image_y < 0 or
                self.new_image_y > self.canvas_height)

    def moveImage(self):
        move_img_x = self.new_image_x - self.start_x
        move_img_y = self.new_image_y - self.start_y
        self.ui.canvas_for_image.move(self.imagesprite, move_img_x, move_img_y)
