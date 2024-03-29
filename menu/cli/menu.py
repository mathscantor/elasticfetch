import threading
from utils.request_sender import RequestSender
from utils.converter import Converter
from utils.input_validation import InputValidation
from utils.parser import Parser
from utils.data_writer import DataWriter
from utils.config_reader import ConfigReader


class CommandLineMenu:

    def __init__(self,
                 request_sender: RequestSender,
                 converter: Converter,
                 input_validation: InputValidation,
                 parser: Parser,
                 config_reader: ConfigReader):

        self.__request_sender = request_sender
        self.__data_writer = DataWriter()
        self.__converter = converter
        self.__input_validation = input_validation
        self.__menu_options = {
            1: 'Show indices status',
            2: 'Set current index',
            3: 'Set main timestamp name, format and timezone',
            4: 'Show available field names',
            5: 'Convert Timestamp Format',
            6: 'Fetch data between two timestamps',
            7: 'Exit',
        }
        self.__convert_timestamp_menu_options = {
            1: 'Convert datetime to epoch',
            2: 'Convert epoch to datetime'
        }
        self.__input_validation = input_validation
        self.__parser = parser
        self.__config_reader = config_reader
        self.__index_name = "N/A"
        self.__main_timestamp_name = "@timestamp"
        self.__main_timestamp_format = "datetime"
        self.__main_timezone = "+00:00"
        self.__header = r"===============================================================""\n" \
                        r"        _              _    _         __       _         _     ""\n" \
                        r"       | |            | |  (_)       / _|     | |       | |    ""\n" \
                        r"   ___ | |  __ _  ___ | |_  _   ___ | |_  ___ | |_  ___ | |__  ""\n" \
                        r"  / _ \| | / _` |/ __|| __|| | / __||  _|/ _ \| __|/ __|| '_ \ ""\n" \
                        r" |  __/| || (_| |\__ \| |_ | || (__ | | |  __/| |_| (__ | | | |""\n" \
                        r"  \___||_| \__,_||___/ \__||_| \___||_|  \___| \__|\___||_| |_|""\n""\n"\
                        r"    Developed by: Gerald Lim Wee Koon (github: mathscantor)    ""\n" \
                        r"===============================================================""\n"
        return

    def show_menu(self) -> None:
        """
        Display the main menu to the user.

        This method prints the main menu options to the console or user interface.

        :return: None
        :rtype: None
        """
        print(self.__header)
        if self.__index_name == "N/A":
            print("Current index selected:\033[93m N/A (Please set an index before fetching any data!)\033[0m")
        else:
            print("Current index selected:\033[93m {}\033[0m".format(self.__index_name))
        print("Main Timestamp Field: \033[93m {}\033[0m".format(self.__main_timestamp_name))
        print("Main Timestamp Format: \033[93m {}\033[0m".format(self.__main_timestamp_format))
        print("Main Timezone: \033[93m {}\033[0m\n".format(self.__main_timezone))

        for key in self.__menu_options.keys():
            print(key, '--', self.__menu_options[key])
        menu_option = input('Enter your choice: ')
        if not self.__input_validation.is_numeric_valid(menu_option):
            return
        menu_option = int(menu_option)
        if not self.__input_validation.is_option_in_available(menu_option, self.__menu_options):
            return
        print("")

        if menu_option == 1:
            self.show_indices_status()
        elif menu_option == 2:
            self.set_current_index()
        elif menu_option == 3:
            if self.__input_validation.is_index_name_set(self.__index_name):
                self.set_main_timestamp()
        elif menu_option == 4:
            if self.__input_validation.is_index_name_set(self.__index_name):
                self.show_available_fields()
        elif menu_option == 5:
            self.convert_timestamp_format()
        elif menu_option == 6:
            if self.__input_validation.is_index_name_set(self.__index_name):
                self.fetch_elastic_data_between_ts1_ts2()
        elif menu_option == 7:
            exit(0)
        return

    def show_indices_status(self) -> None:
        """
        Display the status of Elasticsearch indices.

        This method retrieves and prints the status of all indices in the Elasticsearch cluster.

        :return: None
        :rtype: None
        """
        indices_status = self.__request_sender.get_indices_status()
        print(indices_status)
        return

    def set_current_index(self) -> None:
        """
        Set the current Elasticsearch index.

        This method allows the user to set the current Elasticsearch index for subsequent operations.

        :return: None
        :rtype: None
        """
        indices_status = self.__request_sender.get_indices_status()
        temp_list = indices_status.split("\n")[1:-1]
        index_dict = dict()

        index_dict[0] = "Custom Index Name (Wildcard * available for use)"
        i = 1
        for entry in temp_list:
            index_name = entry.split()[2]
            index_dict[i] = index_name
            i += 1
        print("Listing all indices:\n")
        for key in index_dict.keys():
            print(key, '--', index_dict[key])
        print("")
        index_option = input('Enter your index choice: ')
        if not self.__input_validation.is_numeric_valid(index_option):
            return
        index_option = int(index_option)
        if not self.__input_validation.is_option_in_available(option=index_option, options_dict=index_dict):
            return

        if index_option == 0:
            self.__index_name = str(input("Enter your custom index name: "))
        else:
            self.__index_name = index_dict[index_option]
        return

    def set_main_timestamp(self) -> None:
        """
        Set the main timestamp configuration.

        This method allows the user to configure the main timestamp, including its name, format, and timezone.

        :return: None
        :rtype: None
        """
        response = self.__request_sender.get_available_fields(index_name=self.__index_name)
        if response is not None:
            parent_field_to_type_dict = self.__converter.convert_field_mapping_keys_pretty(fields_json=response)
        print("{:<30} {:<10} {:<30}".format('TOP LEVEL PARENT', 'TYPE', 'ALL RELATED FIELDS'))
        print("{:<30} {:<10} {:<30}".format('----------------', '----', '------------------'))
        valid_timestamp_name_list = []
        for top_parent_field in parent_field_to_type_dict.keys():
            has_printed_parent = False
            for field_type in parent_field_to_type_dict[top_parent_field].keys():
                if field_type == "date":
                    valid_timestamp_name_list += parent_field_to_type_dict[top_parent_field][field_type]
                    if not has_printed_parent:
                        print("{:<30} {:<10} {:<30}".format(top_parent_field, field_type,
                                                            ', '.join(
                                                                parent_field_to_type_dict[top_parent_field][
                                                                    field_type])))
                        has_printed_parent = True
                    else:
                        print("{:<30} {:<10} {:<30}".format('', field_type,
                                                            ', '.join(
                                                                parent_field_to_type_dict[top_parent_field][
                                                                    field_type])))
                    print("")

        chosen_timestamp_name = input("Main Timestamp Name: ").strip()
        if not self.__input_validation.is_timestamp_name_valid(chosen_timestamp_name=chosen_timestamp_name,
                                                               valid_timestamp_name_list=valid_timestamp_name_list):
            return
        chosen_timestamp_format = input("Main Timestamp Format: ").strip()
        if not self.__input_validation.is_timestamp_format_valid(chosen_timestamp_format=chosen_timestamp_format):
            return

        if chosen_timestamp_format == "datetime":
            chosen_timezone = input("Main Timezone: ").strip()
        elif chosen_timestamp_format == "epoch":
            chosen_timezone = "+00:00"
        if not self.__input_validation.is_timezone_valid(chosen_timezone=chosen_timezone):
            return

        self.__main_timestamp_name = chosen_timestamp_name
        self.__main_timestamp_format = chosen_timestamp_format
        self.__main_timezone = chosen_timezone
        return

    def show_available_fields(self) -> None:
        """
        Display the available fields in the current Elasticsearch index.

        This method queries the current Elasticsearch index and prints a list of available fields.

        :return: None
        :rtype: None
        """
        response = self.__request_sender.get_available_fields(index_name=self.__index_name)
        if response is not None:
            parent_field_to_type_dict = self.__converter.convert_field_mapping_keys_pretty(fields_json=response)
            print("{:<30} {:<20} {:<30}".format('TOP LEVEL PARENT', 'TYPE', 'ALL RELATED FIELDS'))
            print("{:<30} {:<20} {:<30}".format('----------------', '----', '------------------'))

            for top_parent_field in parent_field_to_type_dict.keys():
                has_printed_parent = False
                for field_type in parent_field_to_type_dict[top_parent_field].keys():
                    if not has_printed_parent:
                        print("{:<30} {:<20} {:<30}".format(top_parent_field, field_type,
                                                            ', '.join(parent_field_to_type_dict[top_parent_field][
                                                                          field_type])))
                        has_printed_parent = True
                    else:
                        print("{:<30} {:<20} {:<30}".format('', field_type,
                                                            ', '.join(parent_field_to_type_dict[top_parent_field][
                                                                          field_type])))
                print("")

        return

    def convert_timestamp_format(self) -> None:
        """
        Convert the timestamp format of the main timestamp, either from epoch to datetime and vice-versa.

        This method allows the user to convert the format of the main timestamp field.

        :return: None
        :rtype: None
        """
        for key in self.__convert_timestamp_menu_options.keys():
            print(key, '--', self.__convert_timestamp_menu_options[key])
        convert_timestamp_menu_option = input('Enter your choice: ')
        if not self.__input_validation.is_numeric_valid(convert_timestamp_menu_option):
            return
        convert_timestamp_menu_option = int(convert_timestamp_menu_option)
        if not self.__input_validation.is_option_in_available(convert_timestamp_menu_option,
                                                              self.__convert_timestamp_menu_options):
            return
        if convert_timestamp_menu_option == 1:
            self.convert_datetime_range_to_epoch_range()
        elif convert_timestamp_menu_option == 2:
            self.convert_epoch_range_to_datetime_range()
        return

    def convert_datetime_range_to_epoch_range(self) -> None:
        """
        Convert a datetime range to an epoch timestamp range.

        This method allows the user to convert the start and end timestamps from a datetime range
        to corresponding epoch timestamps in the configured timezone.

        :return: None
        :rtype: None
        """
        print("timestamp format: <%Y-%m-%d>T<%H:%M:%S> or <%Y-%m-%d>T<%H:%M:%S.%f>\n"
              "eg. 2022-05-01T00:00:00 or 2022-05-01T00:00:00.000")
        start_ts = input("Start Timestamp: ")
        if not self.__input_validation.is_datetime_timestamp_valid(timestamp=start_ts):
            return
        end_ts = input("End Timestamp: ")
        if not self.__input_validation.is_datetime_timestamp_valid(timestamp=end_ts):
            return
        chosen_timezone = input("Timezone: ")
        if not self.__input_validation.is_timezone_valid(chosen_timezone=chosen_timezone):
            return
        start_ts_epoch = self.__converter.convert_datetime_to_epoch_millis(date_time=start_ts, timezone=chosen_timezone)
        end_ts_epoch = self.__converter.convert_datetime_to_epoch_millis(date_time=end_ts, timezone=chosen_timezone)

        print("Epoch Range: {} - {}".format(start_ts_epoch, end_ts_epoch))
        return

    def convert_epoch_range_to_datetime_range(self) -> None:
        """
        Convert an epoch timestamp range to a datetime range.

        This method allows the user to convert the start and end epoch timestamps
        to corresponding datetimes in the configured timezone.

        :return: None
        :rtype: None
        """
        print("timestamp format: <10 / 13 digit string>\n"
              "eg. 1420070400 or 1420070400001")
        start_ts = input("Start Timestamp: ")
        if not self.__input_validation.is_epoch_timestamp_valid(timestamp=start_ts):
            return
        end_ts = input("End Timestamp: ")
        if not self.__input_validation.is_epoch_timestamp_valid(timestamp=end_ts):
            return
        chosen_timezone = input("Timezone: ")
        if not self.__input_validation.is_timezone_valid(chosen_timezone=chosen_timezone):
            return
        start_ts_datetime = self.__converter.convert_epoch_millis_to_datetime(epoch=start_ts, timezone=chosen_timezone)
        end_ts_datetime = self.__converter.convert_epoch_millis_to_datetime(epoch=end_ts, timezone=chosen_timezone)

        print("Datetime Range: {} - {}".format(start_ts_datetime, end_ts_datetime))
        return

    def fetch_elastic_data_between_ts1_ts2(self) -> None:
        """
        Fetch Elasticsearch data between two timestamps.

        This method retrieves data from the configured Elasticsearch index
        between the start and end timestamps using the specified query parameters.

        :return: None
        :rtype: None
        """
        if self.__main_timestamp_format == "datetime":
            print("timestamp format: <%Y-%m-%d>T<%H:%M:%S> or <%Y-%m-%d>T<%H:%M:%S.%f>\n"
                  "eg. 2022-05-01T00:00:00 or 2022-05-01T00:00:00.000")
        elif self.__main_timestamp_format == "epoch":
            print("timestamp format: <10 / 13 digit string>\n"
                  "eg. 1420070400 or 1420070400001")

        start_ts = input("Start Timestamp: ")
        if self.__main_timestamp_format == "datetime":
            if not self.__input_validation.is_datetime_timestamp_valid(timestamp=start_ts):
                return
            end_ts = input("End Timestamp: ")
            if not self.__input_validation.is_datetime_timestamp_valid(timestamp=end_ts):
                return

        elif self.__main_timestamp_format == "epoch":
            if not self.__input_validation.is_epoch_timestamp_valid(timestamp=start_ts):
                return
            end_ts = input("End Timestamp: ")
            if not self.__input_validation.is_epoch_timestamp_valid(timestamp=end_ts):
                return
            # Since elasticsearch only supports epoch_millis by default,
            # standardize all user input epoch to epoch_millis
            if len(start_ts) == 10:
                start_ts += "000"
            if len(end_ts) == 10:
                end_ts += "000"

        if not self.__input_validation.is_endts_gte_startts(timestamp_format=self.__main_timestamp_format,
                                                            start_ts=start_ts,
                                                            end_ts=end_ts):
            return
        num_logs = input("Number of logs to retrieve: ")
        if not self.__input_validation.is_numeric_valid(num_logs):
            return
        fields = input("Select your field names (eg. event.created,event.code,message): ")
        fields_list = [x.strip() for x in fields.split(',')]
        num_logs = int(num_logs)

        print("\nFilter Format: <FIELD_NAME> <FILTER_KEYWORD> <VALUE>;")
        print("Supported Filter Keywords:\n"
              "- is_not_gte\n"
              "- is_not_lte\n"
              "- is_not_gt\n"
              "- is_not_lt\n"
              "- is_not_one_of\n"
              "- is_not\n"
              "- is_gte\n"
              "- is_lte\n"
              "- is_gt\n"
              "- is_lt\n"
              "- is_one_of\n"
              "- is\n")
        print("eg. event.code is_gt 4000; event.code is_lte 5000; event.category is authentication;")
        filter_raw = input("(OPTIONAL - PRESS ENTER TO SKIP) Filter your queries: ")
        if filter_raw.strip() != "":
            if not self.__input_validation.is_filter_valid(filter_raw=filter_raw):
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

        file_format = str(input("File format(jsonl / csv): ")).strip()
        if not self.__input_validation.is_file_format_valid(file_format=file_format):
            return

        # Configure the batch size according to elasticfetch.ini
        index_max_result_window_dict = self.__request_sender.get_max_result_window(index_name=self.__index_name)
        for index in index_max_result_window_dict:
            if self.__config_reader.batch_size > index_max_result_window_dict[index]:
                self.__request_sender.put_max_result_window(index_name=index, size=self.__config_reader.batch_size)

        data_fetch_thread = threading.Thread(target=self.__request_sender.get_fetch_elastic_data_between_ts1_ts2,
                                             kwargs={
                                                 "index_name": self.__index_name,
                                                 "num_logs": num_logs,
                                                 "main_timestamp_name": self.__main_timestamp_name,
                                                 "main_timestamp_format": self.__main_timestamp_format,
                                                 "main_timezone": self.__main_timezone,
                                                 "start_ts": start_ts,
                                                 "end_ts": end_ts,
                                                 "fields_list": fields_list,
                                                 "query_bool_must_list": query_bool_must_list,
                                                 "query_bool_must_not_list": query_bool_must_not_list
                                             })

        if file_format == "csv":
            data_write_csv_thread = threading.Thread(target=self.__data_writer.write_to_csv,
                                                     kwargs={
                                                         "request_sender": self.__request_sender,
                                                         "fields_list": fields_list
                                                     })
            data_write_csv_thread.start()
            data_fetch_thread.start()

            data_write_csv_thread.join()
            data_fetch_thread.join()

        elif file_format == "jsonl":
            data_write_json_thread = threading.Thread(target=self.__data_writer.write_to_jsonl,
                                                      kwargs={
                                                          "request_sender": self.__request_sender,
                                                      })
            data_write_json_thread.start()
            data_fetch_thread.start()

            data_write_json_thread.join()
            data_fetch_thread.join()

        # Configure back to the original settings
        for index in index_max_result_window_dict:
            if self.__config_reader.batch_size > index_max_result_window_dict[index]:
                self.__request_sender.put_max_result_window(index_name=index, size=index_max_result_window_dict[index])
        return
