from ZeloEngineScript.common import log

test_id = 0


def test_log(title=''):
    global test_id
    log('%s %s' % (
        style_string('---- start test %s ' % test_id, bcolors.WARNING),
        style_string(title, bcolors.OKBLUE)))
    test_id += 1


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def style_string(s, style):
    return style + s + bcolors.ENDC


def log_style(msg, style):
    log(style + msg + bcolors.ENDC)


def log_style_warning(msg):
    log_style(msg, bcolors.WARNING)
