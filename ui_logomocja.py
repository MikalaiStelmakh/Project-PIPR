import tkinter as tk


class UI(tk.Frame):
    def setupUi(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, height=700, width=800)
        self.canvas.pack()
        self.menu = tk.Menu(self.master)
        self.fileMenu = tk.Menu(self.menu, tearoff=0)
        self.master.config(menu=self.menu)
        self.menu.add_cascade(label='File', menu=self.fileMenu)
        self.canvas_for_image = tk.Canvas(master, bg='white')
        self.canvas_for_image.place(
            relx=0.5,
            rely=0.5,
            width=700,
            height=525,
            anchor='center')
        self.canvas_for_image.update()
        self.label_frame = tk.Frame(master, borderwidth=2, relief="sunken")
        self.label_frame.place(rely=0.9, relwidth=1, relheight=0.07)
        self.label = tk.Label(
            self.label_frame,
            text='Hello\n',
            fg='black',
            font=("Modern", 10),
            justify='left',
            bd=4)
        self.label.pack(side='top', anchor='w')
        self.entry_frame = tk.Frame(master)
        self.entry_frame.place(rely=0.97, relwidth=1.1, relheight=0.03)
        self.entry = tk.Entry(self.entry_frame, bg='white', fg='black')
        self.entry.place(relwidth=1)
