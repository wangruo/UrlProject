# encoding: utf-8
__author__ = 'Administrator'

if __name__ == '__main__':
    fileLocation = open(r'D:\base_station_address')
    fileBaseStation = open(r'E:\test\grids\base_station_grids')
    fileOutput = open(r'D:\get_grids_location', mode='w')

    dict_station_location = {}
    for line in fileLocation:
        words = line.split('\t')
        dict_station_location[words[1]] = words[7]

    dict_grids_station = []
    for line in fileBaseStation:
        words = line.split('\t')
        item = '%s\t%s' % (words[4], words[5])
        if item not in dict_grids_station:
            dict_grids_station.append(item)
            fileOutput.write('%s\t%s\n' % (item, dict_station_location[words[1]]))

    fileLocation.close()
    fileBaseStation.close()
    fileOutput.close()
    print '任务完成'
