## 适配 JavaWeb 后端

在 Flask 靶场基础上，同一套框架被复用到自建 JavaWeb 学生成绩管理系统（Spring Boot + MyBatis + MySQL），覆盖 Flask 靶场没有的多角色与权限安全场景：

- **多角色状态流转（case4，串行）**：一条链路内顺序使用 admin / teacher / student 三种角色的独立会话，数据随角色流转——如管理员建班级 → 教师排课/录成绩 → 学生选课/查成绩，验证跨角色的业务状态传递，强依赖顺序，串行执行。
- **越权鉴权用例（case5，并行）**：单角色独立执行，覆盖垂直越权（学生调用管理员接口）、水平越权（教师 A 修改教师 B 数据）、未登录访问等鉴权场景，无依赖可并行。
- **多角色会话管理**：JavaWeb 使用 HttpSession 鉴权，框架用 requests.Session 为 admin / teacher / student 各维护独立会话，模拟真实角色登录态。
- **双重断言**：接口返回校验 + MySQL 落库数据校验；越权被拦截后，额外校验数据库数据未被篡改。
- **权限校验结果**：垂直/水平越权预期返回 403 拦截，并验证服务端未落库。

**前置条件**

JavaWeb 后端独立部署，需先启动学生成绩管理系统（Spring Boot + MySQL），并确保 `.env` 中 `BASE_URL_JAVA`、`JAVA_DB_*` 指向正确的服务地址与数据库。

> JavaWeb 后端仓库地址：[student-management-system](https://gitee.com/S1lenceYYY/student-management-system)

**执行命令**

```bash
# case4 多角色状态流转（串行）
pytest -m "javaweb and serial"

# case5 越权鉴权用例（并行，4 个 worker）
pytest -n 4 -m "javaweb and parallel"

