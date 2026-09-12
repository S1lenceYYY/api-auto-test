import logging
import pytest

from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.allure_utils import allure_init
from utils.extractor import json_extractor, jdbc_extractor, task_id_extractor
from utils.render_obj import render_obj
from utils.send_request import send_http_request

pytestmark = pytest.mark.serial

data = read_excel(sheet_name="case1")


class TestRunner:
    all = {}

    @pytest.mark.usefixtures("fixture_get_token")
    @pytest.mark.parametrize("case", data)
    def test_case(self, case, clean_db_by_id):
        task_id_list = clean_db_by_id
        extract = TestRunner.all
        case = render_obj(case, extract)

        allure_init(case)
        logging.info(f"0.用例ID:{case['id']}  模块:{case['feature']}  场景:{case['story']}  标题:{case['title']}")

        request_data = analyse_case(case)
        res = send_http_request(**request_data)

        json_extractor(case, extract, res)
        jdbc_extractor(case, extract)
        task_id_extractor(task_id_list, extract)

        http_assert(case, res, request_data)
        jdbc_assert(case, extract)