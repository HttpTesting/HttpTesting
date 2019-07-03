#coding=utf-8
from web.view import views

class Custom_Urls(object):

    @staticmethod
    def urls_route(app):
        """
        Flask实例
        :param app: app = Flask(__name__)实例
        :return: 无
        """

        ###########################################################################
        #以下定义url路由
        #例:app.add_url_rule('/', view_func=views.report)
        ###########################################################################

        #report文件
        app.add_url_rule('/report/<report_dir>/<report_name>', view_func=views.report)
        #根目录访问与/report/访问跳转到report目录
        app.add_url_rule("/", view_func=views.report_dir)
        app.add_url_rule("/report/", view_func=views.report_dir)

        app.add_url_rule("/case/", view_func=views.case)