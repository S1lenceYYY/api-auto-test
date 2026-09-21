import pytest
from utils.auth_utils import create_java_sessions, clean_java_tables


@pytest.fixture(scope="session")
def get_session():
    return create_java_sessions()
    #串行,获取与角色相对应的session,并存入

@pytest.fixture(scope="function")
def get_session_parallel():
    return create_java_sessions()

@pytest.fixture(scope="session")
def clean_db_java():
    yield
    clean_java_tables()

@pytest.fixture(scope="function")
def clean_db_java_parallel():
    yield
    clean_java_tables()






