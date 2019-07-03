import time
import os
import random
from functools import wraps
import yaml,requests

from HttpTesting.globalVar import gl
from requests.exceptions import (ConnectTimeout,ConnectionError,Timeout,HTTPError)
from HttpTesting.library.case_queue import case_exec_queue


'''
#日期时间串
'''
def get_datetime_str():
    """
    随机字符串
    :return: 日期时间
    """
    time.sleep(0.5)
    datetime= str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    return datetime

@property
def get_timestamp_int():
    """
    秒级时间戳
    :return: 时间戳
    """
    return int(time.time())

'''
写yaml内容
'''
def write_ymal(path,data):
    """
    写yaml文件
    :param path: yaml文件路径
    :param data: 数据内容
    :return: 无
    """
    with open(path,'wb') as fp:
        yaml.dump(data,fp)


'''
读yaml文件
'''
def get_yaml_field(path):
    """
    获取yaml配置内容
    :param path: yaml文件路径
    :return: 返回字典所有内容
    """
    with open(path,'rb') as fp:
        cont = fp.read()

    ret = yaml.load(cont)
    return ret



#获取配置文件中,运行标记
def get_run_flag(skey):
    """
    获取配置文件中执行标记
    :param skey: 场景字段
    :return: 标记值;Y or N
    """
    yaml_dict = get_yaml_field(gl.exeConfigFile)
    ret_flag = yaml_dict['RUNING'][skey]['Flag']
    return ret_flag




def load_ddt_data(Itype='t', filename='Charge.yaml', caseflag='CHARGE_CASE1'):
    """
    从yaml加载ddt数据
    :param Itype: t:tcode; s:scenario
    :param filename: 'Charge.yaml'
    :param caseflag:  yaml中接口case的起始节点
    :return: ddt数据list
    """
    ddtData = []
    if Itype == 't':
        configDir = gl.tcodePath
    else:
        configDir = gl.dataScenarioPath

    #拼接yam数据路径，并读取数据内容
    yamPath = os.path.join(configDir, filename)
    readYam = get_yaml_field(yamPath)

    dictCase = readYam[caseflag]

    #循环遍历，配置数据中节点下，所以case开头用例
    for key in dictCase:
        #配置数据中以case开头的，被认为是一条用例
        if str(key).lower().startswith('case'):

            if Itype =='t':
                # 为每个case添加一个Url
                dictCase[key]['Url'] = dictCase['Url']

            #组织ddt[]数据，每一条case为一个dict对象
            ddtData.append(dictCase[key])

    return ddtData


def load_case_data(flag='TEST_CASE'):
    """
    :func 
        从yaml加载ddt数据
    :param flag:  
        yaml中接口case的起始节点
        default:
            TEST_CASE
    :import
        from HttpTesting.library.scripts import load_case_data
        or
        form HttpTesting.library import scripts
    :invoke
        load_case_data()
        or
        scripts.load_case_data()

    :return: ddt数据list
    """
    ddtData = []

    for _ in range(0, case_exec_queue.qsize()):
        if not case_exec_queue.empty():
            case_name = case_exec_queue.get()

            #读取case用例
            readYam = get_yaml_field(case_name)
            #yam开始节点，默认为TEST_CASE
            dictCase = readYam[flag]

            #循环遍历，配置数据中节点下，所以case开头用例
            for key in dictCase:
                #配置数据中以case开头的，被认为是一条用例
                if str(key).lower().startswith('case'):

                    #组织ddt[]数据，每一条case为一个dict对象
                    ddtData.append(dictCase[key])
        else:
            raise Exception("CASE执行队列为空.")
    return ddtData



def retry(**kw):
    """
    装饰器：http请求，出错重试功能
    :param arg: ()元组，异常类
    :param kw: reNum = n；n为重试次数
    :return: 函数本身
    """
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args,**kwargs):
            raise_ex = None
            for n in range(kw['reNum']):
                try:
                    ret = func(*args,**kwargs)
                    time.sleep(random.randint(1,3))
                    return ret
                except (ConnectTimeout,ConnectionError,Timeout,HTTPError) as ex:
                    raise_ex = ex
                print('重试第{0}次'.format(n))
            return ret
        return _wrapper
    return wrapper



def rm_dirs_files(dirpath):
    """
    删除目标,目录下文件及文件夹
    :param dirpath: 目标目录
    :return: 无
    """
    listdir = os.listdir(dirpath)
    if listdir:
        for f in listdir:
            filepath = os.path.join(dirpath,f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            if os.path.isdir(filepath):
                os.rmdir(filepath)


def send_msg_dding(msg, token, url=''):
    """
    发送消息到,钉钉群
    :param msg: 要发送到钉钉的消息文本
    :return: 响影内容
    """
    text = {
            "msgtype": "text", 
            "text": {
                "content": msg
            }, 
            # "at": {
            #     "isAtAll": True
            # }
        }
    url_str = "{}{}".format(url, token)

    res = requests.request("POST", url_str, json=text)
    return res.json()



# # multipart/form-data
# class MultipartFormData(object):
#     """multipart/form-data格式转化"""

#     @staticmethod
#     def to_form_data(data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW", headers={}):
#         """
#         form data
#         :param: data:  {"req":{"cno":"18990876","flag":"Y"},"ts":1,"sig":1,"v": 2.0}
#         :param: boundary: "----WebKitFormBoundary7MA4YWxkTrZu0gW"
#         :param: headers: 包含boundary的头信息；如果boundary与headers同时存在以headers为准
#         :return: str
#         :rtype: str
#         """
#         #从headers中提取boundary信息
#         if "content-type" in headers:
#             fd_val = str(headers["content-type"])
#             if "boundary" in fd_val:
#                 fd_val = fd_val.split(";")[1].strip()
#                 boundary = fd_val.split("=")[1].strip()
#             else:
#                 raise("multipart/form-data头信息错误，请检查content-type key是否包含boundary")
#         #form-data格式定式
#         jion_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'
#         end_str = "--{}--".format(boundary)
#         args_str = ""

#         if not isinstance(data, dict):
#             raise("multipart/form-data参数错误，data参数应为dict类型")
#         for key, value in data.items():
#             args_str = args_str + jion_str.format(boundary, key, value)
        
#         args_str = args_str + end_str.format(boundary)
#         args_str = args_str.replace("\'", "\"")
#         return args_str



if __name__=="__main__":
    msg = "测试机器人发送消息"
    token = "3ba50c804de8e286a95948fdbeb3e8b8177f4e32099643c98388c53adc36e3ed"
    res = send_msg_dding(msg, token)
    print(res)

