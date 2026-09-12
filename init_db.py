"""
数据库初始化脚本
用法：python init_db.py
"""
import os
import re
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "task_system")
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

TABLE_TASK = os.getenv("TABLE_TASK", "task")
TABLE_USERS = os.getenv("TABLE_USERS", "users")

LOGIN_USER = os.getenv("LOGIN_USER", "admin")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "123456")


def safe_table(name):
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
        raise ValueError(f"非法表名: {name}")
    return name


def main():
    task = safe_table(TABLE_TASK)
    users = safe_table(TABLE_USERS)

    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset=DB_CHARSET,
    )
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARSET utf8mb4")
    cur.execute(f"USE {DB_NAME}")

    # users 表：按真实结构
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {users} (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(11) NOT NULL
    )
    """)

    # task 表：按真实结构
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {task} (
        id INT PRIMARY KEY AUTO_INCREMENT,
        task_name VARCHAR(11) NOT NULL,
        description TEXT,
        assign_user VARCHAR(50),
        deadline DATETIME,
        status VARCHAR(20) DEFAULT 'pending',
        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)

    # 初始化登录账号
    cur.execute(f"SELECT id FROM {users} WHERE username=%s", (LOGIN_USER,))
    if not cur.fetchone():
        cur.execute(
            f"INSERT INTO {users}(username, password) VALUES(%s, %s)",
            (LOGIN_USER, LOGIN_PASSWORD),
        )
        print(f"已创建默认用户: {LOGIN_USER} / {LOGIN_PASSWORD}")
    else:
        print(f"用户已存在: {LOGIN_USER}")

    conn.commit()
    cur.close()
    conn.close()

    print("数据库初始化完成")
    print(f"库名: {DB_NAME}")
    print(f"表: {users}, {task}")


if __name__ == "__main__":
    main()