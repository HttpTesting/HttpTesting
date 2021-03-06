import queue
import re
from httptesting.library.http import HttpWebRequest
from httptesting.library.assert_case import Ac
from httptesting.library.func import FUNC
from httptesting.library.scripts import parse_args_func

def out_param_parse(oname, param):
    """
    Parse args
    Param:
        oname: object
        param: args
    Usage:
        ret = out_param_parse('result', 'result.res.data[0].id')
    Example:
        Data.tr.id为 Data['tr']['id']
        res.tr.id为 res['tr]['id]
        res[0].tr.id 为res[0]['tr']['id']
        cookie.SESSION 为 Response cookie, cookie['SESSION']
        headers.Content-Type为 headers['Content-Type']
    Return: 
        Example:
        result['res']['data'][0]['id']
    """
    paramList = param.split(".")
    dt = oname
    tmpl = "['{}']"
    mJion = ''
    
    #Filter parameters.
    if paramList[0] in ('result', 'res', 'cookie', 'headers', 'header'):
        paramList.pop(0)

    ds = paramList[0]
    #Parse parammeters.
    if ds in  paramList:
        for args in paramList:
            if "[" in args:
                aJion = ''
                for num,val in enumerate(args.split("[")):
                    if num == 0:
                        val = "['{}']".format(val)
                    aJion = aJion + val +"["
                
                aJion = (aJion[:-1])
                mJion = mJion + aJion
            else:
                mJion = mJion + tmpl.format(args)
    else:
        print("出参错误,格式应为data.2级.3级:{}".format(param))
    return dt + mJion



def assert_func(self, res, headers, cookie, result, assertlist):
    """
    Assertion function.
    Args:
        self: Unittest instance object.
        res: Request object.
        headers: Reponse headers object.
        cookie: Reponse cookie object.
        result: Reponse text or reponse json.
    Usage:
        assert_func(self, res, headers, cookie, result, data[i]['Assert'])
    Return:
        There is no return.
    """
    for ass_dit in assertlist:
    
        for key, value in ass_dit.items():

            ac = getattr(Ac, key)

            for ite, val in enumerate(value):

                if '.' in str(val):
                    value[ite]= eval(out_param_parse(val.split(".")[0], val))
            #Distinguish between two parameters and one parameter by key.
            if value.__len__() == 1:
                eval(ac.format(value[0]))
            if value.__len__() == 2:
                eval(ac.format(value[0], value[1]))


def param_content_parse(queue, data):
    """
    Pass parameters with DATA information.

    args:
        queue: List the queue.
        data: The DATA content.
    
    return:
        There is no return.
    """

    for ki, value in enumerate(queue):
        for key, val in value.items():
            filed_list= ['Headers', 'Data', 'Url', 'Assert']
            for filed in filed_list:
                #data参数 正则匹配
                m = str(data[filed])
                content = re.findall('\$\{.*?}\$', m)
                if content:
                    k = ""
                    #替换数到data中
                    for k in content:
                        if key in content:
                            if isinstance(val, str):
                                m = m.replace(str(k), str(val))
                            else:
                                m = m.replace("'{}'".format(k), str(val)).replace('"{}"'.format(k), str(val))   
                            try:
                                m = eval(m)
                            except Exception:
                                pass                                  
                        data[filed] = m
                        break #break


