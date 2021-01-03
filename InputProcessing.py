from logomocja_choice import Turn, Move


class InputProcessing:
    def __init__(self, master):
        self.chooseCommand(master)

    def splitInput(self, master, message):
        splitted_message = message.split()
        master.command = splitted_message[0]
        master.units = float(splitted_message[1])

    def valueErrorText(self, master):
        master.text = (
            'ValueError\n'
            'Example of a correct entry: naprzod 100'
            )

    def undefinedCommandText(self, master):
        master.text = (
            f'Undefined command: {master.result}\n'
            'Example of a correct entry: obrot 90'
            )

    def indexErrorText(self, master):
        if master.result == 'podnies' or master.result == 'opusc':
            master.text = master.result
        else:
            master.text = (
                f'Undefined command: {master.result}\n'
                'Example of a correct entry: obrot 90'
                )

    def chooseCommand(self, master):
        if master.result == 'podnies':
            master.is_up = True
        elif master.result == 'opusc':
            master.is_up = False
        try:
            self.splitInput(master, master.result)
            if master.command == 'obrot':
                master.text = master.result
                self.turnCommand(master)
            elif master.command == 'naprzod':
                master.text = master.result
                self.moveCommand(master)
            elif master.command == 'podnies' or master.command == 'opusc':
                self.valueErrorText(master)
            else:
                self.undefinedCommandText(master)
        except IndexError:
            self.indexErrorText(master)
        except ValueError:
            self.valueErrorText(master)
        self.returnEntry(master)

    def returnEntry(self, master):
        master.label.config(text=master.text)
        master.entry.delete(0, 'end')

    def turnCommand(self, master):
        turn = Turn(master)
        master.previous_angle = turn.angle
        master.simple_angle = turn.simplifyAngle()
        master.direction = turn.direction
        master.anchor = turn.setImageAnchor()
        turn.setRotateValue(master.units)
        turn.setResizeValue()
        master.canvas_for_image.image = turn.createImage()
        master.imagesprite = turn.drawImage()

    def moveCommand(self, master):
        move = Move(master)
        master.image_x, master.image_y = move.setNewCoordinates()
        move.moveImage()
        move.drawLine()
