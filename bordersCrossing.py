import math


class BorderCrossed:
    def __init__(self, ui, gui, new_image_x, new_image_y, move_x, move_y):
        self.ui = ui
        self.gui = gui
        self.image_x = gui.image_x
        self.image_y = gui.image_y
        self.new_image_x = new_image_x
        self.new_image_y = new_image_y
        self.angle = gui.simple_angle
        self.move_x = move_x
        self.move_y = move_y
        self.borderCrossed()

    def drawIfDown(self, x0, y0, x1, y1):
        if self.gui.is_up is False:
            self.ui.canvas_for_image.create_line(x0, y0, x1, y1)
            self.ui.draw.line([x0, y0, x1, y1], fill='black')
            self.ui.pil_image.show()

    def isBorderCrossed(self):
        return (self.new_image_x < 0 or
                self.new_image_x > self.gui.canvas_width or
                self.new_image_y < 0 or
                self.new_image_y > self.gui.canvas_height)

    def borderCrossed(self):
        self.passed_x, self.passed_y = 0, 0
        self.start_x = self.image_x
        self.start_y = self.image_y

        if self.gui.simple_angle == 90 or self.gui.simple_angle == 270:
            self.angle = 0
        while self.isBorderCrossed() is True:
            if self.move_x > 0:
                self.rightBorderCrossed()
            elif self.move_x < 0:
                self.leftBorderCrossed()
            else:
                self.topOrBotBorderCrossed()
            self.drawIfDown(self.image_x, self.image_y, self.x1, self.y1)
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
            new_y = self.gui.canvas_height
            new_x = x1
        elif self.image_y + y > self.gui.canvas_height:
            y = self.gui.canvas_height - self.image_y
            x = -y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = self.gui.canvas_height
            new_y = 0
            new_x = x1
        else:
            x1 = 0
            y1 = self.image_y + y
            new_y = y1
            new_x = self.gui.canvas_width
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.new_x, self.new_y = new_x, new_y

    def rightBorderCrossed(self):
        x = self.gui.canvas_width - self.image_x
        y = x*math.tan(math.radians(self.angle))
        if self.move_y < 0: y = -y
        if self.image_y + y < 0:
            y = -self.image_y
            x = -y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = 0
            new_y = self.gui.canvas_height
            new_x = x1
        elif self.image_y + y > self.gui.canvas_height:
            y = self.gui.canvas_height - self.image_y
            x = y/math.tan(math.radians(self.angle))
            x1 = self.image_x + x
            y1 = self.gui.canvas_height
            new_y = 0
            new_x = x1
        else:
            x1 = self.gui.canvas_width
            y1 = self.image_y + y
            new_y = y1
            new_x = 0
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.new_x, self.new_y = new_x, new_y

    def topOrBotBorderCrossed(self):
        x = 0
        if self.move_y > 0:
            y = self.gui.canvas_height - self.image_y
            y1 = self.gui.canvas_height
            new_y = 0
        else:
            y = -self.image_y
            y1 = 0
            new_y = self.gui.canvas_height
        x1 = self.image_x
        new_x = self.image_x
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.new_x, self.new_y = new_x, new_y
