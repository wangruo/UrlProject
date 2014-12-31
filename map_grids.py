#!/usr/bin/python
# encoding: utf-8
__author__ = 'Administrator'

if __name__ == '__main__':
    input_path = unicode(r'E:\prj\位置移动数据项目文档及代码\获取百度地址及划分格子\1. 获取地址\base_station_address',
                         'utf8')
    output_path = unicode(r'E:\prj\位置移动数据项目文档及代码\获取百度地址及划分格子\2. 格子化\base_station_grids',
                          'utf8')
    output_path_dict = \
        unicode(r'E:\prj\位置移动数据项目文档及代码\获取百度地址及划分格子\2. 格子化\base_station_grids_dict', 'utf8')

    fileInput = open(input_path)
    fileOutput = open(output_path, mode='w')
    fileOutput_dict = open(output_path_dict, mode='w')

    for line in fileInput:
        # 分割base_station_grids
        temp = line.strip().split('\t')
        # 百度米制坐标
        mc_x = float(temp[5])
        mc_y = float(temp[6])
        # 基站LAC
        lacs = temp[-1]

        # 16级地图，即zoom = 16时，grid = coord / 1024
        grid_x = int(mc_x / 1024.0)
        grid_y = int(mc_y / 1024.0)
        grid = '%s_%s' % (grid_x, grid_y)

        # 输出格子与lac对应文件
        output_str = '%s\t%s' % (grid, lacs)
        print output_str
        fileOutput.write(output_str + '\n')

        # 输出lac与格子对应文件
        lac_list = lacs.split(',')
        for lac in lac_list:
            output_str_dict = '%s\t%s' % (lac, grid)
            print output_str_dict
            fileOutput_dict.write(output_str_dict + '\n')

    fileInput.close()
    fileOutput.close()
    fileOutput_dict.close()
    print('任务完成')

# 格子计算公式
# grid_x = x / (2^(zoom - 18) / 256
# grid_y = y / (2^(zoom - 18) / 256

# 14级地图，即zoom = 14时，grid = coord / 4096
# grid_x = int(float(temp[4]) / 4096.0)
# grid_y = int(float(temp[5]) / 4096.0)