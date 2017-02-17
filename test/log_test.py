#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016
# 
########################################################################

"""
File: config_test.py
Author: tangweimin
Date: 2016/07/04
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/spider')

from log import *


class ConfigTestCase(unittest.TestCase):
    """ test log module. """

    def setUp(self):
        """ test fixture setUp """
        pass

    def tearDown(self):
        """ test fixture tearDown """
        pass

    def test_warning(self):
        """ test log function."""
        dblog = log('ljdb')
        crlog = log('crawler')
        dblog.debug('this is a %s from db','DEBUG')
        crlog.debug('this is a %s form cr','DEBUG')
        dblog.info('this is a %s from db','info')
        crlog.info('this is a %s form cr','info')
        dblog.warning('this is a %s from db','warning')
        crlog.warning('this is a %s form cr','warning')
        dblog.error('this is a %s from db','error')
        crlog.error('this is a %s form cr','error')
        dblog.critical('this is a %s from db','critical')
        crlog.critical('this is a %s form cr','critical')


if __name__ == '__main__':
    unittest.main()



