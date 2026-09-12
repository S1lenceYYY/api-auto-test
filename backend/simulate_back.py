from flask import Flask, request, jsonify
import pymysql
import jwt
import time
import logging
from settings import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

SECRET_KEY = SECRET_KEY

# 配置日志
logging.basicConfig(level=logging.INFO)


# ==================== 数据库连接 ====================
def get_db_conn():
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset=DB_CHARSET
    )
    return conn


# ==================== Token校验装饰器 ====================
def token_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"code": 401, "msg": "未携带Token，请先登录"}), 401
        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"code": 401, "msg": "Token无效或已过期"}), 401
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# ==================== 健康检查 ====================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ==================== 登录 ====================
@app.route("/user/login", methods=["POST"])
def login():
    logging.info(f"登录请求: {request.get_json()}")

    req_data = request.get_json()
    username = req_data.get("username")
    password = req_data.get("password")

    if not username or not password:
        return jsonify({"code": 400, "msg": "账号和密码不能为空"}), 400

    conn = get_db_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user_info = cur.fetchone()
    cur.close()
    conn.close()

    if not user_info:
        return jsonify({"code": 400, "msg": "账号密码错误"}), 400

    payload = {
        "username": username,
        "exp": time.time() + JWT_EXPIRE
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"code": 200, "msg": "登录成功", "data": {"token": token}})


# ==================== 新增任务 ====================
@app.route("/task/add", methods=["POST"])
@token_required
def add_task():
    data = request.get_json()
    logging.info(f"新增任务: {data}")

    task_name = data.get("task_name")
    description = data.get("description", "")
    assign_user = data.get("assign_user", "")
    deadline = data.get("deadline")

    if not task_name:
        return jsonify({"code": 400, "msg": "任务名称不能为空"}), 400

    conn = get_db_conn()
    cur = conn.cursor()
    sql = "INSERT INTO task(task_name, description, assign_user, deadline) VALUES(%s,%s,%s,%s)"
    cur.execute(sql, (task_name, description, assign_user, deadline))
    conn.commit()
    new_task_id = cur.lastrowid
    cur.close()
    conn.close()

    return jsonify({"code": 200, "msg": "新增成功", "data": {"id": new_task_id}})


# ==================== 查询单个任务 ====================
@app.route("/task/get/<int:tid>", methods=["GET"])
@token_required
def get_task(tid):
    logging.info(f"查询任务: id={tid}")

    conn = get_db_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM task WHERE id=%s", (tid,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"code": 404, "msg": "任务不存在"}), 404
    return jsonify({"code": 200, "data": row})


# ==================== 分页查询任务列表 ====================
@app.route("/task/list", methods=["GET"])
@token_required
def list_task():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    offset = (page - 1) * size

    logging.info(f"查询任务列表: page={page}, size={size}")

    conn = get_db_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM task LIMIT %s,%s", (offset, size))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"code": 200, "data": rows})


# ==================== 修改任务 ====================
@app.route("/task/update", methods=["PUT"])
@token_required
def update_task():
    data = request.get_json()
    logging.info(f"修改任务: {data}")

    tid = data.get("id")
    task_name = data.get("task_name")
    description = data.get("description")
    assign_user = data.get("assign_user")
    deadline = data.get("deadline")

    if not tid:
        return jsonify({"code": 400, "msg": "任务id不能为空"}), 400
    if not task_name:
        return jsonify({"code": 400, "msg": "任务名称不能为空"}), 400

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM task WHERE id=%s", (tid,))
    exist = cur.fetchone()
    if not exist:
        cur.close()
        conn.close()
        return jsonify({"code": 404, "msg": "任务不存在"}), 404

    sql = "UPDATE task SET task_name=%s, description=%s, assign_user=%s, deadline=%s WHERE id=%s"
    cur.execute(sql, (task_name, description, assign_user, deadline, tid))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"code": 200, "msg": "修改成功"})


# ==================== 更新任务状态 ====================
@app.route("/task/status", methods=["PUT"])
@token_required
def change_status():
    data = request.get_json()
    logging.info(f"更新状态: {data}")

    tid = data.get("id")
    status = data.get("status")
    allow_status_list = ["pending", "doing", "finished", "closed"]

    if not tid:
        return jsonify({"code": 400, "msg": "任务id不能为空"}), 400
    if status not in allow_status_list:
        return jsonify({"code": 400, "msg": "非法任务状态"}), 400

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM task WHERE id=%s", (tid,))
    exist = cur.fetchone()
    if not exist:
        cur.close()
        conn.close()
        return jsonify({"code": 404, "msg": "任务不存在"}), 404

    cur.execute("UPDATE task SET status=%s WHERE id=%s", (status, tid))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"code": 200, "msg": "状态更新成功"})


# ==================== 删除任务 ====================
@app.route("/task/delete/<int:tid>", methods=["DELETE"])
@token_required
def delete_task(tid):
    logging.info(f"删除任务: id={tid}")

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM task WHERE id=%s", (tid,))
    exist = cur.fetchone()
    if not exist:
        cur.close()
        conn.close()
        return jsonify({"code": 404, "msg": "任务不存在"}), 404

    cur.execute("DELETE FROM task WHERE id=%s", (tid,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"code": 200, "msg": "删除成功"})


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)