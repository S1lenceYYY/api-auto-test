import logging

import allure
import pymysql
import requests

from config.config import *


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    session = request_data.pop("session", None)
    if isinstance(session,requests.Session):
        res=session.request(**request_data)
    else:
        res = requests.request(**request_data)
    logging.info(f"2.发送HTTP请求,响应文本:{res.json()}")
    return res


def send_jdbc_request(sql,db_config, index=0):
    conn = pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        charset=db_config["charset"],
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[index]