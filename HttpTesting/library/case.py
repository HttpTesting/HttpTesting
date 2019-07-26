import queue
import re
from HttpTesting.library.http import HttpWebRequest
from HttpTesting.library.assert_case import Ac

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
        There is no.
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
    outParaQueue = []
    oPara = {}
    #HTTP request instance.
    req = HttpWebRequest()

    #Through the case.
    for i in range(0, len(data)):
        if i == 0:
            desc = data[0]['Desc']
            continue
        res = None
            
        #Pass parameters with DATA information.
        for ki, value in enumerate(outParaQueue):
            for key, val in value.items():
                filed_list= ['Headers', 'Data', 'Url', 'Assert']
                for filed in filed_list:
                    #data参数 正则匹配
                    m = str(data[i][filed])
                    content = re.findall('\$\{.*?}\$', m)
                    if content:
                        k = ""
                        #替换数到data中
                        for k in content:
                            if key in content:
                                try:
                                    m = eval(m.replace(k, val))
                                except Exception:
                                    m = m.replace(k, val) 
                            data[i][filed] = m
                            break #break

        desc = data[i]['Desc']
        #处理请求
        method = data[i]['Method']
        if ('GET' in method) or (r'DELETE' in method):
            res, headers, cookie, result = req.get(
                params=data[i]['Data'], 
                desc=desc, 
                gurl=data[i]['Url'],
                headers=data[i]['Headers'],
                method= method
                )
        elif ('POST' in method) or ('PUT' in method):
            res, headers, cookie, result = req.post(
                data=data[i]['Data'], 
                desc=desc, 
                gurl=data[i]['Url'],
                headers=data[i]['Headers'],
                method= method
                )
        else:
            raise "Error:请求Mehod:{}错误.".format(data[i]['Method'])
            
        #断言解析
        assert_func(self, res, headers, cookie, result, data[i]['Assert'])

        #出参写入队列
        if data[i]['OutPara']:
            header = data[i]['Headers']
            #组参数
            for key, value in data[i]['OutPara'].items():
                #解释用例中的出参
                out_data = data[i]
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

                oPara[key] = queue_val
            outParaQueue.append(oPara)





if __name__ == "__main__":
    param = "result.res[0].cno"
    pm = param.split(".")[0]
    if '[' in pm:
        pm = pm.split("[")[0]
    if pm.lower() == "result": 
        head = "result"
    else:
        head = "out_data"
    ot = out_param_parse(head, param)
    print(ot)
