#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
# 
########################################################################

"""
This module provide the logger setting initialize.

File: log.py
Author: tangweimin
Date: 2016/8/12
"""

import os
import sys
import logging
import logging.handlers


class log():
    """
    """
    _inited = False
    _logers = []

    @staticmethod
    def RootInit(fmt = "%(name)s/%(levelname)s/%(asctime)s/%(filename)s/%(lineno)d/%(thread)d: %(message)s"):
        '''
        init root log handlers
        '''
        try:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
    
            fmtr = logging.Formatter(fmt)
    
            shdlr = logging.StreamHandler()
            shdlr.setLevel(logging.DEBUG)
            shdlr.setFormatter(fmtr)
            logger.addHandler(shdlr)
    
            wfhdlr = logging.handlers.TimedRotatingFileHandler( "../log/main.warning+.log", when='D',backupCount=7)
            wfhdlr.setLevel(logging.WARNING)
            wfhdlr.setFormatter(fmtr)
            logger.addHandler(wfhdlr)

            efhdlr = logging.handlers.TimedRotatingFileHandler( "../log/main.error+.log", when='D',backupCount=7)
            efhdlr.setLevel(logging.ERROR)
            efhdlr.setFormatter(fmtr)
            logger.addHandler(efhdlr)

        except IOError as e:
            logger.error("open log file error : %s" % e)
            return False

        log._inited = True
        return True


    def __init__(self, name, level=logging.DEBUG,
             format="%(levelname)s /%(asctime)s/%(filename)s/%(lineno)d: %(message)s"):

        if name in log._logers:
            print 'duplitecate loger!!!'
            sys.exit()

        log._logers.append(name)

        if log._inited == False:
            log.RootInit()

        fmtr = logging.Formatter(format)
        
        hdlr = logging.FileHandler('../log/'+ name+'.log')
        hdlr.setLevel(level)
        hdlr.setFormatter(fmtr)

        self._logger = logging.getLogger(name)
        self._logger.addHandler(hdlr)

        self._func = {
        'debug': self._logger.debug , 
        'info': self._logger.info ,
        'warning': self._logger.warning ,
        'error': self._logger.error ,
        'critical': self._logger.critical }

    def __getattr__(self, key):
        '''
        get log function.
        '''
        if self._func.has_key(key):
            return self._func[key]
        else:
            print key + ' is invalid key for log!!!'
            sys.exit()

    def __str__(self):
        return  'I am a logger obj(%s) in str' %  ','.join(log._logers)

    def __repr__(self):
        return  'I am a logger obj(%s) in repr' %  ','.join(log._logers)

    def __unicode__(self):
        return  'I am a logger obj(%s) in unicode' %  ','.join(log._logers)




if __name__ == '__main__':
    import master

    a = log('alpha')
    b = log('beta')

    mgr = master.MasterP()

    if mgr.is_worker():
        c = log('cccc')
        d = log('dddd')

        c.debug('c.debug')
        d.debug('d.debug')

        c.info('c.info')
        d.info('d.info')

        c.warning('c.warning')
        d.warning('d.warning')

        c.error('c.error')
        d.error('d.error')

        c.critical('c.critical')
        d.critical('d.critical')
    else:
        a.debug('a.debug')
        b.debug('b.debug')

        a.info('a.info')
        b.info('b.info')

        a.warning('a.warning')
        b.warning('b.warning')

        a.error('a.error')
        b.error('b.error')

        a.critical('a.critical')
        b.critical('b.critical')

