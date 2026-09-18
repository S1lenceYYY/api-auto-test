
import pytest


from utils.auth_utils import create_flask_token, clean_db_flask


@pytest.fixture(scope="session")
def fixture_get_token():
    #串行：登录获取 token，存入共享上下文 TestRunner.all
    return create_flask_token()




@pytest.fixture(scope="session")
def get_token_p():
    #并行：每个 worker 独立登录获取 token
    return create_flask_token()


@pytest.fixture(scope="class")
def clean_db_by_id():
    # 串行：class 级后置清理，整个 class 跑完统一删除
    task_id_list = []
    yield task_id_list
    clean_db_flask(task_id_list)


@pytest.fixture(scope="function")
def clean_db_by_id_p():
    #并行：function 级后置清理，每条用例独立删除
    task_id_list = []
    yield task_id_list
    clean_db_flask(task_id_list)