from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

class color:
    header = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    gray = '\033[37m'
    dark_gray = '\033[90m'
    pyna_colada = '\033[93m'
    warn = '\033[33m'
    fail = '\033[91m'
    end = '\033[0m'

def color_print(message,printed_color):
    print(printed_color + message + color.end)
