from utils.request_sender import RequestSender
from utils.config_reader import ConfigReader
from utils.converter import Converter
from utils.menu.commandline_menu import CommandLineMenu
from utils.menu.gui_menu import GUIMenu
from utils.input_validation import InputValidation
from utils.messenger import messenger
from utils.parser import Parser


def validate_config_inputs():
    messenger(3, "Checking elasticfetch.ini configuration inputs...")
    if not input_validation.is_protocol_valid(config_dict["elastic.protocol"]):
        exit(1)
    if not input_validation.is_ip(config_dict["elastic.ip"]):
        exit(1)
    if not input_validation.is_port(config_dict["elastic.port"]):
        exit(1)
    messenger(0, "All configuration inputs are valid.")


def main():

    '''validate_config_inputs()
    if config_dict["elastic.protocol"] == "https" and not request_sender.get_authentication_status_bool():
        exit(1)'''

    if not config_dict["interface.graphical"]:
        menu = CommandLineMenu(request_sender=request_sender,
                               converter=converter,
                               input_validation=input_validation,
                               parser=parser)
        while True:
            menu.show_menu()
    else:
        menu = GUIMenu(request_sender=request_sender,
                       converter=converter,
                       input_validation=input_validation,
                       parser=parser)
        menu.show_menu()



if __name__ == "__main__":
    config_reader = ConfigReader()
    config_dict = config_reader.read_config_file()
    converter = Converter()
    request_sender = RequestSender(
        protocol=config_dict["elastic.protocol"],
        elastic_ip=config_dict["elastic.ip"],
        elastic_port=config_dict["elastic.port"],
        username=config_dict["credentials.username"],
        password=config_dict["credentials.password"]
    )
    input_validation = InputValidation()
    parser = Parser()
    main()
