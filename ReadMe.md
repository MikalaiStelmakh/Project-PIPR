# User guide

### What is Imagine logo

Imagine logo is an entertainment program for creating 2D drawings by giving commands to a turtle.

### Getting started

To start using the program go to the `gui.py` file and run the code.

### Controlling turtle

To <u>move</u> the turtle use command `move [units]`. By default turtle faces north and there it will go. To <u>turn</u> the turtle clockwise use command `turn [angle]`. The turtle will now move in the direction you specified. By default, the turtle leaves a trail when it moves, to change this, <u>pick up</u> the turtle using command `up`. To <u>put</u> it <u>down</u> use command `down`.

### Menu

1. **File menu**  

   **1.1 New**

   Returns everything to its original position. **Attention!** Make sure all changes are saved before creating a new file.

   **2.2 Open**

   Opens a text file with commands and executes them. **Attention!** All undefined commands will be skipped.

   **2.3 Save image**

   Opens a window for choosing a direction to save the image obtained while moving the turtle.

   **2.4 Save txt**

   Opens a window for choosing a direction to save commands in `.txt` format obtained while moving the turtle.

   **2.5 Exit**

   Closes the application. **Attention!** Make sure all changes are saved before closing the application.

2. **Help**

   **2.1 User guide**

   Shows user guide.
   
   **2.2 For developers**
   
   Shows technical documentation.
   
   

# Technical documentation

### <a name='gui'>`gui`</a>

The main program file. Initialization of the `MainWindow` class creates a `UI` class (from ui_logomocja.py module) object responsible for the main program interface, creates turtle image and calls `createMenu` and `initialValues` methods. Calls `main` method when the command is entered.

`createMenu` method creates a `Menu` class (from [menu.py](#menu)) object responsible for creating and managing top program menu.

`initialValues` method sets the initial values of the variables when the program starts.

`main` method creates a `InputProcessing` class (from [InputProcessing.py](#InputProcessing)) object responsible for processing the input.

### <a name='menu'>`menu`</a>

Module responsible for managing top program menu.

### <a name='inputProcessing'>`inputProcessing`</a>

Module responsible for processing the input. If the input is correct, depending on it, creates an object of `Move` or `Turn` class (from [logomocja_choice.py](#Logomocja_choice)). Shows an error if the input is incorrect.

### <a name='choice'>`choice`</a>

##### `Turn` class:

Initialized when the `turn` command is given. Rotates the image, sets the anchor.

##### `Move` class:

Initialized when the `move` command is given. Sets new coordinates of the image, moves it and draws a line if the turtle is down. Creates  a `CrossedBorder` class (from `bordersCrossing.py`) object if canvas border is crossed while moving the image.