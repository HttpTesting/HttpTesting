[打包]
python3 setup.py bdist_wheel

[上传PYPI]
twine upload dist/*


[测试用例]

包路径testScenario\testScenarioCase.py ;此文件用于unittest框架，执行测试用例
读取用例来源于，场景：data\Scenario ，单接口:data\TCode*

[执行]

唯一入口main.py,此文件执行所有用例，包含单接口和场景用例*

[用例格式]


   #字段功能说明:
  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
  - 
       Desc: 用例描述
  -
      #获取token
      Url: Url相对路径
      Method: 请求方法GET或POST  
      Data: 请求要传入的参数dict或json类型
         id: "b9b0e8e985a911e894a01c3947952e7e"
         secret: "71ee217e2f1bdfcc"
      InPara: "" 接口入参，没有入参填空
      OutPara: 接口出参字段
          ${H_token}$: res['data']
      Assert: 断言 
          "self.assertEquals(res['status'], 'success', res['status'])" 
  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   *


示例：
NAME: POS日报表
POS_INFO:
Case2: #用例1
    -
        Desc: 获取Token-POS门店信息-POS消费项目-POS收入项目-POS日报表
    -
        #获取token
        Url: /cloudfi/token/generatetoke
        Method: GET
        Data: 
            id: "b9b0e8e985a911e894a01c3947952e7e"
            secret: "71ee217e2f1bdfcc"
        InPara: ""
        OutPara: 
            ${H_token}$: res['data']
        Assert: "self.assertEquals(res['status'], 'success', res['status'])"
    -
        #POS门店信息
        Url: /cloudfi/api/store/batchhandle/store
        Method: POST
        Data: 
            -
                transactionid: "555"
                number: "555"
                name: 门店1
                profitcenterid: ""
        InPara: ${H_token}$
        OutPara: ""
        Assert: "self.assertEquals(res['status'], 'success', res['message'])"
    -
        #POS消费项目
        Url: /cloudfi/api/store/batchhandle/paytype
        Method: POST
        Data: 
            -
                transactionid: "566"
                number: "566"
                name: "门店1"
                type: "收银"
                typename: ""
        InPara: ${H_token}$
        OutPara: ""
        Assert: "self.assertEquals(res['status'], 'success', res['message'])"
    -
        #POS收入项目
        Url: /cloudfi/api/store/batchhandle/incometype
        Method: POST
        Data: 
            -
                transactionid: "577"
                number: "577"
                name: "收入项目1"
        InPara: ${H_token}$
        OutPara: ""
        Assert: "self.assertEquals(res['status'], 'success', res['message'])"
    -
        #POS日报表
        Url: /cloudfi/api/store/batchhandle/busidaily
        Method: POST
        Data: 
            -
                transactionid: "588"
                number: "588"
                busidate: "2019-6-14"
                incomeamount: 6000
                payamount: 7000
                storeid: 555
                fullincome: 5000
                discount: 0
                busidailyentrys:
                    - 
                        paytypeid: ""
                        incometypeid: "566"
                        amount: 888
                        netamount: 999
                        type: "default"
                    -
                        paytypeid: ""
                        incometypeid: "577"
                        amount: 888
                        netamount: 999
                        type: "default"
        InPara: ${H_token}$
        OutPara: ""
        Assert: "self.assertEquals(res['status'], 'success', res['message'])"
[测试报告]

文件夹report\report.html*

[全局路径]
文件夹globalVar\gl.py
[框架配置]

文件夹config*

[调用示例]
有两种用例编写方法，1.数据驱动，传参；2.部分数据驱动加调用传参
示例1：
import os
import unittest
import ddt
from library.scripts import load_ddt_data
from library import HTMLTESTRunnerCN
from library.http import HttpWebRequest
from library.case import exec_test_case
from globalVar import gl
'''
天子星－云财务接口场景
'''
@ddt.ddt
class TestScenario(unittest.TestCase):
'''天子星－云财务接口场景'''
def setUp(self):
    pass


@ddt.data(*load_ddt_data(Itype='s',filename='demo.yaml',caseflag='POS_INFO'))
def testPosInfo(self, data):
    '''POS信息:获取Token-POS门店信息-POS消费项目-POS收入项目-POS日报表'''
    exec_test_case(self, data)
if name=="main":
suite = unittest.TestSuite()
tests = [unittest.TestLoader().loadTestsFromTestCase(TestScenario)]
suite.addTests(tests)

filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
print(filePath)

with open(filePath, 'wb') as fp:
    runner = HTMLTESTRunnerCN.HTMLTestRunner(
        stream=fp,
        title=u'接口自动化测试报告',
        description=u'详细测试用例结果',  # 不传默认为空
        tester=u"yhleng"  # 测试人员名字，不传默认为小强
    )
    # 运行测试用例
    runner.run(suite)
示例2：
import os
import unittest
import ddt
from library.scripts import load_ddt_data
from library import HTMLTESTRunnerCN
from library.http import HttpWebRequest
from library.case import exec_test_case
from globalVar import gl
'''
天子星－云财务接口场景
'''
@ddt.ddt
class TestScenario(unittest.TestCase):
'''天子星－云财务接口场景'''
def setUp(self):
    pass


@ddt.data(*load_ddt_data(Itype='s',filename='POS_INFO.yaml',caseflag='POS_INFO'))
def testPosInfo(self, data):
    '''POS信息:获取Token-POS门店信息-POS消费项目-POS收入项目-POS日报表'''
    ###实例化http请求类###
    req = HttpWebRequest()

    '''--------------------------获取token信息----------------------'''
    res = req.get(params=data['TokenData'], desc=data['Desc'], gurl=data['TokenUrl'])
    token = res['data']
    self.assertEquals(res['status'], 'success', res['status'])

    '''--------------------------POS获取门店信息----------------------'''  
    req.headers['token'] = token
    res = req.post(data=data['StoreData'], desc=data['Desc'], gurl=data['StoreUrl'])
    self.assertEquals(res['status'], 'success', res['message'])

    '''--------------------------POS获取消费项目----------------------'''  
    req.headers['token'] = token
    res = req.post(data=data['PayData'], desc=data['Desc'], gurl=data['PayTypeUrl'])
    self.assertEquals(res['status'], 'success', res['message'])

    '''--------------------------POS获取收入项目----------------------'''  
    req.headers['token'] = token
    res = req.post(data=data['IncomeData'], desc=data['Desc'], gurl=data['IncomeUrl'])
    self.assertEquals(res['status'], 'success', res['message'])

    '''--------------------------POS获取日报表----------------------'''  
    req.headers['token'] = token
    res = req.post(data=data['BusData'], desc=data['Desc'], gurl=data['BusidailyUrl'])
    self.assertEquals(res['status'], 'success', res['message'])