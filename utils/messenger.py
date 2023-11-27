from enum import Enum


class Severity(Enum):
    DEBUG = '\033[94m [DEBUG] \033[0m'
    INFO = '\033[92m [INFO] \033[0m'
    WARNING = '\033[93m [WARNING] \033[0m'
    ERROR = '\033[91m [ERROR] \033[0m'


class Messenger:
    """
    Messenger class responsible for giving meaning outputs to users and developers.
    """
    def __init__(self,
                 verbosity_level: int = 1):
        self.__verbosity_level = verbosity_level

    def print_message(self, sev: Severity,
                      message: str) -> None:

        """
        Utility function to print messages of different severity levels.

        :param sev: A Severity Enum.
        :param message: The string to be printed.
        :return: None
        :rtype: None
        """

        # If verbosity is default, then do not print DEBUG messages
        if self.__verbosity_level == 1 and sev == Severity.DEBUG:
            return

        # Prints all messages under the sun
        print(sev.value + message)
        return
