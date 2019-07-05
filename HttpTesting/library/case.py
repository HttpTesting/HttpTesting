import queue
import re
from HttpTesting.library.http import HttpWebRequest
from HttpTesting.library.assert_case import Ac

def out_param_parse(oname, param):
    """
    解析参数:
    Data.tr.id为 Data['tr']['id']
    res.tr.id为 res['tr]['id]
    res[0].tr.id 为res[0]['tr']['id']
    :para oname: res or Data
    
    """
    pa = param.split(".")
    dt = oname
    sk = "['{}']"
    m = ''
    
    #过滤参数
    if pa[0]=='result' or pa[0]=='res' or pa[0]=='cookie' or pa[0]=='headers':
        pa.pop(0)

    ds = pa[0]

    if ds in  pa:
        for args in pa:
            if "[" in args:
                a = ''
                for i,v in enumerate(args.split("[")):
                    if i == 0:
                        v = "['{}']".format(v)
                    a = a + v +"["
                
                a = (a[:-1])
                m = m + a
            else:
                m = m + sk.format(args)
    else:
        print("出参错误,格式应为data.2级.3级:{}".format(param))
    return dt + m


def exec_test_case(self, data):
    """
    param self: unittest.TestCase
    param data: ddt数据
    """
    outParaQueue = []
    oPara = {}
    ###实例化http请求类###
    req = HttpWebRequest()

    #遍历case
    for i in range(0, len(data)):
        if i == 0:
            desc = data[0]['Desc']
            continue
        res = None
            
        #接口入参
        if  data[i]['InPara'] != "":
            for ki, value in enumerate(outParaQueue):
                for key, val in value.items():
                    if 'H_' in key: #H_头参数 D_数据参数
                        ke = key.split('H_')[1].split('}')[0]
                        data[i]['Headers'][ke] = val
                    if 'D_' in key:
                        #data参数 正则匹配
                        m = str(data[i]['Data'])
                        c = re.findall('\$\{.*?}\$', m)
                        k = ""
                        #替换数到data中
                        for k in c:
                            if key in c:
                                m = eval(m.replace(k, val))
                            data[i]['Data'] = m
                            break #break

        #处理请求
        if 'GET' in data[i]['Method']:
            res, headers, cookie, result = req.get(
                params=data[i]['Data'], 
                desc=desc, 
                gurl=data[i]['Url'],
                headers=data[i]['Headers']
                )
        elif 'POST' in data[i]['Method']:
            res, headers, cookie, result = req.post(
                data=data[i]['Data'], 
                desc=desc, 
                gurl=data[i]['Url'],
                headers=data[i]['Headers']
                )
        else:
            raise "Error:请求Mehod:{}错误.".format(data[i]['Method'])


        #出参写入队列
        if data[i]['OutPara'] != "":
            #组参数
            for key, value in data[i]['OutPara'].items():

                #解释用例中的出参
                out_data = data[i]
                strsplit = stra = str(value).split(".")
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
                oPara[key] = queue_val
            outParaQueue.append(oPara)


        #断言解析
        assert_list = data[i]['Assert']
        for ass_dit in assert_list:
            for key, value in ass_dit.items():
                if key == 'eq':
                    #解析断言
                    oname = value[0].split(".")[0]
                    eval(
                        Ac.eq.format(
                            out_param_parse(oname, value[0]), value[1])
                        )




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
