from utils.request_sender import RequestSender
from utils.config_reader import ConfigReader
from utils.converter import Converter
from menu.cli.menu import CommandLineMenu
from menu.gui.menu import GUIMenu
from utils.input_validation import InputValidation
from utils.messenger import Messenger, Severity
from utils.parser import Parser


def validate_config_inputs():
    messenger.print_message(Severity.INFO, "Checking elasticfetch.ini configuration inputs...")
    if not input_validation.is_protocol_valid(config_reader.elastic_protocol):
        exit(1)
    if not input_validation.is_ip_valid(config_reader.elastic_ip):
        exit(1)
    if not input_validation.is_port_valid(config_reader.elastic_port):
        exit(1)
    if not input_validation.is_batch_size_valid(config_reader.batch_size):
        exit(1)
    messenger.print_message(Severity.INFO, "All configuration inputs are valid.")


def main():

    validate_config_inputs()
    if not request_sender.get_authentication_status_bool():
        exit(1)

    if not config_reader.interface_graphical:
        menu = CommandLineMenu(request_sender=request_sender,
                               converter=converter,
                               input_validation=input_validation,
                               parser=parser,
                               config_reader=config_reader)
        while True:
            menu.show_menu()
    else:
        menu = GUIMenu(request_sender=request_sender,
                       converter=converter,
                       input_validation=input_validation,
                       parser=parser)
        menu.show_menu()


if __name__ == "__main__":
    messenger = Messenger()
    config_reader = ConfigReader()
    converter = Converter()
    request_sender = RequestSender(
        protocol=config_reader.elastic_protocol,
        elastic_ip=config_reader.elastic_ip,
        elastic_port=config_reader.elastic_port,
        username=config_reader.credentials_username,
        password=config_reader.credentials_password,
        batch_size=config_reader.batch_size
    )
    input_validation = InputValidation()
    parser = Parser()
    main()
