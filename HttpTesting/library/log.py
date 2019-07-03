#_*_coding:utf-8_*_
import logging
import logging.config
import time
from HttpTesting.globalVar import gl
import os

class LogDebug(object):
    #log配置
    log_filename = os.path.join(gl.reportPath,"logging.log")
    logging.basicConfig(level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a',
        filename=log_filename
                        )

    #信息
    def info(self,msg):
        logging.info(msg)

    #错误
    def error(self,msg):
        logging.error(msg)

    #警告
    def warning(self,msg):
        logging.warning(msg)


if __name__=="__main__":
    LogDebug().info('这是一个测试log....')
    print LogDebug().log_filename


