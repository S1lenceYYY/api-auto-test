import allure
import requests
import pymysql
from config.config import LOGIN_USER_JAVA, BASE_URL_JAVA, BASE_URL, LOGIN_USER_FLASK, FLASK_DB, FLASK_TASK_TABLE, \
    JAVA_DB, CLEAN_TABLES, CLEAN_MARK


def create_java_sessions():
    session_list = {}
    with allure.step("前置:登录获取session"):
        login_url = f"{BASE_URL_JAVA}/student-system/login"
        for role, account in LOGIN_USER_JAVA.items():
            session = requests.Session()
            res = session.post(login_url, data=account)
            assert res.status_code == 200, f"登录接口 http 状态码异常:{res.status_code}"
            assert res.json()["code"] == 200, f"登录业务失败，msg:{res.json().get('msg')}"
            session_list[f"session_{role}"] = session
    return session_list

def create_flask_token():
    with allure.step("前置：登录接口获取 token"):
        login_url = f"{BASE_URL}/user/login"
        resp = requests.post(login_url, json=LOGIN_USER_FLASK)
        assert resp.status_code == 200, f"登录接口 http 状态码异常:{resp.status_code}"
        res_json = resp.json()
        assert res_json["code"] == 200, f"登录业务失败，msg:{res_json.get('msg')}"
    return res_json["data"]["token"]

def clean_db(task_id_list):
    if not task_id_list:
        return
    conn = pymysql.connect(
        host=FLASK_DB["host"],
        port=FLASK_DB["port"],
        user=FLASK_DB["user"],
        password=FLASK_DB["password"],
        database=FLASK_DB["database"],
        charset=FLASK_DB["charset"],
    )
    cur = conn.cursor()
    with allure.step("后置：删除本次用例产生的任务数据"):
        for tid in task_id_list:
            cur.execute(f"DELETE FROM {FLASK_TASK_TABLE} WHERE id=%s", (tid,))
    conn.commit()
    cur.close()
    conn.close()

def clean_java_tables():
    conn = pymysql.connect(
        host=JAVA_DB["host"],
        port=JAVA_DB["port"],
        user=JAVA_DB["user"],
        password=JAVA_DB["password"],
        database=JAVA_DB["database"],
        charset=JAVA_DB["charset"],
    )
    cur = conn.cursor()
    with allure.step("后置：删除本次用例产生的带标记的数据"):
        for table, field in CLEAN_TABLES.items():
            cur.execute(f"DELETE FROM {table} WHERE {field} LIKE %s", (f"{CLEAN_MARK}%",))
            conn.commit()
    cur.close()
    conn.close()