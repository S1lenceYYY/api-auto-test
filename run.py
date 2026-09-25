import pytest
import subprocess

# 串行：业务链路用例（存在数据依赖，不能并行）
# 并行：无依赖独立接口用例，开启 xdist 多进程执行
if __name__ == '__main__':
    #====================== Flask 串行 ======================
    pytest.main([
        "-vs",
        "testunion/flask/test_runner.py",
        "--alluredir", "./report/flask_serial/json",
        "--clean-alluredir",
        "--allure-no-capture",
    ])
    subprocess.run(
        ["cmd", "/c", "allure", "generate", "./report/flask_serial/json",
         "-o", "./report/flask_serial/html", "--clean"],
        check=True,
    )

    # ====================== Flask 并行【需要时打开注释】 ======================
    # pytest.main([
    #     "-vs",
    #     "-n", "4",
    #     "testunion/flask/test_parallel.py",
    #     "--alluredir", "./report/flask_parallel/json",
    #     "--clean-alluredir",
    #     "--allure-no-capture",
    # ])
    # subprocess.run(
    #     ["cmd", "/c", "allure", "generate", "./report/flask_parallel/json",
    #      "-o", "./report/flask_parallel/html", "--clean"],
    #     check=True,
    # )


# =============================Javaweb===========================
# pytest -m "javaweb and serial" --alluredir=./report/java_serial/json --clean-alluredir;
# allure generate ./report/java_serial/json -o ./report/java_serial/html --clean

# pytest -n 4 -m "javaweb and parallel" --alluredir=./report/java_parallel/json --clean-alluredir;
# allure generate ./report/java_parallel/json -o ./report/java_parallel/html --clean