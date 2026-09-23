import pytest
from framework import BaseRunner
from config.config import BASE_URL_JAVA, JAVA_DB
from testunion.javaweb.conftest import get_session_parallel
from utils.excel_utils import read_excel


pytestmark = pytest.mark.parallel

data = read_excel(sheet_name="case5")

@pytest.mark.javaweb
class TestRunner:


    @pytest.mark.usefixtures("clean_db_java_parallel")
    @pytest.mark.parametrize("case",data)
    def test_case(self, case, get_session_parallel,parallel_context):
        context = parallel_context
        context.data.update(get_session_parallel)
        runner = BaseRunner(case, context, None, BASE_URL_JAVA, JAVA_DB)
        runner.execute()