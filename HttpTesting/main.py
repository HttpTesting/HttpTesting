# ########################################################
# 将根目录加入sys.path中,解决命令行找不到包的问题
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.insert(0, rootPath)
# ########################################################

import unittest
import shutil
import time,json
import logging
from httptesting.globalVar import gl
from httptesting.library import HTMLTESTRunnerCN
from httptesting.library import scripts
from httptesting.library.scripts import (get_yaml_field)
from httptesting.library.emailstmp import EmailClass
from httptesting.library.case_queue import case_exec_queue
from httptesting import case
from httptesting.library.falsework import create_falsework
from httptesting.library.har import ConvertHarToYAML
from httptesting import __version__
import argparse


########################################################################
cmd_path = ''
# Command line mode.
def run_min():

    # Takes the current path of the command line
    cur_dir = os.getcwd()
    os.chdir(cur_dir)

    parse = argparse.ArgumentParser(
        description='httptesting parameters', 
        prog='httptesting'
        )
    parse.add_argument(
        "-v",
        "--version",
        action='version',
        version="%(prog)s {}".format(__version__),
        help='Framework version.'
        )
    parse.add_argument(
        "-f",
        "--file", 
        default='', 
        help='The file path; File absolute or relative path.'
        )
    parse.add_argument(
        "-d",
        "--dir", 
        default='',
        help='The folder path; folder absolute or relative path.'
        )
    parse.add_argument(
        "-sp",
        "--startproject", 
        default='',
        help='Generate test case templates.'
        )
    parse.add_argument(
        "-conf",
        "--config", 
        default='',
        help='Basic setting of framework.'
        )
    parse.add_argument(
        "-har", 
        default='',
        help='Convert the har files to YAML. har file is *.har'
        )
    parse.add_argument(
        "-c",
        "--convert", 
        default='',
        help='Convert the har files to YAML. YAML file is *.yaml'
        )

    args = parse.parse_args()
    case_file = args.file
    case_dir = args.dir
    start_project = args.startproject
    config = args.config
    har = args.har
    vert = args.convert

    # Conver YAML.
    if vert:
        yamlfile = os.path.join(cur_dir, str(vert).strip())
        scripts.generate_case_tmpl(yamlfile)


    # Convert har files to YAML.
    # r'D:\httphar.har'
    if har:
        temp_dict = ConvertHarToYAML.convert_har_to_ht(har)
        ConvertHarToYAML.write_case_to_yaml('', temp_dict)

    # Setting global var.
    if config == 'set':
        try:
            os.system(gl.configFile)
        except (KeyboardInterrupt, SystemExit):
            print("已终止执行.")

    if start_project:
        create_falsework(os.path.join(os.getcwd(), start_project))

    # Get the yaml file name and write to the queue.
    if case_file:
        case_exec_queue.put(case_file)
        # Began to call.
        Run_Test_Case.invoke()

    if case_dir:
        for root, dirs, files in os.walk(case_dir):
            for f in files:
                if 'yaml' in f:
                    case_exec_queue.put(os.path.join(case_dir, f))
        # Began to call.
        Run_Test_Case.invoke()


#########################################################################
# Not in command mode --dir defaults to the testcase directory.
# Example:
# python3 main.py --dir=r"D:\test_project\project\cloud_fi_v2\testcase"
#########################################################################

class Run_Test_Case(object):

    @classmethod
    def load_tests_list(cls, to):
        """
        Specifies the order in which test cases are loaded
        :return: There is no.
        """
        tests = [unittest.TestLoader().loadTestsFromModule(to)]

        return tests

    @classmethod
    def create_report_file(cls):
        # 测试报告文件名
        report_dir = time.strftime('%Y%m%d_%H%M%S', time.localtime())

        rdir = os.path.join(os.getcwd() ,'report')

        cls.file_name = 'report.html'
        portdir = os.path.join(rdir, report_dir)

        # 按日期创建测试报告文件夹
        if not os.path.exists(portdir):
            # os.mkdir(portdir)
            os.makedirs(portdir)

        cls.filePath = os.path.join(portdir, cls.file_name)  # 确定生成报告的路径

        return cls.filePath


    @staticmethod
    def copy_custom_function():
        # 自定义函数功能
        func = os.path.join(os.getcwd(), 'extfunc.py')
        target = os.path.join(gl.loadcasePath, 'extfunc.py')

        if os.path.exists(func):
            shutil.copy(func, target)   


    @staticmethod
    def copy_report(filePath, file_name):
        # 复制report下子文件夹到 templates/report/下
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

        config = get_yaml_field(gl.configFile)
        # report外网发布地址ip+port
        report_url = config['REPORT_URL']
        content = config['DING_TITLE']
        # 发送钉钉消息
        msg = """{}已完成:{},{}\n测试报告地址:{}/{}/{}"""
        msg = msg.format(content, result_str, msg_1, report_url, low_path, file_name)

        return msg

    @staticmethod
    def run(filePath):
        """
        Execute the test and generate the test report file.
        :param filePath: Report file absolute path.
        :return: There is no.
        """
        # custom function
        Run_Test_Case.copy_custom_function()

        # Load the unittest framework, which must be written here or DDT will be loaded first.
        from httptesting.case import load_case

        # Unittest test suite.
        suite = unittest.TestSuite()
        suite.addTests(Run_Test_Case.load_tests_list(load_case))

        # Execute the test and generate the test report file.
        with open(filePath, 'wb') as fp:
            runner = HTMLTESTRunnerCN.HTMLTestRunner(
                stream=fp,
                title= '接口自动化测试报告',
                description= '详细测试用例结果',  # Do not default to null.
                tester= "测试组",  # tester name ,not default to jack.
                verbosity=2
            )
            # Run the test case.
            runner.run(suite)

    @staticmethod
    def invoke():
        """
        Start executing tests generate test reports.
        :return: There is no.
        """
        # #########################Read configuration information###############
        config = get_yaml_field(gl.configFile)
        dd_enable = config['ENABLE_DDING']
        dd_token = config['DD_TOKEN']
        dd_url = config['DING_URL']
        email_enable = config['EMAIL_ENABLE']
        ########################################################################

        # Test report file name.
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        filePath = Run_Test_Case.create_report_file()

        # Start test the send pin message.
        if dd_enable:
            scripts.send_msg_dding(
                '{}:★开始API接口自动化测试★'.format(time_str),
                dd_token,
                dd_url
            )

        # Execute the test and send the test report.
        Run_Test_Case.run(filePath)

        print(filePath)
        # Copy the folder under the report directory under  /templates/report/
        # low_path = Run_Test_Case.copy_report(filePath, Run_Test_Case.file_name)

        if dd_enable:
            # Template message.
            dir_list = filePath.split('\\')
            low_path = dir_list[len(dir_list) - 2]
            msg = Run_Test_Case.tmpl_msg(low_path, Run_Test_Case.file_name)
            print(msg)
            scripts.send_msg_dding(msg, dd_token, dd_url)

        if email_enable:
            # Send test report to EMAIL.
            email = EmailClass()
            email.send(filePath)


if __name__ == "__main__":
    run_min()
