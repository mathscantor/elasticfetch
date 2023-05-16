from configparser import ConfigParser
import ast

class ConfigReader:

    def __init__(self):
        self.description = "reads configuration from elasticfetch.ini"
        self.config_path = "elasticfetch.ini"

    '''
    Reads in the user input from the configuration file and put them into a config_dict for easy access to 
    user's chosen parameters.
    '''
    def read_config_file(self) -> dict:
        config_dict = {}
        config_options = ConfigParser()
        config_options.read(self.config_path)
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

        if config_options.has_section("interface"):
            if config_options.has_option("interface", "graphical"):
                config_dict["interface.graphical"] = ast.literal_eval(config_options.get("interface", "graphical"))

        return config_dict
