#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created Date: June 19. 2020
Copyright: UNMANNED SOLUTION
Author: Dae Jong Jin 
Description: Can Logger Class
'''
import logging
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = '{}/log'.format(current_dir)
# FILE_NAME = '{}/log'.format(current_dir)

class Logger():
    
    def __init__(self, logdir,logname='umd_can', level=logging.DEBUG):
        self.log_dir = logdir
        self.__filename = self.log_dir + os.sep + "my.log"
        self.checkDir()

        self.logger = logging.getLogger(logname)
        self.logger.setLevel(level)
        self.handler()

    def handler(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(self.__filename)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def checkDir(self,):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            print("make log file")


if __name__ == "__main__":
    log = Logger(log_dir)
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    # log.error('error')

            

