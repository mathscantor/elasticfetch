import customtkinter
import tkinter
from utils.menu.gui_ts_converter import GUITSConverter
from utils.menu.gui_show_indices_status import GUIShowIndicesStatus
from utils.menu.gui_show_available_field_names import GUIShowAvailableFields
import os

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class GUIMenu:

    def __init__(self,
                 request_sender,
                 converter,
                 input_validation,
                 parser):

        # Backend related
        self.request_sender = request_sender
        self.converter = converter
        self.input_validation = input_validation
        self.parser = parser

        # Frontend related
        self.primary_app_window = customtkinter.CTk()
        self.app_windows = [self.primary_app_window]
        self.frame_left = None
        self.frame_right = None
        self.frame_info = None
        self.theme_optionmenu = None
        self.label_options = None

        # Index related Assets
        self.show_indices_status_button = None
        self.current_index_label = None
        self.current_index_optionmenu = None
        self.indices_status = "placeholder"
        self.current_index = "N/A"
        self.index_list = ["placeholder"]
        self.available_field_list = ["placeholder"]
        self.parent_field_to_type_dict = {}

        # Time related assets
        self.main_timestamp_field_name_label = None
        self.main_timestamp_field_name_optionmenu = None
        self.main_timestamp_field_format_label = None
        self.main_timestamp_field_format_optionmenu = None
        self.main_timezone_label = None
        self.main_timezone_optionmenu = None
        self.valid_timestamp_name_list = ["placeholder"]
        self.main_timestamp_field_name = "N/A"
        self.main_timestamp_format = "datetime"
        self.main_timezone = "+00:00"  # Default UTC
        self.datetime_to_epoch_button = None

        self.primary_app_window.protocol("WM_DELETE_WINDOW", self.on_closing_primary_app_window)
        self.available_themes = ["Light Theme", "Dark Theme", "System Default"]
        self.init_primary_app_window()
        self.init_frames()
        self.init_indices()

    def init_primary_app_window(self):
        self.primary_app_window.title("elasticfetch - Main")
        self.primary_app_window.geometry("1120x520")

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
        if self.indices_status is None:
            exit(1)
        temp_list = self.indices_status.split("\n")[1:-1]
        i = 1
        self.index_list = []
        for entry in temp_list:
            index_name = entry.split()[2]
            self.index_list.append(index_name)
            i += 1
        return

    def show_menu(self):

        self.label_options = customtkinter.CTkLabel(master=self.frame_left,
                                                    text="Options",
                                                    text_font=("Arial", 15))  # font name and size in px
        self.label_options.grid(row=1, column=0, pady=10, padx=10)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        # Show Indices Status Button
        self.show_indices_status_button = customtkinter.CTkButton(master=self.frame_left,
                                                                  text="Show Indices Status",
                                                                  command=self.show_indices_status)
        self.show_indices_status_button.grid(row=2, column=0, pady=10, padx=20)

        # DateTime to Epoch
        self.datetime_to_epoch_button = customtkinter.CTkButton(master=self.frame_left,
                                                                text="TS Format Converter",
                                                                command=self.display_ts_converter_window)
        self.datetime_to_epoch_button.grid(row=3, column=0, pady=10, padx=20)

        # Theme Option Menu
        self.theme_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                            values=self.available_themes,
                                                            dynamic_resizing=False,
                                                            command=self.change_appearance_mode)
        self.theme_optionmenu.grid(row=10, column=0, sticky="s")
        self.theme_optionmenu.set("Dark Theme")

        # Selecting Index
        self.current_index_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Selected Index:",
                                                          text_font=("Arial", 11))  # font name and size in px
        self.current_index_label.grid(row=0, column=2, pady=20, padx=0)
        self.current_index_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_info,
                                                                    values=self.index_list,
                                                                    width=200,
                                                                    dynamic_resizing=False,
                                                                    command=self.set_current_index)
        # Show available fields button
        self.show_available_field_names_button = customtkinter.CTkButton(master=self.frame_info,
                                                                         state=customtkinter.DISABLED,
                                                                         text="Show Available Fields",
                                                                         fg_color="grey",
                                                                         command=self.show_available_field_names)
        self.show_available_field_names_button.grid(row=0, column=4, pady=10, padx=20)

        # Selecting main timestamp field name
        self.current_index_optionmenu.grid(row=0, column=3, pady=5, padx=0)
        self.current_index_optionmenu.set(self.current_index)
        self.main_timestamp_field_name_label = customtkinter.CTkLabel(master=self.frame_info,
                                                                      text="Timestamp Field:",
                                                                      text_font=("Arial", 11))

        self.main_timestamp_field_name_label.grid(row=1, column=2, pady=5, padx=0)
        self.main_timestamp_field_name_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_info,
                                                                                values=self.valid_timestamp_name_list,
                                                                                state=customtkinter.DISABLED,
                                                                                width=200,
                                                                                dynamic_resizing=False,
                                                                                button_color="grey",
                                                                                fg_color="grey",
                                                                                command=self.set_main_timestamp_field_name)
        self.main_timestamp_field_name_optionmenu.set(self.main_timestamp_field_name)
        self.main_timestamp_field_name_optionmenu.grid(row=1, column=3, pady=5, padx=0)

        # Selecting timestamp format
        self.main_timestamp_field_format_label = customtkinter.CTkLabel(master=self.frame_info,
                                                                        text="Timestamp Format:",
                                                                        text_font=(
                                                                            "Arial", 11))  # font name and size in px
        self.main_timestamp_field_format_label.grid(row=2, column=2, pady=5, padx=0)
        self.main_timestamp_field_format_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_info,
                                                                                  values=self.input_validation.valid_timestamp_format_list,
                                                                                  state=customtkinter.DISABLED,
                                                                                  width=200,
                                                                                  dynamic_resizing=False,
                                                                                  button_color="grey",
                                                                                  fg_color="grey",
                                                                                  command=self.set_main_timestamp_format)
        self.main_timestamp_field_format_optionmenu.set(self.main_timestamp_format)
        self.main_timestamp_field_format_optionmenu.grid(row=2, column=3, pady=5, padx=0)

        # Selecting Timezone
        self.main_timezone_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Timezone:",
                                                          text_font=("Arial", 11))  # font name and size in px
        self.main_timezone_label.grid(row=3, column=2, pady=5, padx=0)
        self.main_timezone_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_info,
                                                                    values=self.input_validation.valid_timezone_list,
                                                                    state=customtkinter.DISABLED,
                                                                    width=200,
                                                                    dynamic_resizing=False,
                                                                    button_color="grey",
                                                                    fg_color="grey",
                                                                    command=self.set_main_timezone)
        self.main_timezone_optionmenu.set(self.main_timezone)
        self.main_timezone_optionmenu.grid(row=3, column=3, pady=5, padx=0)

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

    def set_main_timestamp_field_name(self, main_timestamp_field_name):
        self.main_timestamp_field_name = main_timestamp_field_name
        print("Main Timestamp Name: {}".format(self.main_timestamp_field_name))
        return

    def set_main_timestamp_format(self, main_timestamp_format):
        self.main_timestamp_format = main_timestamp_format
        print("Main Timestamp Format: {}".format(self.main_timestamp_format))
        return

    def set_main_timezone(self, main_timezone):
        self.main_timezone = main_timezone
        print("Main Timezone: {}".format(self.main_timezone))
        return

    def get_available_field_list(self):
        del self.available_field_list
        self.available_field_list = []
        for top_parent_field in self.parent_field_to_type_dict.keys():
            for field_type in self.parent_field_to_type_dict[top_parent_field].keys():
                self.available_field_list += self.parent_field_to_type_dict[top_parent_field][field_type]

    def get_valid_timestamp_name_list(self):
        del self.valid_timestamp_name_list
        self.valid_timestamp_name_list = []
        for top_parent_field in self.parent_field_to_type_dict.keys():
            for field_type in self.parent_field_to_type_dict[top_parent_field].keys():
                if field_type == "date":
                    self.valid_timestamp_name_list += self.parent_field_to_type_dict[top_parent_field][field_type]
        return

    def set_current_index(self, index_choice):

        if index_choice != "N/A":
            del self.parent_field_to_type_dict
            self.current_index = index_choice
            response = self.request_sender.get_available_fields(index_name=self.current_index)
            if response is not None:
                self.parent_field_to_type_dict = self.converter.convert_field_mapping_keys_pretty(
                    index_name=self.current_index,
                    fields_json=response)
                self.get_valid_timestamp_name_list()
                self.get_available_field_list()
                self.show_available_field_names_button.configure(state=customtkinter.NORMAL,
                                                                 fg_color="#395E9C")
                self.main_timestamp_field_name_optionmenu.configure(values=self.valid_timestamp_name_list,
                                                                    state=customtkinter.NORMAL,
                                                                    button_color="#144870",
                                                                    fg_color="#395E9C"
                                                                    )
                self.main_timestamp_field_format_optionmenu.configure(state=customtkinter.NORMAL,
                                                                      button_color="#144870",
                                                                      fg_color="#395E9C")
                self.main_timezone_optionmenu.configure(state=customtkinter.NORMAL,
                                                        button_color="#144870",
                                                        fg_color="#395E9C")
        else:
            self.parent_field_to_type_dict = {}

        return

    def show_indices_status(self):
        gui_show_indices_status = GUIShowIndicesStatus(indices_status=self.indices_status)
        gui_show_indices_status.mainloop()
        return

    def show_available_field_names(self):
        gui_show_available_fields = GUIShowAvailableFields(current_index=self.current_index,
                                                           parent_field_to_type_dict=self.parent_field_to_type_dict)
        gui_show_available_fields.mainloop()
        return

    def display_ts_converter_window(self):
        gui_ts_converter = GUITSConverter(converter=self.converter,
                                          input_validation=self.input_validation)
        gui_ts_converter.mainloop()
        return

    def on_closing_primary_app_window(self):
        self.primary_app_window.destroy()
        return
