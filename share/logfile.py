#coding:utf-8
__author__ = 'Administrator'

import logging
import logging.handlers
import os
import sys

app_path=""
if getattr(sys,'frozen',False):
    app_path=os.path.dirname(sys.executable) #sys.executable：python.exe所在目录
else:
    app_path=os.path.abspath('.')
file="temp/error.log"
log_filename=os.path.join(app_path,file)
handler=logging.handlers.RotatingFileHandler(log_filename,maxBytes=1024*1024,backupCount=3) #实例化handler
format_log='%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
formatter=logging.Formatter(format_log) #实例化formatter
handler.setFormatter(formatter) #为handler添加formatter

logger=logging.getLogger() #获取logger
logger.addHandler(handler) #为logger添加handler
logger.setLevel(logging.ERROR)   #CRITICAL、ERROR、WARNING、INFO、DEBUG、NOTSET
