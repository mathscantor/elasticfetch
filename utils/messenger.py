class bcolors:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    ALERT = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAILURE = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def messenger(sev, message):

    if sev == 0:
        print(bcolors.SUCCESS + " [SUCCESS] " + bcolors.ENDC + message)
    elif sev == 1:
        print(bcolors.WARNING + " [WARN] " + bcolors.ENDC + message)
    elif sev == 2:
        print(bcolors.FAILURE + " [FAILURE] " + bcolors.ENDC + message)
    elif sev == 3:
        print(bcolors.INFO + " [INFO] " + bcolors.ENDC + message)
    elif sev == 4:
        print(bcolors.ALERT + " [ALERT] " + bcolors.ENDC + message)
    return