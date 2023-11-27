from datetime import datetime
import os
from typing import *
from utils.messenger import Messenger, Severity
import csv
import json
import threading
from utils.request_sender import RequestSender


class DataWriter:

    def __init__(self):
        self.__messenger = Messenger()
        self.__datasets_folder = "./datasets"
        self.__csv_filepath = ""
        self.__json_filepath = ""
        self.__data_writer_lock = threading.Lock()
        return

    def write_to_csv(self,
                     request_sender: RequestSender,
                     fields_list: List[str]):
        """
        Write data received from a RequestSender to a CSV file.

        :param request_sender: An instance of RequestSender used to fetch data.
        :type request_sender: RequestSender

        :param fields_list: A list of field names to include in the CSV file.
        :type fields_list: List[str]

        :return: None
        :rtype: None
        """
        current_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        self.__csv_filepath = "{}/{}Z.csv".format(self.__datasets_folder, current_datetime)
        os.makedirs(os.path.dirname( self.__csv_filepath), exist_ok=True)
        self.__messenger.print_message(Severity.INFO, "Saving data to {}".format( self.__csv_filepath))

        f_csv = open( self.__csv_filepath, "w", newline='', encoding="utf8")
        csv_writer = csv.writer(f_csv)
        # Write header
        csv_writer.writerow(fields_list)
        f_csv.flush()

        while True:

            if request_sender.has_finished_fetching and len(request_sender.data_json_list) == 0:
                return

            with request_sender.fetch_lock:
                if request_sender.data_json_list:
                    data_json = request_sender.pop_from_data_json_list()
                    for hit in data_json["hits"]["hits"]:
                        row_list = []
                        for field in fields_list:
                            field_tokens = field.split('.')
                            value = ""
                            if len(field_tokens) == 1:
                                if field_tokens[0] in hit["_source"].keys():
                                    value = hit["_source"][field_tokens[0]]
                            elif len(field_tokens) == 2:
                                if field_tokens[0] in hit["_source"].keys():
                                    if field_tokens[1] in hit["_source"][field_tokens[0]].keys():
                                        value = hit["_source"][field_tokens[0]][field_tokens[1]]
                            elif len(field_tokens) == 3:
                                if field_tokens[0] in hit["_source"].keys():
                                    if field_tokens[1] in hit["_source"][field_tokens[0]].keys():
                                        if field_tokens[2] in hit["_source"][field_tokens[0]][field_tokens[1]].keys():
                                            value = hit["_source"][field_tokens[0]][field_tokens[1]][field_tokens[2]]
                            elif len(field_tokens) == 4:
                                if field_tokens[0] in hit["_source"].keys():
                                    if field_tokens[1] in hit["_source"][field_tokens[0]].keys():
                                        if field_tokens[2] in hit["_source"][field_tokens[0]][field_tokens[1]].keys():
                                            if field_tokens[3] in hit["_source"][field_tokens[0]][field_tokens[1]][field_tokens[2]].keys():
                                                value = hit["_source"][field_tokens[0]][field_tokens[1]][field_tokens[2]][field_tokens[3]]
                            row_list.append(value)

                        with self.__data_writer_lock:
                            csv_writer.writerow(row_list)
                            f_csv.flush()
        return

    def write_to_jsonl(self,
                       request_sender: RequestSender) -> None:
        """
        Write data received from a RequestSender to a JSON Lines (JSONL) file.

        :param request_sender: An instance of RequestSender used to fetch and process data.
        :type request_sender: RequestSender

        :return: None
        :rtype: None
        """
        current_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        self.__json_filepath = "{}/{}Z.jsonl".format(self.__datasets_folder, current_datetime)
        os.makedirs(os.path.dirname(self.__json_filepath), exist_ok=True)

        self.__messenger.print_message(Severity.INFO, "Saving data to {}".format(self.__json_filepath))

        f = open(self.__json_filepath, "w", encoding="utf-8")
        while True:
            if request_sender.has_finished_fetching and len(request_sender.data_json_list) == 0:
                return

            with request_sender.fetch_lock:
                if request_sender.data_json_list:
                    data_json = request_sender.pop_from_data_json_list()
                    with self.__data_writer_lock:
                        json.dump(data_json, f, ensure_ascii=False, separators=(',', ':'))
                        f.write("\n")
                        f.flush()
        return

    @property
    def csv_filepath(self) -> str:
        """
        Get the filepath for the CSV file where data is written or read.

        :return: The filepath for the CSV file.
        :rtype: str
        """
        return self.__csv_filepath

    @property
    def json_filepath(self) -> str:
        """
        Get the filepath for the JSON Lines (JSONL) file where data is written or read.

        :return: The filepath for the JSONL file.
        :rtype: str
        """
        return self.__json_filepath

    @property
    def data_writer_lock(self) -> threading.Lock:
        """
        Get the threading lock used to synchronize access to data writing operations.

        :return: The threading lock.
        :rtype: threading.Lock
        """
        return self.__data_writer_lock
