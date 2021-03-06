﻿# HttpTesting

![PyPI](https://img.shields.io/pypi/v/Httptesting)
![PyPI - License](https://img.shields.io/pypi/l/HttpTesting)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/HttpTesting)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/HttpTesting)


HttpTesting 是HTTP(S)协议接口测试框架，通过YAML来编写测试用例，通过命令行运行代码，不固定目录结构，支持通过命令行生成脚手架。


## 功能描述
httptesting通过YAML编写测试用例，安装httptesting后通过amt命令执行测试用例，支持指定YAML中CASE名称进行单用例执行，支持指定请求头默认值来共享请求头，支持自定义扩展功能(在case执行根目录下创建extfunc.py文件来自定义代码)。
支持多进程执行用例，支持用例执行出错重试功能，支持设定执行用例次数；支持设置控制台输出和报告输出；支持参数化功能与用户自定义用户变量。




## 版本信息

|序号|版本号|描述|
|:---|:---|:---| 
|1|v1.0|使用unittest框架|
|2|v1.1|使用pytest框架|




## 快速开始

### python虚拟环境virtualenv使用

- 安装虚拟环境: pip install virtualenv

- 创建虚拟环境: virtualenv  demo_env

- 命令行模式切换到虚拟环境Script目录: /../scripts/

- 激活虚拟环境: activate.bat 

### HttpTesting安装


#### pip在线安装

- pip install HttpTesting==1.0.26

#### 下载whl文件进行安装

- pip install HttpTesting-1.0.40-py3-none-any.whl 


#### 更新HttpTesting包

已安装HttpTesting包,通过pip命令进行更新

- pip list  查看HttpTesting安装包版本信息

- pip install --upgrade HttpTesting

- pip install --upgrade HttpTesting==1.0.26



### 命令

以下四个命令作用相同

- am 
- AM
- amt
- AMT

|序号|命令参数|描述|
|:---|:---|:---|  
|1|amt -conf set 或--config set|此命令用来设置config.yaml基本配置|
|2|amt -f template.yaml或--file template.yaml|执行YAML用例，支持绝对或相对路径|
|3|amt -d testcase或--dir testcase|批量执行testcase目录下的YAML用例，支持绝对路径或相对路径|
|4|amt -sp demo或--startproject demo|生成脚手架demo目录,以及用例模版|
|5|amt -har httphar.har|根据抓包工具导出的http har文件，生成测试用例YAML|
|6|amt -c demo.yaml或--convert demo.yaml|转换数据为HttpTesting测试用例|




#### 基本配置

- URL设置

- 钉钉机器人设置

- 测试报告设置

- EMAIL邮箱设置


#### 用例执行

- YAML执行: amt -file template.yaml

- YAML批量执行: amt -dir testcase



####  脚手架生成

- 脚手架功能,是生成一个测试用例模版.



#### HAR

har命令来解析, Charles抓包工具导出的http .har请求文件, 自动生成HttpTesting用例格式.





## 用例编写


### 用例模型

>TESTCASE{

>>'case1':['description',{},{}],  #场景模式每个{}一个接口

>>'case2':['description',{}],     #单接口模式

>}


### YAML用例格式  

### 场景模式
	TESTCASE:
		#Case1由两个请求组成的场景
		Case1:
			-
				Desc: xxxx业务场景(登录->编辑)
			-
				Desc: 登录接口
				Url: /login/login
				Method: GET
				Headers:
					content-type: "application/json"
					cache-control: "no-cache"
				Data:
					name: "test"
					pass: "test123"
				OutPara: 
					"H_token": result.data
					"content_type": header.content-type
					"name": Data.name 
					"pass": Data.pass
				Assert:
					- eq: [result.status, 'success']
			-
				Desc: 编辑接口
				Url: /user/edit
				Method: GET
				Headers:
					content-type: "${content_type}$"   
					cache-control: "no-cache"
					token: "$H_token$"
				Data:
					name: "${name}$"
					pass: "${pass}$"
				OutPara: 
					"$H_token$": result.data
				Assert:
					- ai: ['success', result.status]
					- eq: ['result.status', '修改成功']

### 多CASE模式

	TESTCASE:
		#同一接口,不同参数,扩充为多个CASE
		Case1:
			-
				Desc: 登录接口-正常登录功能
			-
				Desc: 登录接口
				Url: /login/login
				Method: GET
				Headers:
					content-type: "application/json"
					cache-control: "no-cache"
				Data:
					name: "test"
					pass: "test123"
				OutPara: 
					"H_cookie": cookie.SESSION
				Assert:
					- eq: [result.status, 'success']
		Case2:
			-
				Desc: 登录接口-错误密码
			-
				Desc: 登录接口
				Url: /login/login
				Method: GET
				Headers:
					content-type: "application/json"
					cache-control: "no-cache"
				Data:
					name: "test"
					pass: "test123"
				OutPara:
					"H_cookie": cookie.SESSION 
				Assert:
					- eq: [result.status, 'error']


### 参数说明

- "${H_token}$": 为参数变量,可以头信息里与Data数据里进行使用
- "%{md5('aaaa')}%": 为函数原型,具体支持函数下方表格可见.

### 自定义变量

变量作用域为当前CASE.

- 通过在Case下定义USER_VAR字段，来自定义变量
- USER_VAR字段下定义的字段为用户变量，作用于当前Case

### 示例1(自定义变量)

	TESTCASE: 
		Case1:
			- 
				Desc: 接口详细描述
				USER_VAR:
					token:  xxxxxxxx
			-
				Url: /xxxx/xxxx
				Method: POST
				Headers: 
					token: ${token}$
				Data:
				OutPara:
				Assert: []

### 示例2(自定义变量)

	TEST_CASE:
		Case1:
		-   
			Desc: 扫码校验券(支持检测微信券二维码码、微信会员h5券二维码、条码)
			USER_VAR:
				version: 1.0
				data: 
					req:
						sid: '1380598237'
						wxcode: "164073966187485312752286" #209736174428
					appid: dp0Rm4wNl6A7q6w1QzcZQstr
					sig: 9c8c96b38d759abe6633c124a5d37225
					v: "${version}$"
					ts: 1564643536
			
		-   Desc: 扫码校验券
			Url: /pos/checkcoupon
			Method: POST
			Headers:
				content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
				cache-control: no-cache
			Data: ${data}$
			OutPara: 
			Assert:
			-   eq: [result.errcode, 0]


- 以上通过USER_VAR字典对象来定义变量, key为变量名, value为变量值; 使用方法: ${token}$

- 无需定义变量, USER_VAR字段在用例中,可以省略.

#### OutPara字段变量使用

OutPara字段用来做公共变量,供其它接口使用,默认为""; 

-  示例: "H_token": result.data 是请求结果，返回的嵌套级别,使用方法: ${H_token}$
-  OutPara为dict类型,可以做多个公共变量.


#### Assert断言

Assert字段默认为[].

|序号|断言方法|断言描述|
|:---|:---|:---|
|1|eq: [a, b]|判断 a与b相等,否则fail|
|2|nq: [a, b]|判断 a与b不相等,否则fail|
|3|al: [a, b]|判断 a is b 相当于id(a) == id(b),否则fail|
|4|at: [a, b]|判断 a is not b 相当于id(a) != id(b)|
|5|ai: [a, b]|判断 a in b ,否则fail|
|6|ani: [a, b]|判断 a in not b,否则fail|
|7|ais: [a, b]|判断 isinstance(a, b) True|
|8|anis: [a, b]|判断 isinstance(a, b) False|
|9|ln: [a]|判断 a is None,否则fail|
|10|lnn: [a]|判断 a is not none|
|11|bt: [a]|判断 a 为True|
|12|bf: [a]|判断 a 为False|


#### 内置函数及扩展

使用原型(带参数与不带参数)

- "%{md5('aaaa')}%" 或 "%{timestamp()}%"



|函数名|参数|说明|
|:---|:---|:---|
|md5|txt字符串|生成md5字符串示例: cbfbf4ea6d7c8032584dcf0defa10276|
|timestamp|-|秒级时间戳示例: 1563183829|
|uuid1|-|生成唯一id,uuid1示例:ebcd6df8a77611e99bb588b111064583|
|datetimestr|-|生成日期时间串,示例:2019-07-16 10:50:16|
|mstimestamp|-|毫秒级时间戳,20位|
|sleep_time|-|线程睡眠,0.5为500毫秒，1为1秒|
|rnd_list|[]|随机从列表中选择值|

- 其它后续添加

### 自定义函数扩展功能说明
- 在执行用例root目录，新建extfunc.py文件
- 按模型自定义函数
- 类名 Extend不可更改
- @staticmethod函数必须定义为静态
- 函数各数不做限制

### 自定义函数扩展功能模型
	class Extend:
		@staticmethod
		def func1():
			return 'ext func'
		
		@staticmethod
		def func2(args):
			return args

- 使用示例1："%{func1()}%" 
- 使用示例2: "%{func1('aaaa')}%" 


### 参数化功能
定义参数化参数后，同一用例会按照参数个数决定用例执行次数。
- 通过在用例Case下定义PARAM_VAR字段
- PARAM_VAR字段下定义参数化变量，供之后引用
- 如果在PARAM_VAR下定义多个，参数化变量，参数个数要匹配。
- 现在如果定义了多个参数化变量，执行用例的次数是排列组合数。
- 之后如有必要会改成，按参数化变量内参数的各数决定执行用例次数。

### 参数化功能模型
	TEST_CASE:
		Case2:
		-   Desc: 给指定用户发送验证码
			USER_VAR:
				cno_list:
				- '1674921314241197'
				- '1581199496593872'
				- '1623770534820512'
				- '1674921701066628'
				- '1581199096195979'
				- '1623770606653991'
			PARAM_VAR: 
				sig: [1,2,3,4,5]

		-   Desc: 给指定用户发送验证码
			Url: /user/sendcode
			Method: POST
			Headers:
				content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
				cache-control: no-cache
			Data:
				req:
					cno: '%{rnd_list("${cno_list}$")}%'
				appid: dp1svA1gkNt8cQMkoIv7HmD1
				sig: "${sig}$"
				v: 2.0
				ts: 123
			OutPara: null
			Assert:
			-   eq:
				- result.errcode
				- 0
			-   eq:
				- result.res.result
				- SUCCESS


## 常用对象(通常做参数变量时使用)
- res: 请求Response对象
- result: res.json 或 res.text
- cookie: res.cookie 响应cookie字典对象;  当做为参数时如果cookie.SESSION这样的写法代表取cookie中的SESSION对象. 如果只写cookie,会解析成"SESSION=xxxxxxx; NAME=xxxxxx"
- headers: res.headers 响应头字典对象
- header: header.content-type 请求头对象


## 用例执行
- 1、生成脚手架
- 2、编写脚手架中testcase下YAML模版用例
- 3、切换到testcase目录
- 4、amt -dir testcase 自动运行testcase下YAML用例
- 5、自动生成测试报告Html


##  框架基本配置
- 1、通过命令打开框架config.yaml
- 2、amt -config set
- 3、修改基本配置，并保存


## 新增功能

### 指定case编号执行

- 指定单个Case执行 amt -f xxxx.yaml Case1
- 指定多个Case执行 amt -f xxxx.yaml Case1 Case2 Case3


### 请求头默认值
	TEST_CASE:
		Case1:
		-   Desc: 给用户发送验证码业务场景(发送1->发送2)
			USER_VAR:
				cno_list:
				- '1674921314241197'
				- '1581199496593872'
				- '1623770534820512'
				- '1674921701066628'
				- '1581199096195979'
				- '1623770606653991'

			REQ_HEADER:
				content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
				cache-control: no-cache            

		-   Desc: 给指定用户发送验证码1
			Url: /user/sendcode
			Method: POST
			Data:
				req:
					cno: '%{rnd_list("${cno_list}$")}%'
				appid: dp1svA1gkNt8cQMkoIv7HmD1
				sig: "123"
				v: 2.0
				ts: 123
			OutPara: null
			Assert:
			-   eq:
				- result.errcode
				- 0
			-   eq:
				- result.res.result
				- SUCCESS
		-   Desc: 给指定用户发送验证码2
			Url: /user/sendcode
			Method: POST
			Data:
				req:
					cno: '%{rnd_list("${cno_list}$")}%'
				appid: dp1svA1gkNt8cQMkoIv7HmD1
				sig: "123"
				v: 2.0
				ts: 123
			Headers:
				content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
				cache-control: no-cache    			
			OutPara: null
			Assert:
			-   eq:
				- result.errcode
				- 0
			-   eq:
				- result.res.result
				- SUCCESS
- 在Case中增加REQ_HEADER字段来做为公共的请求头。
- 之后Case中执行共享此请求头
- 如果在用例中设置了REQ_HEADER字段与请求中也单独设置了请求头，那么第一顺序为请求中的为主。
- 上边的例子为场景用例，由两个请求组成，请求1，使用的是请求头默认值，请求2，使用自身请求头。

### 功能对比
|序号|功能|V1.0|V1.1|配置参数|
|--|--|--|--|--|
|1|并发执行|-|√|ENABLE_EXECUTION:False EXECUTION_NUM: 4|
|2|失败重新执行|√|√|ENABLE_RERUN: False  RERUN_NUM:  2|
|3|重复执行|-|√|ENABLE_REPEAT: False REPEAT_NUM: 2
|4|钉钉消息|√|√|ENABLE_DDING:  False |
|5|发送报告邮件|√|√|EMAIL_ENABLE: False|
|6|控制台输出|-|√|ENABLE_EXEC_MODE: False|
|7|自定义函数扩展|√|√|用例执行root目录增加extfunc.py|
|8|自定义变量|√|√|在用例中用USER_VAR字段定义变量，作用于当前Case|
|9|用例参数化|√|√|在用例中用PARAM_VAR字段定义参数化变量,作用于当前Case|
|10|请求头默认值|√|√|设置用例请求头默认值,整个case共享请求头。|
|11|指定case执行|-|√|单个yaml文件指定case执行|

## 代码打包与上传PyPi

  

### 通过setuptools工具进行框架打包,需要编写setup.py



- 打包：python3 setup.py bdist_wheel

  

- 上传PyP: twine upload dist/*

  
### 通过poetry工具打包

- poetry build

- poetry config repositories.testpypi https://pypi.org/project/HttpTesting

- poetry pushlish  输入pypi用户名和密码