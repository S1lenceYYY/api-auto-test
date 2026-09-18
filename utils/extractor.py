import logging

import jsonpath
import json
import allure

from config.config import VAR_NAME
from utils.send_request import send_jdbc_request

@allure.step("3.数据提取")
def json_extractor(case,extract,res):
    if case["jsonExData"]:
        with allure.step("3.JSON提取"):
            for key, value in json.loads(case["jsonExData"]).items():
                value_ = jsonpath.jsonpath(res.json(), value)[0]
                extract[key] = value_
            logging.info(f"3.JSON提取,根据{case['jsonExData']}提取数据，此时全局变量为:{extract}")



def jdbc_extractor(case,extract,db_config):
    if case["sqlExData"]:
        with allure.step("3.JDBC提取"):
            for key, value in json.loads(case["sqlExData"]).items():
                value_ = send_jdbc_request(value,db_config)
                extract[key] = value_
                logging.info(f"3.JDBC提取,根据{case['sqlExData']}提取数据，此时全局变量为:{extract}")



def task_id_extractor(task_id_list,extract):
    for key, value in extract.items():
        if key.startswith(VAR_NAME):  # 键名以 ID 开头就提取
            if value not in task_id_list:
                task_id_list.append(value)