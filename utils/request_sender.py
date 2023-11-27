import requests
from utils.config_reader import ConfigReader
from utils.messenger import Messenger, Severity
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm.auto import tqdm
import sys
from typing import *
import threading
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestSender:

    def __init__(self,
                 protocol: str,
                 elastic_ip: str,
                 elastic_port: int,
                 username: str,
                 password: str,
                 batch_size: str):
        self.__messenger = Messenger()
        self.__headers = {"Content-Type": "application/json"}
        self.__protocol = protocol
        self.__elastic_ip = elastic_ip
        self.__elastic_port = elastic_port
        self.__username = username
        self.__password = password
        self.__batch_size = batch_size

        # Data related
        self.__data_json_list = []
        self.__total_results_size = 0
        self.__fetch_lock = threading.Lock()
        self.__has_finished_fetching = False
        return

    def get_authentication_status_bool(self) -> bool:
        """
        Get the authentication status as a boolean.

        :return: True if authentication is successful, False otherwise.
        :rtype: bool
        """
        if self.__protocol == "https":
            url = "{}://{}:{}/_security/_authenticate?pretty".format(self.__protocol, 
                                                                     self.__elastic_ip, 
                                                                     self.__elastic_port)
            self.__messenger.print_message(Severity.INFO, "Checking Authentication Credentials...")
            try:
                response = requests.get(url=url,
                                        verify=False,
                                        auth=(self.__username, self.__password))

                if response.status_code == 200:
                    self.__messenger.print_message(Severity.INFO, "Successfully Authenticated with Credentials.")
                    return True
                elif response.status_code == 401:
                    self.__messenger.print_message(Severity.ERROR, "Authentication Error.")
                else:
                    self.__messenger.print_message(Severity.ERROR, "Unable to Authenticate. General Error.")
                return False
            except requests.RequestException:
                self.__messenger.print_message(Severity.ERROR, 
                                               "Cannot resolve request to {}. Please ensure your elasticsearch's "
                                               "server firewall is configured properly!".format(url))
            except requests.ConnectTimeout:
                self.__messenger.print_message(Severity.ERROR, "Connection timeout to {}".format(url))
            except requests.ConnectionError:
                self.__messenger.print_message(Severity.ERROR, "Cannot connect to {}".format(url))

        elif self.__protocol == "http":
            self.__messenger.print_message(Severity.INFO, 
                                           "Skipping Authentication as http protocol does not require credentials!")
            return True

        return False

    def get_max_result_window(self,
                              index_name: str) -> Dict[str, int]:
        """
        Get the maximum result window size for a given Elasticsearch index.

        :param index_name: The name of the Elasticsearch index. (Wildcard is accepted as well)
        :type index_name: str
        Example:
        ```
        index_name = *filebeat*
        This matches:
        1. .ds-filebeat-8.11.1-2023.11.21-000001
        2. .ds-filebeat-8.11.1-2023.11.22-000002
        3. .ds-filebeat-8.11.1-2023.11.23-000003

        Thus, our dictionary returned would look like this:
        {
            ".ds-filebeat-8.11.1-2023.11.21-000001": 10000,
            ".ds-filebeat-8.11.1-2023.11.22-000002": 10000,
            ".ds-filebeat-8.11.1-2023.11.23-000003": 10000
        }
        ```

        :return: A dictionary containing the maximum result window size for the provided index.
                 The key is the actual index name and the value is the maximum window size.
        :rtype: Dict[str, int]
        """
        index_max_result_window_dict = dict()
        url = "{}://{}:{}/{}/_settings".format(self.__protocol, self.__elastic_ip, self.__elastic_port, index_name)
        # Get the current index.max_result_window first for a particular index or indices if you use wildcard matching.
        try:
            response = requests.get(url=url,
                                    headers=self.__headers,
                                    verify=False,
                                    auth=(self.__username, self.__password))
            if response.status_code == 200:
                settings_json = response.json()
                if len(settings_json) == 0:
                    self.__messenger.print_message(Severity.ERROR, "There are no matching indices for: {}".format((index_name)))
                    return index_max_result_window_dict

                for index in settings_json.keys():
                    index_max_result_window_dict[index] = int(settings_json[index]["settings"]["index"]["max_result_window"])
                return index_max_result_window_dict

            elif response.status_code == 400:
                self.__messenger.print_message(Severity.ERROR, "Unable to get settings of index: {}\n"
                                                               "Bad Request in headers/data.".format(index_name))
            elif response.status_code == 401:
                self.__messenger.print_message(Severity.ERROR, "Unable to get settings of index: {}\n"
                                                               "Authentication Error.".format(index_name))
            else:
                self.__messenger.print_message(Severity.ERROR, "Unable to get settings of index: {}\n"
                                                               "Unknown Error.".format(index_name))
        except requests.RequestException:
            self.__messenger.print_message(Severity.ERROR, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            self.__messenger.print_message(Severity.ERROR, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            self.__messenger.print_message(Severity.ERROR, "Cannot connect to {}".format(url))
        return index_max_result_window_dict

    def put_max_result_window(self,
                              index_name: str,
                              size: int) -> None:
        """
        Set the maximum result window size for a given Elasticsearch index.

        :param index_name: The name of the Elasticsearch index.
        :type index_name: str

        :param size: The maximum result window size to be set.
        :type size: int

        :return: None
        :rtype: None
        """
        url = "{}://{}:{}/{}/_settings".format(self.__protocol, self.__elastic_ip, self.__elastic_port, index_name)
        data = {"index.max_result_window": size}

        self.__messenger.print_message(Severity.INFO, "Changing max_results_window of {} size to {}".format(index_name,
                                                                                                            size))
        try:
            response = requests.put(url=url,
                                    headers=self.__headers,
                                    data=json.dumps(data),
                                    verify=False,
                                    auth=(self.__username, self.__password))
            if response.status_code == 200:
                if size == 10000:
                    self.__messenger.print_message(Severity.INFO, "Successfully changed max_result_window "
                                                                  "size to {} (default)".format(size))
                else:
                    self.__messenger.print_message(Severity.INFO, "Successfully changed max_result_window "
                                                                  "size to {}".format(size))
                return
            elif response.status_code == 400:
                self.__messenger.print_message(Severity.ERROR, "Unable to change max_result_window_size to {}. "
                                                               "Bad Request in headers/data.".format(size))
            elif response.status_code == 401:
                self.__messenger.print_message(Severity.ERROR, "Unable to change max_result_window_size to {}. "
                                                               "Authentication Error.".format(size))
            else:
                self.__messenger.print_message(Severity.ERROR, "Unable to change max_result_window_size to {}. "
                                                               "Unknown Error.".format(size))
        except requests.RequestException:
            self.__messenger.print_message(Severity.ERROR, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            self.__messenger.print_message(Severity.ERROR, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            self.__messenger.print_message(Severity.ERROR, "Cannot connect to {}".format(url))
        return

    def get_fetch_elastic_data_between_ts1_ts2(self,
                                               index_name: str,
                                               num_logs: int,
                                               main_timestamp_name: str,
                                               main_timestamp_format: str,
                                               main_timezone: str,
                                               start_ts: str,
                                               end_ts: str,
                                               fields_list: List[str],
                                               query_bool_must_list: List[Dict[str, Dict]],
                                               query_bool_must_not_list: List[Dict[str, Dict]]) -> None:
        """
        Fetch Elasticsearch data between two timestamps for a given index.

        :param index_name: The name of the Elasticsearch index.
        :type index_name: str

        :param num_logs: The number of logs to fetch.
        :type num_logs: int

        :param main_timestamp_name: The name of the main timestamp field.
        :type main_timestamp_name: str

        :param main_timestamp_format: The format of the main timestamp field.
        :type main_timestamp_format: str

        :param main_timezone: The timezone of the main timestamp field.
        :type main_timezone: str

        :param start_ts: The start timestamp for data retrieval.
        :type start_ts: str

        :param end_ts: The end timestamp for data retrieval.
        :type end_ts: str

        :param fields_list: A list of field names to include in the fetched data.
        :type fields_list: List[str]

        :param query_bool_must_list: A list of dictionaries representing must clauses in the Elasticsearch query.
        :type query_bool_must_list: List[Dict[str, Dict]]

        :param query_bool_must_not_list: A list of dictionaries representing must_not clauses in the Elasticsearch query.
        :type query_bool_must_not_list: List[Dict[str, Dict]]

        :return: None
        :rtype: None
        """
        url = "{}://{}:{}/{}/_search?pretty".format(self.__protocol, self.__elastic_ip, self.__elastic_port, index_name)
        is_first_loop = True
        last_ids = []
        self.__messenger.print_message(Severity.INFO, "Fetching elastic data...")

        pbar = tqdm(total=num_logs, desc="Fetch Progress", file=sys.stdout)

        self.__total_results_size = 0
        self.__data_json_list = []
        self.__has_finished_fetching = False
        while num_logs > 0:
            if num_logs >= self.__batch_size:
                batch_size = self.__batch_size
            else:
                batch_size = num_logs
            num_logs -= batch_size

            if main_timestamp_format == "datetime":
                data = \
                {
                    "size": batch_size,
                    "_source": fields_list,
                    "query": {
                        "bool": {
                            "filter": {
                                "range": {
                                    main_timestamp_name: {
                                        "time_zone": main_timezone,
                                        "gte": start_ts,
                                        "lte": end_ts
                                    }
                                }
                            },
                        }
                    },
                    "sort": [
                        {main_timestamp_name: {"order": "asc", "format": "strict_date_optional_time_nanos"}}
                    ]
                }

            # epoch time is according to UTC 0
            elif main_timestamp_format == "epoch":
                data = \
                    {
                        "size": batch_size,
                        "_source": fields_list,
                        "query": {
                            "bool": {
                                "filter": {
                                    "range": {
                                        main_timestamp_name: {
                                            "time_zone": "+00:00",
                                            "gte": start_ts,
                                            "lte": end_ts
                                        }
                                    }
                                },
                            }
                        },
                        "sort": [
                            {main_timestamp_name: {"order": "asc"}}
                        ]
                    }
            if len(query_bool_must_list) > 0:
                data["query"]["bool"]["must"] = query_bool_must_list
            if len(query_bool_must_not_list) > 0:
                data["query"]["bool"]["must_not"] = query_bool_must_not_list
                if not is_first_loop:
                    data["query"]["bool"]["must_not"] += [{"terms": {"_id": last_ids}}]
            else:
                if not is_first_loop:
                    data["query"]["bool"]["must_not"] = [{"terms": {"_id": last_ids}}]
            # print(json.dumps(data, indent=4))
            try:
                response = requests.get(url=url,
                                        headers=self.__headers,
                                        data=json.dumps(data),
                                        verify=False,
                                        auth=(self.__username, self.__password))
                data_json = response.json()
                if response.status_code == 200:
                    results_size = len(data_json["hits"]["hits"])
                    if results_size == 0:
                        pbar.close()
                        self.__messenger.print_message(Severity.ERROR, "There are no hits! Please try again with a different time range!")
                        self.__has_finished_fetching = True
                        return

                    pbar.update(results_size)
                    self.__total_results_size += results_size

                    with self.fetch_lock:
                        self.__data_json_list.append(data_json)

                    # LOGIC for getting the next batch by filtering out duplicates
                    start_ts = data_json["hits"]["hits"][-1]["sort"][0]

                    # edge case: if our whole batch of results has the same timestamp,
                    # then we do not clear our last_ids yet
                    # Thus, we will only clear when the last timestamp
                    # is different from the first timestamp in the batch
                    if data_json["hits"]["hits"][-1]["sort"][0] != data_json["hits"]["hits"][0]["sort"][0]:
                        # print("CLearing list - Size {}".format(len(last_ids)))
                        last_ids.clear()

                    for i in range(1, results_size + 1):
                        last_id = data_json["hits"]["hits"][results_size-i]["_id"]
                        last_ids.append(last_id)
                        if data_json["hits"]["hits"][results_size - i]["sort"][0] != start_ts:
                            break
                    is_first_loop = False
                    if results_size < batch_size:
                        break
                elif response.status_code == 400:
                    self.__messenger.print_message(Severity.ERROR, "Unable to fetch elastic data. Bad Request in headers/data.")
                elif response.status_code == 401:
                    self.__messenger.print_message(Severity.ERROR, "Unable to fetch elastic data. Authentication Error.")

            except requests.RequestException:
                self.__messenger.print_message(Severity.ERROR, "Cannot resolve request to {}".format(url))
                return None
            except requests.ConnectTimeout:
                self.__messenger.print_message(Severity.ERROR, "Connection timeout to {}".format(url))
                return None
            except requests.ConnectionError:
                self.__messenger.print_message(Severity.ERROR, "Cannot connect to {}".format(url))
                return None

        pbar.close()
        self.__messenger.print_message(Severity.INFO, "Successfully fetched {} data!".format(self.__total_results_size))
        self.__has_finished_fetching = True
        return

    def get_indices_status(self) -> str:
        """
        Get the status of Elasticsearch indices.

        This method retrieves and prints the status of all indices in the Elasticsearch cluster.

        :return: The string of the response.
        :rtype: str
        """
        url = "{}://{}:{}/_cat/indices/*?v=true&s=index&pretty".format(self.__protocol, self.__elastic_ip, self.__elastic_port)
        try:
            response = requests.get(url=url,
                                    verify=False,
                                    auth=(self.__username, self.__password))

            return response.text
        except requests.RequestException:
            self.__messenger.print_message(Severity.ERROR, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            self.__messenger.print_message(Severity.ERROR, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            self.__messenger.print_message(Severity.ERROR, "Cannot connect to {}".format(url))
        return ""

    def get_available_fields(self,
                             index_name: str) -> Dict:
        """
        Get the available fields and their types in a specific Elasticsearch index.

        This method queries the specified Elasticsearch index and returns a dictionary
        where keys are field names, and values are the corresponding field types.

        :param index_name: The name of the Elasticsearch index.
        :type index_name: str

        :return: A dictionary mapping field names to their types in the specified index.
        :rtype: Dict
        """
        url = "{}://{}:{}/{}/_mapping/field/*".format(self.__protocol, self.__elastic_ip, self.__elastic_port, index_name)
        try:
            response = requests.get(url=url,
                                    verify=False,
                                    auth=(self.__username, self.__password))
            if response is not None:
                self.__messenger.print_message(Severity.INFO, "Retrieved available fields for index: {}\n".format(index_name))
                return response.json()
            else:
                self.__messenger.print_message(Severity.ERROR, "No fields are available! Please check "
                                                               "whether elasticsearch is parsing properly!")
        except requests.RequestException:
            self.__messenger.print_message(Severity.ERROR, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            self.__messenger.print_message(Severity.ERROR, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            self.__messenger.print_message(Severity.ERROR, "Cannot connect to {}".format(url))
        return

    def pop_from_data_json_list(self) -> Dict:
        """
        Pop and return the first element from the data JSON list.

        :return: The first element from the data JSON list.
        :rtype: Dict
        """
        return self.__data_json_list.pop(0)

    @property
    def total_results_size(self) -> int:
        """
        Get the total size of results.

        :return: The total size of results.
        :rtype: int
        """
        return self.__total_results_size

    @property
    def data_json_list(self) -> List[Dict]:
        """
        Get the list of data in JSON format.

        :return: The list of data in JSON format.
        :rtype: List[Dict]
        """
        return self.__data_json_list

    @property
    def has_finished_fetching(self) -> bool:
        """
        Get the flag indicating whether fetching has finished.

        :return: True if fetching has finished, False otherwise.
        :rtype: bool
        """
        return self.__has_finished_fetching

    @has_finished_fetching.setter
    def has_finished_fetching(self, value: bool) -> None:
        """
        Set the flag indicating whether fetching has finished.

        :param value: The value to set for the flag.
        :type value: bool

        :return: None
        :rtype: None
        """
        self.__has_finished_fetching = value
        return

    @property
    def fetch_lock(self) -> threading.Lock:
        """
        Get the lock used for synchronization during fetching.

        :return: The lock object.
        :rtype: threading.Lock
        """
        return self.__fetch_lock
