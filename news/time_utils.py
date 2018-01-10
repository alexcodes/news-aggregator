import time
from datetime import datetime


# parse string to timestamp truncated to seconds
# example: 2018-01-10T07:24:00+00:00
def parse(line):
    return int(time.mktime(datetime.strptime(line, "%Y-%m-%dT%H:%M:%S+00:00").timetuple()))
