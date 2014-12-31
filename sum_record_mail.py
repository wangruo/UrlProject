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
    return_code = process.returncode
    if return_code:
        send_mail(return_code, cla, out)
        print(out)
        sys.exit()
    else:
        print '%s is done!' % key


def send_mail(return_code, mail_path_root, out):
    abspath = os.path.abspath(mail_path_root)
    file_path = abspath + "/sum_record_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mail"
    # print(file_path)
    fp = open(file_path, 'w')
    fp.write('to:\"wangruo_2012_log@163.com\"\n')
    fp.write('topic:\"sum_record\"\n')
    print(return_code)
    if return_code == 3:
        fp.write('content:\"The input_path1 cannot find.\"')
    elif return_code == 4:
        fp.write('content:\"The input_path2 cannot find.\"')
    else:
        fp.write('content:\"' + out + '\"')

    fp.close()


def dir_path_check(path):
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        print 'The path [%s] is not exist, exit' % abspath
        return False, abspath
    if not os.path.isdir(abspath):
        print 'The path [%s] is not a directory, exit' % abspath
        return False, abspath
    return True, abspath


def get_date():
    now = datetime.now()
    today = str(now).split(' ')[0]
    yesterday = str(now - timedelta(days=1)).split(' ')[0]
    day_before_yesterday = str(now - timedelta(days=2)).split(' ')[0]
    return re.sub('-', '/', today), re.sub('-', '/', yesterday), re.sub('-', '/', day_before_yesterday)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: sum_record.py <jar_path> <input_path_root> <output_path_root> <mail_path>'
        sys.exit()

    # get input params
    jar_path = sys.argv[1]

    # define the root directories
    # input_path_root = '/data/category/internet_union/'
    # output_path_root = '/home/ruo.wang/output/'
    input_path_root = sys.argv[2]
    output_path_root = sys.argv[3]
    res, mail_path = dir_path_check(sys.argv[4])
    if not res:
        sys.exit()

    the_day, pre_day, pre_pre_day = get_date()
    # if today is the third day, use input_path_root for the first day
    if the_day.split('/')[2] == '03':
        input_path1 = input_path_root + '/' + pre_pre_day
    else:
        input_path1 = output_path_root + '/' + pre_pre_day

    input_path2 = input_path_root + '/' + pre_day
    output_path = output_path_root + '/' + pre_day

    # main process
    cmd_string = "hadoop jar %s %s %s %s" % (jar_path, input_path1, input_path2, output_path)
    Sub(cmd_string, mail_path, 'internet_union')

    print '=' * 60
