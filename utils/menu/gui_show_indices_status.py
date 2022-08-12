import customtkinter
import tkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))


class GUIShowIndicesStatus(customtkinter.CTkToplevel):
    def __init__(self, indices_status):
        super().__init__()

        self.title("elasticfetch - Indices Status")
        self.geometry("900x520")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=1)

        # root window is the parent window
        fram = tkinter.Frame(self)
        fram.grid(row=0, column=0, sticky="we")

        # adding label to search box
        tkinter.Label(fram, text='Text to find:').grid(row=0, column=0)

        # adding of single line text box
        search_term = tkinter.Entry(fram)

        # positioning of text box
        search_term.grid(row=0, column=1)

        # setting focus
        search_term.focus_set()

        # adding of search button
        butt = tkinter.Button(fram, text='Find')
        butt.grid(row=0, column=2)
        butt.config(command=lambda: self.find_in_textbox(textbox=tk_textbox, search_term=search_term))

        # create scrollable textbox
        tk_textbox = tkinter.Text(self, highlightthickness=0)
        tk_textbox.grid(row=1, column=0, sticky="nsew")
        tk_textbox.insert(tkinter.INSERT, indices_status)

        # create CTk scrollbar
        ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self, command=tk_textbox.yview)
        ctk_textbox_scrollbar.grid(row=1, column=1, sticky="ns")

        # connect textbox scroll event to CTk scrollbar
        tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    def find_in_textbox(self, textbox, search_term):
        # remove tag 'found' from index 1 to END
        textbox.tag_remove('found', '1.0', tkinter.END)

        # returns to widget currently in focus
        s = search_term.get()
        if s:
            idx = '1.0'
            while 1:
                # searches for desired string from index 1
                idx = textbox.search(s, idx, nocase=1,
                                     stopindex=tkinter.END)
                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '%s+%dc' % (idx, len(s))

                # overwrite 'Found' at idx
                textbox.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as red
            textbox.tag_config('found', foreground='red')
        search_term.focus_set()



