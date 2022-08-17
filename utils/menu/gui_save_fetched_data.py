import customtkinter
from utils.converter import Converter
from utils.input_validation import InputValidation
from utils.request_sender import RequestSender
import os
import datetime

PATH = os.path.dirname(os.path.realpath(__file__))

class GUISavedFetchedData(customtkinter.CTkToplevel):
    def __init__(self,
                 data_json_list: list,
                 converter: Converter,
                 input_validation: InputValidation):
        super().__init__()
        self.data_json_list = data_json_list
        self.converter = converter
        self.input_validation = input_validation
        self.geometry("680x300")
        self.title("elasticfetch - Fetch Progress")
        self.resizable(False, False)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1, minsize=20)

        self.frame_main = customtkinter.CTkFrame(master=self, width=640, height=260, corner_radius=15)
        self.frame_main.grid(row=0, column=0, padx=20, pady=20, columnspan=3, sticky="nsew")
        self.frame_main.grid_columnconfigure(0, weight=1)
        self.frame_main.grid_columnconfigure(1, weight=1)


        '''if len(data_json_list) == 0:
            return
        while True:
            filename = input("File name to save as (.json, .csv): ")
            is_valid_file_extension = self.input_validation.is_file_extension_valid(filename=filename)
            if is_valid_file_extension:
                break
        file_path = "datasets/" + filename
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if file_path.lower().endswith(".csv"):
            self.converter.convert_json_data_to_csv(data_json_list=data_json_list, fields_list=fields_list,
                                                    file_path=file_path)
        elif file_path.lower().endswith(".json"):
            self.converter.convert_json_data_to_json(data_json_list=data_json_list, file_path=file_path)'''
        return

    def get_progress_bar(self):
        return self.progress_bar


