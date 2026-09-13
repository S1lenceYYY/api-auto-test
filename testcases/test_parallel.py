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
    def test_parallel_case(self, case, get_token_p, clean_db_by_id_p):
        task_id_list = clean_db_by_id_p
        extract = {"token": get_token_p}
        case = render_obj(case, extract)

        allure_init(case)
        logging.info(f"0.用例ID:{case['id']}  模块:{case['feature']}  场景:{case['story']}  标题:{case['title']}")

        request_data = analyse_case(case)
        resp = send_http_request(**request_data)
        json_extractor(case, extract, resp)
        jdbc_extractor(case, extract)
        # 收集本用例产生的 ID，供后置清理
        task_id_extractor(task_id_list, extract)

        http_assert(case, resp, extract)
        jdbc_assert(case, extract)