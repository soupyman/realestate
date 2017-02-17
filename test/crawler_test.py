#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################

"""
File: crawl_thread_test.py
Author: wanghaifeng03(wanghaifeng03@baidu.com)
Date: 2016/01/06 13:42:48
"""

import os
import sys
import threading
import Queue
import re
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import CommuniteCrawlerT


class CrawlThreadTestCase(unittest.TestCase):
    """ test crawl_thread module. """

    def setUp(self):
        """ test fixture setUp """

    def tearDown(self):
        """ test fixture tearDown """

    def test_run(self):
        """ test crawl_thread run method."""
        CommuniteCrawlerT.region('朝阳')


if __name__ == '__main__':
    unittest.main()
