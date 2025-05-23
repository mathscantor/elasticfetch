import re
from utils.messenger import Messenger, Severity
from datetime import datetime
from typing import *


class InputValidation:

    def __init__(self):
        self.__messenger = Messenger()
        self.__valid_protocols = ["http", "https"]
        self.__port_regex = re.compile(r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$")
        self.__ip_regex = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        self.__domain_regex = re.compile(r"(?i)^([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+)$")
        self.__numeric_regex = re.compile(r"^\d+$")
        self.__timestamp_datetime_format_seconds_regex = re.compile(r"^\d{4}-(0[1-9]|1[0-2]?)-(0[1-9]|1[0-9]|2[0-9]|3[0-1]?)T"
                                                            r"(0[0-9]|1[0-9]|2[0-3]?):"
                                                            r"(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?):"
                                                            r"(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?)$")
        self.__timestamp_datetime_format_milliseconds_regex = re.compile(r"^\d{4}-(0[1-9]|1[0-2]?)-(0[1-9]|1[0-9]|2[0-9]|3[0-1]?)T"
                                                            r"(0[0-9]|1[0-9]|2[0-3]?):"
                                                            r"(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?):"
                                                            r"(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]?)(.\d{3})?$")
        self.__timestamp_epoch_format_regex = re.compile(r'^\d{10}$|^\d{13}$')
        self.__datetime_format_seconds = '%Y-%m-%dT%H:%M:%S'
        self.__datetime_format_milliseconds = '%Y-%m-%dT%H:%M:%S.%f'
        self.__filter_raw_regex = re.compile(
            r"^(([-_.a-zA-Z\d]+ (is_not_gte|is_not_lte|is_not_gt|is_not_lt|is_not_one_of|is_not|is_gte|is_lte|is_gt|is_lt|is_one_of|is) [,-_.a-zA-Z\d]+;(\s+|))+)$")
        self.__valid_filter_keywords = ["is_not_gte", "is_not_lte", "is_not_gt", "is_not_lt", "is_not_one_of", "is_not",
                                      "is_gte", "is_lte", "is_gt", "is_lt", "is_one_of", "is"]
        self.__valid_file_extensions = ['.json', '.csv']
        self.__valid_file_format = ['jsonl', 'csv']
        self.__valid_timestamp_format_list = ['datetime', 'epoch']
        self.__valid_timezone_list = ["+00:00", "+01:00", "+02:00", "+03:00", "+04:00", "+05:00", "+06:00", "+07:00", "+08:00", "+09:00", "+10:00", "+11:00", "+12:00",
                                    "-01:00", "-02:00", "-03:00", "-04:00", "-05:00", "-06:00", "-07:00", "-08:00", "-09:00" , "-10:00", "-11:00", "-12:00"]

    def is_protocol_valid(self,
                          protocol: str) -> bool:
        """
        Check if the provided protocol is valid.

        :param protocol: The protocol string to be validated.
        :type protocol: str

        :return: True if the protocol is valid, False otherwise.
        :rtype: bool
        """
        if protocol not in self.__valid_protocols:
            self.__messenger.print_message(Severity.ERROR, "Protocol '{}' is not supported! Please ensure "
                                                           "it is either 'http' or 'https'!".format(protocol))
            return False
        else:
            return True

    def is_port_valid(self,
                      user_input: int) -> bool:
        """
        Check if the provided port number is valid.

        :param user_input: The port number to be validated.
        :type user_input: int

        :return: True if the port is valid, False otherwise.
        :rtype: bool
        """
        if 1 <= user_input < 65535:
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Port '{}' is invalid. Please check that "
                                                           "it is within 1 to 65535.".format(user_input))
            return False

    def is_ip_valid(self,
                    user_input: str) -> bool:
        """
        Check if the provided IP address is valid.

        :param user_input: The IP address to be validated.
        :type user_input: str

        :return: True if the IP address is valid, False otherwise.
        :rtype: bool
        """
        match_ip = self.__ip_regex.search(user_input)
        match_domain = self.__domain_regex.search(user_input)
        if match_ip:
            return True
        if match_domain:
            return True

        self.__messenger.print_message(Severity.ERROR, "IP Address / Domain Name: '{}' is invalid. "
                                                       "Please check that it is within"
                                                       " 0.0.0.0 to 255.255.255.255 or "
                                                       "any valid domain name".format(user_input))
        return False

    def is_numeric_valid(self,
                         user_input: str) -> bool:
        """
        Check if the provided string represents a valid numeric value.

        :param user_input: The string to be validated.
        :type user_input: str

        :return: True if the string represents a valid numeric value, False otherwise.
        :rtype: bool
        """
        match = self.__numeric_regex.search(user_input)
        if match:
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Invalid input. Expected only numbers buy got something "
                                                           "else instead. Please try again.")
            return False

    def is_datetime_timestamp_valid(self,
                                    timestamp: str) -> bool:
        """
        Check if the provided timestamp string is a valid datetime format.

        :param timestamp: The timestamp string to be validated.
        :type timestamp: str

        :return: True if the timestamp is a valid datetime format, False otherwise.
        :rtype: bool
        """
        if self.__timestamp_datetime_format_seconds_regex.search(timestamp) or self.__timestamp_datetime_format_milliseconds_regex.search(timestamp):
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Invalid input! Expected <%Y-%m-%d>T<%H:%M:%S> or "
                                                           "<%Y-%m-%d>T<%H:%M:%S.%f> but got something else instead. "
                                                           "Please try again!")
            return False

    def is_epoch_timestamp_valid(self,
                                 timestamp: str) -> bool:
        """
        Check if the provided timestamp string is a valid epoch timestamp.

        :param timestamp: The timestamp string to be validated.
        :type timestamp: str

        :return: True if the timestamp is a valid epoch timestamp, False otherwise.
        :rtype: bool
        """
        if self.__timestamp_epoch_format_regex.search(timestamp):
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Invalid input! Expected <standard unix epoch time> "
                                                           "but got something else instead. Please try again!")
            return False

    def is_endts_gte_startts(self,
                             timestamp_format: str,
                             start_ts: str,
                             end_ts: str) -> bool:
        """
        Check if the end timestamp is greater than or equal to the start timestamp.

        :param timestamp_format: The format of the timestamps.
        :type timestamp_format: str

        :param start_ts: The start timestamp.
        :type start_ts: str

        :param end_ts: The end timestamp.
        :type end_ts: str

        :return: True if end timestamp is greater than or equal to the start timestamp, False otherwise.
        :rtype: bool
        """
        tstamp1 = ""
        tstamp2 = ""
        if timestamp_format == "datetime":
            if self.__timestamp_datetime_format_seconds_regex.search(start_ts):
                tstamp1 = datetime.strptime(start_ts, self.__datetime_format_seconds)
            elif self.__timestamp_datetime_format_milliseconds_regex.search(start_ts):
                tstamp1 = datetime.strptime(start_ts, self.__datetime_format_milliseconds)

            if self.__timestamp_datetime_format_seconds_regex.search(end_ts):
                tstamp2 = datetime.strptime(end_ts, self.__datetime_format_seconds)
            elif self.__timestamp_datetime_format_milliseconds_regex.search(end_ts):
                tstamp2 = datetime.strptime(end_ts, self.__datetime_format_milliseconds)

            if tstamp2 >= tstamp1:
                return True
            else:
                self.__messenger.print_message(Severity.ERROR, "Invalid end timestamp because "
                                                               "end timestamp is earlier than start timestamp. "
                                                               "Please try again.")
                return False
        elif timestamp_format == "epoch":
            if int(end_ts) >= int(start_ts):
                return True
            else:
                self.__messenger.print_message(Severity.ERROR, "Invalid end timestamp because "
                                                               "end timestamp is earlier than start timestamp. "
                                                               "Please try again.")
                return False

    def is_option_in_available(self,
                               option: int,
                               options_dict: Dict[int, str]) -> bool:
        """
        Check if the provided option is present in the available options dictionary.

        :param option: The option to be validated.
        :type option: int

        :param options_dict: A dictionary of available options.
        :type options_dict: Dict[int, str]

        :return: True if the option is in the available options, False otherwise.
        :rtype: bool
        """
        if option in options_dict.keys():
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Invalid option number. Please try again.")
            return False

    def is_filter_valid(self,
                        filter_raw: str) -> bool:
        """
        Check if the provided filter string is valid.

        :param filter_raw: The filter string to be validated.
        :type filter_raw: str

        :return: True if the filter is valid, False otherwise.
        :rtype: bool
        """
        match = self.__filter_raw_regex.search(filter_raw)
        if match:
            return True
        else:
            self.__messenger.print_message(Severity.ERROR,
                                           "Invalid filter command/commands detected!\n"
                                           "Please ensure you end your filters with ';'!\n"
                                           "Please ensure there are no trailing spaces for each filter!\n"
                                           "Please also check that your filter keywords are:\n"
                                           " - is_not_gte\n"
                                           " - is_not_lte\n"
                                           " - is_not_gt\n"
                                           " - is_not_lt\n"
                                           " - is_not_one_of\n"
                                           " - is_not\n"
                                           " - is_gte\n"
                                           " - is_lte\n"
                                           " - is_gt\n"
                                           " - is_lt\n"
                                           " - is_one_of\n"
                                           " - is\n")
            return False

    def is_file_extension_valid(self,
                                filename: str) -> bool:
        """
        Check if the provided file name has a valid file extension.

        :param filename: The file name to be validated.
        :type filename: str

        :return: True if the file extension is valid, False otherwise.
        :rtype: bool
        """
        if filename.lower().endswith(self.__valid_file_extensions):
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Invalid File Extension. Current supported "
                                                           "extensions: {}".format(self.__valid_file_extensions))
            return False

    def is_file_format_valid(self,
                             file_format: str) -> bool:
        """
        Check if the provided file format is valid.

        :param file_format: The file format to be validated.
        :type file_format: str

        :return: True if the file format is valid, False otherwise.
        :rtype: bool
        """
        if file_format in self.__valid_file_format:
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "Invalid File Format. Current supported "
                                                           "file formats: {}".format(self.__valid_file_format))
            return False

    def is_index_name_set(self,
                          index_name: str) -> bool:
        """
        Check if the provided index name is set.

        :param index_name: The index name to be validated.
        :type index_name: str

        :return: True if the index name is set, False otherwise.
        :rtype: bool
        """
        if index_name != "N/A":
            return True
        else:
            self.__messenger.print_message(Severity.ERROR, "No index currently selected. Please set your index first!")
            return False

    def is_timestamp_name_valid(self,
                                chosen_timestamp_name: str,
                                valid_timestamp_name_list: str) -> bool:
        """
        Check if the provided timestamp name is in the list of valid timestamp names.

        :param chosen_timestamp_name: The chosen timestamp name to be validated.
        :type chosen_timestamp_name: str

        :param valid_timestamp_name_list: A list of valid timestamp names.
        :type valid_timestamp_name_list: str

        :return: True if the timestamp name is valid, False otherwise.
        :rtype: bool
        """
        if chosen_timestamp_name not in valid_timestamp_name_list:
            self.__messenger.print_message(Severity.ERROR, "'{}' is not a valid Main Timestamp! "
                                                           "Please try again!".format(chosen_timestamp_name))
            return False
        else:
            return True

    def is_timestamp_format_valid(self,
                                  chosen_timestamp_format: str) -> bool:
        """
        Check if the provided timestamp format is valid.

        :param chosen_timestamp_format: The chosen timestamp format to be validated.
        :type chosen_timestamp_format: str

        :return: True if the timestamp format is valid, False otherwise.
        :rtype: bool
        """
        if chosen_timestamp_format not in self.__valid_timestamp_format_list:
            self.__messenger.print_message(Severity.ERROR, "'{}' is not a valid timestamp format option! "
                                                           "Please use only {}".format(chosen_timestamp_format, '/'.join(self.__valid_timestamp_format_list)))
            return False
        else:
            return True

    def is_timezone_valid(self,
                          chosen_timezone: str) -> bool:
        """
        Check if the provided timezone is valid.

        :param chosen_timezone: The chosen timezone to be validated.
        :type chosen_timezone: str

        :return: True if the timezone is valid, False otherwise.
        :rtype: bool
        """
        if chosen_timezone not in self.__valid_timezone_list:
            self.__messenger.print_message(Severity.ERROR, "'{}' is not a valid timezone! "
                                                           "Please use only {}".format(chosen_timezone, '/'.join(self.__valid_timezone_list)))
            return False
        else:
            return True

    def is_batch_size_valid(self,
                            size: int):
        """
        Check if the provided batch size is valid.

        :param size: The batch size to be validated.
        :type size: int

        :return: True if the batch size is valid, False otherwise.
        :rtype: bool
        """
        if size > 0:
            return True
        elif size == 0:
            self.__messenger.print_message(Severity.ERROR, "Batch size cannot be 0!")
            return False
        else:
            self.__messenger.print_message(Severity.ERROR, "Batch size cannot be negative!")
            return False

    @property
    def valid_protocols(self) -> List[str]:
        """
        Get the list of valid protocols for communication.

        :return: The list of valid protocols.
        :rtype: List[str]
        """
        return self.__valid_protocols

    @property
    def port_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating port numbers.

        :return: The regular expression pattern for port validation.
        :rtype: Pattern[str]
        """
        return self.__port_regex

    @property
    def ip_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating IP addresses.

        :return: The regular expression pattern for IP address validation.
        :rtype: Pattern[str]
        """
        return self.__ip_regex

    @property
    def numeric_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating numeric values.

        :return: The regular expression pattern for numeric value validation.
        :rtype: Pattern[str]
        """
        return self.__numeric_regex

    @property
    def timestamp_datetime_format_seconds_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating datetime format with seconds precision.

        :return: The regular expression pattern for datetime format with seconds precision validation.
        :rtype: Pattern[str]
        """
        return self.__timestamp_datetime_format_seconds_regex

    @property
    def timestamp_datetime_format_milliseconds_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating datetime format with milliseconds precision.

        :return: The regular expression pattern for datetime format with milliseconds precision validation.
        :rtype: Pattern[str]
        """
        return self.__timestamp_datetime_format_milliseconds_regex

    @property
    def timestamp_epoch_format_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating epoch timestamp format.

        :return: The regular expression pattern for epoch timestamp format validation.
        :rtype: Pattern[str]
        """
        return self.__timestamp_epoch_format_regex

    @property
    def datetime_format_seconds(self) -> Pattern[str]:
        """
        Get the regular expression pattern for datetime format with seconds precision.

        :return: The regular expression pattern for datetime format with seconds precision.
        :rtype: Pattern[str]
        """
        return self.__datetime_format_seconds

    @property
    def datetime_format_milliseconds(self) -> Pattern[str]:
        """
        Get the regular expression pattern for datetime format with milliseconds precision.

        :return: The regular expression pattern for datetime format with milliseconds precision.
        :rtype: Pattern[str]
        """
        return self.__datetime_format_milliseconds

    @property
    def filter_raw_regex(self) -> Pattern[str]:
        """
        Get the regular expression pattern for validating raw filter strings.

        :return: The regular expression pattern for raw filter string validation.
        :rtype: Pattern[str]
        """
        return self.__filter_raw_regex

    @property
    def valid_filter_keywords(self) -> List[str]:
        """
        Get the list of valid filter keywords.

        :return: The list of valid filter keywords.
        :rtype: List[str]
        """
        return self.__valid_filter_keywords

    @property
    def valid_file_extensions(self) -> List[str]:
        """
        Get the list of valid file extensions.

        :return: The list of valid file extensions.
        :rtype: List[str]
        """
        return self.__valid_file_extensions

    @property
    def valid_file_format(self) -> List[str]:
        """
        Get the list of valid file formats.

        :return: The list of valid file formats.
        :rtype: List[str]
        """
        return self.__valid_file_format

    @property
    def valid_timestamp_format_list(self) -> List[str]:
        """
        Get the list of valid timestamp formats.

        :return: The list of valid timestamp formats.
        :rtype: List[str]
        """
        return self.__valid_timestamp_format_list

    @property
    def valid_timezone_list(self) -> List[str]:
        """
        Get the list of valid timezones.

        :return: The list of valid timezones.
        :rtype: List[str]
        """
        return self.__valid_timezone_list