def user_params_variables(data):
    """
        User parameterized execution.

        Args:
            data:
            [
                {
                    "Desc": "接口用例详细描述",
                    "PARAM_VAR":{
                        "sig": [1,2]
                    },
                },
                {   
                    "Desc": "接口名称1",
                    "Url": "/send/code",
                    "Method": "POST",
                    "Headers":{},
                    "Data":                 
                        {
                            "appid": "dp1svA1gkNt8cQMkoIv7HmD1",
                            "req": {
                                "cno": "1623770534820512"
                            },
                            "sig": "${sig}$",
                            "ts": 123,
                            "v": 2.0
                        },
                    "OutPara": None,
                    "Assert": [],

                }

            ]
        
        Usage:
            user_params_variables(data) 
        
        After:
            data:
            [
                {
                    "Desc": "接口用例详细描述",
                    "PARAM_VAR":{
                        "sig": [1,2]
                    },
                },
                {   
                    "Desc": "接口名称1_2",
                    "Url": "/send/code",
                    "Method": "POST",
                    "Headers":{},
                    "Data":                 
                        {
                            "appid": "dp1svA1gkNt8cQMkoIv7HmD1",
                            "req": {
                                "cno": "1623770534820512"
                            },
                            "sig": "2",
                            "ts": 123,
                            "v": 2.0
                        },
                    "OutPara": None,
                    "Assert": [],

                },
                {   
                    "Desc": "接口名称1_1",
                    "Url": "/send/code",
                    "Method": "POST",
                    "Headers":{},
                    "Data":                 
                        {
                            "appid": "dp1svA1gkNt8cQMkoIv7HmD1",
                            "req": {
                                "cno": "1623770534820512"
                            },
                            "sig": "1",
                            "ts": 123,
                            "v": 2.0
                        },
                    "OutPara": None,
                    "Assert": [],

                }
            ] 
        Returns:
            There is no return.
    """
    if 'PARAM_VAR' in data[0].keys():
        params_dict = data[0]['PARAM_VAR']
        if params_dict:
            for key, value in params_dict.items():
                #取到参数${key}$，到其它case中遍历，并扩充case
                for _num, val_dict in enumerate(data):
                    if _num == 0:
                        continue
                    content = val_dict
                    init_desc = val_dict['Desc']
                    #如果${key}$变量在Data中，说明要进行参数化。
                    var_name = "${%s}$" % str(key)
                    if var_name in str(content):
                        #遍历参数化，增加case
                        params_len = len(params_dict[str(key)])
                        for _iter , val in enumerate(params_dict[str(key)]):
                            #更改Desc描述，给加个序号
                            content['Desc'] = '{}_{}'.format(content['Desc'], _iter + 1)
                            #最后一个参数化后，将原来${sig}$替换掉
                            if val != params_len:
                                new_content = eval(str(content).replace(str(var_name), str(val)))
                                data.append(new_content)
                            else:
                                data[_num] = eval(str(content).replace(str(var_name), str(val)))
                            
                            #恢复最初描述
                            content['Desc'] = init_desc

def user_custom_variables(queue, args, data):
    """
    Handles custom variables in USER_VAR

    args:
        queue: variables queue
        args: User variables
        data: user variables value
    
    return:
        There is no return.
    """
    #User-defined variables.
    if 'USER_VAR' in data.keys():
        for key, value in data['USER_VAR'].items():
            if "${" in str(value):
                content = re.findall('\$\{.*?}\$', str(value))
                for ilist in content:
                    if str(ilist) in args.keys():
                        va = args[str(ilist)]
                        if isinstance(value, str):
                            value = str(value).replace(str(ilist), str(va))
                        else:
                            value = str(value).replace("'{}'".format(ilist), str(va))

            if '%{' in str(value):
                temp = parse_args_func(FUNC, value)
            else:
                temp = value

            args['${%s}$' % key] =  temp
        queue.append(args)

        var_dict = queue[0]

        #Handles custom variables in USER_VAR
        for key, val in var_dict.items():
            content = re.findall('\$\{.*?}\$', str(val))
            if content:
                for klist in content:
                    var_dict[key] = eval(str(val).replace(str(klist), str(var_dict[klist])))


def req_headers_default(data, index):
    """
    Specify the default request header.
    Args:
        data: [
            {"Desc": 'xxxx', "REQ_HEADER": {"content-type": 'application/json'}},
            {"Desc": 'xxxx', 'Url': 'ccc', "Assert":[], "Method": "POST", "Data": 'xxx', "OutPara": "xxxx"}
            {"Desc": 'xxxx', 'Url': 'ccc', "Assert":[], "Method": "POST", "Data": 'xxx', "OutPara": "xxxx"}
        ]
        index:
            data[index]
    Usage:
        req_headers_default(data)
    Return:
        There is no return.
    """
    if 'REQ_HEADER' in data[0].keys():
        headers_default = data[0]['REQ_HEADER']
        if 'Headers' in data[index].keys():
            if not data[index]['Headers']:
                data[index]['Headers'] = headers_default
        else:
            data[index]['Headers'] = headers_default
    else:
        # No request header is specified.
        pass


