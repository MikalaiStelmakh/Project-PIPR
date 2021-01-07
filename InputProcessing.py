from logomocja_choice import Turn, Move


class InputProcessing:
    def __init__(self, master):
        self.master = master
        self.chooseCommand()

    def splitInput(self, message):
        splitted_message = message.split()
        self.master.command = splitted_message[0]
        self.master.units = float(splitted_message[1])

    def valueErrorText(self):
        self.master.text = (
            'ValueError\n'
            'Example of a correct entry: naprzod 100'
            )

    def undefinedCommandText(self):
        self.master.text = (
            f'Undefined command: {self.master.result}\n'
            'Example of a correct entry: obrot 90'
            )

    def indexErrorText(self):
        if self.master.result == 'podnies' or self.master.result == 'opusc':
            self.master.text = self.master.result
        else:
            self.master.text = (
                f'Undefined command: {self.master.result}\n'
                'Example of a correct entry: obrot 90'
                )

    def chooseCommand(self):
        if self.master.result == 'podnies':
            self.master.is_up = True
        elif self.master.result == 'opusc':
            self.master.is_up = False
        try:
            self.splitInput(self.master.result)
            if self.master.command == 'obrot':
                self.master.text = self.master.result
                self.turnCommand()
            elif self.master.command == 'naprzod':
                self.master.text = self.master.result
                self.moveCommand()
            elif self.master.command == 'podnies' or self.master.command == 'opusc':
                self.valueErrorText()
            else:
                self.undefinedCommandText()
        except IndexError:
            self.indexErrorText()
        except ValueError:
            self.valueErrorText()
        self.returnEntry()

    def returnEntry(self):
        self.master.label.config(text=self.master.text)
        self.master.entry.delete(0, 'end')

    def turnCommand(self):
        turn = Turn(self.master)
        turn.simplifyAngle()
        turn.setImageAnchor()
        turn.createImage()
        turn.drawImage()

    def moveCommand(self):
        move = Move(self.master)
        move.setNewCoordinates()
