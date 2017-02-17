#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2016
# 
########################################################################

"""
File: args_test.py
Author: tangweimin
Date: 2016/12/24
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/spider')

from args import *


class ArgsTestCase(unittest.TestCase):
    """ test args module. """

    def setUp(self):
        """ test fixture setUp """

    def tearDown(self):
        """ test fixture tearDown """

    def test_parse(self):
        """ test Args parse function."""
        a = Args(['-d', '-t', '4'])
        self.assertEquals(a.d, True)
        self.assertEquals(a.fff, 0)
        self.assertEquals(a.t, '4')

if __name__ == '__main__':
    unittest.main()





