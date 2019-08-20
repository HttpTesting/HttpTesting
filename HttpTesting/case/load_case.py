import os
import unittest
import ddt
from httptesting.library.scripts import (load_case_data, get_run_flag)
from httptesting.library import HTMLTESTRunnerCN
from httptesting.library.http import HttpWebRequest
from httptesting.library.case import exec_test_case
from httptesting.globalVar import gl
from httptesting.library.emailstmp import EmailClass
from httptesting.library.case_queue import case_exec_queue

#########################################
#单个文件Debug时启用
# case_exec_queue.put("POS_INFO.yaml")
########################################3

'''
Use the python unittest framework.
'''
@ddt.ddt
class TestCaseExec(unittest.TestCase):
    """
        Use the python unittest framework.
        usage:
            test_case(data)
        return:
            There is no.
    """
    @classmethod
    def setUpClass(cls):
        cls.__name__ = "接口测试用例集"

    @classmethod
    def tearDownClass(self):
        pass

    @ddt.data(*load_case_data())
    def test_case(self, data):
        # Test method description
        self._testMethodName = data[0]['Desc']
        # self._testMethodDoc = data[0]['Desc']


        #Execution the YAML test case.
        exec_test_case(self, data)
        



if __name__=="__main__":


    suite = unittest.TestSuite()
    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCaseExec)]
    suite.addTests(tests)

    #输出report.html路径
    print(gl.reportFile)

    with open(gl.reportFile, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title= '接口自动化测试报告',
            description= '详细测试用例结果',  # 不传默认为空
            tester= "微生活－测试组"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)

    # email = EmailClass()
    # email.send(gl.reportFile)


