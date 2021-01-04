import math


class borderCrossing:
    def __init__(self, choice, ui):
        self.ui = ui
        self.move_x = choice.move_x
        self.move_y = choice.move_y
        self.image_x = ui.image_x
        self.image_y = ui.image_y
        self.simple_angle = ui.simple_angle
        self.imagesprite = ui.imagesprite
        self.canvas_for_image = ui.canvas_for_image
        self.canvas_height = ui.canvas_height
        self.canvas_width = ui.canvas_width
        self.is_up = ui.is_up
        self.tangens = math.tan(math.radians(self.simple_angle))

    def drawIfNotUp(self, x0, y0, x, y):
        if self.is_up is False:
            self.canvas_for_image.create_line(
                x0, y0,
                x, y)
            self.ui.draw.line(
                [x0, y0, x, y],
                fill='black')


class upperBorderCrossing(borderCrossing):
    def __init__(self, choice, ui):
        super().__init__(choice, ui)
        self.new_image_x = choice.new_image_x
        self.passed_y = self.image_y
        self.new_image_y = self.canvas_height + self.move_y + self.passed_y
        if self.simple_angle == 0 or self.simple_angle == 360:
            self.crossingAtRightAngle()
        else:
            self.crossingAtNotRightAngle()

    def crossingAtRightAngle(self):
        super().drawIfNotUp(
            self.image_x, self.image_y,
            self.new_image_x, 0
        )
        while self.new_image_y < 0:
            self.passed_y += self.canvas_height
            self.new_image_y = self.move_y + self.passed_y
            super().drawIfNotUp(
                self.image_x, 0,
                self.new_image_x, self.canvas_height
            )
        super().drawIfNotUp(
            self.image_x, self.canvas_height,
            self.new_image_x, self.new_image_y
        )

    def crossingAtNotRightAngle(self):
        self.passed_x = self.passed_y/self.tangens
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
            self.passed_y += self.canvas_height
            self.new_image_y = self.move_y + self.passed_y
            self.passed_x += self.canvas_height/self.tangens
            self.new_image_x = top_x
            if self.move_x > 0:
                top_x = self.image_x + self.passed_x
            else:
                top_x = self.image_x - self.passed_x
            super().drawIfNotUp(
                self.new_image_x, self.canvas_height,
                top_x, 0
            )
        self.new_image_x = top_x
        self.passed_y += self.canvas_height - self.new_image_y
        self.passed_x += (self.canvas_height - self.new_image_y)/self.tangens
        if self.move_x > 0:
            top_x = self.image_x + self.passed_x
        else:
            top_x = self.image_x - self.passed_x
        super().drawIfNotUp(
            self.new_image_x, self.canvas_height,
            top_x, self.new_image_y
        )
        self.new_image_x, top_x = top_x, self.new_image_x


class bottomBorderCrossing(borderCrossing):
    def __init__(self, choice, ui):
        super().__init__(choice, ui)
        self.new_image_x = choice.new_image_x
        self.passed_y = self.canvas_height - self.image_y
        self.new_image_y = self.move_y - self.passed_y
        if self.simple_angle == 180:
            self.crossingAtRightAngle()
        else:
            self.crossingAtNotRightAngle()

    def crossingAtRightAngle(self):
        super().drawIfNotUp(
            self.image_x, self.image_y,
            self.new_image_x, self.canvas_height
        )
        while self.new_image_y > self.canvas_height:
            self.passed_y += self.canvas_height
            self.new_image_y = self.move_y - self.passed_y
            super().drawIfNotUp(
                self.image_x, 0,
                self.new_image_x, self.canvas_height
            )
        super().drawIfNotUp(
            self.image_x, 0,
            self.new_image_x, self.new_image_y
        )

    def crossingAtNotRightAngle(self):
        self.passed_x = self.passed_y/self.tangens
        if self.move_x > 0:
            bot_x = self.image_x + self.passed_x
        else:
            bot_x = self.image_x - self.passed_x
        self.new_image_x = bot_x
        super().drawIfNotUp(
            self.image_x, self.image_y,
            bot_x, self.canvas_height
        )
        while self.new_image_y > self.canvas_height:
            self.passed_y += self.canvas_height
            self.new_image_y = self.move_y - self.passed_y
            self.passed_x += self.canvas_height/self.tangens
            self.new_image_x = bot_x
            if self.move_x > 0:
                bot_x = self.image_x + self.passed_x
            else:
                bot_x = self.image_x - self.passed_x
            super().drawIfNotUp(
                self.new_image_x, 0,
                bot_x, self.canvas_height
            )
        self.new_image_x = bot_x
        self.passed_y += self.new_image_y
        self.passed_x += self.new_image_y/self.tangens
        if self.move_x > 0:
            bot_x = self.image_x + self.passed_x
        else:
            bot_x = self.image_x - self.passed_x
        super().drawIfNotUp(
            self.new_image_x, 0,
            bot_x, self.new_image_y
        )
        self.new_image_x, bot_x = bot_x, self.new_image_x


