import re
from utils.messenger import messenger
from datetime import datetime

class InputValidation:

    def __init__(self):
        self.description = "Checks for any illegal expression of user inputs and rejects any invalid expressions"
        self.valid_protocols = ["http", "https"]
        self.port_regex = re.compile("^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$")
        self.ip_regex = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        self.numeric_regex = re.compile("^\d+$")
        self.timestamp_date_type_regex = re.compile("^\d{4}-(0[1-9]|1[0-2]?)-(0[1-9]|1[0-9]|2[0-9]|3[0-1]?)T"
                                     "(0[0-9]|1[0-9]|2[0-3]?):"
                                     "(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?):"
                                     "(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?)$")
        self.timestamp_epoch_type_regex = re.compile('^\d{10}$|^\d{13}$')
        self.datetime_format = '%Y-%m-%dT%H:%M:%S'
        self.filter_raw_regex = re.compile(
            r"^(([-_.a-zA-Z\d]+ (is_not_gte|is_not_lte|is_not_gt|is_not_lt|is_not|is_gte|is_lte|is_gt|is_lt|is) [-_.a-zA-Z\d]+;(\s+|))+)$")
        self.valid_file_extensions = ('.json', '.csv')
        self.valid_timestamp_type_list = ['date', 'epoch']

    def is_protocol_valid(self, protocol):
        if protocol not in self.valid_protocols:
            messenger(2, "Protocol '{}' is not supported! Please ensure it is either 'http' or 'https'!".format(protocol))
            return False
        else:
            return True

    def is_port(self, user_input):
        match = self.port_regex.search(user_input)
        if match:
            return True
        else:
            messenger(2, "Port '{}' is invalid. Please check that it is within 1 to 65535.".format(user_input))
            return False

    def is_ip(self, user_input):
        match = self.ip_regex.search(user_input)
        if match:
            return True
        else:
            messenger(2, "IP address '{}' is invalid. Please check that it is within 0.0.0.0 to 255.255.255.255".format(user_input))
            return False

    def is_numeric_valid(self, user_input):
        match = self.numeric_regex.search(user_input)
        if match:
            return True
        else:
            messenger(2, "Invalid input. Expected only numbers buy got something else instead. Please try again.")
            return False

    def is_timestamp_valid(self,
                           timestamp_type: str,
                           timestamp: str):
        if timestamp_type == "date":
            match = self.timestamp_date_type_regex.search(timestamp)
            if match:
                return True
            else:
                messenger(2, "Invalid input! Expected <YYYY-MM-DD>T<HH:mm:ss> but got something else instead. Please try again!")
                return False
        elif timestamp_type == "epoch":
            match = self.timestamp_epoch_type_regex.search(timestamp)
            if match:
                return True
            else:
                messenger(2, "Invalid input! <standard unix epoch time> but got something else instead. Please try again!")


    def is_endts_gte_startts(self, timestamp_type, start_ts, end_ts):

        if timestamp_type == "date":
            tstamp1 = datetime.strptime(start_ts, self.datetime_format)
            tstamp2 = datetime.strptime(end_ts, self.datetime_format)
            if tstamp2 >= tstamp1:
                return True
            else:
                messenger(2, "Invalid end timestamp because "
                             "end timestamp is earlier than start timestamp. Please try again.")
                return False
        elif timestamp_type == "epoch":
            if int(end_ts) >= int(start_ts):
                return True
            else:
                messenger(2, "Invalid end timestamp because "
                             "end timestamp is earlier than start timestamp. Please try again.")
                return False

    def is_option_in_available(self, option, options_dict):
        if option in options_dict.keys():
            return True
        else:
            messenger(2, "Invalid option number. Please try again.")
            return False

    def is_filter_valid(self, filter_raw):
        match = self.filter_raw_regex.search(filter_raw)
        if match:
            return True
        else:
            messenger(2, "Invalid filter command/commands detected. Please end your filters with ';'!\nPlease also check that your filter keywords are:\n"
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
            return False

    def is_file_extension_valid(self, filename):
        if filename.lower().endswith(self.valid_file_extensions):
            return True
        else:
            messenger(2, "Invalid File Extension. Current supported extensions: .json, .csv")
            return False

    def is_index_name_set(self, index_name):
        if index_name != "":
            return True
        else:
            messenger(2, "No index currently selected. Please set your index first!")
            return False

    def is_timestamp_name_valid(self,
                                chosen_timestamp_name: str,
                                valid_timestamp_name_list: str):
        if chosen_timestamp_name not in valid_timestamp_name_list:
            messenger(2, "'{}' is not a valid Main Timestamp! Please try again!".format(chosen_timestamp_name))
            return False
        else:
            return True

    def is_timestamp_type_valid(self,
                                chosen_timestamp_type: str):
        if chosen_timestamp_type not in self.valid_timestamp_type_list:
            messenger(2, "'{}' is not a valid timestamp type! Please use only {}".format(chosen_timestamp_type, '/'.join(self.valid_timestamp_type_list)))
            return False
        else:
            return True
