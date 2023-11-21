from datetime import datetime
import os
from typing import *
from utils.messenger import messenger
import csv
import json
import threading
from utils.request_sender import RequestSender


class DataWriter:

    def __init__(self):
        self.__datasets_folder = "./datasets"

        self.__data_writer_lock = threading.Lock()
        return

    def write_to_csv(self,
                     request_sender: RequestSender,
                     fields_list: List[str]):

        current_datetime = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        csv_filepath = "{}/{}.csv".format(self.__datasets_folder, current_datetime)
        os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)
        messenger(3, "Saving data to {}".format(csv_filepath))

        f_csv = open(csv_filepath, "w", newline='', encoding="utf8")
        csv_writer = csv.writer(f_csv)
        # Write header
        csv_writer.writerow(fields_list)
        f_csv.flush()

        while True:
            with request_sender.fetch_lock:
                if request_sender.data_json_list:
                    data_json = request_sender.data_json_list.pop(0)
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
                        csv_writer.writerow(row_list)
                        f_csv.flush()
                    # messenger(0, "Appended data to {}".format(csv_filepath))

            if request_sender.has_finished_fetching:
                return
        return

    def write_to_json(self,
                      request_sender: RequestSender):

        current_datetime = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        json_filepath = "{}/{}.json".format(self.__datasets_folder, current_datetime)
        os.makedirs(os.path.dirname(json_filepath), exist_ok=True)

        messenger(3, "Saving data to {}".format(json_filepath))

        is_first_data_json = True
        master_data_json = None
        master_size = 0

        f = open(json_filepath, "w", encoding="utf-8")
        while True:
            with request_sender.fetch_lock:
                if request_sender.data_json_list:
                    data_json = request_sender.data_json_list.pop(0)
                    if is_first_data_json:
                        master_data_json = data_json
                        is_first_data_json = False
                    else:
                        master_data_json["hits"]["hits"] += (data_json["hits"]["hits"])

                    master_size += len(data_json["hits"]["hits"])

                    master_data_json["hits"]["total"]["value"] = master_size
                    json.dump(master_data_json, f, ensure_ascii=False, indent=4)
                    f.flush()
                    # messenger(0, "Appended data to {}".format(json_filepath))

            if request_sender.has_finished_fetching:
                return
        return

    @property
    def data_writer_lock(self):
        return self.__data_writer_lock