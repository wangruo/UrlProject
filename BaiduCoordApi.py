#!/usr/bin/python
# encoding: utf-8
__author__ = 'Administrator'
import sys
import urllib2
import json

reload(sys)
sys.setdefaultencoding("utf-8")


# 获取米制坐标
def get_mc_result(coordinators):
    url = 'http://api.map.baidu.com/geoconv/v1/?coords=' + coordinators + '&from=1&to=6&ak=rq2jN7Lc0nYYKSHBjB8FcpjM'
    html = urllib2.urlopen(url).read()
    # print(url, html)
    result = json.loads(html)
    # print(result)
    if result['status'] != 0:
        print(u'返回失败！' + url)
        return
    # print(result['result'])
    return result['result']


# 由米制坐标获取地址，改地址可分为5级
def get_address_result(x, y):
    url = 'http://api.map.baidu.com/?qt=rgc&x=' + x + '&y=' + y + '&dis_poi=1&poi_num=1&ie=utf-8'
    html = urllib2.urlopen(url).read()
    # print(html)
    result = json.loads(html)
    return result['content']


if __name__ == '__main__':
    # input_path = unicode(r'E:\prj\位置移动数据项目文档及代码\获取百度地址及划分格子\1. 获取地址\base_station_address',
    #                      'utf8')
    # output_path = unicode(r'E:\prj\位置移动数据项目文档及代码\获取百度地址及划分格子\2. 格子化\base_station_grids',
    #                       'utf8')

    fileInput = open(r'D:\base_station')
    fileOutput = open(r'D:\base_station_address', mode='a')
    begin_count = 0
    counter = 0
    for line in fileInput:
        counter += 1
        if counter < begin_count:
            continue

        temp = line.split('\t')

        table_id = temp[0]  # Oracle表ID
        lac = temp[4].replace('/', ',')  # 基站LAC与扇区
        std_x = temp[5]     # 标准GPS经度
        std_y = temp[6]     # 标准GPS纬度
        baidu_x = temp[7]   # 百度GPS经度
        baidu_y = temp[8]   # 百度GPS纬度

        # 获取米制坐标
        res = get_mc_result(std_x + ',' + std_y)
        error_count = 0
        if not res:
            while error_count < 5:
                res = get_mc_result(std_x + ',' + std_y)
                error_count += 1
                print(table_id + '   retry.....')

            if error_count >= 5:
                print("retry failed!")
                sys.exit(1)

        # 获取详细地址
        address = get_address_result(str(res[0]['x']), str(res[0]['y']))

        # 整理数据文件格式
        output_line = [str(counter),                                 # 序号
                       std_x, std_y,                                 # 标准GPS
                       baidu_x, baidu_y,                             # 百度GPS
                       str(res[0]['x']), str(res[0]['y']),           # 百度米制坐标
                       str(address['address_detail']['city_code']),  # 城市code
                       address['address'],                           # 详细地址
                       address['address_detail']['province'],        # 省级
                       address['address_detail']['city'],            # 市级
                       address['address_detail']['district'],        # 区县级
                       address['address_detail']['street'],          # 街道
                       address['address_detail']['street_number'],   # 号码
                       lac]                                          # 基站LAC编号

        str_output = '\t'.join(output_line)
        print(str_output)
        fileOutput.write(str_output + '\n')

    fileInput.close()
    fileOutput.close()
    print("任务完成！")