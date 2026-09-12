import logging

import allure
import pymysql
import requests

from config.config import *


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    res = requests.request(**request_data)
    logging.info(f"2.发送HTTP请求,响应文本:{res.json()}")
    return res


def send_jdbc_request(sql, index=0):
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET,
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[index]