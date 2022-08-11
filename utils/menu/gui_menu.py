import customtkinter
import tkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUIMenu:

    def __init__(self,
                 request_sender,
                 converter,
                 input_validation,
                 parser):
        self.request_sender = request_sender
        self.primary_app_window = customtkinter.CTk()
        self.app_windows = [self.primary_app_window]
        self.frame_left = None
        self.frame_right = None
        self.frame_info = None
        self.show_indices_status_button = None
        self.current_index_label = None
        self.theme_optionmenu = None
        self.current_index_optionmenu = None
        self.indices_status = "placeholder"
        self.current_index = "N/A"
        self.index_list = ["placeholder"]
        self.primary_app_window.protocol("WM_DELETE_WINDOW", self.on_closing_primary_app_window)
        self.available_themes = ["Light Theme", "Dark Theme", "System Default"]
        self.init_primary_app_window()
        self.init_frames()
        self.init_indices()

    def init_primary_app_window(self):
        self.primary_app_window.title("elasticfetch - Main")
        self.primary_app_window.geometry("1080x520")

        # configure grid layout (2x1)
        self.primary_app_window.grid_columnconfigure(1, weight=1)
        self.primary_app_window.grid_rowconfigure(0, weight=1)
        return

    def init_frames(self):
        # ---------------------LEFT FRAME--------------------- #
        self.frame_left = customtkinter.CTkFrame(master=self.primary_app_window,
                                                 width=180)
        self.frame_left.grid(row=0, column=0, sticky="nswe", pady=10)

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        # ---------------------RIGHT FRAME--------------------- #
        self.frame_right = customtkinter.CTkFrame(master=self.primary_app_window)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # configure grid layout (3x7)
        self.frame_right.grid_columnconfigure((0, 1), weight=1)
        self.frame_right.grid_columnconfigure(2, weight=0)
        self.frame_right.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.grid_rowconfigure(7, weight=1)

        # ---------------------INFO FRAME--------------------- #
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")
        return

    def init_indices(self):

        # Clean up properly per refresh
        del self.indices_status
        del self.index_list

        self.indices_status = self.request_sender.get_indices_status()
        temp_list = self.indices_status.split("\n")[1:-1]
        i = 1
        self.index_list = []
        for entry in temp_list:
            index_name = entry.split()[2]
            self.index_list.append(index_name)
            i += 1
        return

    def show_menu(self):

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Options",
                                              text_font=("Arial", 15))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        # Buttons
        self.show_indices_status_button = customtkinter.CTkButton(master=self.frame_left,
                                                                  text="Show Indices Status",
                                                                  command=self.show_indices_status)
        self.show_indices_status_button.grid(row=2, column=0, pady=10, padx=20)



        # Theme Option Menu
        self.theme_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                            values=self.available_themes,
                                                            command=self.change_appearance_mode)
        self.theme_optionmenu.grid(row=10, column=0, sticky="s")
        self.theme_optionmenu.set("Dark Theme")

        # Selected Index Option Menu
        self.current_index_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Selected Index:",
                                                          text_font=("Arial", 11))  # font name and size in px
        self.current_index_label.grid(row=0, column=2, pady=5, padx=0)
        self.current_index_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_info,
                                                                    values=self.index_list,
                                                                    command=self.set_current_index)
        self.current_index_optionmenu.set("N/A")
        self.current_index_optionmenu.grid(row=0, column=3, pady=5, padx=0)

        self.main_timestamp_field_name_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Main Timestamp Field:",
                                                          text_font=("Arial", 11))  # font name and size in px
        self.main_timestamp_field_name_label.grid(row=0, column=2, pady=5, padx=0)
        self.main_timestamp_field_name = customtkinter.CTkOptionMenu(master=self.frame_right,
                                                                    values=self.index_list,
                                                                    command=self.set_current_index)
        self.main_timestamp_field_name.set("@timestamp")
        self.main_timestamp_field_name.grid(row=7, column=0, pady=0, padx=10, sticky='w')

        # show window
        self.primary_app_window.mainloop()
        return

    def change_appearance_mode(self, new_appearance_mode):
        if new_appearance_mode not in self.available_themes:
            customtkinter.set_appearance_mode("System")
            return
        value = ""
        if new_appearance_mode == "Light Theme":
            value = "Light"
        elif new_appearance_mode == "Dark Theme":
            value = "Dark"
        elif new_appearance_mode == "System Default":
            value = "System"
        customtkinter.set_appearance_mode(value)
        return

    def set_current_index(self, index_choice):
        self.current_index = index_choice
        return

    def show_indices_status(self):
        temp_app_window = customtkinter.CTk()
        temp_app_window.protocol("WM_DELETE_WINDOW", func=lambda: self.close_app_window(temp_app_window))

        temp_app_window.title("elasticfetch - Indices Status")
        temp_app_window.geometry("780x520")

        temp_app_window.grid_rowconfigure(0, weight=1)
        temp_app_window.grid_columnconfigure(0, weight=1)

        # create scrollable textbox

        tk_textbox = customtkinter.CTkTextbox(temp_app_window, highlightthickness=0)
        tk_textbox.grid(row=0, column=0, sticky="nsew")
        tk_textbox.insert(tkinter.INSERT, self.indices_status)

        # create CTk scrollbar
        ctk_textbox_scrollbar = customtkinter.CTkScrollbar(temp_app_window, command=tk_textbox.yview)
        ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

        # connect textbox scroll event to CTk scrollbar
        tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

        self.app_windows.append(temp_app_window)
        temp_app_window.mainloop()
        return

    def close_app_window(self, app_window: customtkinter.CTk):
        self.app_windows.remove(app_window)
        app_window.destroy()
        return

    '''
    Closes every app window if the primary app window is closed.
    This provides a quick and easy way to clean up objects.
    '''

    def on_closing_primary_app_window(self):
        # TODO: Add a warning when user tries to close parent app_window
        for app_window in self.app_windows:
            app_window.destroy()
