import threading
import time
import os
from utils.data_writer import DataWriter
from utils.converter import Converter
from utils.config_reader import ConfigReader
from utils.request_sender import RequestSender
from utils.input_validation import InputValidation
from utils.parser import Parser
config_reader = ConfigReader()
config_dict = config_reader.read_config_file()
if config_dict["interface.graphical"]:
    import tkinter
    import customtkinter
    # from menu.gui.save_fetched_data import GUISaveFetchedData
    from menu.gui.ts_converter import GUITSConverter
    from menu.gui.show_indices_status import GUIShowIndicesStatus
    from menu.gui.show_available_field_names import GUIShowAvailableFields
    from tkinter import ttk
    from PIL import Image, ImageTk

    PATH = os.path.dirname(os.path.realpath(__file__))

    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUIMenu:

    def __init__(self,
                 request_sender: RequestSender,
                 converter: Converter,
                 input_validation: InputValidation,
                 parser: Parser):

        # Backend related
        self.request_sender = request_sender
        self.converter = converter
        self.input_validation = input_validation
        self.parser = parser
        self.__data_writer = DataWriter()

        # Frontend related
        self.primary_app_window = customtkinter.CTk()
        self.app_windows = [self.primary_app_window]
        self.frame_left = None
        self.frame_right = None
        self.frame_info = None
        self.frame_info_error_label = None
        self.filter_list_label = None
        self.progress_bar = None
        self.progress_bar_label = None
        self.fetch_data_button = None
        self.label_mode = None
        self.show_available_field_names_button = None
        self.theme_optionmenu = None
        self.label_options = None
        self.icon_photo = None

        # Index related Assets
        self.show_indices_status_button = None
        self.current_index_label = None
        self.current_index_combobox = None
        self.indices_status = "placeholder"
        self.current_index = "N/A"
        self.selected_index = tkinter.StringVar()
        self.selected_index.set(value="N/A")
        self.index_list = ["placeholder"]
        self.available_field_list = ["placeholder"]
        self.parent_field_to_type_dict = {}

        # Time related assets
        self.main_timestamp_name_label = None
        self.main_timestamp_name_combobox = None
        self.main_timestamp_format_label = None
        self.main_timestamp_format_combobox = None
        self.main_timezone_label = None
        self.main_timezone_combobox = None
        self.valid_timestamp_name_list = ["placeholder"]
        self.main_timestamp_name = "N/A"
        self.selected_main_timestamp_name = tkinter.StringVar()
        self.selected_main_timestamp_name.set(value="N/A")
        self.main_timestamp_format = "datetime"
        self.selected_main_timestamp_format = tkinter.StringVar()
        self.selected_main_timestamp_format.set(value="datetime")
        self.main_timezone = "+00:00"  # Default UTC
        self.selected_main_timezone = tkinter.StringVar()
        self.selected_main_timezone.set(value="+00:00")
        self.datetime_to_epoch_button = None

        # Data Fetch assets
        self.start_timestamp_label = None
        self.start_timestamp_entry = None
        self.end_timestamp_label = None
        self.end_timestamp_entry = None
        self.fields_list_label = None
        self.fields_list_entry = None
        self.num_logs_label = None
        self.num_logs_entry = None
        self.fields_list_label = None
        self.fields_list_entry = None
        self.filter_list_label = None
        self.filter_list_entry = None
        self.file_format_label = None
        self.file_format_combobox = None
        self.file_format = "csv" # Default file format
        self.selected_file_format = tkinter.StringVar()
        self.selected_file_format.set(value="csv")
        self.saved_filepath_label = None

        self.primary_app_window.protocol("WM_DELETE_WINDOW", self.on_closing_primary_app_window)
        self.available_themes = ["Light Theme", "Dark Theme", "System Default"]
        self.init_primary_app_window()
        self.init_frames()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("green.Horizontal.TProgressbar",
                             foreground='green',
                             background='green')
        self.style.configure("TCombobox",
                             fieldbackground='#395E9C',
                             background="#395E9C",
                             foreground='#E5E5E5',
                             lightcolor="grey",
                             darkcolor="grey")  # changes colour of combobox itself (foreground is the text colour, background is the background colour of the arrow to drop down)
        self.frame_info.option_add("*TCombobox*Listbox*Background", "#333333")  # changes background of drop down menu of combobox
        self.frame_info.option_add('*TCombobox*Listbox*Foreground', '#E5E5E5')  # changes colour of text of options in combobox
        self.init_indices()  # Comment out for testing

    '''
    Easy way to initialize the main window
    '''
    def init_primary_app_window(self):
        self.primary_app_window.title("elasticfetch - Main")
        self.primary_app_window.geometry("1120x640")
        self.primary_app_window.resizable(False, False)

        self.icon_photo = self.load_image(path="/images/icon.png", image_size=60)
        self.primary_app_window.wm_iconphoto(False, self.icon_photo)

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
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=5, pady=20, padx=20, sticky="nsew")
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
                                                            text_font=("Arial", 10),
                                                            dynamic_resizing=False,
                                                            command=self.change_appearance_mode)
        self.theme_optionmenu.grid(row=10, column=0, sticky="s")
        self.theme_optionmenu.set("Dark Theme")

        # Selecting Index
        self.current_index_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Selected Index:",
                                                          text_font=("Arial", 11))  # font name and size in px
        self.current_index_label.grid(row=0, column=2, pady=20, padx=0)
        self.current_index_combobox = ttk.Combobox(master=self.frame_info,
                                                   values=self.index_list,
                                                   font=("Arial", 11),
                                                   textvariable=self.selected_index)
        self.current_index_combobox.bind('<<ComboboxSelected>>', self.set_current_index)

        self.current_index_combobox.grid(row=0, column=3, columnspan=3, pady=5, padx=0, sticky="we")
        self.current_index_combobox.set(self.current_index)

        # Show available fields button
        self.show_available_field_names_button = customtkinter.CTkButton(master=self.frame_info,
                                                                         state=customtkinter.DISABLED,
                                                                         width=60,
                                                                         text="Show All Fields",
                                                                         fg_color="grey",
                                                                         command=self.show_available_field_names)
        self.show_available_field_names_button.grid(row=0, column=6, pady=10, padx=20)

        # Selecting main timestamp field name
        self.main_timestamp_name_label = customtkinter.CTkLabel(master=self.frame_info,
                                                                text="Timestamp Field:",
                                                                text_font=("Arial", 11))

        self.main_timestamp_name_label.grid(row=1, column=2, pady=5, padx=0)
        self.main_timestamp_name_combobox = ttk.Combobox(master=self.frame_info,
                                                         values=self.valid_timestamp_name_list,
                                                         state=tkinter.DISABLED,
                                                         font=("Arial", 10),
                                                         textvariable=self.selected_main_timestamp_name)

        self.main_timestamp_name_combobox.bind('<<ComboboxSelected>>', self.set_main_timestamp_name)
        self.main_timestamp_name_combobox.grid(row=1, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        # Selecting timestamp format
        self.main_timestamp_format_label = customtkinter.CTkLabel(master=self.frame_info,
                                                                  text="Timestamp Format:",
                                                                  text_font=("Arial", 11))
        self.main_timestamp_format_label.grid(row=2, column=2, pady=5, padx=0)
        self.main_timestamp_format_combobox = ttk.Combobox(master=self.frame_info,
                                                           values=self.input_validation.valid_timestamp_format_list,
                                                           font=("Arial", 10),
                                                           textvariable=self.selected_main_timestamp_format)
        self.main_timestamp_format_combobox.bind('<<ComboboxSelected>>', self.set_main_timestamp_format)
        self.main_timestamp_format_combobox.grid(row=2, column=3, pady=5, padx=0)

        # Selecting Timezone
        self.main_timezone_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Timezone:",
                                                          text_font=("Arial", 11))  # font name and size in px
        self.main_timezone_label.grid(row=3, column=2, pady=5, padx=0)
        self.main_timezone_combobox = ttk.Combobox(master=self.frame_info,
                                                   values=self.input_validation.valid_timezone_list,
                                                   font=("Arial", 10),
                                                   textvariable=self.selected_main_timezone)
        self.main_timezone_combobox.bind('<<ComboboxSelected>>', self.set_main_timezone)
        self.main_timezone_combobox.grid(row=3, column=3, pady=5, padx=0)

        # Fetch Data Section
        self.start_timestamp_label = customtkinter.CTkLabel(master=self.frame_info,
                                                            text="Start Timestamp:",
                                                            text_font=("Arial", 11))
        self.start_timestamp_label.grid(row=4, column=2, pady=5, padx=0)
        self.start_timestamp_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                            width=200,
                                                            height=32,
                                                            text_font=("Arial", 10),
                                                            placeholder_text="eg. 2022-05-01T00:00:00")
        self.start_timestamp_entry.grid(row=4, column=3, pady=5, padx=0)
        self.end_timestamp_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="End Timestamp:",
                                                          text_font=("Arial", 11))
        self.end_timestamp_label.grid(row=4, column=4, pady=5, padx=0)
        self.end_timestamp_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                          width=200,
                                                          height=32,
                                                          text_font=("Arial", 10),
                                                          placeholder_text="eg. 2022-05-20T00:00:00")
        self.end_timestamp_entry.grid(row=4, column=5, pady=5, padx=0)
        self.num_logs_label = customtkinter.CTkLabel(master=self.frame_info,
                                                     text='Number of Logs:',
                                                     text_font=("Arial", 11))
        self.num_logs_label.grid(row=5, column=2, pady=5, padx=0)
        self.num_logs_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                     width=200,
                                                     height=32,
                                                     text_font=("Arial", 10),
                                                     placeholder_text="eg. 100000")
        self.num_logs_entry.grid(row=5, column=3, pady=5, padx=0)
        self.fields_list_label = customtkinter.CTkLabel(master=self.frame_info,
                                                        text='Fields:',
                                                        text_font=("Arial", 11))
        self.fields_list_label.grid(row=6, column=2, pady=5, padx=0)
        self.fields_list_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                        height=32,
                                                        text_font=("Arial", 10),
                                                        placeholder_text="eg. @timestamp, event.code, event.category...")
        self.fields_list_entry.grid(row=6, column=3, columnspan=3, pady=5, padx=0, sticky="we")
        self.filter_list_label = customtkinter.CTkLabel(master=self.frame_info,
                                                        text="Filters:",
                                                        text_font=("Arial", 11))
        self.filter_list_label.grid(row=7, column=2, pady=5, padx=0)
        self.filter_list_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                        height=32,
                                                        text_font=("Arial", 10),
                                                        placeholder_text="eg. event.code is_gte 4000; event.category is_not authentication; ...")
        self.filter_list_entry.grid(row=7, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        self.file_format_label = customtkinter.CTkLabel(master=self.frame_info,
                                                        text="File Format:",
                                                        text_font=("Arial", 11))
        self.file_format_label.grid(row=8, column=2, pady=5, padx=0)

        self.file_format_combobox = ttk.Combobox(master=self.frame_info,
                                                 values=self.input_validation.valid_file_format,
                                                 font=("Arial", 10),
                                                 textvariable=self.selected_file_format)
        self.file_format_combobox.bind('<<ComboboxSelected>>', self.set_file_format)

        self.file_format_combobox.grid(row=8, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        self.frame_info_error_label = customtkinter.CTkLabel(master=self.frame_info,
                                                             text_color="red",
                                                             text="",
                                                             text_font=("Arial", 10))
        self.frame_info_error_label.grid(row=9, column=2, columnspan=2, pady=0)

        self.fetch_data_button = customtkinter.CTkButton(master=self.frame_right,
                                                         text="Fetch Data  ",
                                                         image=self.icon_photo,
                                                         fg_color="grey",
                                                         text_font=("Arial", 11),
                                                         state=customtkinter.DISABLED,
                                                         command=self.fetch_elastic_data_between_ts1_ts2)
        self.fetch_data_button.grid(row=3, column=0, columnspan=2, pady=0, sticky="s")

        self.progress_bar = ttk.Progressbar(master=self.frame_right,
                                            mode="determinate",
                                            style="green.Horizontal.TProgressbar",
                                            orient=tkinter.HORIZONTAL)
        self.progress_bar.grid(row=8, column=0, padx=20, pady=0, columnspan=3, sticky="we")
        self.progress_bar_label = customtkinter.CTkLabel(master=self.frame_right,
                                                         text="",
                                                         text_font=("Consolas", 12))
        self.progress_bar_label.grid(row=9, column=0, padx=20, pady=20, sticky="w")
        self.saved_filepath_label = customtkinter.CTkLabel(master=self.frame_right,
                                                           text="",
                                                           text_font=("Consolas", 12))
        self.saved_filepath_label.grid(row=9, column=1, padx=20, pady=20, sticky="w")

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

    def set_main_timestamp_name(self, event):
        self.main_timestamp_name = self.selected_main_timestamp_name.get()
        return

    def set_file_format(self, event):
        self.file_format = self.selected_file_format.get()
        return

    def set_main_timestamp_format(self, event):
        self.main_timestamp_format = self.selected_main_timestamp_format.get()
        # change the placeholder of start time and end time accordingly.
        if self.start_timestamp_entry is not None and self.end_timestamp_entry is not None:
            if self.main_timestamp_format == "datetime":
                self.start_timestamp_entry.configure(placeholder_text="eg. 2022-05-01T00:00:00")
                self.end_timestamp_entry.configure(placeholder_text="eg. 2022-05-20T00:00:00")
                self.main_timezone_combobox.configure(state=tkinter.NORMAL)
            elif self.main_timestamp_format == "epoch":
                self.start_timestamp_entry.configure(placeholder_text="eg. 1651363200000")
                self.end_timestamp_entry.configure(placeholder_text="eg. 1653004800000")
                self.main_timezone_combobox.set(value="+00:00")
                self.main_timezone = "+00:00"
                self.main_timezone_combobox.configure(state=tkinter.DISABLED)
        return

    def set_main_timezone(self, event):
        self.main_timezone = self.selected_main_timezone.get()
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

    def set_current_index(self, event):
        self.show_available_field_names_button.configure(state=customtkinter.DISABLED,
                                                         fg_color="grey")
        if self.selected_index.get() != "N/A":
            self.current_index = self.selected_index.get()
            response = self.request_sender.get_available_fields(index_name=self.current_index)
            if response is not None:
                self.parent_field_to_type_dict = self.converter.convert_field_mapping_keys_pretty(
                    index_name=self.current_index,
                    fields_json=response)
                self.get_valid_timestamp_name_list()
                self.get_available_field_list()
            self.show_available_field_names_button.configure(state=customtkinter.NORMAL,
                                                             fg_color="#395E9C")
            self.main_timestamp_name_combobox.configure(values=self.valid_timestamp_name_list,
                                                        state=tkinter.NORMAL)
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
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

    def fetch_elastic_data_between_ts1_ts2(self):
        self.frame_info_error_label.set_text("")
        self.fetch_data_button.configure(state=customtkinter.DISABLED,
                                         fg_color="grey")
        self.primary_app_window.update()
        start_ts = self.start_timestamp_entry.get().strip()
        end_ts = self.end_timestamp_entry.get().strip()
        num_logs = self.num_logs_entry.get().strip()
        fields = self.fields_list_entry.get().strip()
        filter_raw = self.filter_list_entry.get().strip()

        if not self.input_validation.is_timestamp_name_valid(chosen_timestamp_name=self.main_timestamp_name_combobox.get(),
                                                             valid_timestamp_name_list=self.valid_timestamp_name_list):
            self.frame_info_error_label.configure(text="'Timestamp Field: {}' is not a valid!".format(self.main_timestamp_name_combobox.get()))
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                             fg_color="#395E9C")
            return

        if self.main_timestamp_format == "datetime":
            if not self.input_validation.is_datetime_timestamp_valid(timestamp=start_ts):
                self.frame_info_error_label.configure(text="Start Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return
            if not self.input_validation.is_datetime_timestamp_valid(timestamp=end_ts):
                self.frame_info_error_label.configure(text="End Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return
        elif self.main_timestamp_format == "epoch":
            if not self.input_validation.is_epoch_timestamp_valid(timestamp=start_ts):
                self.frame_info_error_label.configure(text="Start Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return
            if not self.input_validation.is_epoch_timestamp_valid(timestamp=end_ts):
                self.frame_info_error_label.configure(text="End Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return

        if not self.input_validation.is_numeric_valid(user_input=num_logs):
            self.frame_info_error_label.configure(text="Number of Logs: Invalid Numeric Expression!")
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                             fg_color="#395E9C")
            return
        num_logs = int(num_logs)
        fields_list = [x.strip() for x in fields.split(',')]
        if len(fields_list) == 1 and fields_list[0] == "":
            self.frame_info_error_label.configure(text="Fields: Cannot be empty!")
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                             fg_color="#395E9C")
            return

        if filter_raw != "":
            if not self.input_validation.is_filter_valid(filter_raw=filter_raw):
                self.frame_info_error_label.configure(text="Filters: Invalid Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return

        keyword_sentences_dict = self.parser.parse_filter_raw(filter_raw=filter_raw)
        query_bool_must_list = self.converter.convert_all_is_list_to_must_list(
            filter_is_list=keyword_sentences_dict["is"],
            filter_is_gte_list=keyword_sentences_dict["is_gte"],
            filter_is_lte_list=keyword_sentences_dict["is_lte"],
            filter_is_gt_list=keyword_sentences_dict["is_gt"],
            filter_is_lt_list=keyword_sentences_dict["is_lt"],
            filter_is_one_of_list=keyword_sentences_dict["is_one_of"])
        query_bool_must_not_list = self.converter.convert_all_is_not_list_to_must_not_list(
            filter_is_not_list=keyword_sentences_dict["is_not"],
            filter_is_not_gte_list=keyword_sentences_dict["is_not_gte"],
            filter_is_not_lte_list=keyword_sentences_dict["is_not_lte"],
            filter_is_not_gt_list=keyword_sentences_dict["is_not_gt"],
            filter_is_not_lt_list=keyword_sentences_dict["is_not_lt"],
            filter_is_not_one_of_list=keyword_sentences_dict["is_not_one_of"])

        if not self.input_validation.is_file_format_valid(file_format=self.file_format):
            self.frame_info_error_label.configure(text="File Format: Invalid format!")
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                             fg_color="#395E9C")
            return

        data_fetch_thread = threading.Thread(target=self.request_sender.get_fetch_elastic_data_between_ts1_ts2,
                                             kwargs={
                                                "index_name": self.current_index,
                                                "num_logs": num_logs,
                                                "main_timestamp_name": self.main_timestamp_name,
                                                "main_timestamp_format": self.main_timestamp_format,
                                                "main_timezone": self.main_timezone,
                                                "start_ts": start_ts,
                                                "end_ts": end_ts,
                                                "fields_list": fields_list,
                                                "query_bool_must_list": query_bool_must_list,
                                                "query_bool_must_not_list": query_bool_must_not_list,
                                            })

        self.progress_bar["value"] = 0
        self.progress_bar_label.set_text("Current Progress: {}/{} --- {:.2f}%".format(0,
                                                                                      num_logs,
                                                                                      self.progress_bar["value"]))
        self.primary_app_window.update()

        if self.file_format == "csv":
            data_write_csv_thread = threading.Thread(target=self.__data_writer.write_to_csv,
                                                     kwargs={
                                                         "request_sender": self.request_sender,
                                                         "fields_list": fields_list
                                                     })
            data_write_csv_thread.start()
            data_fetch_thread.start()

            self.saved_filepath_label.set_text("Saving data to {}".format(self.__data_writer.csv_filepath))
            while not self.request_sender.has_finished_fetching:
                self.progress_bar["value"] = (self.request_sender.total_results_size / float(num_logs)) * 100
                self.progress_bar_label.set_text(
                    "Current Progress: {}/{} --- {:.2f}%".format(self.request_sender.total_results_size,
                                                                 num_logs,
                                                                 self.progress_bar["value"]))
                self.primary_app_window.update()

            data_write_csv_thread.join()
            data_fetch_thread.join()

            self.progress_bar_label.set_text("")
            self.saved_filepath_label.set_text("Successfully saved data to {}".format(self.__data_writer.csv_filepath))
            self.primary_app_window.update()

        elif self.file_format == "json":
            data_write_json_thread = threading.Thread(target=self.__data_writer.write_to_json,
                                                      kwargs={
                                                          "request_sender": self.request_sender,
                                                      })
            data_write_json_thread.start()
            data_fetch_thread.start()

            self.saved_filepath_label.set_text("Saving data to {}".format(self.__data_writer.json_filepath))
            while not self.request_sender.has_finished_fetching:
                self.progress_bar["value"] = (self.request_sender.total_results_size / float(num_logs)) * 100
                self.progress_bar_label.set_text(
                    "Current Progress: {}/{} --- {:.2f}%".format(self.request_sender.total_results_size,
                                                                 num_logs,
                                                                 self.progress_bar["value"]))

                self.primary_app_window.update()

            data_write_json_thread.join()
            data_fetch_thread.join()

            self.progress_bar_label.set_text("")
            self.saved_filepath_label.set_text("Successfully saved data to {}".format(self.__data_writer.json_filepath))
            self.primary_app_window.update()

        self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                         fg_color="#395E9C")
        return

    def display_ts_converter_window(self):
        gui_ts_converter = GUITSConverter(converter=self.converter,
                                          input_validation=self.input_validation)
        gui_ts_converter.mainloop()
        return

    def on_closing_primary_app_window(self):
        self.primary_app_window.destroy()
        return

    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, int(image_size*0.75))))
