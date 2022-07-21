from configparser import ConfigParser
import ast

class ConfigReader:

    def __init__(self):
        self.description = "reads configuration from elasticfetch.ini"

    def read_config_file(self):

        config_dict = {}
        config_options = ConfigParser()
        config_options.read("elasticfetch.ini")
        if config_options.has_section("elastic"):
            if config_options.has_option("elastic", "protocol"):
                config_dict["elastic.protocol"] = ast.literal_eval(config_options.get("elastic", "protocol"))
            if config_options.has_option("elastic", "ip"):
                config_dict["elastic.ip"] = ast.literal_eval(config_options.get("elastic", "ip"))
            if config_options.has_option("elastic", "port"):
                config_dict["elastic.port"] = ast.literal_eval(config_options.get("elastic", "port"))

        if config_options.has_section("credentials"):
            if config_options.has_option("credentials", "username"):
                config_dict["credentials.username"] = ast.literal_eval(config_options.get("credentials", "username"))
            if config_options.has_option("credentials", "password"):
                config_dict["credentials.password"] = ast.literal_eval(config_options.get("credentials", "password"))

        return config_dict