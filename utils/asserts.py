import logging
from jinja2 import Template

import jsonpath
import json
import allure
from utils.allure_utils import allure_init
from utils.send_request import send_jdbc_request

@allure.step("4.HTTP响应断言")
def http_assert(case, res, request_data=None):
    res_json = res.json()          # ① 只解析一次
    try:
        if case["check"]:
            result_list = jsonpath.jsonpath(res_json, case["check"])
            if not result_list:
                raise AssertionError(
                    f"jsonpath未匹配到数据：路径={case['check']}"
                )
            result = result_list[0]
            logging.info(f"4.HTTP响应: 实际({result}) == 预期({case['expect']})")
            assert str(result) == str(case["expect"]), (
                f"jsonpath校验失败：\n实际: {result}\n预期: {case['expect']}"
            )
        else:
            full_text = json.dumps(res_json, ensure_ascii=False)
            logging.info(f"4.HTTP响应: 预期({case['expect']}) in 实际({full_text})")
            assert case["expect"] in full_text, (
                f"文本包含校验失败：\n预期:{case['expect']}不在响应结果内"
            )
    except AssertionError as e:
        if request_data:
            allure.attach(...)
        allure.attach(json.dumps(res_json, ...), ...)
        allure.attach(f"HTTP断言失败: {e}", ...)
        raise e


def jdbc_assert(case, extract):
    if not (case["sql_check"] and case["sql_expect"]):
        return
    real_sql = None
    result = None
    with allure.step("4.数据库响应断言"):
        try:
            real_sql = Template(case.get("sql_check")).render(**extract)
            result = send_jdbc_request(real_sql)
            logging.info(f"4.JDBC: 实际({result}) == 预期({case['sql_expect']})")
            assert str(result) == str(case["sql_expect"]), (
                f"数据库校验失败：\n实际: {result}\n预期: {case['sql_expect']}"
            )
        except AssertionError as e:
            allure.attach(
                f"SQL: {real_sql or case.get('sql_check')}\n"
                f"预期: {case['sql_expect']}\n"
                f"实际: {result or '无'}",
                name="SQL断言详情",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                f"SQL断言失败: {e}",
                name="SQL断言结果",
                attachment_type=allure.attachment_type.TEXT
            )
            raise e