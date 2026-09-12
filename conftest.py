import allure
import pymysql
import pytest
import requests

from config.config import (
    INIT_LOGIN_USER, BASE_URL,
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET,
)
from testcases.test_runner import TestRunner


@pytest.fixture(scope="session")
def fixture_get_token():
    #串行：登录获取 token，存入共享上下文 TestRunner.all
    with allure.step("前置：登录接口获取 token"):
        login_url = f"{BASE_URL}/user/login"
        resp = requests.post(login_url, json=INIT_LOGIN_USER)
        assert resp.status_code == 200, f"登录接口 http 状态码异常:{resp.status_code}"
        res_json = resp.json()
        assert res_json["code"] == 200, f"登录业务失败，msg:{res_json.get('msg')}"
        token = res_json["data"]["token"]
        TestRunner.all["token"] = token
    return token


@pytest.fixture(scope="session")
def get_token_p():
    #并行：每个 worker 独立登录获取 token
    with allure.step("前置：登录接口获取 token"):
        login_url = f"{BASE_URL}/user/login"
        resp = requests.post(login_url, json=INIT_LOGIN_USER)
        assert resp.status_code == 200, f"登录接口 http 状态码异常:{resp.status_code}"
        res_json = resp.json()
        assert res_json["code"] == 200, f"登录业务失败，msg:{res_json.get('msg')}"
    return res_json["data"]["token"]


@pytest.fixture(scope="class")
def clean_db_by_id():
    #串行：class 级后置清理，整个 class 跑完统一删除
    task_id_list = []
    yield task_id_list

    if not task_id_list:
        return
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET,
    )
    cur = conn.cursor()
    with allure.step("后置：删除本次用例产生的任务数据"):
        for tid in task_id_list:
            cur.execute("DELETE FROM task WHERE id=%s", (tid,))
    conn.commit()
    cur.close()
    conn.close()


@pytest.fixture(scope="function")
def clean_db_by_id_p():
    #并行：function 级后置清理，每条用例独立删除
    task_id_list = []
    yield task_id_list

    if not task_id_list:
        return
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET,
    )
    cur = conn.cursor()
    with allure.step("后置：删除本次用例产生的任务数据"):
        for tid in task_id_list:
            cur.execute("DELETE FROM task WHERE id=%s", (tid,))
    conn.commit()
    cur.close()
    conn.close()