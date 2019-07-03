import unittest
import shutil
import os,time,json
import logging
from HttpTesting.globalVar import gl
from HttpTesting.library import HTMLTESTRunnerCN
from HttpTesting.library import scripts
from HttpTesting.library.scripts import get_yaml_field
from HttpTesting.library.emailstmp import EmailClass
from HttpTesting.library.case_queue import case_exec_queue
from HttpTesting import case
from HttpTesting.library.falsework import create_falsework
import argparse


########################################################################
#命令行模式
def run_min():

    #为了命令行执行取命令行路径
    cur_dir= os.getcwd()
    os.chdir(cur_dir)

    parse = argparse.ArgumentParser("执行测试用例......")
    parse.add_argument("--file", default='')
    parse.add_argument("--dir", default=gl.testCasePath)
    parse.add_argument("--startproject", default='')

    args = parse.parse_args()
    case_file = args.file
    case_dir = args.dir
    start_project = args.startproject

    if start_project !='':
        create_falsework(os.path.join(os.getcwd(), start_project))
    else:
        #获取case yam文件名写入执行队列
        if case_file == '':
            for root, dirs, files in os.walk(case_dir):
                for f in files:
                    if 'yaml' in f:
                        case_exec_queue.put(os.path.join(case_dir, f))
        else:
            case_exec_queue.put(case_file)

        #调用开始
        Run_Test_Case.invoke()


#########################################################################
# 命令行模式下，不指写--dir参数；默认为testcase目录
# 指定路径必须是绝对路径
######示例##########
# python3 main.py --dir=r"D:\test_project\project\cloud_fi_v2\testcase"
#########################################################################

class Run_Test_Case(object):

    @classmethod
    def load_tests_list(cls, to):
        """
        指定加载测试用例顺序
        :return:
        """
        tests = [unittest.TestLoader().loadTestsFromModule(to)]

        return tests

    @classmethod
    def create_report_file(cls):
        #测试报告文件名
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        report_dir = time_str.split('_')[0]
        cls.file_name = 'Report_{}.html'.format(time_str)
        portdir = os.path.join(gl.reportPath, report_dir)

        #按日期创建测试报告文件夹
        if not os.path.exists(portdir):
            os.mkdir(os.path.join(gl.reportPath,report_dir))
        rpath = os.path.join(gl.reportPath, report_dir)
        cls.filePath = os.path.join(rpath, cls.file_name)  # 确定生成报告的路径

        return cls.filePath

    @staticmethod
    def copy_report(filePath, file_name):
        #复制report下子文件夹到 templates/report/下
        split_path = os.path.dirname(filePath).split("\\")
        low_path = split_path[split_path.__len__() - 1]
        web_path = os.path.join(gl.templatesReportPath, low_path)
        if not os.path.exists(web_path):
            shutil.copytree(os.path.dirname(filePath), web_path)
        else:
            shutil.copy(filePath, os.path.join(web_path, file_name))
        return low_path

    @staticmethod
    def tmpl_msg(low_path, file_name):
        # 发送钉钉模版测试结果
        result_str = """共{}个用例, 通过{}, 失败{}, 错误{}, 通过率{}""".format(
            gl.get_value('sum'),
            gl.get_value('passed'),
            gl.get_value('failed'),
            gl.get_value('error'),
            gl.get_value('passrate')
        )

        # 测试结论
        if '100' in str(gl.get_value('passrate')):
            msg_1 = '本次测试★通过★'
        else:
            msg_1 = '本次测试★不通过★'

        #report外网发布地址ip+port
        report_url = get_yaml_field(gl.configFile)['REPORT_URL']

        # 发送钉钉消息
        msg = """接口自动化测试已完成:{},{}\n测试报告地址:{}/report/{}/{}"""
        msg = msg.format(result_str, msg_1, report_url, low_path, file_name)

        return msg

    @staticmethod
    def run(filePath):
        """
        去行unittest并生成报告
        :param filePath: report.html绝对路径
        :return: 无
        """
        
        #加载unittest框架，必须写在此处否则会先加载ddt
        from HttpTesting.case import load_case

        # unittest测试套件
        suite = unittest.TestSuite()
        suite.addTests(Run_Test_Case.load_tests_list(load_case))

        # 执行测试并生成测试报告文件
        with open(filePath, 'wb') as fp:
            runner = HTMLTESTRunnerCN.HTMLTestRunner(
                stream=fp,
                title= '接口自动化测试报告',
                description= '详细测试用例结果',  # 不传默认为空
                tester= "测试组"  # 测试人员名字，不传默认为小强
            )
            # 运行测试用例
            runner.run(suite)



    @staticmethod
    def invoke():
        """
        开始执行测试生成测试报告
        :return:
        """
        ##########################读取配置信息##################################
        config  = get_yaml_field(gl.configFile)
        dd_enable = config['ENABLE_DDING']
        dd_token = config['DD_TOKEN']
        dd_url = config['DING_URL']

        email_enable = config['EMAIL_ENABLE']
        ########################################################################

        # 测试报告文件名
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        filePath = Run_Test_Case.create_report_file()
        print(filePath)

        # 开始测试发送钉钉消息
        if dd_enable:
            scripts.send_msg_dding('{}:★开始API接口自动化测试★'.format(time_str),  dd_url, dd_token)

        # 执行测试并生成测试报告文件
        Run_Test_Case.run(filePath)

        # 复制report下子文件夹到 templates/report/下
        low_path = Run_Test_Case.copy_report(filePath, Run_Test_Case.file_name)

        if dd_enable:
            # 模版消息
            msg = Run_Test_Case.tmpl_msg(low_path, Run_Test_Case.file_name)
            print(msg)
            scripts.send_msg_dding(msg, dd_url, dd_token)

        if email_enable:
            # 发送测试报告To Email
            email = EmailClass()
            email.send(filePath)


# if __name__=="__main__":
#     run_min()
