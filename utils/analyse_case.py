import json
import logging
import requests
import allure
from config.config import BASE_URL


@allure.step("1.解析请求函数")
def analyse_case(case,extract,URL_BASE=BASE_URL):
    method = case["method"]
    url = URL_BASE + case["path"]
    headers = json.loads(case.get("headers"), strict=False) if isinstance(case.get("headers"), str) and case.get("headers").strip() else None
    params = json.loads(case["params"], strict=False) if isinstance(case["params"], str) and case["params"].strip() else None
    data_ = json.loads(case["data"], strict=False) if isinstance(case["data"], str) and case["data"].strip() else None
    files = json.loads(case["files"], strict=False) if isinstance(case["files"], str) and case["files"].strip() else None
    json_ = json.loads(case["json"], strict=False) if isinstance(case["json"], str) and case["json"].strip() else None
    session=None
    session_key=case.get("session")
    if session_key and extract:
        session=extract.get(session_key)
        if not isinstance(session, requests.Session):
            session = None

    request_data = {
        "method": method,
        "url": url,
        "params": params,
        "data": data_,
        "json": json_,
        "files": files,
        "headers": headers,
    }
    logging.info(f"1.解析请求数据,请求数据为:{request_data}")
    allure.attach(f"{request_data}",name="解析数据结果",attachment_type=allure.attachment_type.TEXT)
    request_data["session"] = session
    return request_data