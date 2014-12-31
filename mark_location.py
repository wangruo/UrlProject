# encoding: utf-8
__author__ = 'Administrator'

if __name__ == '__main__':
    fileLocation = open(r'D:\get_grids_location')
    fileData = open(r'D:\day_merge_count')
    fileOutput = open(r'D:\day.txt', mode='w')

    dict_location = {}
    for line in fileLocation:
        words = line.strip().split('\t')
        key = '%s_%s' % (words[0], words[1])
        dict_location[key] = words[2]

    for line in fileData:
        line = line.strip()
        words = line.split('\t')
        key = '%s_%s' % (words[1], words[2])
        temp = '%s\t%s\n' % (line, dict_location[key])
        print temp,
        fileOutput.write(temp)

    fileLocation.close()
    fileOutput.close()
    print 'Task complete!'
