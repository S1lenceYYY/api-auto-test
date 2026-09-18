import os
from dotenv import load_dotenv

load_dotenv()

# ============== 通用配置 ==========================
EXCEL_FILE = os.getenv("EXCEL_FILE", "./data/用例.xlsx")
VAR_NAME = os.getenv("VAR_NAME", "ID")

# ============== Flask 项目配置 ====================

# Flask 服务地址
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

# Flask 登录账号
LOGIN_USER_FLASK = {
    "username": os.getenv("LOGIN_USER", "admin"),
    "password": os.getenv("LOGIN_PASSWORD", ""),
}

# Flask 数据库配置
FLASK_DB = {
    "host": os.getenv("FLASK_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("FLASK_DB_PORT", 3306)),
    "database": os.getenv("FLASK_DB_NAME", "task_system"),
    "user": os.getenv("FLASK_DB_USER", "root"),
    "password": os.getenv("FLASK_DB_PASSWORD", "123456"),
    "charset": os.getenv("FLASK_DB_CHARSET", "utf8mb4"),
}

# Flask 数据表名
FLASK_TASK_TABLE = os.getenv("FLASK_TASK_TABLE", "task")


# ============== JavaWeb 项目配置 ==================

# JavaWeb 服务地址
BASE_URL_JAVA = os.getenv("BASE_URL_JAVA", "http://127.0.0.1:8080")

# JavaWeb 登录账号（多角色）
LOGIN_USER_JAVA = {
    "admin": {
        "username": os.getenv("JAVA_ADMIN_USERNAME", "admin"),
        "password": os.getenv("JAVA_ADMIN_PASSWORD", "admin123"),
    },
    "teacher": {
        "username": os.getenv("JAVA_TEACHER_USERNAME", "teacher1"),
        "password": os.getenv("JAVA_TEACHER_PASSWORD", "teacher123"),
    },
    "student": {
        "username": os.getenv("JAVA_STUDENT_USERNAME", "student1"),
        "password": os.getenv("JAVA_STUDENT_PASSWORD", "student123"),
    },
}

# JavaWeb 数据库配置
JAVA_DB = {
    "host": os.getenv("JAVA_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("JAVA_DB_PORT", 3306)),
    "database": os.getenv("JAVA_DB_NAME", "student_management"),
    "user": os.getenv("JAVA_DB_USER", "root"),
    "password": os.getenv("JAVA_DB_PASSWORD", "123456"),
    "charset": os.getenv("JAVA_DB_CHARSET", "utf8mb4"),
}

# JavaWeb 数据表名
JAVA_CLASS_TABLE = os.getenv("JAVA_CLASS_TABLE", "class")
JAVA_SCORE_TABLE = os.getenv("JAVA_SCORE_TABLE", "score")
JAVA_COURSE_TABLE = os.getenv("JAVA_COURSE_TABLE", "course")

#清理数据标记
CLEAN_TABLES = {
    "class": os.getenv("JAVA_CLEAN_CLASS_FIELD", "class_name"),
    "score": os.getenv("JAVA_CLEAN_SCORE_FIELD", "remark"),
    "course": os.getenv("JAVA_CLEAN_COURSE_FIELD", "course_name"),
}

CLEAN_MARK=os.getenv("CLEAN_MARK", "TEST")