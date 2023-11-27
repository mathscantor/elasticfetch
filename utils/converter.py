import time
import os
import datetime
from typing import *
os.environ['TZ'] = 'UTC'


class Converter:

    def __init__(self):
        self.timestamp_format = '%Y-%m-%dT%H:%M:%S'

    def convert_all_is_list_to_must_list(self,
                                         filter_is_list: List[str],
                                         filter_is_gte_list: List[str],
                                         filter_is_lte_list: List[str],
                                         filter_is_gt_list: List[str],
                                         filter_is_lt_list: List[str],
                                         filter_is_one_of_list: List[str]) -> List[Dict[str, Dict]]:
        """
        Convert multiple "is" filter lists into request["query"]["bool"]["must"] format
        {
            "size": batch_size,
             "_source": fields_list,
             "query": {
                "bool": {
                    "must": [{"term": { "log.file.path": "/var/log/auth.log" }}]
        ....
        }

        :param filter_is_list: A list of terms that must be present in the result.
        :type filter_is_list: List[str]

        :param filter_is_gte_list: A list of terms where the field must be greater than or equal to the specified values.
        :type filter_is_gte_list: List[str]

        :param filter_is_lte_list: A list of terms where the field must be less than or equal to the specified values.
        :type filter_is_lte_list: List[str]

        :param filter_is_gt_list: A list of terms where the field must be greater than the specified values.
        :type filter_is_gt_list: List[str]

        :param filter_is_lt_list: A list of terms where the field must be less than the specified values.
        :type filter_is_lt_list: List[str]

        :param filter_is_one_of_list: A list of terms where the field must match any of the specified values.
        :type filter_is_one_of_list: List[str]

        :return: A list of dictionaries representing the Elasticsearch query format.
        :rtype: List[Dict[str, Dict]]
        """
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

        for filter_is_one_of in filter_is_one_of_list:
            temp_dict = {}
            tokens = filter_is_one_of.strip().split("is_one_of")
            key = tokens[0].strip()
            value = tokens[1].strip().split(",")
            temp_dict[key] = value
            query_bool_must_list.append({"terms": temp_dict})
        return query_bool_must_list

    def convert_all_is_not_list_to_must_not_list(self,
                                                 filter_is_not_list: List[str],
                                                 filter_is_not_gte_list: List[str],
                                                 filter_is_not_lte_list: List[str],
                                                 filter_is_not_gt_list: List[str],
                                                 filter_is_not_lt_list: List[str],
                                                 filter_is_not_one_of_list: List[str]) -> List[Dict[str, Dict]]:

        """
        Convert multiple "is not" filter lists into request["query"]["bool"]["must_not"] format
        {
            "size": batch_size,
             "_source": fields_list,
             "query": {
                "bool": {
                    "must_not": [{"term": { "log.file.path": "/var/log/auth.log" }}]
        ....
        }

        :param filter_is_not_list: A list of terms that must not be present in the result.
        :type filter_is_not_list: List[str]

        :param filter_is_not_gte_list: A list of terms where the field must not be greater than or equal to the specified values.
        :type filter_is_not_gte_list: List[str]

        :param filter_is_not_lte_list: A list of terms where the field must not be less than or equal to the specified values.
        :type filter_is_not_lte_list: List[str]

        :param filter_is_not_gt_list: A list of terms where the field must not be greater than the specified values.
        :type filter_is_not_gt_list: List[str]

        :param filter_is_not_lt_list: A list of terms where the field must not be less than the specified values.
        :type filter_is_not_lt_list: List[str]

        :param filter_is_not_one_of_list: A list of terms where the field must not match any of the specified values.
        :type filter_is_not_one_of_list: List[str]

        :return: A list of dictionaries representing the Elasticsearch query format for "must not" conditions.
        :rtype: List[Dict[str, Dict]]
        """
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

        for filter_is_not_one_of in filter_is_not_one_of_list:
            temp_dict = {}
            tokens = filter_is_not_one_of.strip().split("is_not_one_of")
            key = tokens[0].strip()
            value = tokens[1].strip().split(",")
            temp_dict[key] = value
            query_bool_must_not_list.append({"terms": temp_dict})

        return query_bool_must_not_list

    def convert_field_mapping_keys_pretty(self,
                                          fields_json: Dict) -> Dict[str, Dict[str, Set[str]]]:
        """
        Convert field mapping keys to a more readable and standardized format.

        :param fields_json: A dictionary representing field mappings, where keys may need prettifying.
        :type fields_json: Dict

        :return: A dictionary with field mapping keys in a prettified format.
        :rtype: Dict[str, Dict[str, Set[str]]]
        """
        top_parent_to_type_dict = dict()
        for index_name in fields_json.keys():
            if "error" in fields_json.keys():
                continue
            field_list = list(fields_json[index_name]["mappings"].keys())
            field_list.sort()
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
                    top_parent_to_type_dict[top_parent_field] = dict()

                if last_child_field_type not in top_parent_to_type_dict[top_parent_field]:
                    top_parent_to_type_dict[top_parent_field][last_child_field_type] = set()
                    top_parent_to_type_dict[top_parent_field][last_child_field_type].add(field)
                else:
                    top_parent_to_type_dict[top_parent_field][last_child_field_type].add(field)

        return top_parent_to_type_dict

    def convert_datetime_to_epoch_millis(self,
                                         date_time: str,
                                         timezone: str) -> str:
        """
        Convert a datetime string to epoch milliseconds.

        :param date_time: A string representing the datetime format (%Y-%m-%dT%H:%M:%S)
        :type date_time: str

        :param timezone: The timezone of the datetime string. (eg. -06:00, +08:00)
        :type timezone: str

        :return: The epoch time in milliseconds.
        :rtype: str
        """
        epoch_milliseconds_string = "000"
        if "." in date_time:
            pattern = self.timestamp_format+".%f"
            epoch_milliseconds_string = date_time.split('.')[1][0:3]
        else:
            pattern = self.timestamp_format

        epoch_delta_sign = timezone[0]
        epoch_delta_seconds = int(timezone[1:3]) * 3600

        if epoch_delta_sign == "+":
            epoch = str(int(time.mktime(time.strptime(date_time, pattern))) - epoch_delta_seconds)
        elif epoch_delta_sign == "-":
            epoch = str(int(time.mktime(time.strptime(date_time, pattern))) + epoch_delta_seconds)

        epoch += epoch_milliseconds_string
        return epoch

    def convert_epoch_millis_to_datetime(self,
                                         epoch: str,
                                         timezone: str) -> str:
        """
        Convert epoch milliseconds to a datetime string in the specified timezone.

        :param epoch: A string representing the epoch time in milliseconds.
        :type epoch: str

        :param timezone: The timezone for the converted datetime string.
        :type timezone: str

        :return: A string representing the datetime in the specified timezone.
        :rtype: str
        """
        if len(epoch) == 13:
            epoch = float(int(epoch) / 1000.0)
        elif len(epoch) == 10:
            epoch = int(epoch)

        epoch_delta_sign = timezone[0]
        epoch_delta_seconds = int(timezone[1:3]) * 3600

        if epoch_delta_sign == "+":
            epoch = epoch + epoch_delta_seconds
        elif epoch_delta_sign == "-":
            epoch = epoch - epoch_delta_seconds

        date_time = datetime.datetime.fromtimestamp(epoch).strftime(self.timestamp_format+".%f")[0:-3]
        return date_time

