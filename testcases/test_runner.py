import logging
import pytest


from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.allure_utils import allure_init
from utils.extractor import json_extractor, jdbc_extractor, task_id_extractor
from utils.render_obj import render_obj
from utils.send_request import send_http_request, send_jdbc_request

#数据
# case_login=[{
#     "method":"post",
#     "url":"http://127.0.0.1:5000/user/login",
#     "params":None,
#     "data":None,
#     "json":{"username":"admin","password":"123456"},
#     "files":None,
#     "headers":None,
# }]
# case_list=[{
#     "method":"get",
#     "url":"http://127.0.0.1:5000/task/list",
#     "params":{"page":1,"size":2},
#     "data":None,
#     "json":None,
#     "files":None,
#     "headers":None
# }]
# case_add=[{
#     "method":"post",
#     "url":"http://127.0.0.1:5000/task/add",
#     "params":None,
#     "data":None,
#     "json":{"task_name":"大扫除","description":"清理二楼卫生","assign_user":"姜承録","deadline":"2026-11-20"},
#     "files":None,
#     "headers":None
# }]
# case_delete=[{
#     "method":"delete",
#     "url":"http://127.0.0.1:5000/task/delete/6",
#     "params":None,
#     "data":None,
#     "json":None,
#     "files":None,
#     "headers":None
# }]
# case_update=[{
#     "method": "put",
#     "url": "http://127.0.0.1:5000/task/update",
#     "params": None,
#     "data": None,
#     "json": {"id":"1","task_name": "二月财政报告", "description": "根据账本计算出二月的盈亏", "assign_user": "彭立勋", "deadline": "2026-11-11"},
#     "files": None,
#     "headers": None
# }]
# case_statue=[{
#       "method": "put",
#     "url": "http://127.0.0.1:5000/task/status",
#     "params": None,
#     "data": None,
#     "json": {"id":"1","status":"doing"},
#     "files": None,
#     "headers": None
# }]
# data=[case_login[0],case_list[0]]

# def get_token():   获取json的方法两种
#     res=requests.request(**login[0])
#     token1=jsonpath.jsonpath(res.json(),"$.data.token")[0]
#     token=res.json()["data"]["token"]
#     print(f'token=',token)
#     print(f'token=',token1)


# def get_token():
#     res = requests.request(**case_login[0])
#     token=jsonpath.jsonpath(res.json(),"$.data.token")[0]
#     return token

pytestmark = pytest.mark.serial

data = read_excel(sheet_name="case1")
# 读取测试用例文件中的全部数据属性保存即可


class TestRunner:
    all = {}

    @pytest.mark.usefixtures("fixture_get_token")
    @pytest.mark.parametrize("case", data)
    def test_case(self,case,clean_db_by_id):
        task_id_list = clean_db_by_id
        #引用全局的all
        extract=TestRunner.all
        # 根据all的值，渲染case
        case=render_obj(case,extract)
        logging.info(f"渲染后的测试用例:{case}")
        # case = eval(Template(str(case)).render(**all))
        #初始化allure 报告
        allure_init(case)

        #核心步骤0:测试用例的描述信息日志

        logging.info(f"0.用例ID:{case['id']}  模块:{case['feature']}  场景:{case['story']}  标题:{case['title']}")

        #核心步骤1：解析请求数据

        request_data=analyse_case(case)

         #核心步骤2：发起请求得到相应结果

        res=send_http_request(**request_data)

        #核心步骤3：提取
        # json提取
        json_extractor(case, extract, res)
        # sql提取
        jdbc_extractor(case, extract)
        # 测试id的提取
        task_id_extractor(task_id_list, extract)

        # 核心步骤4：断言
        # http响应断言
        http_assert(case, res,request_data)
        #sql响应断言
        jdbc_assert(case,extract)












            #此时data中url不存在仅有路径
#部分字符串的值需要变为字典
#预期结果不能在请求中传输


    # @pytest.mark.parametrize("case", case_login)
    # def test_login(self,case):
    #     res=requests.request(**case)
    #     print(res.json())
    #
    # @pytest.mark.parametrize("case",case_statue)
    # def test_list(self,case):
    #     token=get_token()#调用函数拿去token值
    #     case["headers"]={"authorization":f"Bearer {token}"}#组装header让请求头有token
    #     res=requests.request(**case)
    #     print(res.json())

