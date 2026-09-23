import logging
import pytest

from config.config import BASE_URL_JAVA, JAVA_DB
from framework import Context, BaseRunner
from testunion.javaweb.conftest import get_session
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.allure_utils import allure_init
from utils.extractor import json_extractor, jdbc_extractor, task_id_extractor
from utils.render_obj import render_obj
from utils.send_request import send_http_request

pytestmark = pytest.mark.serial

data = read_excel(sheet_name="case4")

@pytest.mark.javaweb
class TestRunner:


    @pytest.mark.usefixtures("clean_db_java")
    @pytest.mark.parametrize("case",data)
    def test_case(self, case, get_session,serial_context):
        context=serial_context
        context.data.update(get_session)
        runner=BaseRunner(case,context,None,BASE_URL_JAVA,JAVA_DB)
        runner.execute()
