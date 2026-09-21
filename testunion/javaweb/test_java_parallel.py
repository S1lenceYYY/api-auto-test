import logging
import pytest

from config.config import BASE_URL_JAVA, JAVA_DB
from testunion.javaweb.conftest import get_session_parallel
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.allure_utils import allure_init
from utils.extractor import json_extractor, jdbc_extractor, task_id_extractor
from utils.render_obj import render_obj
from utils.send_request import send_http_request

pytestmark = pytest.mark.parallel

data = read_excel(sheet_name="case5")

@pytest.mark.javaweb
class TestRunner:


    @pytest.mark.usefixtures("clean_db_java_parallel")
    @pytest.mark.parametrize("case",data)
    def test_case(self, case, get_session_parallel):
        extract ={}
        extract.update(get_session_parallel)
        case = render_obj(case, extract)
        logging.info(f"渲染后的：   {case}")

        allure_init(case)

        request_data = analyse_case(case,extract,BASE_URL_JAVA)
        res = send_http_request(**request_data)
        request_data.pop("session", None)
        json_extractor(case, extract, res)
        jdbc_extractor(case, extract,JAVA_DB)
        # task_id_extractor(task_id_list, extract)

        http_assert(case, res, request_data)
        jdbc_assert(case, extract,JAVA_DB)
