#coding=utf-8
import os
from flask import render_template
from HttpTesting.library.scripts import get_yaml_field
from HttpTesting.globalVar import gl

def case():
    """读取case"""
    path = os.path.join(gl.dataScenarioPath, "POS_INFO.yaml")
    yam_dict = get_yaml_field(path)['POS_INFO']['Case1']
    
    return render_template('dt.html', data=yam_dict)

def  report(report_dir, report_name):
    """
    report文件路径精准访问
    :param report_dir:
    :param report_name:
    :return:
    """
    return render_template(r'/report/{}/{}'.format(report_dir, report_name))


def report_dir():
    all_list = []
    folder_list = []

    #report路径
    webpath = os.path.abspath(os.path.dirname("__file__"))
    templatesReportPath = os.path.join(webpath, 'templates')
    redir = os.path.join(templatesReportPath, 'report')

    #遍历路径,取文件夹名称和html文件存入list
    for root, subdirs, _ in os.walk(redir):
        for sdirs in subdirs:
            folder_list.append(sdirs)
            for subroot, dirs, files in os.walk(os.path.join(root,sdirs)):
                for fi in files:
                    folder_list.append(fi)
                all_list.append(folder_list)
            folder_list = []


    return render_template('directory.html', all_list = all_list)