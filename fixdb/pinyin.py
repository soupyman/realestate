#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
File: pingyin.py
Author: tangweimin
Date: 2016/11/14
Desc: chinese to pingyin converter class  
"""

import os.path


class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}

        if not os.path.exists(dict_file):
            raise IOError("NotFoundFile")

        with file(dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]


    def convert(self, string="", join=False, delimit=""):
        result = []
        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        
        for char in string:
            key = '%X' % ord(char)
            if self.word_dict.get(key):
                result.append(self.word_dict.get(key, char).split()[0][:-1].lower())
            elif ord(char) <= 0x7F:
                result.append(char.lower())
            else :
                pass
                #not chinese not asiic, so ignore it.

        if join == True:
            result = delimit.join(result)

        return result


if __name__ == "__main__":
    test = PinYin()

    string = "123阿斯顿·马丁abc"
    print "in: %s" % string
    print "seperate out: %s" % str(test.convert(string=string))
    print "join out: %s" % test.convert(string=string, join=True)
