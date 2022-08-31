import requests
from utils.messenger import messenger
import json
import customtkinter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
import sys
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestSender:

    def __init__(self, protocol, elastic_ip, elastic_port, username, password):
        self.description = "Sends POST/GET request to elasticsearch server"
        self.headers = {"Content-Type": "application/json"}
        self.protocol = protocol
        self.elastic_ip = elastic_ip
        self.elastic_port = elastic_port
        self.username = username
        self.password = password

    def get_authentication_status_bool(self):
        if self.protocol == "https":
            url = "{}://{}:{}/_security/_authenticate?pretty".format(self.protocol, self.elastic_ip, self.elastic_port)
            messenger(3, "Checking Authentication Credentials...")
            try:
                response = requests.get(url=url,
                                        verify=False,
                                        auth=(self.username, self.password))

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

        elif self.protocol == "http":
            messenger(3, "Skipping Authentication as http protocol does not require credentials!")
            return True

        return False


    '''
    A point in time must be opened explicitly before being used in search requests. 
    The keep_alive parameter tells Elasticsearch how long it should keep a point in time alive, e.g. ?keep_alive=60m
    '''
    def post_fetch_pit_id(self, index_name):
        url = "{}://{}:{}/{}/_pit?keep_alive=60m&pretty".format(self.protocol, self.elastic_ip, self.elastic_port, index_name)
        messenger(3, "Fetching PIT id...")
        try:
            response = requests.post(url=url,
                                     headers=self.headers,
                                     verify=False,
                                     auth=(self.username, self.password))
            if response.status_code == 200:
                pit_id = response.json()["id"]
                messenger(0, "Successfully fetched PIT id. This id will be used for fetching elasticsearch data.\n"
                             "PIT id: {}".format(pit_id))
                return pit_id
            elif response.status_code == 400:
                messenger(2, "Unable to fetch PIT id. Bad Request in headers/data.")
            elif response.status_code == 401:
                messenger(2, "Unable to fetch PIT id. Authentication Error.")
            else:
                messenger(2, "Unable to fetch PIT id. General Error.")
            # In case fetch pid fails, reset back to default
            self.put_max_result_window(size=10000)
            return None
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return


    '''
    Point-in-time is automatically closed when its keep_alive has been elapsed. However keeping point-in-times 
    has a cost, as discussed in the previous section. Point-in-times should be closed 
    as soon as they are no longer used in search requests.
    '''
    def delete_pit_id(self,
                      pit_id: str):
        data = {"id": pit_id}
        url = "{}://{}:{}/_pit?pretty".format(self.protocol, self.elastic_ip, self.elastic_port)
        messenger(3, "Deleting PIT id {}...".format(pit_id))
        try:
            response = requests.delete(url=url,
                                       headers=self.headers,
                                       data=json.dumps(data),
                                       verify=False,
                                       auth=(self.username, self.password))
            if response.status_code == 200:
                messenger(0, "Successfully deleted PIT id.")
                return
            elif response.status_code == 400:
                messenger(2, "Unable to delete PIT id. Bad Request in headers/data.")
            elif response.status_code == 401:
                messenger(2, "Unable to delete PIT id. Authentication Error.")
            else:
                messenger(2, "Unable to delete PIT id. General Error.")
            return
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return

    '''
    The maximum value of from + size for searches to this index. Defaults to 10000. 
    Search requests take heap memory and time proportional to from + size and this limits that memory.
    '''
    def put_max_result_window(self,
                              size: int):
        data = {"index.max_result_window": size}
        url = "{}://{}:{}/_settings".format(self.protocol, self.elastic_ip, self.elastic_port)
        messenger(3, "Changing max_results_window size to {}".format(size))
        try:
            response = requests.put(url=url,
                                    headers=self.headers,
                                    data=json.dumps(data),
                                    verify=False,
                                    auth=(self.username, self.password))
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
                                               query_bool_must_not_list: list,
                                               app_window: customtkinter.CTk = None,
                                               progress_bar: customtkinter.CTkProgressBar = None,
                                               progress_bar_label: customtkinter.CTkLabel = None) -> list:
        url = "{}://{}:{}/{}/_search?pretty".format(self.protocol, self.elastic_ip, self.elastic_port, index_name)
        data_json_list = []
        is_first_loop = True
        last_ids = []
        messenger(3, "Fetching elastic data...")
        pbar = tqdm(total=num_logs, desc="Fetch Progress", file=sys.stderr)
        total_results_size = 0
        original_num_logs = num_logs

        # Mainly for UI
        if app_window is not None and progress_bar_label is not None and progress_bar is not None:
            progress_bar["value"] = (total_results_size / float(original_num_logs)) * 100
            progress_bar_label.set_text("Current Progress: {}/{} --- {:.2f}%".format(total_results_size,
                                                                                 original_num_logs,
                                                                                 progress_bar["value"]))
            app_window.update()
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
                            # BUG: KEEP GETTING NO HITS epoch seconds
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
                                        headers=self.headers,
                                        data=json.dumps(data),
                                        verify=False,
                                        auth=(self.username, self.password))
                data_json = response.json()
                if response.status_code == 200:
                    results_size = len(data_json["hits"]["hits"])
                    if results_size == 0:
                        # Return an empty data_json_list
                        messenger(2, "There are no hits! Please try again with a different time range!")
                        return data_json_list
                    pbar.update(results_size)
                    total_results_size += results_size

                    # For UI
                    if app_window is not None and progress_bar_label is not None and progress_bar is not None:
                        progress_bar["value"] = (total_results_size/float(original_num_logs))*100
                        progress_bar_label.set_text("Current Progress: {}/{} --- {:.2f}%".format(total_results_size,
                                                                                             original_num_logs,
                                                                                             progress_bar["value"]))
                        app_window.update()

                    data_json_list.append(data_json)
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

        messenger(0, "Successfully fetched {} data entries!".format(total_results_size))
        return data_json_list

    def get_indices_status(self):
        url = "{}://{}:{}/_cat/indices/*?v=true&s=index&pretty".format(self.protocol, self.elastic_ip, self.elastic_port)
        try:
            response = requests.get(url=url,
                                    verify=False,
                                    auth=(self.username, self.password))

            return response.text
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return

    def get_available_fields(self, index_name):
        url = "{}://{}:{}/{}/_mapping/field/*".format(self.protocol, self.elastic_ip, self.elastic_port, index_name)
        try:
            response = requests.get(url=url,
                                    verify=False,
                                    auth=(self.username, self.password))
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
