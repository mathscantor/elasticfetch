from configparser import ConfigParser
import ast


class ConfigReader:

    def __init__(self):
        self.__config_path = "elasticfetch.ini"
        self.__elastic_protocol = None
        self.__elastic_ip = None
        self.__elastic_port = None
        self.__credentials_username = None
        self.__credentials_password = None
        self.__interface_graphical = None
        self.__read_config_file()

    '''
    Reads in the user input from the configuration file and put them into a config_dict for easy access to 
    user's chosen parameters.
    '''
    def __read_config_file(self) -> dict:
        config_options = ConfigParser()
        config_options.read(self.__config_path)
        if config_options.has_section("elastic"):
            if config_options.has_option("elastic", "protocol"):
                self.__elastic_protocol = ast.literal_eval(config_options.get("elastic", "protocol"))
            if config_options.has_option("elastic", "ip"):
                self.__elastic_ip = ast.literal_eval(config_options.get("elastic", "ip"))
            if config_options.has_option("elastic", "port"):
                self.__elastic_port = ast.literal_eval(config_options.get("elastic", "port"))

        if config_options.has_section("credentials"):
            if config_options.has_option("credentials", "username"):
                self.__credentials_username = ast.literal_eval(config_options.get("credentials", "username"))
            if config_options.has_option("credentials", "password"):
                self.__credentials_password = ast.literal_eval(config_options.get("credentials", "password"))

        if config_options.has_section("interface"):
            if config_options.has_option("interface", "graphical"):
                self.__interface_graphical = ast.literal_eval(config_options.get("interface", "graphical"))

        return

    @property
    def elastic_protocol(self):
        return self.__elastic_protocol

    @property
    def elastic_ip(self):
        return self.__elastic_ip

    @property
    def elastic_port(self):
        return self.__elastic_port

    @property
    def credentials_username(self):
        return self.__credentials_username

    @property
    def credentials_password(self):
        return self.__credentials_password

    @property
    def interface_graphical(self):
        return self.__interface_graphical

