import customtkinter
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))


class GUITSConverter(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("600x260")
        self.title("elasticfetch - Timestamp Converter")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,2), weight=1, minsize=20)

        self.frame_left = customtkinter.CTkFrame(master=self, width=200, height=240, corner_radius=15)
        self.frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_left.grid_columnconfigure(0, weight=1)
        self.frame_left.grid_columnconfigure(1, weight=1)

        self.frame_middle = customtkinter.CTkFrame(master=self, width=40, height=100, corner_radius=15)
        self.frame_middle.grid(row=0, column=1, padx=5, sticky="ew")
        self.frame_middle.grid_columnconfigure(0, weight=1)

        self.frame_right = customtkinter.CTkFrame(master=self, width=200, height=240, corner_radius=15)
        self.frame_right.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=1)

        self.left_arrow_image = self.load_image("/images/icons8-left-arrow-50.png", 20)
        self.right_arrow_image = self.load_image("/images/icons8-right-arrow-50.png", 20)

        self.datetime_label = customtkinter.CTkLabel(master=self.frame_left, text="DateTime Format", text_font=("Arial", 13))
        self.datetime_label.grid(row=0, column=0, pady=10, padx=20)
        self.datetime_start_ts_label = customtkinter.CTkLabel(master=self.frame_left, text="Start Timestamp:", text_font=("Arial", 10))
        self.datetime_start_ts_label.grid(row=1, column=0)
        self.datetime_start_ts_entry = customtkinter.CTkEntry(master=self.frame_left, height=32, placeholder_text="eg. 2022-05-01T00:00:00")
        self.datetime_start_ts_entry.grid(row=2, column=0, columnspan=3, padx=20, pady=0, sticky="ew")

        self.datetime_end_ts_label = customtkinter.CTkLabel(master=self.frame_left, text="End Timestamp:", text_font=("Arial", 10))
        self.datetime_end_ts_label.grid(row=3, column=0)
        self.datetime_end_ts_entry = customtkinter.CTkEntry(master=self.frame_left, height=32, placeholder_text="eg. 2022-05-20T00:00:00")
        self.datetime_end_ts_entry.grid(row=4, column=0, columnspan=3, padx=20, pady=0, sticky="ew")

        self.right_arrow_button = customtkinter.CTkButton(master=self.frame_middle, image=self.right_arrow_image, text="", width=40, height=40,
                                                          corner_radius=10, fg_color="gray40", hover_color="gray25",
                                                          command=self.button_function)
        self.right_arrow_button.grid(row=2, column=0, columnspan=1, padx=5, pady=10, sticky="nswe")

        self.left_arrow_button = customtkinter.CTkButton(master=self.frame_middle, image=self.left_arrow_image, text="", width=40, height=40,
                                                         corner_radius=10, fg_color="gray40", hover_color="gray25",
                                                         command=self.button_function)
        self.left_arrow_button.grid(row=4, column=0, columnspan=1, padx=5, pady=10, sticky="nsew")

        self.epoch_label = customtkinter.CTkLabel(master=self.frame_right, text="Epoch Format",
                                                  text_font=("Arial", 13))
        self.epoch_label.grid(row=0, column=0, pady=10, padx=20)
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


    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def button_function(self):
        print("button pressed")

