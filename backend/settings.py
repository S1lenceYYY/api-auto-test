import os
from dotenv import load_dotenv

load_dotenv()

# ============== Flask 服务配置 ====================
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"


# ============== Flask 数据库配置 ==================
DB_HOST = os.getenv("FLASK_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("FLASK_DB_PORT", 3306))
DB_NAME = os.getenv("FLASK_DB_NAME", "task_system")
DB_USER = os.getenv("FLASK_DB_USER", "root")
DB_PASSWORD = os.getenv("FLASK_DB_PASSWORD", "")
DB_CHARSET = os.getenv("FLASK_DB_CHARSET", "utf8mb4")


# ============== Flask 数据表名 ====================
FLASK_USER_TABLE = os.getenv("FLASK_USER_TABLE", "users")
FLASK_TASK_TABLE = os.getenv("FLASK_TASK_TABLE", "task")


# ============== JWT 配置 ==========================
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
JWT_EXPIRE = int(os.getenv("JWT_EXPIRE", 7200))