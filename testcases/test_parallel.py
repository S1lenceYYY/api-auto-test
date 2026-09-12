import logging
import pytest
from utils.allure_utils import allure_init
from utils.extractor import json_extractor, jdbc_extractor, task_id_extractor
from utils.excel_utils import read_excel
from utils.send_request import send_http_request
from utils.asserts import http_assert, jdbc_assert
from utils.render_obj import render_obj
from utils.analyse_case import analyse_case

pytestmark = pytest.mark.parallel


data = read_excel(sheet_name="case2")
class TestRunnerParallel:

    @pytest.mark.parametrize("case", data)
    def test_parallel_case(self,case, get_token_p, clean_db_by_id_p):
        # 拿到夹具产出的id收集列表
        task_id_list = clean_db_by_id_p
        # 初始化上下文
        extract = {"token": get_token_p}
        # 渲染占位符
        case = render_obj(case, extract)
        # 解析用例得到请求参数

        allure_init(case)
        # 核心步骤0:测试用例的描述信息日志
        logging.info(f"0.用例ID:{case['id']}  模块:{case['feature']}  场景:{case['story']}  标题:{case['title']}")

        request_data = analyse_case(case)
        # 发送接口请求
        resp = send_http_request(**request_data)
        # 接口返回值提取，写入extract
        json_extractor(case, extract, resp)
        # sql数据提取
        jdbc_extractor(case, extract)
        # 将extract里的task_id存入收集列表，用于后置删除
        task_id_extractor(task_id_list, extract)
        # 断言
        http_assert(case, resp, extract)
        jdbc_assert(case, extract)
        logging.info(f"已提取的id{task_id_list}")
        logging.info(f"全局变量{extract}")
