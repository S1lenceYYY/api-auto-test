
#os.system(命令)==在从，cmd窗口执行命令
#--allureair ./report/test指定一个目录,并生成中间结果
#--clean-alluredir 每次运行清空中间结果
#allure generate 中间结果 -o 目标报告目录 --clean   生成离线报告
#allure serve生成在线
#"--allure-no-capture"取消抓取日志生成log

import pytest
import subprocess

# 串行：业务链路用例（存在数据依赖，不能并行）
# 并行：无依赖独立接口用例，开启xdist多进程执行
if __name__ == '__main__':
    # ====================== 串行执行【默认启用】 ======================
    pytest.main([
        "-vs",
        "./testcases/test_runner.py",
        "--alluredir", "./report/json_report",
        "--clean-alluredir",
        "--allure-no-capture"
    ])
    # 生成串行离线HTML报告（替换os.system）
    subprocess.run(
        ["cmd", "/c", "allure", "generate", "./report/json_report", "-o", "./report/html_report", "--clean"],
        check=True
    )
    # ====================== 并行执行【需要时打开注释】 ======================
    # pytest.main([
    #     "-vs",
    #     "-n", "4",
    #     "./testcases/test_parallel.py",
    #     "--alluredir", "./report/json_parallel",
    #     "--clean-alluredir",
    #     "--allure-no-capture"
    # ])
    # # 生成并行离线HTML报告
    # subprocess.run(
    #     ["cmd", "/c", "allure", "generate", "./report/json_parallel", "-o", "./report/html_parallel", "--clean"],
    #     check=True
    # )



    # # 自动打开并行报告
    # subprocess.run(["allure", "open", "./report/html_parallel"], check=True)
