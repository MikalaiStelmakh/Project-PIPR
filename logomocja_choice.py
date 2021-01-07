from PIL import Image, ImageTk
import math


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

    def setResizeValue(self):
        resize_value = (self.ui.image_height, self.ui.image_width)
        return resize_value

    def createImage(self):
        rotate_value = self.setRotateValue(self.ui.units)
        resize_value = self.setResizeValue()
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

    def moveValue(self):
        units = self.ui.units
        direction = self.ui.direction
        x = units * math.cos(math.radians(self.ui.simple_angle))
        y = units * math.sin(math.radians(self.ui.simple_angle))
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
        if self.ui.is_up is False:
            self.ui.canvas_for_image.create_line(x0, y0, x1, y1)
            self.ui.draw.line([x0, y0, x1, y1], fill='black')

    def setNewCoordinates(self):
        self.move_x, self.move_y = self.moveValue()
        self.border()

    def border(self):

        image_x = self.ui.image_x
        image_y = self.ui.image_y
        canvas_width = self.ui.canvas_width
        canvas_height = self.ui.canvas_height
        angle = self.ui.simple_angle
        imagesprite = self.ui.imagesprite
        new_image_x = image_x + self.move_x
        new_image_y = image_y + self.move_y
        passed_x, passed_y = 0, 0
        if angle == 90 or angle == 270:
            angle = 0
        while new_image_x < 0 or new_image_x > canvas_width or new_image_y < 0 or new_image_y > canvas_height:
            if self.move_x > 0:
                x = canvas_width - image_x
                y = x*math.tan(math.radians(angle))
                if self.move_y < 0: y = -y
                if image_y + y < 0:
                    y = -image_y
                    x = -y/math.tan(math.radians(angle))
                    x1 = image_x + x
                    y1 = 0
                    new_y = canvas_height
                    new_x = x1
                elif image_y + y > canvas_height:
                    y = canvas_height - image_y
                    x = y/math.tan(math.radians(angle))
                    x1 = image_x + x
                    y1 = canvas_height
                    new_y = 0
                    new_x = x1
                else:
                    x1 = canvas_width
                    y1 = image_y + y
                    new_y = y1
                    new_x = 0
            elif self.move_x < 0:
                x = -image_x
                y = x*math.tan(math.radians(angle))
                if self.move_y > 0: y = -y
                if image_y + y < 0:
                    y = -image_y
                    x = y/math.tan(math.radians(angle))
                    x1 = image_x + x
                    y1 = 0
                    new_y = canvas_height
                    new_x = x1
                elif image_y + y > canvas_height:
                    y = canvas_height - image_y
                    x = -y/math.tan(math.radians(angle))
                    x1 = image_x + x
                    y1 = canvas_height
                    new_y = 0
                    new_x = x1
                else:
                    x1 = 0
                    y1 = image_y + y
                    new_y = y1
                    new_x = canvas_width
            else:
                x = 0
                if self.move_y > 0:
                    y = canvas_height - image_y
                    y1 = canvas_height
                    new_y = 0
                else:
                    y = -image_y
                    y1 = 0
                    new_y = canvas_height
                x1 = image_x
                new_x = image_x
            self.drawIfDown(image_x, image_y, x1, y1)
            image_x = new_x
            image_y = new_y
            passed_x += x
            passed_y += y
            new_image_x = image_x + self.move_x - passed_x
            new_image_y = image_y + self.move_y - passed_y
        self.drawIfDown(image_x, image_y, new_image_x, new_image_y)
        move_img_x = new_image_x - start_x
        move_img_y = new_image_y - start_y
        self.ui.canvas_for_image.move(imagesprite, move_img_x, move_img_y)
        self.ui.image_x = new_image_x
        self.ui.image_y = new_image_y
