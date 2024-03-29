import threading
import os
from utils.data_writer import DataWriter
from utils.converter import Converter
from utils.config_reader import ConfigReader
from utils.request_sender import RequestSender
from utils.input_validation import InputValidation
from utils.parser import Parser
config_reader = ConfigReader()

if config_reader.interface_graphical:
    import tkinter
    import customtkinter
    from tkinter import messagebox
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
        self.__request_sender = request_sender
        self.__converter = converter
        self.__input_validation = input_validation
        self.__parser = parser
        self.__data_writer = DataWriter()
        self.__data_fetch_thread = None
        self.__data_write_csv_thread = None
        self.__data_write_json_thread = None

        # Frontend related
        self.primary_app_window = customtkinter.CTk()
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
        self.button_photo = None
        self.__default_font_size = 14

        # Index related Assets
        self.show_indices_status_button = None
        self.current_index_label = None
        self.current_index_combobox = None
        self.current_index_entry = None # For custom name and wildcard usage
        self.index_name_wildcard_switch = None
        self.__indices_status = "placeholder"
        self.current_index = "N/A"
        self.selected_index = tkinter.StringVar()
        self.selected_index.set(value="N/A")
        self.has_pressed_return_key = False
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
    def init_primary_app_window(self) -> None:
        """
        Initialize the primary application window.

        This method sets up and initializes the main window for the application,
        including any necessary components, widgets, or configurations.

        :return: None
        :rtype: None
        """
        self.primary_app_window.title("elasticfetch - Main")
        self.primary_app_window.geometry("1120x640")
        self.primary_app_window.resizable(False, False)

        self.icon_photo = self.load_image(path="images/icon.png", image_size=60)
        self.button_photo = customtkinter.CTkImage(Image.open(os.path.join(PATH, "images/icon.png")), size=(60, 45))
        self.primary_app_window.wm_iconphoto(False, self.icon_photo)

        # configure grid layout (2x1)
        self.primary_app_window.grid_columnconfigure(1, weight=1)
        self.primary_app_window.grid_rowconfigure(0, weight=1)
        return

    def init_frames(self) -> None:
        """
        Initialize frames within the application window.

        This method sets up and initializes frames or containers within the main application window.
        Frames can be used to organize and group different sections or functionalities of the application.

        :return: None
        :rtype: None
        """
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
        self.frame_right.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_right.grid_columnconfigure(3, weight=1)
        self.frame_right.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.frame_right.grid_rowconfigure(7, weight=1)

        # ---------------------INFO FRAME--------------------- #
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=5, pady=20, padx=20, sticky="nsew")
        return

    def init_indices(self) -> None:
        """
        Initialize Elasticsearch indices for the application.
        This method sets up and initializes Elasticsearch indices statuses for use within the application.

        :return: None
        :rtype: None
        """
        self.__indices_status = self.__request_sender.get_indices_status()
        if self.__indices_status is None:
            exit(1)
        temp_list = self.__indices_status.split("\n")[1:-1]
        i = 1
        self.index_list = []
        for entry in temp_list:
            index_name = entry.split()[2]
            self.index_list.append(index_name)
            i += 1
        return

    def show_menu(self) -> None:
        """
        Display the main menu.

        This method prints the main menu options to the console or user interface,
        providing the user with choices for interacting with the application.

        :return: None
        :rtype: None
        """
        self.label_options = customtkinter.CTkLabel(master=self.frame_left,
                                                    text="Options",
                                                    font=customtkinter.CTkFont(family="Arial",
                                                                               size=self.__default_font_size))
        self.label_options.grid(row=1, column=0, pady=10, padx=10, sticky="we")

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left,
                                                 text="Appearance Mode:",
                                                 font=customtkinter.CTkFont(family="Arial",
                                                                            size=self.__default_font_size))
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="we")

        # Show Indices Status Button
        self.show_indices_status_button = customtkinter.CTkButton(master=self.frame_left,
                                                                  text="Show Indices Status",
                                                                  font=customtkinter.CTkFont(family="Arial",
                                                                                             size=self.__default_font_size),
                                                                  command=self.show_indices_status)
        self.show_indices_status_button.grid(row=2, column=0, pady=10, padx=20)

        # DateTime to Epoch
        self.datetime_to_epoch_button = customtkinter.CTkButton(master=self.frame_left,
                                                                text="TS Format Converter",
                                                                font=customtkinter.CTkFont(family="Arial",
                                                                                           size=self.__default_font_size),
                                                                command=self.display_ts_converter_window)
        self.datetime_to_epoch_button.grid(row=3, column=0, pady=10, padx=20)

        # Enable wildcard usage
        self.index_name_wildcard_switch = customtkinter.CTkSwitch(master=self.frame_left,
                                                                  text="Index Name Wildcard Toggle",
                                                                  font=customtkinter.CTkFont(family="Arial",
                                                                                             size=self.__default_font_size),
                                                                  command=self.switch_index_input_method
                                                                  )
        self.index_name_wildcard_switch.grid(row=4, column=0, pady=10, padx=20)

        # Theme Option Menu
        self.theme_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                            values=self.available_themes,
                                                            font=customtkinter.CTkFont(family="Arial",
                                                                                       size=self.__default_font_size),
                                                            dynamic_resizing=False,
                                                            command=self.change_appearance_mode)
        self.theme_optionmenu.grid(row=10, column=0, sticky="s")
        self.theme_optionmenu.set("Dark Theme")

        # Selecting Index
        self.current_index_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Selected Index:",
                                                          font=customtkinter.CTkFont(family="Arial",
                                                                                     size=self.__default_font_size))  # font name and size in px
        self.current_index_label.grid(row=0, column=2, pady=20, padx=0)
        self.current_index_combobox = ttk.Combobox(master=self.frame_info,
                                                   values=self.index_list,
                                                   state="normal",
                                                   font=customtkinter.CTkFont(family="Arial",
                                                                              size=self.__default_font_size),
                                                   textvariable=self.selected_index)
        self.current_index_combobox.bind('<<ComboboxSelected>>', self.set_current_index)

        self.current_index_combobox.grid(row=0, column=3, columnspan=3, pady=5, padx=0, sticky="we")
        self.current_index_combobox.set(self.current_index)

        self.current_index_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                          width=180,
                                                          height=32,
                                                          font=customtkinter.CTkFont(family="Arial",
                                                                                     size=self.__default_font_size),
                                                          textvariable=self.selected_index,
                                                          placeholder_text="eg. *filebeat*")
        self.current_index_entry.bind('<KeyRelease>', self.notify_to_press_return_key)
        self.current_index_entry.bind('<Return>', self.set_current_index)
        self.current_index_entry.grid(row=0, column=3, columnspan=3, pady=5, padx=0, sticky="we")
        self.current_index_entry.grid_forget()

        # Show available fields button
        self.show_available_field_names_button = customtkinter.CTkButton(master=self.frame_info,
                                                                         state=customtkinter.DISABLED,
                                                                         width=60,
                                                                         text="Show All Fields",
                                                                         font=customtkinter.CTkFont(family="Arial",
                                                                                                    size=self.__default_font_size),
                                                                         fg_color="grey",
                                                                         command=self.show_available_field_names)
        self.show_available_field_names_button.grid(row=0, column=6, pady=10, padx=20)

        # Selecting main timestamp field name
        self.main_timestamp_name_label = customtkinter.CTkLabel(master=self.frame_info,
                                                                text="Timestamp Field:",
                                                                font=customtkinter.CTkFont(family="Arial",
                                                                                           size=self.__default_font_size))

        self.main_timestamp_name_label.grid(row=1, column=2, pady=5, padx=0)
        self.main_timestamp_name_combobox = ttk.Combobox(master=self.frame_info,
                                                         values=self.valid_timestamp_name_list,
                                                         state=tkinter.DISABLED,
                                                         font=customtkinter.CTkFont(family="Arial",
                                                                                    size=self.__default_font_size),
                                                         textvariable=self.selected_main_timestamp_name)

        self.main_timestamp_name_combobox.bind('<<ComboboxSelected>>', self.set_main_timestamp_name)
        self.main_timestamp_name_combobox.grid(row=1, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        # Selecting timestamp format
        self.main_timestamp_format_label = customtkinter.CTkLabel(master=self.frame_info,
                                                                  text="Timestamp Format:",
                                                                  font=customtkinter.CTkFont(family="Arial",
                                                                                             size=self.__default_font_size))
        self.main_timestamp_format_label.grid(row=2, column=2, pady=5, padx=0)
        self.main_timestamp_format_combobox = ttk.Combobox(master=self.frame_info,
                                                           values=self.__input_validation.valid_timestamp_format_list,
                                                           font=customtkinter.CTkFont(family="Arial",
                                                                                      size=self.__default_font_size),
                                                           textvariable=self.selected_main_timestamp_format)
        self.main_timestamp_format_combobox.bind('<<ComboboxSelected>>', self.set_main_timestamp_format)
        self.main_timestamp_format_combobox.grid(row=2, column=3, pady=5, padx=0)

        # Selecting Timezone
        self.main_timezone_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="Timezone:",
                                                          font=customtkinter.CTkFont(family="Arial",
                                                                                     size=self.__default_font_size))
        self.main_timezone_label.grid(row=3, column=2, pady=5, padx=0)
        self.main_timezone_combobox = ttk.Combobox(master=self.frame_info,
                                                   values=self.__input_validation.valid_timezone_list,
                                                   font=customtkinter.CTkFont(family="Arial",
                                                                              size=self.__default_font_size),
                                                   textvariable=self.selected_main_timezone)
        self.main_timezone_combobox.bind('<<ComboboxSelected>>', self.set_main_timezone)
        self.main_timezone_combobox.grid(row=3, column=3, pady=5, padx=0)

        # Fetch Data Section
        self.start_timestamp_label = customtkinter.CTkLabel(master=self.frame_info,
                                                            text="Start Timestamp:",
                                                            font=customtkinter.CTkFont(family="Arial",
                                                                                       size=self.__default_font_size))
        self.start_timestamp_label.grid(row=4, column=2, pady=5, padx=0)
        self.start_timestamp_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                            width=180,
                                                            height=32,
                                                            font=customtkinter.CTkFont(family="Arial",
                                                                                       size=self.__default_font_size),
                                                            placeholder_text="eg. 2022-05-01T00:00:00")
        self.start_timestamp_entry.grid(row=4, column=3, pady=5, padx=0)
        self.end_timestamp_label = customtkinter.CTkLabel(master=self.frame_info,
                                                          text="End Timestamp:",
                                                          font=customtkinter.CTkFont(family="Arial",
                                                                                     size=self.__default_font_size))
        self.end_timestamp_label.grid(row=4, column=4, pady=5, padx=0)
        self.end_timestamp_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                          width=180,
                                                          height=32,
                                                          font=customtkinter.CTkFont(family="Arial",
                                                                                     size=self.__default_font_size),
                                                          placeholder_text="eg. 2022-05-20T00:00:00")
        self.end_timestamp_entry.grid(row=4, column=5, pady=5, padx=0)
        self.num_logs_label = customtkinter.CTkLabel(master=self.frame_info,
                                                     text='Number of Logs:',
                                                     font=customtkinter.CTkFont(family="Arial",
                                                                                size=self.__default_font_size))
        self.num_logs_label.grid(row=5, column=2, pady=5, padx=0)
        self.num_logs_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                     width=200,
                                                     height=32,
                                                     font=customtkinter.CTkFont(family="Arial",
                                                                                size=self.__default_font_size),
                                                     placeholder_text="eg. 100000")
        self.num_logs_entry.grid(row=5, column=3, pady=5, padx=0)
        self.fields_list_label = customtkinter.CTkLabel(master=self.frame_info,
                                                        text='Fields:',
                                                        font=customtkinter.CTkFont(family="Arial",
                                                                                   size=self.__default_font_size))
        self.fields_list_label.grid(row=6, column=2, pady=5, padx=0)
        self.fields_list_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                        height=32,
                                                        font=customtkinter.CTkFont(family="Arial",
                                                                                   size=self.__default_font_size),
                                                        placeholder_text="eg. @timestamp, event.code, event.category...")
        self.fields_list_entry.grid(row=6, column=3, columnspan=3, pady=5, padx=0, sticky="we")
        self.filter_list_label = customtkinter.CTkLabel(master=self.frame_info,
                                                        text="Filters:",
                                                        font=customtkinter.CTkFont(family="Arial",
                                                                                   size=self.__default_font_size))
        self.filter_list_label.grid(row=7, column=2, pady=5, padx=0)
        self.filter_list_entry = customtkinter.CTkEntry(master=self.frame_info,
                                                        height=32,
                                                        font=customtkinter.CTkFont(family="Arial",
                                                                                   size=self.__default_font_size),
                                                        placeholder_text="eg. event.code is_gte 4000; event.category is_not authentication; ...")
        self.filter_list_entry.grid(row=7, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        self.file_format_label = customtkinter.CTkLabel(master=self.frame_info,
                                                        text="File Format:",
                                                        font=customtkinter.CTkFont(family="Arial", size=self.__default_font_size))
        self.file_format_label.grid(row=8, column=2, pady=5, padx=0)

        self.file_format_combobox = ttk.Combobox(master=self.frame_info,
                                                 values=self.__input_validation.valid_file_format,
                                                 font=customtkinter.CTkFont(family="Arial", size=self.__default_font_size),
                                                 textvariable=self.selected_file_format)
        self.file_format_combobox.bind('<<ComboboxSelected>>', self.set_file_format)

        self.file_format_combobox.grid(row=8, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        self.frame_info_error_label = customtkinter.CTkLabel(master=self.frame_info,
                                                             text_color="red",
                                                             text="",
                                                             font=customtkinter.CTkFont(family="Arial", size=self.__default_font_size))
        self.frame_info_error_label.grid(row=9, column=2, columnspan=2, pady=0)

        self.fetch_data_button = customtkinter.CTkButton(master=self.frame_right,
                                                         text="Fetch Data  ",
                                                         image=self.button_photo,
                                                         fg_color="grey",
                                                         font=customtkinter.CTkFont(family="Arial", size=self.__default_font_size),
                                                         state=customtkinter.DISABLED,
                                                         command=self.fetch_elastic_data_between_ts1_ts2)
        self.fetch_data_button.grid(row=4, column=0, columnspan=2, pady=0, sticky="s")

        self.progress_bar = ttk.Progressbar(master=self.frame_right,
                                            mode="determinate",
                                            style="green.Horizontal.TProgressbar",
                                            orient=tkinter.HORIZONTAL)
        self.progress_bar.grid(row=8, column=0, padx=20, pady=0, columnspan=3, sticky="we")
        self.progress_bar_label = customtkinter.CTkLabel(master=self.frame_right,
                                                         text="",
                                                         font=customtkinter.CTkFont(family="Arial", size=self.__default_font_size))
        self.progress_bar_label.grid(row=9, column=0, padx=20, pady=20, sticky="w")
        self.saved_filepath_label = customtkinter.CTkLabel(master=self.frame_right,
                                                           text="",
                                                           font=customtkinter.CTkFont(family="Arial", size=self.__default_font_size))
        self.saved_filepath_label.grid(row=9, column=1, padx=20, pady=20, sticky="w")

        # show window
        self.primary_app_window.mainloop()
        return

    def change_appearance_mode(self,
                               new_appearance_mode: str) -> None:
        """
        Change the appearance mode of the application.

        This method allows the user to switch between different appearance modes
        such as light mode, dark mode, or other predefined themes.

        :param new_appearance_mode: The new appearance mode to be set.
        :type new_appearance_mode: str

        :return: None
        :rtype: None
        """
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

    def set_main_timestamp_name(self, event) -> None:
        """
        Set the main timestamp name based on a tkinter event.

        This method allows the user to set the name of the main timestamp field
        in response to a tkinter event, such as a user interface interaction.

        :param event: The tkinter event triggering the timestamp name setting.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """
        self.main_timestamp_name = self.selected_main_timestamp_name.get()
        return

    def set_file_format(self, event) -> None:
        """
        Set the file format based on a tkinter event.

        This method allows the user to set the desired file format
        in response to a tkinter event, such as a user interface interaction.

        :param event: The tkinter event triggering the file format setting.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """
        self.file_format = self.selected_file_format.get()
        return

    def set_main_timestamp_format(self, event) -> None:
        """
        Set the main timestamp format based on a tkinter event.

        This method allows the user to set the format of the main timestamp field
        in response to a tkinter event, such as a user interface interaction.

        :param event: The tkinter event triggering the main timestamp format setting.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """
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

    def set_main_timezone(self, event) -> None:
        """
        Set the main timezone based on a tkinter event.

        This method allows the user to set the timezone of the main timestamp field
        in response to a tkinter event, such as a user interface interaction.

        :param event: The tkinter event triggering the main timezone setting.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """
        self.main_timezone = self.selected_main_timezone.get()
        return

    def get_available_field_list(self) -> None:
        """
        Update the available field list based on parent field and type information.

        This method clears the existing available field list and populates it based on
        the parent field and type dictionary in the class instance.

        :return: None
        :rtype: None
        """
        self.available_field_list.clear()
        for top_parent_field in self.parent_field_to_type_dict.keys():
            for field_type in self.parent_field_to_type_dict[top_parent_field].keys():
                self.available_field_list += self.parent_field_to_type_dict[top_parent_field][field_type]
        return

    def get_valid_timestamp_name_list(self) -> None:
        """
        Update the valid timestamp name list based on parent field and type information.

        This method clears the existing valid timestamp name list and populates it with
        timestamp fields found in the parent field and type dictionary with the "date" type.

        :return: None
        :rtype: None
        """
        self.valid_timestamp_name_list.clear()
        for top_parent_field in self.parent_field_to_type_dict.keys():
            for field_type in self.parent_field_to_type_dict[top_parent_field].keys():
                if field_type == "date":
                    self.valid_timestamp_name_list += self.parent_field_to_type_dict[top_parent_field][field_type]
        return

    def set_current_index(self,  event) -> None:
        """
        Set the current Elasticsearch index based on a tkinter event.

        This method allows the user to set the current Elasticsearch index
        in response to a tkinter event, such as a user interface interaction.

        :param event: The tkinter event triggering the current index setting.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """
        self.show_available_field_names_button.configure(state=customtkinter.DISABLED,
                                                         fg_color="grey")

        self.has_pressed_return_key = True
        self.parent_field_to_type_dict = {}

        self.current_index = self.selected_index.get().strip()

        if self.current_index == "N/A" or self.current_index == "":
            self.frame_info_error_label.configure(text="Current index cannot be empty!")
            self.valid_timestamp_name_list.clear()
            self.main_timestamp_name_combobox.configure(values=self.valid_timestamp_name_list,
                                                        state=tkinter.DISABLED)
            self.fetch_data_button.configure(state=customtkinter.DISABLED,
                                             fg_color="#395E9C")
            return

        self.frame_info_error_label.configure(text="")
        response = self.__request_sender.get_available_fields(index_name=self.current_index)
        if response is not None:
            self.parent_field_to_type_dict = self.__converter.convert_field_mapping_keys_pretty(fields_json=response)
            self.get_valid_timestamp_name_list()
            self.get_available_field_list()
        self.show_available_field_names_button.configure(state=customtkinter.NORMAL,
                                                         fg_color="#395E9C")
        self.main_timestamp_name_combobox.configure(values=self.valid_timestamp_name_list,
                                                    state=tkinter.NORMAL)
        self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                         fg_color="#395E9C")
        return

    def show_indices_status(self) -> None:
        """
        Display the status of Elasticsearch indices.

        This method retrieves and prints the status of Elasticsearch indices,
        providing information such as the number of documents and other relevant details.

        :return: None
        :rtype: None
        """
        self.__indices_status = self.__request_sender.get_indices_status()
        window = GUIShowIndicesStatus(indices_status=self.__indices_status)
        window.after(10, window.lift)
        return

    def show_available_field_names(self) -> None:
        """
        Display the available field names in the current Elasticsearch index.

        This method retrieves and prints the names of available fields in the current Elasticsearch index,
        providing the user with information about the fields they can interact with.

        :return: None
        :rtype: None
        """
        window = GUIShowAvailableFields(current_index=self.current_index,
                                        parent_field_to_type_dict=self.parent_field_to_type_dict)
        window.after(10, window.lift)
        return

    def switch_index_input_method(self) -> None:
        """
        Switch the input method for specifying Elasticsearch indices.

        This method allows the user to switch between ComboBox or Entry
        for specifying Elasticsearch indices.

        :return: None
        :rtype: None
        """
        if self.index_name_wildcard_switch.get() == 1:
            self.current_index_combobox.grid_forget()
            self.current_index_entry.grid(row=0, column=3, columnspan=3, pady=5, padx=0, sticky="we")

        else:
            self.current_index_entry.grid_forget()
            self.current_index_combobox.grid(row=0, column=3, columnspan=3, pady=5, padx=0, sticky="we")
        return

    def fetch_elastic_data_between_ts1_ts2(self) -> None:
        """
        Fetch Elasticsearch data between two specified timestamps.

        This method retrieves data from the configured Elasticsearch index
        within the time range defined by the start and end timestamps.

        :return: None
        :rtype: None
        """
        self.frame_info_error_label.configure(text="")
        self.fetch_data_button.configure(state=customtkinter.DISABLED,
                                         fg_color="grey")
        self.primary_app_window.update()

        self.current_index = self.selected_index.get().strip()
        start_ts = self.start_timestamp_entry.get().strip()
        end_ts = self.end_timestamp_entry.get().strip()
        num_logs = self.num_logs_entry.get().strip()
        fields = self.fields_list_entry.get().strip()
        filter_raw = self.filter_list_entry.get().strip()

        if self.current_index == "N/A" or self.current_index == "":
            self.frame_info_error_label.configure(text="Current index cannot be empty!")
            self.valid_timestamp_name_list.clear()
            self.main_timestamp_name_combobox.configure(values=self.valid_timestamp_name_list,
                                                        state=tkinter.DISABLED)
            self.valid_timestamp_name_list.clear()
            self.main_timestamp_name_combobox.configure(values=self.valid_timestamp_name_list,
                                                        state=tkinter.DISABLED)
            self.fetch_data_button.configure(state=customtkinter.DISABLED,
                                             fg_color="#395E9C")
            return

        if not self.__input_validation.is_timestamp_name_valid(chosen_timestamp_name=self.main_timestamp_name_combobox.get(),
                                                               valid_timestamp_name_list=self.valid_timestamp_name_list):
            self.frame_info_error_label.configure(text="'Timestamp Field: {}' is not a valid!".format(self.main_timestamp_name_combobox.get()))
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                             fg_color="#395E9C")
            return

        if self.main_timestamp_format == "datetime":
            if not self.__input_validation.is_datetime_timestamp_valid(timestamp=start_ts):
                self.frame_info_error_label.configure(text="Start Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return
            if not self.__input_validation.is_datetime_timestamp_valid(timestamp=end_ts):
                self.frame_info_error_label.configure(text="End Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return
        elif self.main_timestamp_format == "epoch":
            if not self.__input_validation.is_epoch_timestamp_valid(timestamp=start_ts):
                self.frame_info_error_label.configure(text="Start Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return
            if not self.__input_validation.is_epoch_timestamp_valid(timestamp=end_ts):
                self.frame_info_error_label.configure(text="End Time: Incorrect Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return

        if not self.__input_validation.is_numeric_valid(user_input=num_logs):
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
            if not self.__input_validation.is_filter_valid(filter_raw=filter_raw):
                self.frame_info_error_label.configure(text="Filters: Invalid Format!")
                self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                                 fg_color="#395E9C")
                return

        keyword_sentences_dict = self.__parser.parse_filter_raw(filter_raw=filter_raw)
        query_bool_must_list = self.__converter.convert_all_is_list_to_must_list(
            filter_is_list=keyword_sentences_dict["is"],
            filter_is_gte_list=keyword_sentences_dict["is_gte"],
            filter_is_lte_list=keyword_sentences_dict["is_lte"],
            filter_is_gt_list=keyword_sentences_dict["is_gt"],
            filter_is_lt_list=keyword_sentences_dict["is_lt"],
            filter_is_one_of_list=keyword_sentences_dict["is_one_of"])
        query_bool_must_not_list = self.__converter.convert_all_is_not_list_to_must_not_list(
            filter_is_not_list=keyword_sentences_dict["is_not"],
            filter_is_not_gte_list=keyword_sentences_dict["is_not_gte"],
            filter_is_not_lte_list=keyword_sentences_dict["is_not_lte"],
            filter_is_not_gt_list=keyword_sentences_dict["is_not_gt"],
            filter_is_not_lt_list=keyword_sentences_dict["is_not_lt"],
            filter_is_not_one_of_list=keyword_sentences_dict["is_not_one_of"])

        if not self.__input_validation.is_file_format_valid(file_format=self.file_format):
            self.frame_info_error_label.configure(text="File Format: Invalid format!")
            self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                             fg_color="#395E9C")
            return

        # Configure the batch size according to elasticfetch.ini
        index_max_result_window_dict = self.__request_sender.get_max_result_window(index_name=self.current_index)
        for index in index_max_result_window_dict:
            if config_reader.batch_size > index_max_result_window_dict[index]:
                self.__request_sender.put_max_result_window(index_name=index, size=config_reader.batch_size)

        self.__data_fetch_thread = threading.Thread(target=self.__request_sender.get_fetch_elastic_data_between_ts1_ts2,
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
        self.progress_bar_label.configure(text="Current Progress: {}/{} --- {:.2f}%".format(0,
                                                                                      num_logs,
                                                                                      self.progress_bar["value"]))
        self.primary_app_window.update()

        if self.file_format == "csv":
            self.__data_write_csv_thread = threading.Thread(target=self.__data_writer.write_to_csv,
                                                     kwargs={
                                                         "request_sender": self.__request_sender,
                                                         "fields_list": fields_list
                                                     })
            self.__data_write_csv_thread.start()
            self.__data_fetch_thread.start()

            self.saved_filepath_label.configure(text="Saving data to {}".format(self.__data_writer.csv_filepath))
            while not self.__request_sender.has_finished_fetching:
                self.progress_bar["value"] = (self.__request_sender.total_results_size / float(num_logs)) * 100
                self.progress_bar_label.configure(text="Current Progress: {}/{} --- {:.2f}%".format(self.__request_sender.total_results_size,
                                                                                                    num_logs,
                                                                                                    self.progress_bar["value"]))
                self.primary_app_window.update()

            self.progress_bar["value"] = (self.__request_sender.total_results_size / float(num_logs)) * 100
            self.progress_bar_label.configure(
                text="Current Progress: {}/{} --- {:.2f}%".format(self.__request_sender.total_results_size,
                                                                  num_logs,
                                                                  self.progress_bar["value"]))
            self.primary_app_window.update()

            self.__data_write_csv_thread.join()
            self.__data_fetch_thread.join()

            self.progress_bar_label.configure(text="")
            self.saved_filepath_label.configure(text="Successfully saved {} data to {}".format(self.__request_sender.total_results_size,
                                                                                               self.__data_writer.csv_filepath))
            self.primary_app_window.update()

        elif self.file_format == "jsonl":
            data_write_json_thread = threading.Thread(target=self.__data_writer.write_to_jsonl,
                                                      kwargs={
                                                          "request_sender": self.__request_sender,
                                                      })
            self.__data_write_json_thread.start()
            self.__data_fetch_thread.start()

            self.saved_filepath_label.configure(text="Saving data to {}".format(self.__data_writer.json_filepath))
            while not self.__request_sender.has_finished_fetching:
                self.progress_bar["value"] = (self.__request_sender.total_results_size / float(num_logs)) * 100
                self.progress_bar_label.configure(text="Current Progress: {}/{} --- {:.2f}%".format(self.__request_sender.total_results_size,
                                                                                                    num_logs,
                                                                                                    self.progress_bar["value"]))
                self.primary_app_window.update()

            self.progress_bar["value"] = (self.__request_sender.total_results_size / float(num_logs)) * 100
            self.progress_bar_label.configure(
                text="Current Progress: {}/{} --- {:.2f}%".format(self.__request_sender.total_results_size,
                                                                  num_logs,
                                                                  self.progress_bar["value"]))
            self.primary_app_window.update()

            self.__data_write_json_thread.join()
            self.__data_fetch_thread.join()

            self.progress_bar_label.configure(text="")
            self.saved_filepath_label.configure(text="Successfully saved {} data to {}".format(self.__request_sender.total_results_size,
                                                                                               self.__data_writer.json_filepath))
            self.primary_app_window.update()

        self.fetch_data_button.configure(state=customtkinter.NORMAL,
                                         fg_color="#395E9C")

        # Configure back to the original settings
        for index in index_max_result_window_dict:
            if config_reader.batch_size > index_max_result_window_dict[index]:
                self.__request_sender.put_max_result_window(index_name=index, size=index_max_result_window_dict[index])
        return

    def display_ts_converter_window(self) -> None:
        """
        Display the timestamp converter window.

        This method opens a window or interface allowing the user to convert timestamps
        between different formats, helping them work with diverse timestamp representations.

        :return: None
        :rtype: None
        """
        window = GUITSConverter(converter=self.__converter,
                                input_validation=self.__input_validation)
        window.after(10, window.lift)
        return

    def on_closing_primary_app_window(self) -> None:
        """
        Handle the closing event of the primary application window.

        This method is called when the user attempts to close the main application window,
        allowing for necessary cleanup operations or confirmation dialogs.

        :return: None
        :rtype: None
        """

        if not messagebox.askokcancel("Quit", "Are you sure?"):
            return

        if self.__data_fetch_thread:
            self.__data_fetch_thread.join()
        if self.__data_write_csv_thread:
            self.__data_write_csv_thread.join()
        if self.__data_write_json_thread:
            self.__data_write_json_thread.join()
        self.primary_app_window.destroy()
        return

    def notify_to_press_return_key(self, event) -> None:
        """
        Notify the user to press the return key in response to a tkinter event.

        This method displays a notification or prompts the user,
        instructing them to press the return key in response to a tkinter event.

        :param event: The tkinter event triggering the notification.
        :type event: tkinter.Event

        :return: None
        :rtype: None
        """
        if self.has_pressed_return_key:
            self.frame_info_error_label.configure(text="")
            self.has_pressed_return_key = False
        else:
            self.frame_info_error_label.configure(text="Hit <Enter> to confirm new index selection!")
        return

    def load_image(self,
                   path: str,
                   image_size: int):
        """
        Load and resize an image from a specified path.

        This method loads an image from the specified path relative to the global PATH,
        resizes it to the given image_size, and returns it as a PhotoImage.

        :param path: The relative path to the image file.
        :type path: str

        :param image_size: The desired size (width) of the loaded image.
        :type image_size: int

        :return: A PhotoImage object representing the loaded and resized image.
        :rtype: ImageTk.PhotoImage
        """
        return ImageTk.PhotoImage(Image.open(os.path.join(PATH, path)).resize((image_size, int(image_size*0.75))))
