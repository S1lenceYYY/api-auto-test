import pytest
import subprocess

# 串行：业务链路用例（存在数据依赖，不能并行）
# 并行：无依赖独立接口用例，开启 xdist 多进程执行
if __name__ == '__main__':
    # ====================== 串行执行【默认启用】 ======================
    pytest.main([
        "-vs",
        "./testcases/test_runner.py",
        "--alluredir", "./report/json_report",
        "--clean-alluredir",
        "--allure-no-capture",
    ])
    subprocess.run(
        ["cmd", "/c", "allure", "generate", "./report/json_report",
         "-o", "./report/html_report", "--clean"],
        check=True,
    )

    # ====================== 并行执行【需要时打开注释】 ======================
    # pytest.main([
    #     "-vs",
    #     "-n", "4",
    #     "./testcases/test_parallel.py",
    #     "--alluredir", "./report/json_parallel",
    #     "--clean-alluredir",
    #     "--allure-no-capture",
    # ])
    # subprocess.run(
    #     ["cmd", "/c", "allure", "generate", "./report/json_parallel",
    #      "-o", "./report/html_parallel", "--clean"],
    #     check=True,
    # )