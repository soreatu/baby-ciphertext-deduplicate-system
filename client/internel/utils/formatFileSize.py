# -*- encoding: utf-8 -*-
'''
@DESCRIPTION : convert Bytes to KBytes/MBytes/GBytes/TBytes/PBytes
@AUTHOR      : jylsec
@TIME        : 2021/06/17
'''

def formatFileSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ('{}.{:>03d} {}'.format(integer, remainder, units[level]))