#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# 
########################################################################

"""
File: mini_spider_test.py
Author: wanghaifeng03(wanghaifeng03@baidu.com)
Date: 2016/01/06 14:57:38
"""
import os
import sys
import shutil
import urllib
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class MiniSpiderTestCase(unittest.TestCase):
    """ test mini_spider module. """

    def setUp(self):
        """ test fixture setUp """
        conf = ("[spider]\n"
                "url_list_file: ./seed.urls ;\n"
                "output_directory: ./output ;\n"
                "max_depth: 2 ;\n"
                "crawl_interval: 1 ;\n"
                "crawl_timeout: 1 ;\n"
                "target_url: .*\.(gif|png|jpg|bmp)$ ;\n"
                "thread_count: 8 ;\n")
        with open("spider_test.conf", "w+") as f:
            f.writelines(conf)

        seedfile = "http://pycm.baidu.com:8081"
        with open("seed.urls", "w+") as f:
            f.writelines(seedfile)

    def tearDown(self):
        """ test fixture tearDown """
        if os.path.exists("seed.urls"):
            os.remove("seed.urls")
        if os.path.exists("spider_test.conf"):
            os.remove("spider_test.conf")
        if os.path.exists("./log"):
            shutil.rmtree("./log")
        if os.path.exists("./output"):
            shutil.rmtree("./output")

    def test_mini_spider(self):
        """ test mini_spider main"""
        os.system("python ../mini_spider.py -c spider_test.conf")
        targets = os.listdir("./output")
        self.assertIn(urllib.quote_plus("http://pycm.baidu.com:8081/3/image.jpg"), targets)


if __name__ == '__main__':
    unittest.main()
