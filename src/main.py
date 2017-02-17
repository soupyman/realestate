#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016
#
########################################################################

"""
The spider module crawl specific URL pattern .

File: main.py
Author: tangweimin
Date: 2016/12/12

"""

import os
import sys

def clear_logs(logdir):
    # clear env
    if not os.path.isdir(logdir):
        try:
            os.makedirs(logdir)
        except OSError as e:
            print "create log directories error : %s" % e
            sys.exit()
    os.system('rm -rf ../log/*')


if __name__ == '__main__':
    logdir = '../log'
    clear_logs(logdir)

    import master
    import spider
    #run now
    mgr = master.MasterP()

    if mgr.is_worker():
        spider.spider()

