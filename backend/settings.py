import os
from dotenv import load_dotenv

load_dotenv()

# MySQL 配置
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "task_system")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# 表名（后端用，测试侧如果要读也可以加）
TABLE_TASK = os.getenv("TABLE_TASK", "task")
TABLE_USERS = os.getenv("TABLE_USERS", "users")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
JWT_EXPIRE = int(os.getenv("JWT_EXPIRE", 7200))

# Flask
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"