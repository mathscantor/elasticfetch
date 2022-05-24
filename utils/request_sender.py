import requests
from utils.messenger import messenger
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestSender:

    def __init__(self, elastic_ip, elastic_port, username, password):
        self.description = "Sends POST/GET request to elasticsearch server"
        self.headers = {"Content-Type": "application/json"}
        self.elastic_ip = elastic_ip
        self.elastic_port = elastic_port
        self.username = username
        self.password = password

    def get_authentication_status_bool(self):
        url = "https://{}:{}/_security/_authenticate?pretty".format(self.elastic_ip, self.elastic_port)
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
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return


    '''
    A point in time must be opened explicitly before being used in search requests. 
    The keep_alive parameter tells Elasticsearch how long it should keep a point in time alive, e.g. ?keep_alive=60m
    '''
    def post_fetch_pit_id(self, index_name):
        url = "https://{}:{}/{}/_pit?keep_alive=60m&pretty".format(self.elastic_ip, self.elastic_port, index_name)
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
    def delete_pit_id(self, pit_id):
        data = {"id": pit_id}
        url = "https://{}:{}/_pit?pretty".format(self.elastic_ip, self.elastic_port)
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
    def put_max_result_window(self, size):
        data = {"index.max_result_window": size}
        url = "https://{}:{}/_settings".format(self.elastic_ip, self.elastic_port)
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
    Sends GET request to fetch data between 2 timestamps
    Example:
    GET _search
    {
      "size": 1000,
      "_source": ["event.created","event.code"],
      "query": {
        "bool": {
          "filter": [
            {
              "range": {
                "@timestamp": {
                  "gte": "2022-05-01T00:00:00",
                  "lte": "2022-05-20T00:00:00"
                }
              }
            }
          ], 
          "must" : [
            {"term" : { "event.outcome" : "success" }},
            {"term" : { "event.category": "authentication" }}
          ]
        }
      },
      "pit": {
        "id": "8_LoAwEQd2lubG9nYmVhdC04LjAuMRZOTlg2bVVzb1Q0bV8yR1B4bVNaQzZnABY1SFNJbG5fWlE3QzB3NU1uRERDbHpnAAAAAAAAb642FlBWekRTejRvU09HV0VITFBLdEtKTkEAARZOTlg2bVVzb1Q0bV8yR1B4bVNaQzZnAAA=",
        "keep_alive": "1m"
      },
      "sort": [
        {
          "@timestamp": {
            "order": "asc",
            "format": "strict_date_optional_time_nanos",
            "numeric_type" : "date_nanos"
          }
        }
      ]
    }
    '''
    def get_fetch_elastic_data_between_ts1_ts2(self, pit_id, num_logs, start_ts, end_ts, fields_list,
                                               query_bool_must_list, query_bool_must_not_list):
        url = "https://{}:{}/_search?pretty".format(self.elastic_ip, self.elastic_port)
        data = \
        {
            "size": num_logs,
            "_source": fields_list,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start_ts,
                                    "lte": end_ts
                                }
                            }
                        }
                    ]
                }
            },
            "pit": {
                "id": pit_id,
                "keep_alive": "60m"
            },
            "sort": [
                {"@timestamp": {"order": "asc","format": "strict_date_optional_time_nanos","numeric_type" : "date_nanos"}}
            ]
        }
        if len(query_bool_must_list) > 0:
            data["query"]["bool"]["must"] = query_bool_must_list
        if len(query_bool_must_not_list) > 0:
            data["query"]["bool"]["must_not"] = query_bool_must_not_list
        messenger(3, "Sending the following request:\nGET {}\n{}".format(url, json.dumps(data, indent=4)))
        try:
            response = requests.get(url=url,
                                    headers=self.headers,
                                    data=json.dumps(data),
                                    verify=False,
                                    auth=(self.username, self.password))
            data_json = response.json()
            if response.status_code == 200:
                messenger(0, "Successfully fetched elastic data ({} hits) ".format(len(data_json["hits"]["hits"])))
                return data_json
            elif response.status_code == 400:
                messenger(2, "Unable to fetch elastic data. Bad Request in headers/data.")
            elif response.status_code == 401:
                messenger(2, "Unable to fetch elastic data. Authentication Error.")
            return None
        except requests.RequestException:
            messenger(2, "Cannot resolve request to {}".format(url))
        except requests.ConnectTimeout:
            messenger(2, "Connection timeout to {}".format(url))
        except requests.ConnectionError:
            messenger(2, "Cannot connect to {}".format(url))
        return

    def get_indices_status(self):
        url = "https://{}:{}/_cat/indices/*beat*?v=true&s=index&pretty".format(self.elastic_ip, self.elastic_port)
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
