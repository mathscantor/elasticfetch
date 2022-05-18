from utils.request_sender import RequestSender
from utils.config_reader import ConfigReader
from utils.converter import Converter
from utils.menu import Menu
from utils.input_validation import InputValidation
from utils.messenger import messenger


def validate_config_inputs():
    messenger(3, "Checking elasticfetch.ini configuration inputs...")
    if not input_validation.is_ip(config_dict["elastic.ip"]):
        exit(1)
    if not input_validation.is_port(config_dict["elastic.port"]):
        exit(1)
    messenger(0, "All configuration inputs are valid.")


def main():

    validate_config_inputs()
    if not request_sender.get_authentication_status_bool():
        exit(1)
    while True:
        menu.show_menu()


if __name__ == "__main__":
    config_reader = ConfigReader()
    config_dict = config_reader.read_config_file()
    converter = Converter()
    request_sender = RequestSender(
        elastic_ip=config_dict["elastic.ip"],
        elastic_port=config_dict["elastic.port"],
        username=config_dict["credentials.username"],
        password=config_dict["credentials.password"]
    )
    input_validation = InputValidation()
    menu = Menu(request_sender=request_sender,
                converter=converter,
                input_validation=input_validation)
    main()
