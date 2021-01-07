import math


class BorderCrossed:
    def __init__(self, master):
        self.master = master
        self.image_x = master.image_x
        self.image_y = master.image_y
        self.new_image_x = master.new_image_x
        self.new_image_y = master.new_image_y
        self.move_x = master.move_x
        self.move_y = master.move_y
        self.canvas_width = master.canvas_width
        self.canvas_height = master.canvas_height
        self.imagesprite = master.imagesprite
        self.angle = master.angle

        self.borderCrossed()

    def isBorderCrossed(self):
        return (self.new_image_x < 0 or
                self.new_image_x > self.canvas_width or
                self.new_image_y < 0 or
                self.new_image_y > self.canvas_height)

    def borderCrossed(self):
        self.passed_x, self.passed_y = 0, 0
        self.start_x = self.image_x
        self.start_y = self.image_y

        if self.angle == 90 or self.angle == 270:
            self.angle = 0
        while self.isBorderCrossed() is True:
            if self.move_x > 0:
                self.rightBorderCrossed()
            elif self.move_x < 0:
                self.leftBorderCrossed()
            else:
                self.topOrBotBorderCrossed()
            self.master.drawIfDown(self.image_x, self.image_y, self.x1, self.y1)
            self.image_x = self.new_x
            self.image_y = self.new_y
            self.passed_x += self.x
            self.passed_y += self.y
            self.new_image_x = self.image_x + self.move_x - self.passed_x
            self.new_image_y = self.image_y + self.move_y - self.passed_y

    def leftBorderCrossed(self):
        x = -self.image_x
        y = x*math.tan(math.radians(self.angle))
        if self.move_y > 0: y = -y
        if self.image_y + y < 0:
            y = -self.image_y
            x = y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = 0
            new_y = self.canvas_height
            new_x = x1
        elif self.image_y + y > self.canvas_height:
            y = self.canvas_height - self.image_y
            x = -y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = self.canvas_height
            new_y = 0
            new_x = x1
        else:
            x1 = 0
            y1 = self.image_y + y
            new_y = y1
            new_x = self.canvas_width
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.new_x, self.new_y = new_x, new_y

    def rightBorderCrossed(self):
        x = self.canvas_width - self.image_x
        y = x*math.tan(math.radians(self.angle))
        if self.move_y < 0: y = -y
        if self.image_y + y < 0:
            y = -self.image_y
            x = -y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = 0
            new_y = self.canvas_height
            new_x = x1
        elif self.image_y + y > self.canvas_height:
            y = self.canvas_height - self.image_y
            x = y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = self.canvas_height
            new_y = 0
            new_x = x1
        else:
            x1 = self.canvas_width
            y1 = self.image_y + y
            new_y = y1
            new_x = 0
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.new_x, self.new_y = new_x, new_y

    def topOrBotBorderCrossed(self):
        x = 0
        if self.move_y > 0:
            y = self.canvas_height - self.image_y
            y1 = self.canvas_height
            new_y = 0
        else:
            y = -self.image_y
            y1 = 0
            new_y = self.canvas_height
        x1 = self.image_x
        new_x = self.image_x
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.new_x, self.new_y = new_x, new_y