class Menu:

    def __init__(self, request_sender, converter, input_validation, parser):
        self.description = "Provides users different options when feteching elastic data"
        self.request_sender = request_sender
        self.converter = converter
        self.input_validation = input_validation
        self.menu_options = {
            1: 'Show indices status',
            2: 'Set current index',
            3: 'Fetch data between two timestamps',
            4: 'Exit',
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
            self.fetch_elastic_data_between_ts1_ts2()
        elif menu_option == 4:
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
        for key in index_dict.keys():
            print(key, '--', index_dict[key])
        index_option = input('Enter your index choice: ')
        if not self.input_validation.is_numeric_valid(index_option):
            return
        index_option = int(index_option)
        if not self.input_validation.is_option_in_available(option=index_option, options_dict=index_dict):
            return
        self.index_name = index_dict[index_option]

    def fetch_elastic_data_between_ts1_ts2(self):
        keyword_sentences_dict = {}
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

        # currently only supporting "is" and "is not"
        #TODO: support "is not"
        print("Filter Format: FIELD1 is VALUE; FIELD2 is_not VALUE;) ")
        filter_raw = input("(OPTIONAL - Press Enter to skip) Filter your queries : ")
        keyword_sentences_dict = self.parser.parse_filter_raw(filter_raw=filter_raw)
        query_bool_must_list = self.converter.convert_is_raw_to_list(filter_is_raw_list=keyword_sentences_dict["is"])
        query_bool_must_not_list = self.converter.convert_is_not_raw_to_list(filter_is_not_raw_list=keyword_sentences_dict["is_not"])

        if num_logs > 10000:
            self.request_sender.put_max_result_window(num_logs)
        pit_id = self.request_sender.post_fetch_pit_id(index_name=self.index_name)
        if pit_id is None:
            return

        data_json = self.request_sender.get_fetch_elastic_data_between_ts1_ts2(pit_id=pit_id,
                                                                               num_logs=num_logs,
                                                                               start_ts=start_ts,
                                                                               end_ts=end_ts,
                                                                               fields_list=fields_list,
                                                                               query_bool_must_list=query_bool_must_list,
                                                                               query_bool_must_not_list = query_bool_must_not_list)
        self.request_sender.delete_pit_id(pit_id)
        self.request_sender.put_max_result_window(10000)
        if data_json is None:
            return
        filename = input("File name to save as: ")
        self.converter.convert_json_to_csv(data_json=data_json, fields_list=fields_list, filename=filename)
        return





