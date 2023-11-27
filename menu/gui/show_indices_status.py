import customtkinter
import tkinter


class GUIShowIndicesStatus(customtkinter.CTkToplevel):
    def __init__(self, indices_status):
        super().__init__()

        self.title("elasticfetch - Indices Status")
        self.geometry("1120x480")
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

        self.total_count_label = tkinter.Label(master=self.frame, height=1, font=customtkinter.CTkFont(family="Arial", size=15))
        self.total_count_label.grid(row=0, column=3)
        self.total_count_label.grid_forget()

        self.arrow_down_button = tkinter.Button(self.frame, text="↓", font=customtkinter.CTkFont(family="Arial", size=12),
                                                command=self.get_search_result_next)
        self.arrow_down_button.grid(row=0, column=5)
        self.arrow_down_button.grid_forget()

        self.arrow_up_button = tkinter.Button(self.frame, text="↑", font=customtkinter.CTkFont(family="Arial", size=12),
                                              command=self.get_search_result_before)
        self.arrow_up_button.grid(row=0, column=5)
        self.arrow_up_button.grid_forget()

        # create scrollable textbox
        self.textbox = tkinter.Text(self,
                                    highlightthickness=0,
                                    wrap="none",
                                    font=customtkinter.CTkFont(family="Consolas", size=15))
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.insert(tkinter.INSERT, indices_status)

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

    def find_in_textbox(self, search_term) -> list:
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

    def get_search_result_next(self):
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

    def get_search_result_before(self):
        self.current_result_index -= 1
        self.current_result_index = self.current_result_index % self.total_num_results
        self.textbox.see(self.idx_list[self.current_result_index][1])
        self.textbox.tag_remove("highlight",
                                self.idx_list[(self.current_result_index + 1) % self.total_num_results][0],
                                self.idx_list[(self.current_result_index + 1) % self.total_num_results][1])
        self.textbox.tag_add("highlight", self.idx_list[self.current_result_index][0], self.idx_list[self.current_result_index][1])
        self.total_count_label.configure(text="{} of {}".format(self.current_result_index + 1, self.total_num_results))
        return
