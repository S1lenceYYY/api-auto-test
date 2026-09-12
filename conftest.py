import allure
import requests
import pytest
import pymysql
from config.config import INIT_LOGIN_USER, BASE_URL, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET
from testcases.test_runner import TestRunner
@pytest.fixture(scope="session")
def fixture_get_token():
    with allure.step("前置：登录接口获取token"):
        login_url=f"{BASE_URL}/user/login"
        login_body=INIT_LOGIN_USER
        resp=requests.post(login_url,json=login_body)
        assert resp.status_code == 200, f"登录接口http状态码异常:{resp.status_code}"
        res_json = resp.json()
        assert res_json["code"] == 200, f"登录业务失败，msg:{res_json.get('msg')}"

        # 提取token存入共享上下文字典
        token = res_json["data"]["token"]
        TestRunner.all["token"] = token
    return token


@pytest.fixture(scope="class")
def clean_db_by_id():
    task_id_list=[]
    yield task_id_list
    if not task_id_list:  # 没有任何 ID，直接返回，不连库
        return
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )
    cur = conn.cursor()
    with allure.step("后置：删除本次用例产生的任务数据"):
        for tid in task_id_list:
            cur.execute("DELETE FROM task WHERE id=%s", (tid,))
    conn.commit()

    cur.close()
    conn.close()

@pytest.fixture(scope="session")
def get_token_p():
    with allure.step("前置：登录接口获取token"):
        login_url=f"{BASE_URL}/user/login"      #并行用于每次获取token
        login_body=INIT_LOGIN_USER
        resp=requests.post(login_url,json=login_body)
        assert resp.status_code == 200, f"登录接口http状态码异常:{resp.status_code}"
        res_json = resp.json()
        assert res_json["code"] == 200, f"登录业务失败，msg:{res_json.get('msg')}"
        token_str = resp.json()["data"]["token"]
    return token_str

@pytest.fixture(scope="function")
def clean_db_by_id_p():
    task_id_list=[]
    yield task_id_list
    if not task_id_list:  # 没有任何 ID，直接返回，不连库
        return
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )
    cur = conn.cursor()
    with allure.step("后置：删除本次用例产生的任务数据"):
        for tid in task_id_list:
            cur.execute("DELETE FROM task WHERE id=%s", (tid,))
    conn.commit()
    cur.close()
    conn.close()