def exec_test_case(self, data):
    """
    Execute unittest test framework.
    Args:
        self: unittest.TestCase object.
        data: DDT data.
    Usage:
        exec_test_case(self, data)
    Return:
        There is no.
    """
    queue_list = []
    args_dict = {}
    #HTTP request instance.
    req = HttpWebRequest()

    #Through the case.
    for i, _ in enumerate(data):
        if i == 0:
            #User parameterized execution
            user_params_variables(data)
            #Handles custom variables in USER_VAR
            user_custom_variables(queue_list, args_dict, data[0]) 
            continue

        res = None
        
        # Request header default value.
        req_headers_default(data, i)

        #Pass parameters with DATA information.
        param_content_parse(queue_list, data[i])

        #Execute the custom function.
        data[i]['Desc'] = parse_args_func(FUNC, data[i]['Desc'])
        data[i]['Data'] = parse_args_func(FUNC, data[i]['Data'])
        data[i]['Url'] = parse_args_func(FUNC, data[i]['Url'])
        data[i]['Headers'] = parse_args_func(FUNC, data[i]['Headers'])
        data[i]['OutPara'] = parse_args_func(FUNC, data[i]['OutPara'])

        #处理请求
        method = data[i]['Method']
        if ('GET' in method) or (r'DELETE' in method):
            res, headers, cookie, result = req.get(
                params=data[i]['Data'], 
                desc=data[i]['Desc'], 
                gurl=data[i]['Url'],
                headers=data[i]['Headers'],
                method= method
                )
        elif ('POST' in method) or ('PUT' in method):
            res, headers, cookie, result = req.post(
                data=data[i]['Data'], 
                desc=data[i]['Desc'], 
                gurl=data[i]['Url'],
                headers=data[i]['Headers'],
                method= method
                )
        else:
            raise ("Error:请求Mehod:{}错误.".format(data[i]['Method']))
            
        #断言解析
        assert_func(self, res, headers, cookie, result, data[i]['Assert'])

        #Output parameters are written to the queue
        param_to_queue(self, queue_list, data[i], args_dict, res, headers, cookie, result)



def param_to_queue(self, queue, data, param_dict, res, headers, cookie, result):
    """
    Output parameters are written to the queue.

    args:
        queue: List the queue.
        data: The DATA content 
        param_dict: Temporary storage queue parameters.
        res: Request object.
        headers: Repsonse headers.
        cookie: Repsonse cookies.
        result: Repsonse content JSON or text.
    
    usage:
        param_to_queue(outParaQueue, data[i], oPara, res, headers, cookie, result)

    return:
        There is no return.
    """
    #出参写入队列
    if data['OutPara']:
        header = data['Headers']
        #组参数
        for key, value in data['OutPara'].items():
            #解释用例中的出参
            out_data = data
            #
            if '.' in value:
                strsplit = str(value).split(".")
                stra = strsplit[0]
                if '[' in stra:
                    stra = stra.split("[")[0]

                if stra.lower() != "data": 
                    head = stra
                else:
                    head = "out_data"
                #处理cookie 
                if strsplit[0].lower() == 'cookie':
                    queue_val = '{}={}'.format(
                        strsplit[1], 
                        eval(out_param_parse(head, value))
                        )
                else:
                    queue_val = eval(out_param_parse(head, value))
            else: #Parameter cookie  result 
                if 'cookie' in str(value).lower():
                    temp_list = []
                    for ky, vak in cookie.items():
                        temp_list.append('{}={}'.format(ky, vak))
                    queue_val = '; '.join(temp_list)
                else:
                    queue_val = eval(value)

            #custom var.
            if not "${" in key:
                key = "${%s}$" % key
            param_dict[key] = queue_val
        queue.append(param_dict)

