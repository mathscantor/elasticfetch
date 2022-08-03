from utils.request_sender import RequestSender
from utils.config_reader import ConfigReader
from utils.converter import Converter
import os


def main():
    config_reader = ConfigReader()
    config_dict = config_reader.read_config_file()
    converter = Converter()

    request_sender = RequestSender(protocol=config_dict["elastic.protocol"],
                                   elastic_ip=config_dict["elastic.ip"],
                                   elastic_port=config_dict["elastic.port"],
                                   username=config_dict["credentials.username"],
                                   password=config_dict["credentials.password"])

    request_sender.get_authentication_status_bool()
    data_json_list = request_sender.get_fetch_elastic_data_between_ts1_ts2(index_name=index_name,
                                                                           num_logs=num_logs,
                                                                           main_timestamp_field_name=main_timestamp_field_name,
                                                                           main_timestamp_field_format=main_timestamp_format,
                                                                           main_timezone=main_timezone,
                                                                           start_ts=start_ts,
                                                                           end_ts=end_ts,
                                                                           fields_list=fields_list,
                                                                           query_bool_must_list=query_bool_must_list,
                                                                           query_bool_must_not_list=query_bool_must_not_list)
    if len(data_json_list) == 0:
        return
    file_path = "datasets/{}.csv".format(index_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if file_path.lower().endswith(".csv"):
        converter.convert_json_data_to_csv(data_json_list=data_json_list, fields_list=fields_list,
                                                file_path=file_path)
    return


if __name__ == "__main__":
    main_timestamp_field_name = "@timestamp"
    main_timestamp_format = "datetime"
    main_timezone = "+08:00"
    index_name = "winlogbeat-8"
    num_logs = 10000
    start_ts = "2022-01-01T00:00:00"
    end_ts = "2022-08-01T00:00:00"
    fields_list = ["@timestamp", "event.code"]
    query_bool_must_list = []
    query_bool_must_not_list = []
    '''query_bool_must_not_list = [
        {
            "term": {
                "event.code": "4000"
            }
        }
    ]'''
    '''query_bool_must_list = [
                {
                    "range": {
                        "event.code": {
                            "lte": "5000"
                        }
                    }
                }
            ]'''
    main()