class rightBorderCrossing(borderCrossing):
    def __init__(self, choice, ui):
        super().__init__(choice, ui)
        self.new_image_y = choice.new_image_y
        self.passed_x = self.canvas_width - self.image_x
        self.new_image_x = self.move_x - self.passed_x
        if self.simple_angle == 90:
            self.crossingAtRightAngle()
        else:
            self.crossingAtNotRightAngle()

    def crossingAtRightAngle(self):
        super().drawIfNotUp(
            self.image_x, self.image_y,
            self.canvas_width, self.new_image_y
        )
        while self.new_image_x > self.canvas_width:
            self.passed_x += self.canvas_width
            self.new_image_x = self.move_x - self.passed_x
            super().drawIfNotUp(
                0, self.image_y,
                self.canvas_width, self.new_image_y
            )
        super().drawIfNotUp(
            0, self.image_y,
            self.new_image_x, self.new_image_y
        )

    def crossingAtNotRightAngle(self):
        self.passed_y = self.passed_x*self.tangens
        if self.move_y > 0:
            right_y = self.image_y + self.passed_y
        else:
            right_y = self.image_y - self.passed_y
        self.new_image_y = right_y
        super().drawIfNotUp(
            self.image_x, self.image_y,
            self.canvas_width, right_y
        )
        while self.new_image_x > self.canvas_width:
            self.passed_x += self.canvas_width
            self.new_image_x = self.move_x - self.passed_x
            self.passed_y += self.canvas_width * self.tangens
            self.new_image_y = right_y
            if self.move_y > 0:
                right_y = self.image_y + self.passed_y
            else:
                right_y = self.image_y - self.passed_y
            super().drawIfNotUp(
                0, self.new_image_y,
                self.canvas_width, right_y
            )
        self.new_image_y = right_y
        self.passed_x += self.new_image_x
        self.passed_y += self.new_image_x * self.tangens
        if self.move_y > 0:
            right_y = self.image_y + self.passed_y
        else:
            right_y = self.image_y - self.passed_y
        super().drawIfNotUp(
            0, self.new_image_y,
            self.new_image_x, right_y
        )
        self.new_image_y, right_y = right_y, self.new_image_y


class leftBorderCrossing(borderCrossing):
    def __init__(self, choice, ui):
        super().__init__(choice, ui)
        self.new_image_y = choice.new_image_y
        self.passed_x = self.image_x
        self.new_image_x = self.canvas_width + self.move_x + self.passed_x
        if self.simple_angle == 270:
            self.crossingAtRightAngle()
        else:
            self.crossingAtNotRightAngle()

    def crossingAtRightAngle(self):
        super().drawIfNotUp(
            self.image_x, self.image_y,
            0, self.new_image_y
        )
        while self.new_image_x < 0:
            self.passed_x += self.canvas_width
            self.new_image_x = self.move_x + self.passed_x
            super().drawIfNotUp(
                self.canvas_width, self.image_y,
                0, self.new_image_y
            )
        super().drawIfNotUp(
            self.canvas_width, self.image_y,
            self.new_image_x, self.new_image_y
        )

    def crossingAtNotRightAngle(self):
        self.passed_y = self.passed_x * self.tangens
        if self.move_y > 0:
            left_y = self.image_y + self.passed_y
        else:
            left_y = self.image_y - self.passed_y
        self.new_image_y = left_y
        super().drawIfNotUp(
            self.image_x, self.image_y,
            0, left_y
        )
        while self.new_image_x < 0:
            self.passed_x += self.canvas_width
            self.new_image_x = self.move_x + self.passed_x
            self.passed_y += self.canvas_width * self.tangens
            self.new_image_y = left_y
            if self.move_y > 0:
                left_y = self.image_y + self.passed_y
            else:
                left_y = self.image_y - self.passed_y
            super().drawIfNotUp(
                self.canvas_width, self.new_image_y,
                0, left_y
            )
        self.new_image_y = left_y
        self.passed_x += self.canvas_width - self.new_image_x
        self.passed_y += (self.canvas_width - self.new_image_x) * self.tangens
        if self.move_y > 0:
            left_y = self.image_y + self.passed_y
        else:
            left_y = self.image_y - self.passed_y
        super().drawIfNotUp(
            self.canvas_width, self.new_image_y,
            self.new_image_x, left_y
        )
        self.new_image_y, left_y = left_y, self.new_image_y
