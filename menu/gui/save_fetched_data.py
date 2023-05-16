import customtkinter
from utils.converter import Converter
from utils.input_validation import InputValidation
import os


class GUISaveFetchedData(customtkinter.CTkToplevel):
    def __init__(self,
                 data_json_list: list,
                 fields_list: list,
                 converter: Converter,
                 input_validation: InputValidation):
        super().__init__()
        self.data_json_list = data_json_list
        self.fields_list = fields_list
        self.converter = converter
        self.input_validation = input_validation
        self.geometry("680x300")
        self.title("elasticfetch - Save Fetched Data")
        self.resizable(False, False)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.frame_main = customtkinter.CTkFrame(master=self, width=640, height=200, corner_radius=15)
        self.frame_main.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_main.grid_columnconfigure((0, 1), weight=1)
        self.frame_main.grid(row=0, column=0, padx=20, pady=20, columnspan=2, rowspan=3, sticky="nsew")

        self.filename_label = customtkinter.CTkLabel(master=self.frame_main,
                                                     text="File Name",
                                                     text_font=("Arial", 11))
        self.filename_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        self.filename_entry = customtkinter.CTkEntry(master=self.frame_main,
                                                     placeholder_text="Valid Extensions: .csv, .json",
                                                     width=200)
        self.filename_entry.grid(row=1, column=0, columnspan=2, pady=5, padx=20, sticky="we")
        self.debug_label = customtkinter.CTkLabel(master=self.frame_main,
                                                  text="",
                                                  text_font=("Arial", 11),
                                                  text_color="red")
        self.debug_label.grid(row=2, column=0, columnspan=2, sticky="w")
        self.save_button = customtkinter.CTkButton(master=self.frame_main,
                                                   text="save",
                                                   text_font=("Arial", 11),
                                                   command=self.save_file,
                                                   width=50)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=30, padx=20, sticky="s")
        return

    def save_file(self):
        self.debug_label.configure(text_color="red")
        self.debug_label.set_text("")
        filename = self.filename_entry.get()
        if not self.input_validation.is_file_extension_valid(filename=filename):
            self.debug_label.set_text("Invalid file extension!")
            return

        self.save_button.configure(state=customtkinter.DISABLED, fg_color="grey")
        file_path = "datasets/" + filename
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if file_path.lower().endswith(".csv"):
            self.converter.convert_json_data_to_csv(data_json_list=self.data_json_list, fields_list=self.fields_list,
                                                    file_path=file_path)
        elif file_path.lower().endswith(".json"):
            self.converter.convert_json_data_to_json(data_json_list=self.data_json_list, file_path=file_path)

        self.debug_label.configure(text_color="green")
        self.debug_label.set_text("Saved to datasets/{}".format(filename))
        self.save_button.configure(state=customtkinter.NORMAL,
                                   fg_color="#395E9C")
        return
