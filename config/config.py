import os
from dotenv import load_dotenv

load_dotenv()

# Excel 配置
EXCEL_FILE = os.getenv("EXCEL_FILE", "./data/用例.xlsx")

# MySQL 配置
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "task_system")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# 服务地址
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

# 登录账号
INIT_LOGIN_USER = {
    "username": os.getenv("LOGIN_USER", "admin"),
    "password": os.getenv("LOGIN_PASSWORD", ""),
}

# ID 提取前缀
VAR_NAME = os.getenv("VAR_NAME", "ID")