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
        self.timestamp_datetime_format_seconds_regex = re.compile("^\d{4}-(0[1-9]|1[0-2]?)-(0[1-9]|1[0-9]|2[0-9]|3[0-1]?)T"
                                                            "(0[0-9]|1[0-9]|2[0-3]?):"
                                                            "(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?):"
                                                            "(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?)$")
        self.timestamp_datetime_format_milliseconds_regex = re.compile("^\d{4}-(0[1-9]|1[0-2]?)-(0[1-9]|1[0-9]|2[0-9]|3[0-1]?)T"
                                                            "(0[0-9]|1[0-9]|2[0-3]?):"
                                                            "(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?):"
                                                            "(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?)(.\d{3})?$")
        self.timestamp_epoch_format_regex = re.compile('^\d{10}$|^\d{13}$')
        self.datetime_format_seconds = '%Y-%m-%dT%H:%M:%S'
        self.datetime_format_milliseconds = '%Y-%m-%dT%H:%M:%S.%f'
        self.filter_raw_regex = re.compile(
            r"^(([-_.a-zA-Z\d]+ (is_not_gte|is_not_lte|is_not_gt|is_not_lt|is_not|is_gte|is_lte|is_gt|is_lt|is) [-_.a-zA-Z\d]+;(\s+|))+)$")
        self.valid_file_extensions = ('.json', '.csv')
        self.valid_timestamp_format_list = ['datetime', 'epoch']
        self.valid_timezone_list = ["+00:00", "+01:00", "+02:00", "+03:00", "+04:00", "+05:00", "+06:00", "+07:00", "+08:00", "+09:00", "+10:00", "+11:00", "+12:00",
                                    "-01:00", "-02:00", "-03:00", "-04:00", "-05:00", "-06:00", "-07:00", "-08:00", "-09:00" , "-10:00", "-11:00", "-12:00"]

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

    def is_datetime_timestamp_valid(self, timestamp: str):
        if self.timestamp_datetime_format_seconds_regex.search(timestamp) or self.timestamp_datetime_format_milliseconds_regex.search(timestamp):
            return True
        else:
            messenger(2, "Invalid input! Expected <%Y-%m-%d>T<%H:%M:%S> or <%Y-%m-%d>T<%H:%M:%S.%f> but got something else instead. Please try again!")
            return False

    def is_epoch_timestamp_valid(self, timestamp: str):
        if self.timestamp_epoch_format_regex.search(timestamp):
            return True
        else:
            messenger(2, "Invalid input! Expected <standard unix epoch time> but got something else instead. Please try again!")
            return False

    def is_endts_gte_startts(self, timestamp_format, start_ts, end_ts):
        tstamp1 = ""
        tstamp2 = ""
        if timestamp_format == "datetime":
            if self.timestamp_datetime_format_seconds_regex.search(start_ts):
                tstamp1 = datetime.strptime(start_ts, self.datetime_format_seconds)
            elif self.timestamp_datetime_format_milliseconds_regex.search(start_ts):
                tstamp1 = datetime.strptime(start_ts, self.datetime_format_milliseconds)

            if self.timestamp_datetime_format_seconds_regex.search(end_ts):
                tstamp2 = datetime.strptime(end_ts, self.datetime_format_seconds)
            elif self.timestamp_datetime_format_milliseconds_regex.search(end_ts):
                tstamp2 = datetime.strptime(end_ts, self.datetime_format_milliseconds)

            if tstamp2 >= tstamp1:
                return True
            else:
                messenger(2, "Invalid end timestamp because "
                             "end timestamp is earlier than start timestamp. Please try again.")
                return False
        elif timestamp_format == "epoch":
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
        if index_name != "N/A":
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

    def is_timestamp_format_valid(self,
                                  chosen_timestamp_format: str):
        if chosen_timestamp_format not in self.valid_timestamp_format_list:
            messenger(2, "'{}' is not a valid timestamp format option! Please use only {}".format(chosen_timestamp_format, '/'.join(self.valid_timestamp_format_list)))
            return False
        else:
            return True

    def is_timezone_valid(self,
                          chosen_timezone: str):
        if chosen_timezone not in self.valid_timezone_list:
            messenger(2, "'{}' is not a valid timezone! Please use only {}".format(chosen_timezone, '/'.join(self.valid_timezone_list)))
            return False
        else:
            return True
