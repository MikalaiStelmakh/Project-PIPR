from choice import Turn, Move
from random import randint


# Generates an example of a correct entry.
def getExample():
    commands = ['move', 'turn', 'up', 'down']
    command = commands[randint(0, 3)]
    if command in ["move", "turn"]:
        units = randint(1, 10)*10
    else:
        units = None
    return f'{command} {units if units else ""}'


class InputProcessing:
    def __init__(self, ui, gui, text):
        self.ui = ui
        self.gui = gui
        self.text = text
        self.chooseCommand()

    # Splits the input into a command and units.
    def splitInput(self, message):
        splitted_message = message.split()
        command = splitted_message[0]
        units = float(splitted_message[1])
        return command, units

    def valueErrorText(self):
        text = 'ValueError\n'
        self.gui.errors += 1
        return text

    def undefinedCommandText(self):
        text = f'Undefined command: {self.text}\n'
        self.gui.errors += 1
        return text

    def indexErrorText(self):
        text = 'IndexError\n'
        self.gui.errors += 1
        return text

    # Checks the input and selects the command depending on it.
    def chooseCommand(self):
        if self.text == 'up':
            self.gui.is_up = True
        elif self.text == 'down':
            self.gui.is_up = False
        example = f'Example of a correct entry: {getExample()}'
        try:
            command, units = self.splitInput(self.text)
            if command == 'turn':
                text = self.text
                Turn(self.ui, self.gui, units)
            elif command == 'move':
                text = self.text
                Move(self.ui, self.gui, units)
            # if entry is "up [units]" or "down [units]"
            elif command == 'up' or command == 'down':
                raise IndexError()
            # if undefined command is entered
            else:
                text = self.undefinedCommandText() + example
        # if a command is entered without units
        except IndexError:
            if self.text == 'up' or self.text == 'down':
                text = self.text
            else:
                text = self.indexErrorText() + example
        # if units is not a number
        except ValueError:
            text = self.valueErrorText() + example
        self.returnEntry(text)

    def returnEntry(self, text):
        self.ui.label.config(text=text)
        self.ui.entry.delete(0, 'end')
