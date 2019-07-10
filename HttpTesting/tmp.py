# import requests
# from requests.sessions import Session
# data={
#     "employeeEntryMSG": '{"employeeEntry":{"clickState":0,"userName":"美美","userNum":"MW00011799","userNumCopy":"MW00011799","photourl":"","checkWorkNo":"80413","firstWorkTime":"","country":"151001","idCardType":"149002","userIDCard":"963258","birthDay":"1980-06-04","isMarried":"","gender":"118002","nation":"","hukouType":"","healthEndTime":"","phone":"","weChat":"","mail":"","userType":"100010","qq":0,"urgentPerson":"","urgentPhone":"","organizeID":370,"chcekOrgID":"","postID":6169,"rankID":"235","startTime":"2019-06-19","offerTime":"","expectOfferTime":"","checkworkcode":"","bankName":"","bankCard":"","checkworkid":"68","expiryDate":"","state":"120001","origin":"","age":39,"baseSalary":0,"unit":"2","contractType":"","hireType":"","contractDateType":"","contractSignDate":"","education":"","gongling":"","subWorkYear":0,"siling":"","idCardEndTime":"","hukouAddress":"","hukouCode":0,"positionID":83,"positionName":"部门主管","political":"","showBankUrl":false,"showContractUrl":false,"showHealthUrl":false,"showIdentityUrl":false,"showRetirecontractUrl":false,"socialSecurity":"","parentSalary":"","childrenEducationSalary":"","parentBankCard":"","parentBankName":"","parentBankNameName":"","leaveType":"666","isBlack":0,"ID":""},"jobexperienceList":[],"educateList":[],"dormitory":{"ID":"","address":"","dormitoryCode":""},"extendList":[{"ID":5,"dbName":"_huodezhengshu","des":"","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":4,"dbName":"_tongjineng","des":"","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":10,"dbName":"_xianjuzhudizhi","des":"","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":14,"dbName":"_biyeyuanxiao","des":"234","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":15,"dbName":"_zhuanye","des":"234","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":16,"dbName":"_biyeshijian","des":"","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":18,"dbName":"_peiou","des":"","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":19,"dbName":"_zhaopinqudao","des":"","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":23,"dbName":"_huiyuankahao","des":"24","tableName":"employee","valid":1,"showType":"show_inputStr"},{"ID":25,"dbName":"_fangbu","des":"","tableName":"employee","valid":1,"showType":"show_radio"},{"ID":26,"dbName":"_goumaiyiwaixianriqi","des":"","tableName":"employee","valid":1,"showType":"show_date"}],"checkworkOrgList":[],"empaccessory":{"identityUrl":"","healthUrl":"","bankUrl":"","contractUrl":"","photoUrl":"","signatureUrl":"","retirecontractUrl":""},"isCommit":1,"saveOrUpdate":"S"}'
# }

# req = Session()
# req.get(url='https://dev.cxyhr.cn/login/login.htm?name=customservice&pass=a2019rlgj', verify=False)

# res = req.post(url='https://dev.cxyhr.cn/acewill/employee/addEmployeeEntry.htm', data=data, verify=False)
# print(res.text)


import io
import json
import os
import collections
import yaml

class ConvertHarToYAML:

    @classmethod
    def from_har_to_dict(cls, harpath):
        """
        Convert from Charles HAR to a dict object.
        :Param harpath: HAR file path.
        usage:
            dictReq = from_har_to_dict(harpath)
        return: dictReq Har's dict object.
        """
        if os.path.exists(harpath):

            with io.open(harpath, 'r+', encoding='utf-8-sig') as fp:
                rjson =fp.read()
                content_dict = json.loads(rjson)
                return content_dict['log']['entries']
        else:
            raise Exception("HAR file path error.{}".format(harpath))

    @classmethod
    def convert_to_list(cls, harpath):
        """
        convert HAR content to list
        :param harpath: HAR file path.
        usage:
            ret_list = convert_to_list(harpath)
        return:
            [] request list.
        """
        ret = cls.from_har_to_dict('d:\httphar.har')

        req_dict = []
        for req in ret:
            req_dict.append(req['request'])

        return req_dict

    @classmethod
    def parse_headers_dict(cls, header):
        """
        parse Headers information.
        """
        try:
            headers = {}
            for i_dict in header:
                headers[i_dict['name']] = i_dict['value']
            # print(headers)
        except (KeyError, TypeError) as ex:
            raise ex
        return headers
    
    @classmethod
    def parse_post_data(cls, postData):
        """
        parse POST Data.
        :param postData: HAR post data.
        usage:
        return:
            dict data.
        """
        if isinstance(postData, dict):
            data = postData['params']
        else:
            data = postData
        dt = {}
        try:
            for i_list in data:
                dt[i_list['name']] = i_list['value']
        except (KeyError, TypeError) as ex:
            raise ex
        return dt

    @classmethod
    def ordered_dump(cls, data, stream=None, Dumper=yaml.Dumper, **kwds):
        """
        Convert the unordered dictionary to ordered and write yaml.
        param:
            data: 
            stream: 
            allow_unicode:
            default_flow_style:
            indent:
        return: There is no.
        """
        class OrderedDumper(Dumper):
            pass
        def _dict_representer(dumper, data):
            return dumper.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data.items())
        OrderedDumper.add_representer(collections.OrderedDict, _dict_representer)
        return yaml.dump(data, stream, OrderedDumper, **kwds)


    @classmethod
    def write_case_to_yaml(cls, yampath, contentDict):
        """
        Write the test case to yaml.
        param:
            yampath: Yaml file path.
        return:
            There is no.
        """
        yamFile = os.path.join(yampath, 'har_testcase.yaml')
        with io.open(yamFile, 'w', encoding='utf-8') as fp:
            cls.ordered_dump(
                contentDict, 
                fp, 
                Dumper=yaml.SafeDumper, 
                allow_unicode=True, 
                default_flow_style=False, 
                indent=4
            )


    @classmethod
    def convert_har_to_ht(cls, harfile):
        """
        Convert har files to HttpTesting the test cases.
        param:
            harfile: HAR file full path.
        return:
            {} dict case.
        """

        temp_dict = {}
        temp_dict['TEST_CASE'] = collections.OrderedDict()

        ret = cls.convert_to_list(harfile)
        # print(ret[0])

        for n, val in enumerate(ret):
            case = 'case{}'.format(n)
            temp_dict['TEST_CASE'][case] =[]
            temp_dict['TEST_CASE'][case].append({'Desc':'请添加接口描述'})

            if val['method'] == 'GET':
                data = val['queryString']
            else:
                data = val['postData']

            url = val['url']
            if '?' in val['url']:
                url = val['url'].split('?')[0]

            temp_dict['TEST_CASE'][case].append(collections.OrderedDict({
                'Url': url,
                'Method': val['method'],
                'Headers': cls.parse_headers_dict(val['headers']),
                'Data': cls.parse_post_data(data),
                'InPara': "",
                'OutPara': "",
                'Assert': []
            }))
        # print(temp_dict)
        return temp_dict


if __name__ == "__main__":
    temp_dict = ConvertHarToYAML.convert_har_to_ht(r'D:\httphar.har')
    ConvertHarToYAML.write_case_to_yaml('', temp_dict)
