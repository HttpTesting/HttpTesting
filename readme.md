# HttpTesting

HttpTesting 是HTTP(S) 协议测试框架，通过YAML来编写测试用例；支持通过pip直接从PyPi安装，支持命令行运行代码，不固定结构，通过命令生成脚手架。

## 版本信息

- v 1.0 unittest

- v 1.1 pytest


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



### amt 或 AMT命令

  

- amt -config set [此命令用来设置config.yaml基本配置]

- amt -file template.yaml [执行YAML用例，支持绝对或相对路径。]

- amt -dir testcase [批量执行testcase目录下的YAML用例，支持绝对路径或相对路径。]

- amt -startproject demo [生成脚手架demo目录]

- amt -har  D:\httphar.har [根据har文件，生成测试用例YAML.]

- amt -service start 启动Report Web服务.

- amt -convert 转换字典列表等数据为case.将请求数据存储在xxxx.yaml中,使用命令行转换.自动生成xxxx.yaml测试用例

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

建议分成业务场景和单接口进行编写.

- 业务场景: 所谓业务场景,即指在一个接口业务流程中,接口之间传参与出参有一定关联.

- 单接口多用例: 指同一接口, 由不同的参数数据,组成不同的CASE.



### 用例模型

>TESTCASE{

>>'case1':['description',{},{}],  #场景模式每个{}一个接口

>>'case2':['description',{}],     #单接口模式

>}


### YAML用例格式  

####  例子1:由两个请求组成的场景

    TESTCASE:
        Case1:
	        -
	            Desc: 登录-修改资料业务场景
	        -
	            Url: /login/login
	            Method: GET
	            Headers:
	                content-type: "application/json"
	                cache-control: "no-cache"
	            Data:
	                name: "test"
	                pass: "test123"
	            OutPara: 
	                "$H_token$": result.data
	            Assert:
	                - eq: [result.status, 'success']
	        -
	            Url: /cloudfi/api/store/batchhandle/store
	            Method: GET
	            Headers:
	                content-type: "application/json"
	                cache-control: "no-cache"
					token: "$H_token$"
	            Data:
	                name: "test"
	                pass: "test123"
	            OutPara: 
	                "$H_token$": result.data
	            Assert:
	                - eq: [result.status, 'success']


####  例子2: 同一接口,不同参数,扩充为多个CASE

    TESTCASE:

		Case1:
		    -
			    Desc: 登录接口-正常登录
            -
	            Url: /login/login
	            Method: GET
	            Headers:
	                content-type: "application/json"
	                cache-control: "no-cache"
	            Data:
	                name: "test"
	                pass: "test123"
	            OutPara: 
	                "$H_cookie$": cookie.SESSION
	            Assert:
	                - eq: [result.status, 'success']
		Case2:
		    -
			    Desc: 登录接口-密码错误
            -
	            Url: /login/login
	            Method: GET
	            Headers:
	                content-type: "application/json"
	                cache-control: "no-cache"
	            Data:
	                name: "test"
	                pass: "test123"
	            OutPara:
	                "$H_cookie$": cookie.SESSION 
	            Assert:
	                - eq: [result.status, 'error']


### 参数说明

- "$H_token $": 为参数变量,可以头信息里与Data数据里进行使用
- "%{md5('aaaa')}%": 为函数原型,具体支持函数下方表格可见.

#### OutPara字段变量使用

OutPara字段用来做公共变量,供其它接口使用,默认为""; 

-  示例: "$H_token $": result.data 是请求结果，返回的嵌套级别
-  OutPara为dict类型,可以做多个公共变量.


#### Assert断言

Assert字段默认为[].

- eq: [a, b]  判断 a与b相等
- nq: [a, b]  判断 a与b不相等
- al: [a, b]  判断 a is b 相当于id(a) == id(b)
- at: [a, b]  判断 a is not b 相当于id(a) != id(b)
- ai: [a, b]  判断 a in b 
- ani:[a, b]  判断 a in not b
- ais:[a, b]  判断 isinstance(a, b) True
- anis:[a, b] 判断 isinstance(a, b) False
- ln:[a]      判断 a is None
- lnn:[a]     判断 a is not none
- bt:[a]      判断 a 为True
- bf:[a]      判断 a 为False


#### 内置函数及扩展

使用原型(带参数与不带参数)

- "%{md5('aaaa')}%" 或 "%{timestamp()}%"



|函数名|参数|说明|
|:---|:---|:---|
|md5|txt字符串|生成md5字符串示例: cbfbf4ea6d7c8032584dcf0defa10276|
|timestamp|-|秒级时间戳示例: 1563183829|
|uuid1|-|生成唯一id,uuid1示例:ebcd6df8a77611e99bb588b111064583|
|datetimestr|-|生成日期时间串,示例:2019-07-16 10:50:16|


- 其它后续添加


## 常用四种对象(通常做参数变量时使用)
- res: 请求Response对象
- result: res.json 或 res.text
- cookie: res.cookie 响应cookie字典对象;  当做为参数时如果cookie.SESSION这样的写法代表取cookie中的SESSION对象. 如果只写cookie,会解析成"SESSION=xxxxxxx; NAME=xxxxxx"
- headers: res.headers 响应头字典对象

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




## 代码打包与上传PyPi

  

### 通过setuptools工具进行框架打包,需要编写setup.py
	from setuptools import setup, find_packages, command
	setup(
		name='HttpTesting',#应用名称
		version='1.0.16',#版本号
		description='HttpTesting',#描述
		long_description="长描述", #此描述显示到PyPi页
		long_description_content_type='text/markdown',
		author='天枢',#作者
		author_email='lengyaohui@163.com',
		url='https://gitlab.acewill.cn/lengyaohui/amtesting.git',
		license='Apache 2.0',
		python_requires='!=3.0.,!=3.1.,!=3.2.,!=3.3.,<4.0.',
		packages=find_packages(),#查找包方法
		package_data={
			'HttpTesting':[
				'config/*.yaml',
				'testcase/*.yaml',
				'report/*.html',
				'report/*.xlsx',
			],
			'':['*.py'],
		},	
		#依赖包
		install_requires=[
			'ddt==1.1.3',
			'Flask==1.0.2',
			'PyYAML==3.12',
			'requests==2.18.4',
			'requests-toolbelt==0.8.0',
		],
		#排出打包文件
		exclude_package_data={
			'':['README.txt'],
		},
		#PyPi页面左侧显示
		classifiers=[
			'Development Status::Beta',
			'Programming Language::Python::3.4',
			'Programming Language::Python::3.5',
			'Programming Language::Python::3.6',
			'Programming Language::Python::3.7',
		],
		#命令行使用命令
		entry_points={
			'console_scripts':[
				'amt=HttpTesting.main:run_min',
				'AMT=HttpTesting.main.run_min',
			],
		},
		#发布时执行的cmd命令
		cmdclass={
			'upload':从Command继承的类，
		},
	)
  

- 打包：python3 setup.py bdist_wheel

  

- 上传PyP: twine upload dist/*

  