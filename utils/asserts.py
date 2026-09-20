import json
import logging

import allure
import jsonpath
from jinja2 import Template

from utils.send_request import send_jdbc_request


@allure.step("4.HTTP响应断言")
def http_assert(case, res, request_data=None):
    res_json = res.json()
    check = case.get("check")
    expect = case.get("expect")

    if check:
        result_list = jsonpath.jsonpath(res_json, check)
        actual = result_list[0] if result_list else None
    else:
        actual = json.dumps(res_json, ensure_ascii=False)

    allure.attach(
        f"断言字段: {check or '文本包含'}\n"
        f"预期: {expect}\n"
        f"实际: {actual}",
        name="HTTP断言详情",
        attachment_type=allure.attachment_type.TEXT,
    )

    try:
        if check:
            result_list = jsonpath.jsonpath(res_json, check)
            if not result_list:
                raise AssertionError(f"jsonpath未匹配到数据：路径={check}")
            result = result_list[0]
            logging.info(f"4.HTTP响应: 实际({result}) == 预期({expect})")
            assert str(result) == str(expect), (
                f"jsonpath校验失败：\n实际: {result}\n预期: {expect}"
            )
        else:
            full_text = json.dumps(res_json, ensure_ascii=False)
            logging.info(f"4.HTTP响应: 预期({expect}) in 实际({full_text})")
            assert expect in full_text, (
                f"文本包含校验失败：\n预期:{expect}不在响应结果内"
            )
    except AssertionError as e:
        if request_data:
            allure.attach(
                json.dumps(request_data, ensure_ascii=False),
                name="请求参数",
                attachment_type=allure.attachment_type.JSON,
            )
        allure.attach(
            json.dumps(res_json, ensure_ascii=False),
            name="响应结果",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            f"HTTP断言失败: {e}",
            name="HTTP断言结果",
            attachment_type=allure.attachment_type.TEXT,
        )
        raise e


def jdbc_assert(case, extract,db_config):
    if case.get("sql_check") in (None, "", "None") or case.get("sql_expect") in (None, "", "None"):
        return

    real_sql = None
    result = None
    with allure.step("4.数据库响应断言"):
        real_sql = Template(case.get("sql_check")).render(**extract)
        real_check = Template(str(case.get("sql_expect"))).render(**extract)
        result = send_jdbc_request(real_sql,db_config)

        allure.attach(
            f"SQL: {real_sql}\n"
            f"预期: {real_check}\n"
            f"实际: {result}",
            name="SQL断言详情",
            attachment_type=allure.attachment_type.TEXT,
        )

        logging.info(f"4.JDBC: 实际({result}) == 预期({real_check})")

        try:
            assert str(result) == str(real_check), (
                f"数据库校验失败：\n实际: {result}\n预期: {real_check}"
            )
        except AssertionError as e:
            allure.attach(
                f"SQL断言失败: {e}",
                name="SQL断言结果",
                attachment_type=allure.attachment_type.TEXT,
            )
            raise e