#!/usr/bin/python
# encoding: utf-8
# __author__ = 'Administrator'
import re
import sys

if __name__ == '__main__':
    fileInput = open(r'E:/prj/grids/raws/test/first')
    fileOutput = open(r'E:/prj/grids/raws/test/second', 'w')

    sys.stderr.write('reporter:status:mapreduce job is started...\n')
    for line in fileInput:
        line = line.decode('gbk')
        fields = line.strip().split('|')

        # 标注成可以识别的变量名
        cell = fields[2]
        date = fields[1]
        lac = fields[3]
        cell_id = fields[4]
        std_x = fields[5]
        std_y = fields[6]
        address = fields[7]

        # 检查号码
        if not re.match('^\d{11}$', cell):
            sys.stderr.write('reporter:counter:mapper,cell_err,1')
            continue

        # 把时间按半小时处理成ID
        time = date.split()[1].split(":")
        hour = int(time[0])
        minute = int(time[1])
        time_seg = 0
        if minute >= 30:
            time_seg = hour * 2 + 1
        else:
            time_seg = hour * 2

        # 以 电话号码_基站lac_基站ID_时间段 为键
        key_str = '%s_%s_%s_%d' % (cell, lac, cell_id, time_seg)
        value_str = '%s\t%s\t%s\t%s' % (date, std_x, std_y, address)
        out_str = '%s\t%s' % (key_str, value_str)
        print(out_str)
        fileOutput.write(out_str + '\n')

    fileInput.close()
    fileOutput.close()
    print('任务完成')
