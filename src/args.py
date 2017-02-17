#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016 tangweimin All Rights Reserved
#
########################################################################

"""
The args module is for user input args parse.

File: args.py
Author: tangweimin
Date: 2016/12/12:

"""
import sys
import log
import docopt

class arg(object):
    """ 
        Usage:
            mini_spider.py -h | -help
            mini_spider.py -v | -version
            mini_spider.py [-d] [-s] [-c] [-r] [-a DT]
        
        
        Options:
            -h --help      Show this screen
            -v --version   Show version
            -d             run in deamon mode, default is not.
            -s             skip the community crawle.
            -c             continue crawle not finished.
            -r             reset db(dangerous!!!),  default is not.
            -a DT          after date DT.
    """
    __ins = None
    __argv = None
    __log = log.log('args')

    def __new__(cls, *args, **kw):
        if cls.__ins is None:
            cls.__ins = super(arg,cls).__new__(cls)
            cls.__argv = docopt.docopt(cls.__doc__, argv = sys.argv[1:] ,version="soup spider for lianjia 0.2")

            cls.__log.info('arg: run in demon: %s',cls.__ins.d)
            cls.__log.info('arg: skip the community crawl: %s',cls.__ins.s)
            cls.__log.info('arg: continue crawl: %s',cls.__ins.c)
            cls.__log.info('arg: reset db: %s',cls.__ins.r)

            if cls.__ins.r and 'y' != raw_input('r u sure to reset DB ?!  y/n  '):
                cls.__argv['-r'] = False
                cls.__log.warning('arg: reset db: change to False!')

        return cls.__ins


    def __getattr__(self, key):
        key = '-'+key
        if self.__argv.has_key(key):
            return self.__argv[key]
        else:
            return key + ' is invalid key!!!';

    def dump(self):
        print self.__argv



if __name__ == '__main__':
    a = arg()
    print a.dump()
    print a.ttt
    print a.d
    print a.abc
    print a.r
    print a.c
    print a.s
    print a.a
    print id(a)

    # b = arg()
    # print b.dump()
    # print b.ttt
    # print b.d
    # print b.abc
    # print b.r
    # print b.c
    # print b.s
    # print id(b)

    # print a.dump()
    # print b.dump()

