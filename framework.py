#=========上下文层=========#
import logging

from config.config import FLASK_DB, BASE_URL
from utils.allure_utils import allure_init
from utils.render_obj import render_obj
from utils.send_request import send_http_request
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.extractor import task_id_extractor, jdbc_extractor, json_extractor


class Context:
    def __init__(self):
        self.data={}
    def set(self,key,value):
        self.data[key]=value
    def get(self,key):
        return self.data.get(key)
#=========数据层=========#
class DataProvider:
    def __init__(self,case):
        self.case = case
    def render(self,context):
        rendered_case=render_obj(self.case,context.data)
        return rendered_case
#=========执行层=========#
class HttpClient:
    def __init__(self,base_url):
        self.base_url = base_url
    def send(self,case,context):
        request_data=analyse_case(case,context.data,self.base_url)
        resp=send_http_request(**request_data)
        request_data.pop("session", None)
        return resp
#=========提取层=========#
class DataExtractor:
    def __init__(self, db_config):  # ← 形参名统一叫 db_config
        self.db_config = db_config
    def extract(self,case,context,resp,task_id_list):
        json_extractor(case, context.data, resp)

        jdbc_extractor(case, context.data, self.db_config)
        if task_id_list:
            task_id_extractor(task_id_list, context.data)
#=========断言层=========#
class AssertionEngine:
    def __init__(self, db_config):  # ← 形参名统一叫 db_config
        self.db_config = db_config
    def assert_all(self,case,context,resp):
        http_assert(case, resp, context.data)
        jdbc_assert(case, context.data, self.db_config)

#=========协调层=========#
class BaseRunner:
    def __init__(self,case,context,task_id_list,base_url,db_config):
        self.case = case
        self.context = context
        self.task_id_list = task_id_list
        self.data_provider = DataProvider(case)
        self.http_client = HttpClient(base_url)
        self.data_extractor=DataExtractor(db_config=db_config)
        self.assert_engine=AssertionEngine(db_config=db_config)

# ----------勾子-----------#
    def setup(self):


        pass

    def teardown(self):
        pass

# ----------模板方法（定义执行流程）-----------#

    def execute(self):
        # 1. 前置钩子
        self.setup()
        # 2. 数据层：渲染
        rendered_case = self.data_provider.render(self.context)
        # allure 初始化
        allure_init(rendered_case)
        logging.info(f"0.用例ID:{rendered_case['id']}  模块:{rendered_case['feature']}  场景:{rendered_case['story']}  标题:{rendered_case['title']}")
        # 3. 执行层：发请求
        resp = self.http_client.send(rendered_case, self.context)

        # 4. 提取层：提取数据到 Context
        self.data_extractor.extract(rendered_case, self.context, resp, self.task_id_list)

        # 5. 断言层：断言
        self.assert_engine.assert_all(rendered_case, self.context, resp)

        # 6. 后置钩子
        self.teardown()
