from PIL import Image, ImageTk
import math
from logomocja_borders_crossing import (
    upperBorderCrossing, bottomBorderCrossing,
    leftBorderCrossing, rightBorderCrossing
)


class Choice:
    def __init__(self, main):
        self.result = main.result
        self.image = main.image
        self.imagesprite = main.imagesprite
        self.image_x = main.image_x
        self.image_y = main.image_y
        self.new_image_x = main.new_image_x
        self.new_image_y = main.new_image_y
        self.image_height = main.image_height
        self.image_width = main.image_width
        self.canvas_height = main.canvas_height
        self.canvas_width = main.canvas_width
        self.canvas_for_image = main.canvas_for_image
        self.previous_angle = main.previous_angle
        self.simple_angle = main.simple_angle
        self.direction = main.direction
        self.is_up = main.is_up
        self.command, self.units = self.splitInput()

    def splitInput(self):
        splitted_result = self.result.split()
        return (splitted_result[0], float(splitted_result[1]))

    def drawIfNotUp(self, x0, y0, x, y):
        if self.is_up is False:
            self.canvas_for_image.create_line(
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
        angle = self.units
        while angle/360 > 1:
            angle -= 360
        image_rotate = -(angle + self.previous_angle)
        image_resize = (self.image_height, self.image_width)
        self.canvas_for_image.image = ImageTk.PhotoImage(
            self.image.rotate(image_rotate).resize(image_resize),
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
        self.imagesprite = self.canvas_for_image.create_image(
            self.image_x,
            self.image_y,
            anchor=anchor,
            image=self.canvas_for_image.image)

    def moveCommand(self):
        self.move_x = self.moveValue()[0]
        self.move_y = self.moveValue()[1]
        self.new_image_x = self.image_x + self.move_x
        self.new_image_y = self.image_y + self.move_y
        if self.new_image_y < 0:
            crossed_border = upperBorderCrossing(self)
        elif self.new_image_y > self.canvas_height:
            crossed_border = bottomBorderCrossing(self)
        elif self.new_image_x > self.canvas_width:
            crossed_border = rightBorderCrossing(self)
        elif self.new_image_x < 0:
            crossed_border = leftBorderCrossing(self)
        else:
            crossed_border = self
            self.drawIfNotUp(
                self.image_x, self.image_y,
                self.new_image_x, self.new_image_y
            )
        self.new_image_x = crossed_border.new_image_x
        self.new_image_y = crossed_border.new_image_y
        self.move_x = self.new_image_x - self.image_x
        self.move_y = self.new_image_y - self.image_y
        self.canvas_for_image.move(self.imagesprite, self.move_x, self.move_y)
        self.image_x = self.new_image_x
        self.image_y = self.new_image_y
