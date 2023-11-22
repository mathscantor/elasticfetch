import requests
from utils.config_reader import ConfigReader
from utils.messenger import messenger
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm.auto import tqdm
import sys
from typing import *
import threading
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestSender:

    def __init__(self, protocol, elastic_ip, elastic_port, username, password):
        self.__headers = {"Content-Type": "application/json"}
        self.__protocol = protocol
        self.__elastic_ip = elastic_ip
        self.__elastic_port = elastic_port
        self.__username = username
        self.__password = password

        # Data related
        self.__data_json_list = []
        self.__total_results_size = 0
        self.__fetch_lock = threading.Lock()
        self.__has_finished_fetching = False
        return

    def get_authentication_status_bool(self):
        if self.__protocol == "https":
            url = "{}://{}:{}/_security/_authenticate?pretty".format(self.__protocol, self.__elastic_ip, self.__elastic_port)
            messenger(3, "Checking Authentication Credentials...")
            try:
                response = requests.get(url=url,
                                        verify=False,
                                        auth=(self.__username, self.__password))

                if response.status_code == 200:
                    messenger(0, "Successfully Authenticated with Credentials.")
                    return True
                elif response.status_code == 401:
                    messenger(2, "Authentication Error.")
                else:
                    messenger(2, "Unable to Authenticate. General Error.")
                return False
            except requests.RequestException:
                messenger(2, "Cannot resolve request to {}. Please ensure your elasticsearch's server "
                             "firewall is configured properly!".format(url))
            except requests.ConnectTimeout:
                messenger(2, "Connection timeout to {}".format(url))
            except requests.ConnectionError:
                messenger(2, "Cannot connect to {}".format(url))

        elif self.__protocol == "http":
            messenger(3, "Skipping Authentication as http protocol does not require credentials!")
            return True

        return False

    '''
    The maximum value of from + size for searches to this index. Defaults to 10000. 
    Search requests take heap memory and time proportional to from + size and this limits that memory.
    '''
    def put_max_result_window(self,
                              size: int):
        data = {"index.max_result_window": size}
        url = "{}://{}:{}/_settings".format(self.__protocol, self.__elastic_ip, self.__elastic_port)
        messenger(3, "Changing max_results_window size to {}".format(size))
        try:
            response = requests.put(url=url,
                                    headers=self.__headers,
                                    data=json.dumps(data),
                                    verify=False,
                                    auth=(self.__username, self.__password))
            if response.status_code == 200:
                if size == 10000:
                    messenger(0, "Successfully changed max_result_window size to {} (default)".format(size))
                else:
                    messenger(0, "Successfully changed max_result_window size to {}".format(size))
                return
            elif response.status_code == 400:
                messenger(2, "Unable to change max_result_window_size to {}. Bad Request in headers/data.".format(size))
            elif response.status_code == 401:
                messenger(2, "Unable to change max_result_window_size to {}. Authentication Error.".format(size))
            else:
                messenger(2, "Unable to delete PIT id. General Error.")
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return

    '''
    Loops through and through to fetch in batches of 10,000 data entries.
    Returns a list of data_json objects which will be converted into either a .json or .csv file.
    '''
    def get_fetch_elastic_data_between_ts1_ts2(self,
                                               index_name: str,
                                               num_logs: int,
                                               main_timestamp_name: str,
                                               main_timestamp_format: str,
                                               main_timezone: str,
                                               start_ts: str,
                                               end_ts: str,
                                               fields_list: list,
                                               query_bool_must_list: list,
                                               query_bool_must_not_list: list) -> None:
        url = "{}://{}:{}/{}/_search?pretty".format(self.__protocol, self.__elastic_ip, self.__elastic_port, index_name)
        is_first_loop = True
        last_ids = []
        messenger(3, "Fetching elastic data...")

        pbar = tqdm(total=num_logs, desc="Fetch Progress", file=sys.stdout)

        self.__total_results_size = 0
        self.__data_json_list = []
        self.__has_finished_fetching = False
        while num_logs > 0:
            if num_logs >= 10000:
                size = 10000
            else:
                size = num_logs
            num_logs -= size

            if main_timestamp_format == "datetime":
                data = \
                {
                    "size": size,
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
                        "size": size,
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
            #print(json.dumps(data, indent=4))
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
                        messenger(2, "There are no hits! Please try again with a different time range!")
                        self.__has_finished_fetching = True
                        return

                    pbar.update(results_size)
                    self.__total_results_size += results_size

                    with self.fetch_lock:
                        self.__data_json_list.append(data_json)

                    start_ts = data_json["hits"]["hits"][results_size - 1]["sort"][0]
                    last_ids.clear()
                    for i in range(1, results_size):
                        last_id = data_json["hits"]["hits"][results_size-i]["_id"]
                        last_ids.append(last_id)
                        if data_json["hits"]["hits"][results_size - i]["sort"][0] != start_ts:
                            break
                    is_first_loop = False
                    if results_size < size:
                        break
                elif response.status_code == 400:
                    messenger(2, "Unable to fetch elastic data. Bad Request in headers/data.")
                elif response.status_code == 401:
                    messenger(2, "Unable to fetch elastic data. Authentication Error.")

            except requests.RequestException:
                messenger(2, "Cannot resolve request to {}".format(url))
                return None
            except requests.ConnectTimeout:
                messenger(2, "Connection timeout to {}".format(url))
                return None
            except requests.ConnectionError:
                messenger(2, "Cannot connect to {}".format(url))
                return None

        pbar.close()
        messenger(0, "Successfully fetched {} data!".format(self.__total_results_size))
        self.__has_finished_fetching = True
        return

    def get_indices_status(self):
        url = "{}://{}:{}/_cat/indices/*?v=true&s=index&pretty".format(self.__protocol, self.__elastic_ip, self.__elastic_port)
        try:
            response = requests.get(url=url,
                                    verify=False,
                                    auth=(self.__username, self.__password))

            return response.text
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return

    def get_available_fields(self, index_name):
        url = "{}://{}:{}/{}/_mapping/field/*".format(self.__protocol, self.__elastic_ip, self.__elastic_port, index_name)
        try:
            response = requests.get(url=url,
                                    verify=False,
                                    auth=(self.__username, self.__password))
            if response is not None:
                messenger(0, "Showing available fields...\n\n")
                return response.json()
            else:
                messenger(2, "No fields are available! Please check whether elasticsearch is parsing properly!")
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return

    def pop_from_data_json_list(self) -> Dict:
        return self.__data_json_list.pop(0)

    @property
    def total_results_size(self) -> int:
        return self.__total_results_size

    @property
    def data_json_list(self) -> List[Dict]:
        return self.__data_json_list

    @property
    def has_finished_fetching(self) -> bool:
        return self.__has_finished_fetching

    @has_finished_fetching.setter
    def has_finished_fetching(self, value: bool) -> None:
        self.__has_finished_fetching = value
        return

    @property
    def fetch_lock(self):
        return self.__fetch_lock
