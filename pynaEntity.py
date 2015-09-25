from datetime import datetime, timezone

class PynaEntity(object):
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

    def color_print(self,message,printed_color):
        print(printed_color + message + self.color.end)

    def utc_to_local(self,utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
