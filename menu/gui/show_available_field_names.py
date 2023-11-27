import customtkinter
import tkinter
import os
from typing import *

PATH = os.path.dirname(os.path.realpath(__file__))


class GUIShowAvailableFields(customtkinter.CTkToplevel):
    def __init__(self,
                 current_index: str,
                 parent_field_to_type_dict: dict):
        super().__init__()

        self.title("elasticfetch - Available Fields for {}".format(current_index))
        self.geometry("800x400")
        # self.resizable(False, False)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=97)
        self.grid_columnconfigure(0, weight=1)
        self.idx_list = []
        self.current_result_index = 0
        self.total_num_results = 0

        # root window is the parent window
        self.frame = tkinter.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # adding label to search box
        tkinter.Label(self.frame, text='Search:', font=customtkinter.CTkFont(family="Arial", size=15)).grid(row=0, column=0)

        # adding of single line text box
        search_term = tkinter.Entry(self.frame)

        # positioning of text box
        search_term.grid(row=0, column=1)

        # setting focus
        search_term.focus_set()

        # adding of search button
        find_button = tkinter.Button(self.frame, text='Find', font=customtkinter.CTkFont(family="Arial", size=15))
        find_button.grid(row=0, column=2)
        find_button.config(command=lambda: self.find_in_textbox(search_term=search_term))

        self.total_count_label = tkinter.Label(master=self.frame, height=1,
                                               font=customtkinter.CTkFont(family="Arial", size=15))
        self.total_count_label.grid(row=0, column=3)
        self.total_count_label.grid_forget()

        self.arrow_down_button = tkinter.Button(self.frame, text="↓", font=customtkinter.CTkFont(family="Arial", size=15),
                                                command=self.get_search_result_next)
        self.arrow_down_button.grid(row=0, column=5)
        self.arrow_down_button.grid_forget()

        self.arrow_up_button = tkinter.Button(self.frame, text="↑", font=customtkinter.CTkFont(family="Arial", size=15),
                                              command=self.get_search_result_before)
        self.arrow_up_button.grid(row=0, column=5)
        self.arrow_up_button.grid_forget()

        # create scrollable textbox
        self.textbox = tkinter.Text(self,
                                    wrap="none",
                                    highlightthickness=0,
                                    font=customtkinter.CTkFont(family="Consolas", size=15))
        self.textbox.grid(row=1, column=0, sticky="nsew")

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
            available_fields_pretty += "\n"

        self.textbox.insert(tkinter.INSERT, available_fields_pretty)
        self.textbox.configure(state=tkinter.DISABLED)

        # create CTk scrollbar
        yscrollbar = customtkinter.CTkScrollbar(self,
                                                orientation="vertical",
                                                command=self.textbox.yview)
        yscrollbar.grid(row=1, column=1, sticky="ns")

        xscrollbar = customtkinter.CTkScrollbar(self,
                                                orientation="horizontal",
                                                command=self.textbox.xview)
        xscrollbar.grid(row=2, column=0, sticky="we")

        # connect textbox scroll event to CTk scrollbar
        self.textbox.configure(yscrollcommand=yscrollbar.set,
                               xscrollcommand=xscrollbar.set,
                               state=tkinter.DISABLED)

    def find_in_textbox(self,
                        search_term: tkinter.Entry) -> None:
        """
        Find and highlight occurrences of a search term in the textbox.

        This method searches for the specified search term in the textbox content,
        highlights the occurrences, and provides navigation buttons for easy traversal.

        :param search_term: The tkinter Entry widget containing the search term.
        :type search_term: tkinter.Entry

        :return: None
        :rtype: None
        """
        # remove tag 'found' from index 1 to END
        self.textbox.tag_remove('found', '1.0', tkinter.END)
        self.textbox.tag_remove("highlight", '1.0', tkinter.END)

        # returns to widget currently in focus
        s = search_term.get()
        self.total_num_results = 0
        self.idx_list.clear()
        if s:
            idx = '1.0'
            while 1:
                # searches for desired string from index 1
                idx = self.textbox.search(s, idx, nocase=1,
                                          stopindex=tkinter.END)
                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '%s+%dc' % (idx, len(s))

                # overwrite 'Found' at idx
                self.textbox.tag_add('found', idx, lastidx)
                self.idx_list.append((idx, lastidx))
                idx = lastidx
                self.total_num_results += 1

            # mark located string as red
            self.textbox.tag_config('found', foreground='red')
        search_term.focus_set()
        self.total_count_label.grid(row=0, column=3)
        if self.total_num_results == 0:
            self.total_count_label.configure(text="No results!")
            self.arrow_up_button.grid_forget()
            self.arrow_down_button.grid_forget()
        if self.total_num_results > 0:
            self.total_count_label.configure(text="1 of {}".format(self.total_num_results))
            self.current_result_index = 0
            self.textbox.see(self.idx_list[self.current_result_index][1])
            self.textbox.tag_add("highlight", self.idx_list[self.current_result_index][0], self.idx_list[self.current_result_index][1])
            self.textbox.tag_configure("highlight", background="yellow")
            self.arrow_down_button.grid(row=0, column=4)
            self.arrow_up_button.grid(row=0, column=5)
        return

    def get_search_result_next(self) -> None:
        """
        Navigate to the next search result in the textbox.

        This method increments the current result index, wraps around if necessary,
        and updates the textbox display to highlight the next search result.

        :return: None
        :rtype: None
        """
        self.current_result_index += 1
        self.current_result_index = self.current_result_index % self.total_num_results
        self.textbox.see(self.idx_list[self.current_result_index][1])
        self.textbox.tag_remove("highlight",
                                self.idx_list[self.current_result_index - 1][0],
                                self.idx_list[self.current_result_index - 1][1])
        self.textbox.tag_add("highlight",
                             self.idx_list[self.current_result_index][0],
                             self.idx_list[self.current_result_index][1])
        self.total_count_label.configure(text="{} of {}".format(self.current_result_index + 1, self.total_num_results))
        return

    def get_search_result_before(self) -> None:
        """
        Navigate to the previous search result in the textbox.

        This method decrements the current result index, wraps around if necessary,
        and updates the textbox display to highlight the previous search result.

        :return: None
        :rtype: None
        """
        self.current_result_index -= 1
        self.current_result_index = self.current_result_index % self.total_num_results
        self.textbox.see(self.idx_list[self.current_result_index][1])
        self.textbox.tag_remove("highlight",
                                self.idx_list[(self.current_result_index + 1) % self.total_num_results][0],
                                self.idx_list[(self.current_result_index + 1) % self.total_num_results][1])
        self.textbox.tag_add("highlight", self.idx_list[self.current_result_index][0], self.idx_list[self.current_result_index][1])
        self.total_count_label.configure(text="{} of {}".format(self.current_result_index + 1, self.total_num_results))
        return
