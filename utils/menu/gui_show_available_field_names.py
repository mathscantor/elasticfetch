import customtkinter
import tkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))


class GUIShowAvailableFields(customtkinter.CTkToplevel):
    def __init__(self,
                 current_index: str,
                 parent_field_to_type_dict: dict):
        super().__init__()

        self.title("elasticfetch - Available Fields for {}".format(current_index))
        self.geometry("800x400")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_columnconfigure(0, weight=1)

        # root window is the parent window
        self.frame = tkinter.Frame(self)
        self.frame.grid(row=0, column=0, sticky="ew")

        # adding label to search box
        tkinter.Label(self.frame, text='Text to find:').grid(row=0, column=0)

        # adding of single line text box
        search_term = tkinter.Entry(self.frame)

        # positioning of text box
        search_term.grid(row=0, column=1)

        # setting focus
        search_term.focus_set()

        # adding of search button
        butt = tkinter.Button(self.frame, text='Find')
        butt.grid(row=0, column=2)
        butt.config(command=lambda: self.find_in_textbox(textbox=tk_textbox, search_term=search_term))

        # create scrollable textbox
        tk_textbox = tkinter.Text(self, highlightthickness=0)
        tk_textbox.grid(row=1, column=0, sticky="nsew")

        # Content
        available_fields_pretty = "{:<30} {:<20} {:<30}\n".format('TOP LEVEL PARENT', 'TYPE', 'ALL RELATED FIELDS')
        available_fields_pretty += "{:<30} {:<20} {:<30}\n".format('----------------', '----', '------------------')

        for top_parent_field in parent_field_to_type_dict.keys():
            has_printed_parent = False
            for field_type in parent_field_to_type_dict[top_parent_field].keys():
                if not has_printed_parent:
                    available_fields_pretty += "{:<30} {:<20} {:<30}\n".format(top_parent_field, field_type,
                                                                               ', '.join(parent_field_to_type_dict[
                                                                                             top_parent_field][
                                                                                             field_type]))
                    has_printed_parent = True
                else:
                    available_fields_pretty += "{:<30} {:<20} {:<30}\n".format('', field_type,
                                                                               ', '.join(parent_field_to_type_dict[
                                                                                             top_parent_field][
                                                                                             field_type]))
                available_fields_pretty += "\n"
            available_fields_pretty += "―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n"

        tk_textbox.insert(tkinter.INSERT, available_fields_pretty)
        tk_textbox.configure(state=tkinter.DISABLED)

        # create CTk scrollbar
        ctk_textbox_yscrollbar = customtkinter.CTkScrollbar(self, command=tk_textbox.yview)
        ctk_textbox_yscrollbar.grid(row=1, column=1, sticky="ns")

        # connect textbox scroll event to CTk scrollbar
        tk_textbox.configure(yscrollcommand=ctk_textbox_yscrollbar.set)

    def find_in_textbox(self, textbox, search_term):
        # remove tag 'found' from index 1 to END
        textbox.tag_remove('found', '1.0', tkinter.END)

        # returns to widget currently in focus
        s = search_term.get()
        total = 0
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
                total += 1

            # mark located string as red
            textbox.tag_config('found', foreground='red')
        search_term.focus_set()

        total_count_textbox = tkinter.Text(master=self.frame, height=1)
        total_count_textbox.grid(row=0, column=3)
        total_count_textbox.insert(tkinter.INSERT, "Found {} results!".format(total))
        total_count_textbox.configure(state=tkinter.DISABLED)
        return



