#coding=utf-8

#########################################################
#将根目录加入sys.path中,解决命令行找不到包的问题
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
#########################################################

from flask import Flask
from sett.urls import Custom_Urls
import argparse


#############################################
#Flask实例
app = Flask("service")
##############################################

##############################################
#urls自定义路由
Custom_Urls.urls_route(app)
##############################################

parse = argparse.ArgumentParser("手动执行脚本......")
parse.add_argument("--host", default='127.0.0.1')
parse.add_argument("--port", default='5002')
parse.add_argument("--debug", default=False)

args = parse.parse_args()
host = args.host
port = args.port
debug = args.debug


if __name__ == "__main__":
    #########################################
    # 启动web service服务
    app.run(host=host, port=port ,debug=debug)
    # app.run(host='172.17.240.230', port=port ,debug=debug)

    #########################################