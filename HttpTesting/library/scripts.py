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
    :Desc: 
        load DDT data form YAML.
    :param flag:  
        The starting node of the interface case in YAML.
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

    :return: [] DDT data list
    """
    ddtData = []

    for _ in range(0, case_exec_queue.qsize()):
        if not case_exec_queue.empty():
            case_name = case_exec_queue.get()

            #Read the case
            readYam = get_yaml_field(case_name)
            #yaml start the node，The default is TEST_CASE.
            dictCase = readYam[flag]

            #Loop through the configuration data under the node, 
            # so case begins the use case
            for key in dictCase:
                #What begins with a case in configuration data is considered a use case.
                if str(key).lower().startswith('case'):

                    #Organize DDT [] data, and each case is a dict object
                    ddtData.append(dictCase[key])
        else:
            raise Exception("The CASE execution queue is empty.")
    return ddtData



def retry(**kw):
    """
    Decorator HTTP request error retry.
    :param arg: ()tuples，Exception class
    :param kw: reNum = n；N is the number of retries
    :return: The function itself
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
                print('Retry the {0} time'.format(n))
            return ret
        return _wrapper
    return wrapper



def rm_dirs_files(dirpath):
    """
    Delete folder and all files.
    :param dirpath: The target path
    :return: no
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
    Send the nail message text to the nail group.
    :param msg: Message text.
    :param token: Rebot token.
    :param url: Nail request url.
    :return: Response content
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


def get_sys_environ(name):
    """
    Gets the environment variable by name
    :param name: environment variable name
    :return:  Reverse an environment variable value
    """
    try:
        if name in os.environ:
            value = os.environ[name]
    except KeyError as ex:
        raise ex
    return value


if __name__=="__main__":
    env = get_sys_environ('HTTPTESTING_PWD')
