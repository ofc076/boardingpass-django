from datetime import datetime, timedelta
import time
from os import listdir, stat
from os.path import isfile, join
from stat import S_ISREG, ST_CTIME, ST_MODE, ST_MTIME
from datetime import datetime
from itertools import groupby

MYPATH = r'/var/barcode'
PROC_DIR = r'/proc/stat'

def boot_time():
    try:
        """Return the system boot time expressed in seconds since the epoch."""
        with open(PROC_DIR, "rb") as f:
            for line in f:
                if line.startswith(b'btime'):
                    ret = float(line.strip().split()[1])
                    return ret
    except:
        return 0

def uptime_str(timestamp):
    if timestamp == 0:
        return 'n/a'
    else:
        now = time.time()
        uptime = now - timestamp
        x = timedelta(seconds=uptime)
        days, seconds = x.days, x.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return '{} day {}h {}m {}s'.format(x.days, hours, minutes, seconds)


def boottime_str(timestamp):
    if timestamp == 0:
        return 'n/a'
    else:
        return datetime.fromtimestamp(timestamp).strftime('%d %b %Y %H:%M:%S')

"""
ret = boot_time()
ret = 1546048398
print('Last PowerON ' + boottime_str(ret))
print('System uptime ' + uptime_str(ret))
"""


def barcodes_total():
    onlyfiles = [f for f in listdir(MYPATH) if isfile(join(MYPATH, f))]
    #NOTE: on Windows `ST_CTIME` is a creation date
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date
    entries = ((stat(join(MYPATH,filename))[ST_MTIME], filename) for filename in onlyfiles)
    entries = sorted(entries, key=lambda e: e[0], reverse=True)

    newarr = []
    for i in entries:
        item = []
        item.append(i[1])
        item.append(datetime.fromtimestamp(i[0]).strftime('%Y-%m-%d'))
        newarr.append(item)
    res = []
    for key, group in groupby(newarr, lambda x: x[1]):
        count = 0
        for thing in group:
            count += 1
        res.append((key, count))
    return res


def barcodes_list():
    onlyfiles = [f for f in listdir(MYPATH) if isfile(join(MYPATH, f))]
    #NOTE: on Windows `ST_CTIME` is a creation date
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date
    entries = ((stat(join(MYPATH, filename))[ST_MTIME], filename, get_barcode_count(join(MYPATH, filename))) for filename in
               onlyfiles)
    entries = sorted(entries, key=lambda e: e[0], reverse=True)

    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    res = []
    for i in entries:
        res.append((datetime.fromtimestamp(i[0]).strftime('%Y-%m-%d %H:%M:%S'),  i[1], i[2]))
        #print('{}  ->  {}  ({})'.format(datetime.fromtimestamp(i[0]).strftime('%Y-%m-%d %H:%M:%S'), i[1], i[2]))
    return res


def get_barcode_count(path):
    try:
        with open(path, 'r') as f:
            i = f.readline()
            count = i.split('#!')[1].replace('\n','')
        return count
    except:
        return '1'