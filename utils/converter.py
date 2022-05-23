import csv
from utils.messenger import messenger
import os

class Converter:

    def __init__(self):
        self.description = "Converter class to convert objects into more maningful objects"

    '''
    Converts a json object into a csv file. Currently, this can only read from a maximum of 3 nested json object
    allowed field names: 
    object1
    object1.object2
    object1.object2.object3
    '''
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

    def convert_all_is_list_to_must_list(self,
                                         filter_is_list: list,
                                         filter_is_gte_list: list,
                                         filter_is_lte_list: list,
                                         filter_is_gt_list: list,
                                         filter_is_lt_list: list) -> list:
        query_bool_must_list = []
        for filter_is in filter_is_list:
            temp_dict = {}
            tokens = filter_is.strip().split("is")
            key = tokens[0].strip()
            value = tokens[1].strip()
            temp_dict[key] = value
            query_bool_must_list.append({"term": temp_dict})

        for filter_is_gte in filter_is_gte_list:
            temp_dict = {}
            tokens = filter_is_gte.strip().split("is_gte")
            key = tokens[0].strip()
            value = {"gte": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_list.append({"range": temp_dict})

        for filter_is_lte in filter_is_lte_list:
            temp_dict = {}
            tokens = filter_is_lte.strip().split("is_lte")
            key = tokens[0].strip()
            value = {"lte": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_list.append({"range": temp_dict})

        for filter_is_gt in filter_is_gt_list:
            temp_dict = {}
            tokens = filter_is_gt.strip().split("is_gt")
            key = tokens[0].strip()
            value = {"gt": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_list.append({"range": temp_dict})

        for filter_is_lt in filter_is_lt_list:
            temp_dict = {}
            tokens = filter_is_lt.strip().split("is_lt")
            key = tokens[0].strip()
            value = {"lt": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_list.append({"range": temp_dict})

        return query_bool_must_list

    def convert_all_is_not_list_to_must_not_list(self,
                                         filter_is_not_list: list,
                                         filter_is_not_gte_list: list,
                                         filter_is_not_lte_list: list,
                                         filter_is_not_gt_list: list,
                                         filter_is_not_lt_list: list) -> list:
        query_bool_must_not_list = []
        for filter_is_not in filter_is_not_list:
            temp_dict = {}
            tokens = filter_is_not.strip().split("is_not")
            key = tokens[0].strip()
            value = tokens[1].strip()
            temp_dict[key] = value
            query_bool_must_not_list.append({"term": temp_dict})

        for filter_is_not_gte in filter_is_not_gte_list:
            temp_dict = {}
            tokens = filter_is_not_gte.strip().split("is_not_gte")
            key = tokens[0].strip()
            value = {"gte": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_not_list.append({"range": temp_dict})

        for filter_is_not_lte in filter_is_not_lte_list:
            temp_dict = {}
            tokens = filter_is_not_lte.strip().split("is_not_lte")
            key = tokens[0].strip()
            value = {"lte": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_not_list.append({"range": temp_dict})

        for filter_is_not_gt in filter_is_not_gt_list:
            temp_dict = {}
            tokens = filter_is_not_gt.strip().split("is_not_gt")
            key = tokens[0].strip()
            value = {"gt": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_not_list.append({"range": temp_dict})

        for filter_is_not_lt in filter_is_not_lt_list:
            temp_dict = {}
            tokens = filter_is_not_lt.strip().split("is_not_lt")
            key = tokens[0].strip()
            value = {"lt": tokens[1].strip()}
            temp_dict[key] = value
            query_bool_must_not_list.append({"range": temp_dict})

        return query_bool_must_not_list
