#!/usr/bin/python
import os

import re
import sys
import subprocess
from datetime import datetime
from datetime import timedelta


def Sub(cmd, cla, key):
    key = '%s_%s' % (cla, key)
    print 'running' + '\n' + cmd + '\n'
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    process.wait()
    out = process.stdout.read()
    if process.returncode:
        print out
        sys.exit()
    else:
        print '%s is done!' % key


#datetime(int(date[0:4]), int(date[6:7]), int(date[9:10]))
def get_next_date(date):
    date_new = datetime.strptime(date, '%Y/%m/%d')
    next_day = date_new + timedelta(days=1)
    return next_day.strftime("%Y/%m/%d")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Command Format: InvokeJar jar_path init_input_path begin_date end_date'
        print 'Date Format:2014/01/02'
        print 'Now the script will exit, please restart it'
        sys.exit()

    # define the root directories
    input_path_root = '/data/category/internet_union/'
    output_path_root = '/home/ruo.wang/output/'

    # get input params
    jar_path = sys.argv[1]
    init_input_path = sys.argv[2]
    begin_date = sys.argv[3]
    end_date = sys.argv[4]

    # get handling directories
    input_path1 = init_input_path
    input_path2 = input_path_root + begin_date
    output_path = output_path_root + begin_date

    # assist variable
    next_date = begin_date
    handle_day = int(re.sub('/', '', begin_date))
    end_day = int(re.sub('/', '', end_date))
    while handle_day <= end_day:
        cmd_string = "hadoop jar %s %s %s %s" % (jar_path, input_path1, input_path2, output_path)
        print cmd_string
        Sub(cmd_string, handle_day, 'internet_union')

        next_date = get_next_date(next_date)
        input_path1 = output_path
        input_path2 = input_path_root + next_date
        output_path = output_path_root + next_date

        handle_day = int(re.sub('/', '', next_date))

    os.system()
    print '=' * 60

