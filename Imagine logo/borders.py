import math

"""
Functions used to set new coordinates of the image,
if one or more borders of the canvas are crossed during movement.
"""


def leftBorderCrossed(img_x, img_y, canvas_height, canvas_width, move_y, angle):
    x = -img_x
    y = x*math.tan(math.radians(angle))
    if move_y > 0:
        y = -y
    if img_y + y < 0:
        y = -img_y
        x = y/math.tan(math.radians(angle))
        x1 = img_x + x
        y1 = 0
        new_y = canvas_height
        new_x = x1
    elif img_y + y > canvas_height:
        y = canvas_height - img_y
        x = -y/math.tan(math.radians(angle))
        x1 = img_x + x
        y1 = canvas_height
        new_y = 0
        new_x = x1
    else:
        x1 = 0
        y1 = img_y + y
        new_y = y1
        new_x = canvas_width
    return x, y, x1, y1, new_x, new_y


def rightBorderCrossed(img_x, img_y, canvas_height, canvas_width, move_y, angle):
    x = canvas_width - img_x
    y = x*math.tan(math.radians(angle))
    if move_y < 0: y = -y
    if img_y + y < 0:
        y = -img_y
        x = -y/math.tan(math.radians(angle))
        x1 = img_x + x
        y1 = 0
        new_y = canvas_height
        new_x = x1
    elif img_y + y > canvas_height:
        y = canvas_height - img_y
        x = y/math.tan(math.radians(angle))
        x1 = img_x + x
        y1 = canvas_height
        new_y = 0
        new_x = x1
    else:
        x1 = canvas_width
        y1 = img_y + y
        new_y = y1
        new_x = 0
    return x, y, x1, y1, new_x, new_y


def topOrBotBorderCrossed(img_x, img_y, canvas_height, canvas_width, move_y):
    x = 0
    if move_y > 0:
        y = canvas_height - img_y
        y1 = canvas_height
        new_y = 0
    else:
        y = -img_y
        y1 = 0
        new_y = canvas_height
    x1 = img_x
    new_x = img_x
    return x, y, x1, y1, new_x, new_y
