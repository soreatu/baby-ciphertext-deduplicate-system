# -*- encoding: utf-8 -*-
'''
@DESCRIPTION : convert CST to common time like %Y-%m-%d %H:%M:%S
@AUTHOR      : jylsec
@TIME        : 2021/06/17
'''

from datetime import datetime

def CST2CommonTime(CST):
    CSTFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
    commonTimeFormat = "%Y-%m-%d %H:%M:%S"
    CST = datetime.strptime(CST,CSTFormat)
    commonTime = CST.strftime(commonTimeFormat)
    return commonTime