import csv
from utils.messenger import messenger
import os

class Converter:

    def __init__(self):
        self.description = "Converter class to convert objects into more maningful objects"

    def convert_json_to_csv(self, data_json, fields_list, filename):
        file_path = "datasets/"+filename
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        messenger(3, "Saving data to {}".format(file_path))
        f_csv = open(file_path, "w", newline='', encoding="utf8")
        csv_writer = csv.writer(f_csv)

        # Write header
        csv_writer.writerow(fields_list)

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
                row_list.append(value)

            csv_writer.writerow(row_list)

    def convert_match_to_dict(self, filter_match_raw: str) -> dict:
        temp_dict = {}
        filter_match_raw_tokens = filter_match_raw.strip().split(";")
        for filter_match_raw_token in filter_match_raw_tokens:
            tokens = filter_match_raw_token.strip().split(" is ")
            key = token[0].strip()
            value = token[1].strip()
            temp_dict[key] = value
        
        filter_match_dict = {"match": temp_dict}
        return filter_match_dict
