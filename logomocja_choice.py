from PIL import Image, ImageTk
import math
from logomocja_borders_crossing import (
    upperBorderCrossing, bottomBorderCrossing,
    leftBorderCrossing, rightBorderCrossing
)


class Choice:
    def __init__(self, main):
        self.main = main
        self.simple_angle = main.simple_angle
        self.direction = main.direction
        self.image_x = main.image_x
        self.image_y = main.image_y
        self.canvas_for_image = main.canvas_for_image
        self.canvas_width = main.canvas_width
        self.canvas_height = main.canvas_height
        self.imagesprite = main.imagesprite


class Turn(Choice):
    def __init__(self, main):
        super().__init__(main)
        self.image = main.image
        self.image_width = main.image_width
        self.image_height = main.image_height
        self.previous_angle = main.previous_angle
        self.angle = main.units + self.previous_angle
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
        return self.angle

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
        return self.anchor

    def setRotateValue(self, angle):
        self.rotate_value = -(angle + self.previous_angle)

    def setResizeValue(self):
        self.resize_value = (self.image_height, self.image_width)

    def createImage(self):
        rotate_value = self.rotate_value
        resize_value = self.resize_value
        self.canvas_for_image.image = ImageTk.PhotoImage(
            self.image.rotate(rotate_value).resize(resize_value),
            Image.ANTIALIAS
            )
        return self.canvas_for_image.image

    def drawImage(self):
        imagesprite = self.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor=self.anchor,
            image=self.canvas_for_image.image
            )
        return imagesprite


class Move(Choice):
    def __init__(self, main):
        super().__init__(main)
        self.units = main.units
        self.is_up = main.is_up

    def moveValue(self):
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
        return x, y

    def setNewCoordinates(self):
        self.move_x, self.move_y = self.moveValue()
        self.new_image_x = self.image_x + self.move_x
        self.new_image_y = self.image_y + self.move_y
        if self.isBorderCrossed() is True:
            crossed_border = self.borderCrossed()
            self.new_image_x = crossed_border.new_image_x
            self.new_image_y = crossed_border.new_image_y
        return self.new_image_x, self.new_image_y

    def isBorderCrossed(self):
        self.isBorderCrossed = (
            self.new_image_x < 0 or
            self.new_image_y > self.canvas_height or
            self.new_image_x > self.canvas_width or
            self.new_image_y < 0
            )
        return self.isBorderCrossed

    def moveImage(self):
        if self.isBorderCrossed is True:
            self.move_x = self.new_image_x - self.image_x
            self.move_y = self.new_image_y - self.image_y
        self.canvas_for_image.move(self.imagesprite, self.move_x, self.move_y)

    def borderCrossed(self):
        if self.new_image_y < 0:
            crossed_border = upperBorderCrossing(self, self.main)
        elif self.new_image_y > self.canvas_height:
            crossed_border = bottomBorderCrossing(self, self.main)
        elif self.new_image_x > self.canvas_width:
            crossed_border = rightBorderCrossing(self, self.main)
        elif self.new_image_x < 0:
            crossed_border = leftBorderCrossing(self, self.main)
        return crossed_border

    def drawLine(self):
        if self.isBorderCrossed is False:
            if self.is_up is False:
                self.canvas_for_image.create_line(
                    self.image_x, self.image_y,
                    self.new_image_x, self.new_image_y
                )
                self.main.draw.line(
                    [self.image_x, self.image_y,
                     self.new_image_x, self.new_image_y], fill='black'
                )
