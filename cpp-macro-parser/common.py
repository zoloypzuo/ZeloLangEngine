# coding=utf-8
import sys


def readall(path):
    with open(path, 'r') as f:
        return f.read()


def writeall(path, text):
    with open(path, 'w') as f:
        f.write(text)


# python2没有enum
class Enum:
    OPTION_ENUM_USE_STRING = True
    _ENUM_ID = -1
    _ENUM_NAMES = set()

    # [x] auto支持使用string，添加开关，关闭时只比较enum-id
    # 替换自动生成代码：Sublime里正则替换(.*) = auto\(\)为\1 = auto\('\1'\)
    def auto(name=''):
        global _ENUM_ID
        _ENUM_ID += 1
        # name默认是空串，那么这个枚举仍然用数字，这个是没有影响的
        if Enum.OPTION_ENUM_USE_STRING and name:
            assert name not in Enum._ENUM_NAMES
            Enum._ENUM_NAMES.add(name)
            return name
        return _ENUM_ID


def text_pointer(index):
    return ' ' * index + '^'


class LogLevel:
    CLOSED = 0
    Error = 1
    Debug = 2


class Logger:
    OPTION_LOG_ENABLED = True
    OPTION_LOG_LEVEL = LogLevel.Debug


def log(msg):
    if Logger.OPTION_LOG_LEVEL >= LogLevel.Debug:
        print(msg)


def log_error(msg):
    if Logger.OPTION_LOG_LEVEL >= LogLevel.Error:
        print>> sys.stderr, msg


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


def log_style_header(msg):
    log_style(msg, bcolors.HEADER)


def log_style_okblue(msg):
    log_style(msg, bcolors.OKBLUE)


def log_style_okgreen(msg):
    log_style(msg, bcolors.OKGREEN)


def log_style_fail(msg):
    log_style(msg, bcolors.FAIL)


def log_style_bold(msg):
    log_style(msg, bcolors.BOLD)


def log_style_underline(msg):
    log_style(msg, bcolors.UNDERLINE)
