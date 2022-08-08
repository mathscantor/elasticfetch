import tkinter

class GUIMenu:

    def __init__(self, request_sender, converter, input_validation, parser):
        self.description = "GUI Menu for v3.0.0+"
        self.main_window = tkinter.Tk()
        self.request_sender = request_sender
        self.converter = converter
        self.input_validation = input_validation
        self.parser = parser
        self.init_main_window()

    def init_main_window(self):

        self.main_window.title("elasticfetch")
        self.main_window.geometry('900x900')
        self.main_window.resizable(True, True)

    def show_menu(self):
        option_1_button = tkinter.Button(self.main_window, text="Show Indices Status", command=self.show_indices_status)
        option_1_button.pack()
        self.main_window.mainloop()

    def show_indices_status(self):
        indices_status_window = tkinter.Tk()
        indices_status_window.title("Indices Status")
        indices_status_window.geometry('900x900')
        indices_status_window.resizable(True, True)

        scrollbar_vertical = tkinter.Scrollbar(indices_status_window)
        scrollbar_vertical.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar_horizontal = tkinter.Scrollbar(indices_status_window, orient=tkinter.HORIZONTAL)
        scrollbar_horizontal.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        indices_status = self.request_sender.get_indices_status()
        print(indices_status)
        text = tkinter.Text(indices_status_window,
                            yscrollcommand=scrollbar_vertical.set,
                            xscrollcommand=scrollbar_horizontal.set,
                            height=500,
                            width=350,
                            wrap=tkinter.NONE,
                            font=('Arial 11'))
        text.pack(fill=tkinter.BOTH, expand=0)
        text.insert(tkinter.END, indices_status)

        scrollbar_vertical.config(command=text.yview)
        scrollbar_horizontal.config(command=text.xview)

        indices_status_window.mainloop()
        return
