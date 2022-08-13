import customtkinter
from PIL import Image, ImageTk
import os
import datetime

PATH = os.path.dirname(os.path.realpath(__file__))


class GUITSConverter(customtkinter.CTkToplevel):
    def __init__(self,
                 converter,
                 input_validation):
        super().__init__()
        self.converter = converter
        self.input_validation = input_validation
        self.timezone = "+00:00"
        self.geometry("680x300")
        self.title("elasticfetch - Timestamp Converter")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1, minsize=20)

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, height=260, corner_radius=15)
        self.frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_left.grid_columnconfigure(0, weight=1)
        self.frame_left.grid_columnconfigure(1, weight=1)

        self.frame_middle = customtkinter.CTkFrame(master=self, width=40, height=100, corner_radius=15)
        self.frame_middle.grid(row=0, column=1, padx=5, sticky="ew")
        self.frame_middle.grid_columnconfigure(0, weight=1)

        self.frame_right = customtkinter.CTkFrame(master=self, width=200, height=260, corner_radius=15)
        self.frame_right.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=1)

        self.left_arrow_image = self.load_image("/images/icons8-left-arrow-50.png", 20)
        self.right_arrow_image = self.load_image("/images/icons8-right-arrow-50.png", 20)

        self.datetime_label = customtkinter.CTkLabel(master=self.frame_left, text="DateTime Format", text_font=("Arial", 13))
        self.datetime_label.grid(row=0, column=0, pady=10, padx=40)
        self.datetime_start_ts_label = customtkinter.CTkLabel(master=self.frame_left, text="Start Timestamp:", text_font=("Arial", 10))
        self.datetime_start_ts_label.grid(row=1, column=0)
        self.datetime_start_ts_entry = customtkinter.CTkEntry(master=self.frame_left, height=32, placeholder_text="eg. 2022-05-01T00:00:00")
        self.datetime_start_ts_entry.grid(row=2, column=0, columnspan=3, padx=20, pady=0, sticky="ew")

        self.datetime_end_ts_label = customtkinter.CTkLabel(master=self.frame_left, text="End Timestamp:", text_font=("Arial", 10))
        self.datetime_end_ts_label.grid(row=3, column=0)
        self.datetime_end_ts_entry = customtkinter.CTkEntry(master=self.frame_left, height=32, placeholder_text="eg. 2022-05-20T00:00:00")
        self.datetime_end_ts_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=0, sticky="ew")

        # Selecting Timezone
        self.timezone_label = customtkinter.CTkLabel(master=self.frame_left,
                                                     text="Timezone:",
                                                     text_font=("Arial", 10))  # font name and size in px
        self.timezone_label.grid(row=5, column=0, pady=0, padx=20)
        self.timezone_optionmenu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                               values=self.input_validation.valid_timezone_list,
                                                               command=self.set_timezone)
        self.timezone_optionmenu.set(self.timezone)
        self.timezone_optionmenu.grid(row=6, column=0, pady=0, padx=20)

        self.frame_left_error_label = customtkinter.CTkLabel(master=self.frame_left,
                                                             text="",
                                                             text_font=("Arial", 10),
                                                             text_color="red")
        self.frame_left_error_label.grid(row=7, column=0, pady=0, padx=20)

        self.right_arrow_button = customtkinter.CTkButton(master=self.frame_middle, image=self.right_arrow_image, text="", width=40, height=40,
                                                          corner_radius=10, fg_color="#395E9C", hover_color="#144870",
                                                          command=self.convert_datetime_to_epoch)
        self.right_arrow_button.grid(row=2, column=0, columnspan=1, padx=5, pady=10, sticky="nswe")

        self.left_arrow_button = customtkinter.CTkButton(master=self.frame_middle, image=self.left_arrow_image, text="", width=40, height=40,
                                                         corner_radius=10, fg_color="#395E9C", hover_color="#144870",
                                                         command=self.convert_epoch_to_datetime)
        self.left_arrow_button.grid(row=4, column=0, columnspan=1, padx=5, pady=10, sticky="nsew")

        self.epoch_label = customtkinter.CTkLabel(master=self.frame_right, text="Epoch Format",
                                                  text_font=("Arial", 13))
        self.epoch_label.grid(row=0, column=0, pady=10, padx=50)
        self.epoch_start_ts_label = customtkinter.CTkLabel(master=self.frame_right, text="Start Timestamp:",
                                                              text_font=("Arial", 10))
        self.epoch_start_ts_label.grid(row=1, column=0)
        self.epoch_start_ts_entry = customtkinter.CTkEntry(master=self.frame_right, height=32,
                                                              placeholder_text="eg. 1651363200000")
        self.epoch_start_ts_entry.grid(row=2, column=0, columnspan=3, padx=20, pady=0, sticky="ew")

        self.epoch_end_ts_label = customtkinter.CTkLabel(master=self.frame_right, text="End Timestamp:",
                                                            text_font=("Arial", 10))
        self.epoch_end_ts_label.grid(row=3, column=0)
        self.epoch_end_ts_entry = customtkinter.CTkEntry(master=self.frame_right, height=32,
                                                            placeholder_text="eg. 1653004800000")
        self.epoch_end_ts_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=0, sticky="ew")

        self.frame_right_error_label = customtkinter.CTkLabel(master=self.frame_right,
                                                              text="",
                                                              text_font=("Arial", 10),
                                                              text_color="red")
        self.frame_right_error_label.grid(row=5, column=0, pady=55, padx=20)

    def convert_datetime_to_epoch(self):
        self.frame_left_error_label.configure(text="")
        self.frame_right_error_label.configure(text="")

        start_ts_datetime = self.datetime_start_ts_entry.get().strip()
        end_ts_datetime = self.datetime_end_ts_entry.get().strip()

        if not self.input_validation.is_datetime_timestamp_valid(timestamp=start_ts_datetime):
            self.frame_left_error_label.configure(text="Start Time: Incorrect format!")
            self.clear_epoch_entries()
            return

        if not self.input_validation.is_datetime_timestamp_valid(timestamp=end_ts_datetime):
            self.frame_left_error_label.configure(text="End Time: Incorrect format!")
            self.clear_epoch_entries()
            return

        if not self.input_validation.is_endts_gte_startts(timestamp_format="datetime",
                                                          start_ts=start_ts_datetime,
                                                          end_ts=end_ts_datetime):
            self.frame_left_error_label.configure(text="End Time < Start Time! Error!")
            self.clear_epoch_entries()
            return

        start_ts_epoch = self.converter.convert_datetime_to_epoch_millis(date_time=start_ts_datetime,
                                                                         timezone=self.timezone)
        end_ts_epoch = self.converter.convert_datetime_to_epoch_millis(date_time=end_ts_datetime,
                                                                       timezone=self.timezone)
        self.clear_epoch_entries()
        self.epoch_start_ts_entry.insert(0, start_ts_epoch)
        self.epoch_end_ts_entry.insert(0, end_ts_epoch)
        return

    def convert_epoch_to_datetime(self):

        self.frame_left_error_label.configure(text="")
        self.frame_right_error_label.configure(text="")

        start_ts_epoch = self.epoch_start_ts_entry.get().strip()
        end_ts_epoch = self.epoch_end_ts_entry.get().strip()

        if not self.input_validation.is_epoch_timestamp_valid(timestamp=start_ts_epoch):
            self.frame_right_error_label.configure(text="Start Time: Incorrect format!")
            self.clear_datetime_entries()
            return

        if not self.input_validation.is_epoch_timestamp_valid(timestamp=end_ts_epoch):
            self.frame_right_error_label.configure(text="End Time: Incorrect Format!")
            self.clear_datetime_entries()
            return

        if not self.input_validation.is_endts_gte_startts(timestamp_format="epoch",
                                                          start_ts=start_ts_epoch,
                                                          end_ts=end_ts_epoch):
            self.frame_right_error_label.configure(text="End Time < Start Time! Error!")
            self.clear_datetime_entries()
            return

        start_ts_date_time = self.converter.convert_epoch_millis_to_datetime(epoch=start_ts_epoch, timezone=self.timezone)
        end_ts_date_time = self.converter.convert_epoch_millis_to_datetime(epoch=end_ts_epoch, timezone=self.timezone)

        self.clear_datetime_entries()
        self.datetime_start_ts_entry.insert(0, start_ts_date_time)
        self.datetime_end_ts_entry.insert(0, end_ts_date_time)
        return

    def set_timezone(self, timezone):
        self.timezone = timezone
        return

    def clear_epoch_entries(self):
        self.epoch_start_ts_entry.delete(0, customtkinter.END)
        self.epoch_end_ts_entry.delete(0, customtkinter.END)
        return

    def clear_datetime_entries(self):
        self.datetime_start_ts_entry.delete(0, customtkinter.END)
        self.datetime_end_ts_entry.delete(0, customtkinter.END)
        return

    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

