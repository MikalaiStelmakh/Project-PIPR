import tkinter as tk
from gui import MainWindow


def monkeypatchCommand(monkeypatch, window, command):
    monkeypatch.setattr('gui.MainWindow.getInput', command)
    window.main("<Return>")


def closeApplication(app):
    app.master.destroy()


def test_correct_input(monkeypatch):
    def move(a):
        return 'move 100'

    def turn(a):
        return 'turn 90'

    def up(a):
        return 'up'

    def down(a):
        return 'down'

    mockFunctions = [move, turn, up, down]
    root = tk.Tk()
    window = MainWindow(root)
    for mockFunction in mockFunctions:
        monkeypatchCommand(monkeypatch, window, mockFunction)
        assert window.ui.label.cget("text") == mockFunction(window)
    closeApplication(window)


def test_incorrect_input(monkeypatch):
    def incorrect_input_undefined_command(a):
        return 'jump 100'

    def incorrect_input_index_error(a):
        return 'move'

    def incorrect_input_value_error(a):
        return 'move a'

    def getExample():
        return 'move 100'

    undefined_command_text = 'Undefined command: jump 100\n'
    index_error_text = 'IndexError\n'
    value_error_text = 'ValueError\n'
    textList = [
        undefined_command_text,
        index_error_text,
        value_error_text
    ]
    mockFunctions = [
        incorrect_input_undefined_command,
        incorrect_input_index_error,
        incorrect_input_value_error]

    root = tk.Tk()
    window = MainWindow(root)
    for mockFunction, text in zip(mockFunctions, textList):
        monkeypatch.setattr('inputProcessing.getExample', getExample)
        monkeypatchCommand(monkeypatch, window, mockFunction)
        example = f'Example of a correct entry: {getExample()}'
        assert window.ui.label.cget("text") == text + example
    closeApplication(window)
