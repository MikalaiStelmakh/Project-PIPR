from logomocja_choice import Turn, Move


class InputProcessing:
    def __init__(self, ui, gui):
        self.ui = ui
        self.gui = gui
        self.chooseCommand()

    def splitInput(self, message):
        splitted_message = message.split()
        command = splitted_message[0]
        units = float(splitted_message[1])
        return command, units

    def valueErrorText(self):
        text = (
            'ValueError\n'
            'Example of a correct entry: naprzod 100'
            )
        self.gui.errors += 1
        return text

    def undefinedCommandText(self):
        text = (
            f'Undefined command: {self.gui.text}\n'
            'Example of a correct entry: obrot 90'
            )
        self.gui.errors += 1
        return text

    def indexErrorText(self):
        if self.gui.text == 'podnies' or self.gui.text == 'opusc':
            text = self.gui.text
        else:
            text = (
                f'Undefined command: {self.gui.text}\n'
                'Example of a correct entry: obrot 90'
                )
        self.gui.errors += 1
        return text

    def chooseCommand(self):
        if self.gui.text == 'podnies':
            self.gui.is_up = True
        elif self.gui.text == 'opusc':
            self.gui.is_up = False
        try:
            command, units = self.splitInput(self.gui.text)
            if command == 'obrot':
                text = self.gui.text
                self.turnCommand(units)
            elif command == 'naprzod':
                text = self.gui.text
                self.moveCommand(units)
            elif command == 'podnies' or command == 'opusc':
                text = self.valueErrorText()
            else:
                text = self.undefinedCommandText()
        except IndexError:
            text = self.indexErrorText()
        except ValueError:
            text = self.valueErrorText()
        self.returnEntry(text)

    def returnEntry(self, text):
        self.ui.label.config(text=text)
        self.ui.entry.delete(0, 'end')

    def turnCommand(self, text):
        turn = Turn(self.ui, self.gui, text)
        turn.simplifyAngle()
        turn.setImageAnchor()
        turn.createImage()
        turn.drawImage()

    def moveCommand(self, text):
        Move(self.ui, self.gui, text)
