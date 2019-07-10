from HttpTesting.base.base_config import BaseConfig
from HttpTesting.library.scripts import (
    get_datetime_str, 
    retry, 
    get_yaml_field
    )
from HttpTesting.library.log import LOG
from requests.exceptions import (HTTPError, ConnectionError, ConnectTimeout)
from HttpTesting.globalVar import gl
from HttpTesting.library.Multipart import MultipartFormData

#########################################################################
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#去掉因请法度时verfiy=False 关闭SSL带来的警告
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
###########################################################################
class HttpWebRequest(object):
    """
    HTTP post requests or get requests.
    usage:
        #instance class 
        http = HttpWebRequest()

        res = http.get(**kwargs)
        
        res = http.post(**kwargs)
    """
    def __init__(self):
        self.config  = get_yaml_field(gl.configFile)
        self.baseUrl  = BaseConfig.base_url()
        self.OUT_TMPL = """\n{0} {1}请求:{2}\r\n{3}\r\n响应:\r"""

    def header_lower(self, hdict):
        """
        Convert HTTP header information to lowercase.
        param:
            hdict: Head dictionary type.
        usage:
            ret = header_lower(hdict)
        return:
            dict Head dictionary type.
        """
        tmp = {}
        for key, val in hdict.items():
            tmp[str(key).lower()] = str(val).lower()
        return tmp 


    @retry(reNum=3)
    def get(self, **kwargs):
        """get请求"""

        #是否采用url = base_url + url
        if self.config['ENABLE_BASE_URL']:
            url = '{}{}'.format(self.baseUrl, str(kwargs['gurl']).strip())
        else:
            url = str(kwargs['gurl']).strip()


        #报告输出模版   
        tmpl = self.OUT_TMPL.format(
            get_datetime_str(),
            'GET',
            url,
            kwargs['params']
        )
        print(tmpl)    

        try:
            res =requests.request("GET", url, params=kwargs['params'], headers=kwargs['headers'], verify=False)
            headers = res.headers
            cookie = res.cookies.get_dict()
            if res.status_code ==200:
                if 'json' in headers['Content-Type']:
                    result = res.json()
                else:
                    result = res.text
            else:
                result =  {"errcode": 9001, "errmsg": str(res)}

        except (HTTPError, ConnectionError, ConnectTimeout) as ex:
            result = {"errcode": 9002, "errmsg": str(ex)}


        LOG.console_info('GET: {} STATUS: {}'.format(url, res.status_code))
        print(result) #res结果报告展示输出
        return res, headers, cookie, result


    # post请求
    @retry(reNum=3)
    def post(self, **kwargs):
        """post请求"""
        #是否采用url = base_url + url
        if self.config['ENABLE_BASE_URL']:
            url = '{}{}'.format(self.baseUrl, str(kwargs['gurl']).strip())
        else:
            url = str(kwargs['gurl']).strip()

        data = kwargs['data']

        #报告输出模版    
        tmpl = self.OUT_TMPL.format(
            get_datetime_str(),
            'POST',
            url,
            kwargs['data']
        )
        print(tmpl)

        header_dict = self.header_lower(kwargs['headers'])
        try:
                    #转换数据为form-data数据
            if 'form-data' in header_dict['content-type']:
                data = MultipartFormData.to_form_data(data, headers=kwargs['headers'])
                res = requests.request(
                    "POST", 
                    url, 
                    data=data, 
                    headers=kwargs['headers'],
                    verify= False
                    )
            elif 'application/json' in header_dict['content-type']:
                res = requests.request(
                    "POST", 
                    url, 
                    json=data, 
                    headers=kwargs['headers'],
                    verify= False
                    )
            elif 'application/x-www-form-urlencoded' in header_dict['content-type']:
                res = requests.request(
                    "POST", 
                    url, 
                    data=data, 
                    headers=kwargs['headers'],
                    verify= False
                    )                
            else:
                res = requests.request(
                    "POST", 
                    url, 
                    params=data, 
                    headers=kwargs['headers'],
                    verify= False
                    )

            headers = res.headers
            cookie = res.cookies.get_dict()

            if res.status_code ==200:
                if 'json' in headers['Content-Type']:
                    result = res.json()
                else:
                    result = res.text
            else:
                result =  {"errcode": 9001, "errmsg": str(res)}

        except (HTTPError, ConnectionError, ConnectTimeout) as ex:
            result =  {"errcode": 9002, "errmsg": str(ex)}

        print(result) #res结果报告展示输出
        return res, headers, cookie, result





