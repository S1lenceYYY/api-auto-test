import pytest
from config.config import FLASK_DB, BASE_URL
from framework import BaseRunner
from utils.excel_utils import read_excel

pytestmark = pytest.mark.parallel

data = read_excel(sheet_name="case2")

@pytest.mark.flask
class TestRunnerParallel:

    @pytest.mark.parametrize("case", data)
    def test_parallel_case(self, case, get_token_parallel, clean_db_by_id_parallel,parallel_context):
        task_id_list = clean_db_by_id_parallel
        context=parallel_context
        context.set("token",get_token_parallel)
        runner=BaseRunner(case,context,task_id_list,BASE_URL,FLASK_DB)
        runner.execute()
