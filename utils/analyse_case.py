import json
import logging
from os import name

import allure
from config.config import BASE_URL


@allure.step("1.解析请求函数")
def analyse_case(case):
    method = case["method"]
    url = BASE_URL + case["path"]
    headers = json.loads(case["headers"], strict=False) if isinstance(case["headers"], str) and case["headers"].strip() else None
    params = json.loads(case["params"], strict=False) if isinstance(case["params"], str) and case["params"].strip() else None
    data_ = json.loads(case["data"], strict=False) if isinstance(case["data"], str) and case["data"].strip() else None
    files = json.loads(case["files"], strict=False) if isinstance(case["files"], str) and case["files"].strip() else None
    json_ = json.loads(case["json"], strict=False) if isinstance(case["json"], str) and case["json"].strip() else None
    request_data = {
        "method": method,
        "url": url,
        "params": params,
        "data": data_,
        "json": json_,
        "files": files,
        "headers": headers
    }
    logging.info(f"1.解析请求数据,请求数据为:{request_data}")
    allure.attach(f"{request_data}",name="解析数据结果",attachment_type=allure.attachment_type.TEXT)
    return request_data