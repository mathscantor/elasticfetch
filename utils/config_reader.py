import configparser

from utils.messenger import Messenger, Severity
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
        self.__messenger = Messenger()
        self.__read_config_file()

    '''
    Reads in the user input from the configuration file and put them into a config_dict for easy access to 
    user's chosen parameters.
    '''
    def __read_config_file(self) -> dict:
        config_options = ConfigParser()

        try:
            config_options.read(self.__config_path)
        except configparser.MissingSectionHeaderError:
            self.__messenger.print_message(Severity.ERROR, "One of the sections is missing: "
                                                           "[elastic], [credentials], [interface], [data]")
            exit(1)
        except configparser.ParsingError as e:
            self.__messenger.print_message(Severity.ERROR, e.message)
            exit(1)

        if config_options.has_section("elastic"):
            if config_options.has_option("elastic", "protocol"):
                self.__elastic_protocol = ast.literal_eval(config_options.get("elastic", "protocol"))
                if type(self.__elastic_protocol) != str:
                    self.__messenger.print_message(Severity.ERROR, "[elastic] Protocol option expected <class 'str'> "
                                                                   "but got {} instead!".format(type(self.__elastic_protocol)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'protocol' option in [elastic] section!")
                exit(1)

            if config_options.has_option("elastic", "ip"):
                self.__elastic_ip = ast.literal_eval(config_options.get("elastic", "ip"))
                if type(self.__elastic_ip) != str:
                    self.__messenger.print_message(Severity.ERROR, "[elastic] IP option expected <class 'str'> "
                                                                   "but got {} instead!".format(type(self.__elastic_ip)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'ip' option in [elastic] section!")
                exit(1)

            if config_options.has_option("elastic", "port"):
                self.__elastic_port = ast.literal_eval(config_options.get("elastic", "port"))
                if type(self.__elastic_port) != int:
                    self.__messenger.print_message(Severity.ERROR, "[elastic] Port option expected <class 'int'> "
                                                                   "but got {} instead!".format(type(self.__elastic_ip)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'port' option in [elastic] section!")
                exit(1)
        else:
            self.__messenger.print_message(Severity.ERROR, "Missing [elastic] section!")
            exit(1)

        if config_options.has_section("credentials"):
            if config_options.has_option("credentials", "username"):
                self.__credentials_username = ast.literal_eval(config_options.get("credentials", "username"))
                if type(self.__credentials_username) != str:
                    self.__messenger.print_message(Severity.ERROR, "[credentials] Username option expected <class 'str'> "
                                                                   "but got {} instead!".format(type(self.__credentials_username)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'username' option in [credentials] section!")
                exit(1)

            if config_options.has_option("credentials", "password"):
                self.__credentials_password = ast.literal_eval(config_options.get("credentials", "password"))
                if type(self.__credentials_password) != str:
                    self.__messenger.print_message(Severity.ERROR, "[credentials] Password option expected <class 'str'> "
                                                                   "but got {} instead!".format(type(self.__credentials_password)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'password' option in [credentials] section!")
                exit(1)
        else:
            self.__messenger.print_message(Severity.ERROR, "Missing [credentials] section!")
            exit(1)

        if config_options.has_section("interface"):
            if config_options.has_option("interface", "graphical"):
                self.__interface_graphical = ast.literal_eval(config_options.get("interface", "graphical"))
                if type(self.__interface_graphical) != bool:
                    self.__messenger.print_message(Severity.ERROR, "[interface] Graphical option expected <class 'bool'> "
                                                                   "but got {} instead!".format(type(self.__interface_graphical)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'graphical' option in [interface] section!")
                exit(1)
        else:
            self.__messenger.print_message(Severity.ERROR, "Missing [interface] section!")
            exit(1)

        if config_options.has_section("data"):
            if config_options.has_option("data", "batch_size"):
                self.__batch_size = ast.literal_eval(config_options.get("data", "batch_size"))
                if type(self.__batch_size) != int:
                    self.__messenger.print_message(Severity.ERROR, "[data] Batch Size option expected <class 'int'> "
                                                                   "but got {} instead!".format(type(self.__batch_size)))
                    exit(1)
            else:
                self.__messenger.print_message(Severity.ERROR, "Missing 'batch_size' option in [data] section!")
                exit(1)
        else:
            self.__messenger.print_message(Severity.ERROR, "Missing [data] section!")
            exit(1)
        return

    @property
    def elastic_protocol(self) -> int:
        return self.__elastic_protocol

    @property
    def elastic_ip(self) -> str:
        return self.__elastic_ip

    @property
    def elastic_port(self) -> int:
        return self.__elastic_port

    @property
    def credentials_username(self) -> str:
        return self.__credentials_username

    @property
    def credentials_password(self) -> str:
        return self.__credentials_password

    @property
    def interface_graphical(self) -> bool:
        return self.__interface_graphical

    @property
    def batch_size(self) -> int:
        return self.__batch_size

