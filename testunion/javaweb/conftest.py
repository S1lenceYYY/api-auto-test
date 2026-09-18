import pytest
import allure
import requests
import pymysql
from config.config import BASE_URL_JAVA, LOGIN_USER_JAVA, CLEAN_TABLES, JAVA_DB, CLEAN_MARK
from utils.auth_utils import create_java_sessions


@pytest.fixture(scope="session")
def get_session():
    return create_java_sessions()
    #串行,获取与角色相对应的session,并存入

@pytest.fixture(scope="function")
def get_session_p():
    return create_java_sessions()

@pytest.fixture(scope="function")
def clean_db_java():
    yield
    conn = pymysql.connect(
        host=JAVA_DB["host"],
        port=JAVA_DB["port"],
        user=JAVA_DB["user"],
        password=JAVA_DB["password"],
        database=JAVA_DB["database"],
        charset=JAVA_DB["charset"],
    )
    cur =conn.cursor()
    with allure.step("后置：删除本次用例产生的带标记的数据"):
        for table,field in CLEAN_TABLES.items():
            cur.execute(f"DELETE FROM {table} WHERE {field} LIKE %s", (f"{CLEAN_MARK}%",))






