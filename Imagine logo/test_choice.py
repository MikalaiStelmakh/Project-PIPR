import tkinter as tk
import math
from gui import MainWindow


def monkeypatchCommand(monkeypatch, window, command):
    monkeypatch.setattr('gui.MainWindow.getInput', command)
    window.main("<Return>")


def closeApplication(app):
    app.master.destroy()


def test_move_north(monkeypatch):
    def move(a):
        return 'move 100'

    root = tk.Tk()
    window = MainWindow(root)
    image_x = window.image_x
    image_y = window.image_y
    monkeypatchCommand(monkeypatch, window, move)
    assert window.image_x == image_x
    assert window.image_y == image_y - 100
    closeApplication(window)


def test_move_east(monkeypatch):
    def turn(a):
        return 'turn 90'

    def move(a):
        return 'move 100'

    root = tk.Tk()
    window = MainWindow(root)
    image_x = window.image_x
    image_y = window.image_y
    monkeypatchCommand(monkeypatch, window, turn)
    assert window.image_x == image_x
    assert window.image_y == image_y
    monkeypatchCommand(monkeypatch, window, move)
    assert window.image_x == image_x + 100
    assert window.image_y == image_y
    closeApplication(window)


def test_move_at_angle(monkeypatch):
    def turn(a):
        return 'turn 30'

    def move(a):
        return 'move 100'

    root = tk.Tk()
    window = MainWindow(root)
    image_x = window.image_x
    image_y = window.image_y
    monkeypatchCommand(monkeypatch, window, turn)
    assert window.image_x == image_x
    assert window.image_y == image_y
    monkeypatchCommand(monkeypatch, window, move)
    move_x = 100 * math.sin(math.radians(30))
    move_y = -(100 * math.cos(math.radians(30)))
    assert round(window.image_x, 2) == round(image_x + move_x, 2)
    assert round(window.image_y, 2) == round(image_y + move_y, 2)
    closeApplication(window)
