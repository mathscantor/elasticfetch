import csv
from utils.messenger import messenger
import json
import time


class Converter:

    def __init__(self):
        self.description = "Converter class to convert objects into more maningful objects"
        self.timestamp_format = '%Y-%m-%dT%H:%M:%S'

    '''
    Converts a json object into a csv file. Currently, this can only read from a maximum of 3 nested json object
    allowed field names: 
    object1
    object1.object2
    object1.object2.object3
    '''
    def convert_json_data_to_csv(self, data_json_list, fields_list, file_path):
        messenger(3, "Saving data to {}".format(file_path))
        f_csv = open(file_path, "w", newline='', encoding="utf8")
        csv_writer = csv.writer(f_csv)
        # Write header
        csv_writer.writerow(fields_list)
        for data_json in data_json_list:
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
        messenger(0, "Successfully saved data to {}".format(file_path))

    def convert_json_data_to_json(self, data_json_list, file_path):
        messenger(3, "Saving data to {}".format(file_path))

        is_first_data_json = True
        master_data_json = None
        master_size = 0
        with open(file_path, "w", encoding="utf-8") as f:
            for data_json in data_json_list:
                if is_first_data_json:
                    master_data_json = data_json
                    is_first_data_json = False
                else:
                    master_data_json["hits"]["hits"] += (data_json["hits"]["hits"])

                master_size += len(data_json["hits"]["hits"])

            master_data_json["hits"]["total"]["value"] = master_size
            json.dump(master_data_json, f, ensure_ascii=False, indent=4)
        messenger(0, "Successfully saved data to {}".format(file_path))

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

    def convert_field_mapping_keys_pretty(self,
                                          index_name: str,
                                          fields_json: dict) -> dict:

        field_list = list(fields_json[index_name]["mappings"].keys())
        field_list.sort()
        top_parent_to_type_dict = {}

        for field in field_list:
            field_tokens = field.split('.')
            top_parent_field = field_tokens[0]
            last_child_field = field_tokens[-1]
            if len(fields_json[index_name]["mappings"][field]["mapping"]) != 0 and "type" in \
                    fields_json[index_name]["mappings"][field]["mapping"][last_child_field].keys():
                last_child_field_type = fields_json[index_name]["mappings"][field]["mapping"][last_child_field]["type"]
            else:
                last_child_field_type = "NoType"

            if top_parent_field not in top_parent_to_type_dict:
                top_parent_to_type_dict[top_parent_field] = {}

            if last_child_field_type not in top_parent_to_type_dict[top_parent_field]:
                top_parent_to_type_dict[top_parent_field][last_child_field_type] = [field]
            else:
                top_parent_to_type_dict[top_parent_field][last_child_field_type].append(field)

        return top_parent_to_type_dict
