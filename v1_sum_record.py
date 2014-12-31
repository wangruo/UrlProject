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
    """
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    process.wait()
    out = process.stdout.read()
    return_code = process.returncode
    if return_code:
        print out
        sys.exit()
    else:
        print '%s is done!' % key
    """


def get_date(n):
    now = datetime.now()
    today = str(now).split(' ')[0]
    yesterday = str(now - timedelta(n)).split(' ')[0]
    day_before_yesterday = str(now - timedelta(n + 1)).split(' ')[0]
    return re.sub('-', '/', today), re.sub('-', '/', yesterday), re.sub('-', '/', day_before_yesterday)


if __name__ == '__main__':
    # get input params
    mr_jar_path = '/data/category/internet_union/merge/sum_record-1.0-SNAPSHOT.jar'
    input_path_root = '/data/category/internet_union'
    output_path_root = '/data/category/internet_merge'
    priority = "NORMAL"

    mail_jar_path = '/home/ruo.wang/send_mail-1.0-SNAPSHOT.jar'
    mail_address = 'wangruo_2012@163.com'
    topic = '....'
    content = '.....'

    n = 18
    the_day, pre_day, pre_pre_day = get_date(n)
    # if yesterday is the pre_day, use input_path_root for the first day
    if pre_day.split('/')[2] == '01':
        print 'pre_day is 01, exit'
        exit()

    if pre_pre_day.split('/')[2] == '01':
        input_path1 = input_path_root + '/' + pre_pre_day
    else:
        input_path1 = output_path_root + '/' + pre_pre_day

    input_path2 = input_path_root + '/' + pre_day
    output_path = output_path_root + '/' + pre_day

    # main process
    cmd_string = "hadoop jar %s %s %s %s %s" % (mr_jar_path, input_path1, input_path2, output_path, priority)
    Sub(cmd_string, the_day, 'internet_union')

    # send mail
    cmd_string = "java -jar %s %s %s %s" % (mail_jar_path, mail_address, topic, content)
    Sub(cmd_string, the_day, 'internet_union')

    print '=' * 60
