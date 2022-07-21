import os

class Menu:

    def __init__(self, request_sender, converter, input_validation, parser):
        self.description = "Provides users different options when feteching elastic data"
        self.request_sender = request_sender
        self.converter = converter
        self.input_validation = input_validation
        self.menu_options = {
            1: 'Show indices status',
            2: 'Set current index',
            3: 'Show available field names',
            4: 'Fetch data between two timestamps',
            5: 'Exit',
        }
        self.input_validation = input_validation
        self.parser = parser
        self.index_name = ""

    def show_menu(self):
        header = "============================================================================================================\n" \
                 "           /$$                       /$$     /$$             /$$$$$$             /$$               /$$      \n" \
                 "          | $$                      | $$    |__/            /$$__  $$           | $$              | $$      \n" \
                 "  /$$$$$$ | $$  /$$$$$$   /$$$$$$$ /$$$$$$   /$$  /$$$$$$$ | $$  \__/ /$$$$$$  /$$$$$$    /$$$$$$$| $$$$$$$ \n" \
                 " /$$__  $$| $$ |____  $$ /$$_____/|_  $$_/  | $$ /$$_____/ | $$$$    /$$__  $$|_  $$_/   /$$_____/| $$__  $$\n" \
                 "| $$$$$$$$| $$  /$$$$$$$|  $$$$$$   | $$    | $$| $$       | $$_/   | $$$$$$$$  | $$    | $$      | $$  \ $$\n" \
                 "| $$_____/| $$ /$$__  $$ \____  $$  | $$ /$$| $$| $$       | $$     | $$_____/  | $$ /$$| $$      | $$  | $$\n" \
                 "|  $$$$$$$| $$|  $$$$$$$ /$$$$$$$/  |  $$$$/| $$|  $$$$$$$ | $$     |  $$$$$$$  |  $$$$/|  $$$$$$$| $$  | $$\n" \
                 " \_______/|__/ \_______/|_______/    \___/  |__/ \_______/ |__/      \_______/   \___/   \_______/|__/  |__/\n\n" \
                 "Developed by: Gerald Lim Wee Koon (github: mathscantor)                                                     \n" \
                 "============================================================================================================\n"
        print(header)
        if self.index_name == "":
            print("Current index selected:\033[93m N/A (Please set an index before fetching any data!)\033[0m\n")
        else:
            print("Current index selected:\033[93m {}\033[0m\n".format(self.index_name))

        for key in self.menu_options.keys():
            print(key, '--', self.menu_options[key])
        menu_option = input('Enter your choice: ')
        if not self.input_validation.is_numeric_valid(menu_option):
            return
        menu_option = int(menu_option)
        if not self.input_validation.is_option_in_available(menu_option, self.menu_options):
            return
        print("")

        if menu_option == 1:
            self.show_indices_status()
        elif menu_option == 2:
            self.set_current_index()
        elif menu_option == 3:
            if self.input_validation.is_index_name_set(self.index_name):
                self.show_available_fields()
        elif menu_option == 4:
            if self.input_validation.is_index_name_set(self.index_name):
                self.fetch_elastic_data_between_ts1_ts2()
        elif menu_option == 5:
            exit(0)
        return

    def show_indices_status(self):
        indices_status = self.request_sender.get_indices_status()
        print(indices_status)
        return

    def set_current_index(self):
        indices_status = self.request_sender.get_indices_status()
        temp_list = indices_status.split("\n")[1:-1]
        index_dict = {}
        i = 1
        for entry in temp_list:
            index_name = entry.split()[2]
            index_dict[i] = index_name
            i += 1
        print("Listing all beats indices:\n")
        for key in index_dict.keys():
            print(key, '--', index_dict[key])
        print("")
        index_option = input('Enter your index choice: ')
        if not self.input_validation.is_numeric_valid(index_option):
            return
        index_option = int(index_option)
        if not self.input_validation.is_option_in_available(option=index_option, options_dict=index_dict):
            return
        self.index_name = index_dict[index_option]

    def show_available_fields(self):
        response = self.request_sender.get_available_fields(index_name=self.index_name)
        print(response)
        return

    def fetch_elastic_data_between_ts1_ts2(self):
        print("timestamp format: <YYYY-MM-DD>T<HH:mm:ss>\neg. 2022-05-01T00:00:00")

        start_ts = input("start timestamp: ")
        if not self.input_validation.is_timestamp_valid(start_ts):
            return
        end_ts = input("end timestamp: ")
        if not self.input_validation.is_timestamp_valid(end_ts):
            return
        if not self.input_validation.is_endts_gte_startts(start_ts=start_ts, end_ts=end_ts):
            return
        num_logs = input("Number of logs to retrieve: ")
        if not self.input_validation.is_numeric_valid(num_logs):
            return
        fields = input("Select your field names (eg. event.created,event.code,message): ")
        fields_list = [x.strip() for x in fields.split(',')]
        num_logs = int(num_logs)

        # currently only supporting "is" and "is_not"
        #TODO: support "is not"
        print("\nFilter Format: <FIELD_NAME> <FILTER_KEYWORD> <VALUE>;")
        print("Supported Filter Keywords:\n"
              "- is_not_gte\n"
              "- is_not_lte\n"
              "- is_not_gt\n"
              "- is_not_lt\n"
              "- is_not\n"
              "- is_gte\n"
              "- is_lte\n"
              "- is_gt\n"
              "- is_lt\n"
              "- is\n")
        print("eg. event.code is_gt 4000; event.code is_lte 5000; event.category is authentication;")
        filter_raw = input("(OPTIONAL - PRESS ENTER TO SKIP) Filter your queries: ")
        if filter_raw.strip() != "":
            if not self.input_validation.is_filter_valid(filter_raw=filter_raw):
                return

        keyword_sentences_dict = self.parser.parse_filter_raw(filter_raw=filter_raw)
        query_bool_must_list = self.converter.convert_all_is_list_to_must_list(filter_is_list=keyword_sentences_dict["is"],
                                                                               filter_is_gte_list=keyword_sentences_dict["is_gte"],
                                                                               filter_is_lte_list=keyword_sentences_dict["is_lte"],
                                                                               filter_is_gt_list=keyword_sentences_dict["is_gt"],
                                                                               filter_is_lt_list=keyword_sentences_dict["is_lt"])
        query_bool_must_not_list = self.converter.convert_all_is_not_list_to_must_not_list(filter_is_not_list=keyword_sentences_dict["is_not"],
                                                                                       filter_is_not_gte_list=keyword_sentences_dict["is_not_gte"],
                                                                                       filter_is_not_lte_list=keyword_sentences_dict["is_not_lte"],
                                                                                       filter_is_not_gt_list=keyword_sentences_dict["is_not_gt"],
                                                                                       filter_is_not_lt_list=keyword_sentences_dict["is_not_lt"])

        data_json_list = self.request_sender.get_fetch_elastic_data_between_ts1_ts2(index_name=self.index_name,
                                                                               num_logs=num_logs,
                                                                               start_ts=start_ts,
                                                                               end_ts=end_ts,
                                                                               fields_list=fields_list,
                                                                               query_bool_must_list=query_bool_must_list,
                                                                               query_bool_must_not_list=query_bool_must_not_list)

        if len(data_json_list) == 0:
            return
        while True:
            filename = input("File name to save as (.json, .csv): ")
            is_valid_file_extension = self.input_validation.is_file_extension_valid(filename=filename)
            if is_valid_file_extension:
                break
        file_path = "datasets/" + filename
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if file_path.lower().endswith(".csv"):
            self.converter.convert_json_data_to_csv(data_json_list=data_json_list, fields_list=fields_list, file_path=file_path)
        elif file_path.lower().endswith(".json"):
            self.converter.convert_json_data_to_json(data_json_list=data_json_list, file_path=file_path)
        return





