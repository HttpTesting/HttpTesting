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
from web.sett.urls import Custom_Urls
import argparse
# from HttpTesting.library.scripts import get_yaml_field
# from HttpTesting.globalVar import gl

#############################################
#Flask实例
app = Flask(__name__)
##############################################

##############################################
#urls自定义路由
Custom_Urls.urls_route(app)
##############################################

_HOST = '127.0.0.1'
_PORT = '5002'

parse = argparse.ArgumentParser(description='Start the service.')
parse.add_argument(
    "--host", 
    default= _HOST, 
    help='The host address; The default is 127.0.0.1'
    )
parse.add_argument(
    "--port", 
    default= _PORT, 
    help='The port number; The default is 5002.'
    )
parse.add_argument(
    "--debug", 
    default=False,
    help='Web service debug mode.'
    )

args = parse.parse_args()
host = args.host
port = args.port
debug = args.debug




if __name__ == "__main__":
#     #########################################
#     # 启动web service服务
    app.run(host=host, port=port ,debug=debug)
#     # app.run(host='172.17.240.230', port=port ,debug=debug)

#     #########################################