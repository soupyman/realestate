#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2016
#
########################################################################

"""
The spider module master process.

File: master.py
Author: soup
Date: 2016/12/12 :


#defineSIGHUP
1/* hangup */
#defineSIGINT
2/* interrupt */
#defineSIGQUIT
3/* quit */
#defineSIGILL
4/* illegal instruction (not reset when caught) */
#defineSIGTRAP
5/* trace trap (not reset when caught) */
#defineSIGABRT
6/* abort() */
#if  (defined(_POSIX_C_SOURCE) && !defined(_DARWIN_C_SOURCE))
#defineSIGPOLL
7/* pollable event ([XSR] generated, not supported) */
#else/* (!_POSIX_C_SOURCE || _DARWIN_C_SOURCE) */
#defineSIGIOT
SIGABRT/* compatibility */
#defineSIGEMT
7/* EMT instruction */
#endif/* (!_POSIX_C_SOURCE || _DARWIN_C_SOURCE) */
#defineSIGFPE
8/* floating point exception */
#defineSIGKILL
9/* kill (cannot be caught or ignored) */
#defineSIGBUS
10/* bus error */
#defineSIGSEGV
11/* segmentation violation */
#defineSIGSYS
12/* bad argument to system call */
#defineSIGPIPE
13/* write on a pipe with no one to read it */
#defineSIGALRM
14/* alarm clock */
#defineSIGTERM
15/* software termination signal from kill */
#defineSIGURG
16/* urgent condition on IO channel */
#defineSIGSTOP
17/* sendable stop signal not from tty */
#defineSIGTSTP
18/* stop signal from tty */
#defineSIGCONT
19/* continue a stopped process */
#defineSIGCHLD
20/* to parent on child stop or exit */
#defineSIGTTIN
21/* to readers pgrp upon background tty read */
#defineSIGTTOU
22/* like TTIN for output if (tp->t_local&LTOSTOP) */
#if  (!defined(_POSIX_C_SOURCE) || defined(_DARWIN_C_SOURCE))
#defineSIGIO
23/* input/output possible signal */
#endif
#defineSIGXCPU
24/* exceeded CPU time limit */
#defineSIGXFSZ
25/* exceeded file size limit */
#defineSIGVTALRM 26
/* virtual time alarm */
#defineSIGPROF
27/* profiling time alarm */
#if  (!defined(_POSIX_C_SOURCE) || defined(_DARWIN_C_SOURCE))
#define SIGWINCH 28/* window size changes */
#define SIGINFO29
/* information request */
#endif
#define SIGUSR1 30/* user defined signal 1 */
#define SIGUSR2 31/* user defined signal 2 */

"""

import os
import sys
# import logging
import signal
import log
import args

class MasterP(object):
    """
    the MasterP class is a concurrent process manage the spider.
    which may waits for a signal to kill the spider that contains the 
    threads.
    """
    _log = log.log('master')

    def __init__(self):
        """ 
        creates a child process, which returns.  the parent 
        process manage the spider which may waits for a 
        KeyboardInterrupt and then kills 
        the child process using child pid.
        """
        deamon = args.arg().d

        try:
            self._child = os.fork()
        except OSError:
            sys.exit("Unable to create new process.")

        if self._child == 0: 
            # new process
            MasterP._log.debug( 'new process runing...')
            return
        else:
            if deamon == True:
                self._run_in_deamon(self._child)
            else:
                self._wait_interrupt()


    def is_worker(self):
        '''
        check if current process is manager process or worker process
        '''
        if self._child == 0:
            return True
        else:
            return False

    def _run_in_deamon(self, pid):
        """ 
        print the information and return.
        """
        MasterP._log.info( 'if u want exit the spider:')
        MasterP._log.info(  'kill -9/SIGKILL %d', pid )



    def _wait_interrupt(self):
        """ 
        wait for KeyboardInterrupt signal to kill the child process.
        """
        MasterP._log.info( 'if u want exit ctrl-c ')
        try:
            os.wait()
        except KeyboardInterrupt:
            MasterP._log.warning("user ctrl-c interrupt to system exit process %d.", self._child)
            os.kill(self._child, signal.SIGKILL)
        sys.exit()


if __name__ == '__main__':
    import threading
    mgr = MasterP()

    def test_thread(p,t):
        loger = log.log(p+t)
        loger.info('%s:%s work doing...'%(p,t))

    if mgr.is_worker():
        threads1 = []
        t1 = threading.Thread(target=test_thread,args=('worker', '1'))
        threads1.append(t1)
        t2 = threading.Thread(target=test_thread,args=('worker','2'))
        threads1.append(t2)
        t3 = threading.Thread(target=test_thread,args=('worker','3'))
        threads1.append(t3)
        for t in threads1:
            t.start()
            t.join()

        MasterP._log.info("all worker finished.")

    else:
        threads2 = []
        t1 = threading.Thread(target=test_thread,args=('master', '1'))
        threads2.append(t1)
        t2 = threading.Thread(target=test_thread,args=('master','2'))
        threads2.append(t2)
        t3 = threading.Thread(target=test_thread,args=('master','3'))
        threads2.append(t3)
        for t in threads2:
            t.start()
            t.join()

        MasterP._log.info("all master finished.")

