import logging
from logging import info

import allure
import requests
import pymysql

from config.config import *


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    res = requests.request(**request_data)
    logging,info(f"2.发送HTTP请求,响应文本:{res.json()}")
    return res


def send_jdbc_request(sql,index=0):
    conn = pymysql.connect(  # 开桥连接
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )
    cur = conn.cursor()  # 把驴牵出来
    cur.execute(sql)
    result = cur.fetchone()  # 拿取一行结果
    cur.close()  # 把驴牵回去
    conn.close()
    return result[index]