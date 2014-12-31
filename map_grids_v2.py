#!/usr/bin/python
# encoding: utf-8
__author__ = 'Administrator'


if __name__ == '__main__':
    fileInput1 = open(r'D:\base_station')
    fileInput2 = open(r'D:\base_station_address_old')
    fileOutput = open(r'D:\base_station_address_new', mode='w')
    dic = {}
    for line in fileInput1:
        parts = line.split('\t')
        dic[parts[0]] = parts[4]
        # print('%s\t%s' % (parts[0], dic[parts[0]]))

    for line in fileInput2:
        parts = line.split('\t')
        format_str = "%s\t%s"
        output_line = format_str % (line.strip('\r\n'), dic[parts[1]])

        print(output_line)
        fileOutput.write(output_line + '\n')

    fileInput1.close()
    fileInput2.close()
    fileOutput.close()
    print('任务完成')