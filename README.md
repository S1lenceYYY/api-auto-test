# 任务管理系统 · 接口自动化测试框架
基于 Python + Pytest 的接口自动化测试框架。被测对象为自建的 Flask 简易后端，用于可控构造测试场景；框架支持 Excel 数据驱动、HTTP + 数据库双重断言、串行与并行执行、Allure 可视化报告，并已部署至阿里云服务器，支持一键部署与测试
## 已适配后端

- **Flask 简易后端**：可控构造测试场景，验证框架基础能力；
- **JavaWeb 学生成绩管理系统**：适配真实业务场景，覆盖多角色状态流转、越权鉴权等安全测试。

> JavaWeb 后端的完整测试流程（抓包 → 接口分析 → 用例设计 → 框架适配 → 缺陷记录 → 回归用例）详见 [student-management-system](https://gitee.com/S1lenceYYY/student-management-system)。

两套后端复用同一套 Excel 数据驱动、断言逻辑、Allure 报告能力，框架通过 `auth_utils` 抽象鉴权差异。

## 技术栈
- **核心**：Python 3.11+ / Pytest / Requests
- **扩展**：pytest-xdist（并行）/ Allure-Pytest（报告）/ Jinja2（动态渲染）/ openpyxl（Excel 驱动）/ pymysql（数据库断言）
- **环境**：Linux / Shell / 阿里云 ECS

## 核心亮点
- **数据驱动**：用例写在 Excel 中，按场景分 Sheet 维护，新增/修改用例无需改代码。
- **双重断言**：接口返回和数据库落库结果都校验，避免“接口返回成功但数据没入库”的漏测。
- **并行执行**：基于 pytest-xdist 多进程并行，function 级后置清理，worker 间数据互不干扰。
- **动态渲染**：用例中的 `{{token}}`、`{{ID}}` 等占位符在执行时动态替换，解决接口间参数传递问题，让链路用例复用同一份 Excel。
- **场景分层**：串行链路、独立正向+反向、边界异常三类用例分开维护，串行用例保证依赖，并行用例提升速度，边界用例展示测试设计。
- **报告可视化**：接入 Allure，用例步骤、请求响应、SQL 断言详情都可在报告中追溯。
- **云端部署 + 一键脚本**：部署至阿里云 Ubuntu，编写 Shell 脚本实现部署、测试自动化
## 性能压测

基于 JMeter 对 Flask 靶场完成10/50/100/150/200 并发阶梯压测，TPS 峰值约 115，拐点在 50 并发。详见 [jmeter/README.md](jmeter/README.md)。
## 项目结构

```text
jkzdh封装/                          # 源代码根目录 (F:\jkzdh封装)
├── backend/                        # 被测系统：Flask 后端
│   ├── settings.py                 # 后端配置（读 .env）
│   └── simulate_back.py            # Flask 服务入口
├── config/                         # 测试侧配置
│   └── config.py                   # 读 .env，暴露数据库/接口常量
├── data/                           # 测试数据
│   └── 用例.xlsx                   # 5 个 Sheet：串行/并行/边界/串行(java)/并行(java)
├── docs/                           # 项目文档
│   ├── allure_serial.png           # 串行报告截图（云端）
│   └── allure_parallel.png         # 并行报告截图（云端）
├── log/                            # 运行日志目录 
│   └── ...                         # 存放执行过程中的日志文件
├── report/                         # 测试报告目录 
│   └── ...                         # 存放 Allure 生成的 HTML 报告
├── scripts/                        # 自动化脚本
│   ├── deploy.sh                   # 日常部署
│   ├── init.sh                     # 首次初始化 
│   └── run_test.sh                 # 测试 + 报告
├── testunion/                      # pytest 测试用例代码总目录 
│   ├── __init__.py                 # 标记为 Python 包
│   ├── flask/                      # Flask 项目测试
│   │   ├── __init__.py
│   │   ├── conftest.py             # Flask 专属 Fixture
│   │   ├── test_parallel.py        # 并行用例（无依赖，可 xdist 多进程）
│   │   └── test_runner.py          # 串行用例（有链路依赖，按顺序执行）
│   └── javaweb/                    # JavaWeb 项目测试 
│       ├── __init__.py
│       ├── conftest.py             # JavaWeb 专属 Fixture（多角色 Session、数据清理）
│       ├── test_java_parallel.py   # JavaWeb 并行用例 
│       └── test_javaweb.py         # JavaWeb 串行用例（登录、越权、双重断言）
├── utils/                          # 工具包
│   ├── __init__.py
│   ├── allure_utils.py             # Allure 报告步骤与附件封装
│   ├── analyse_case.py             # 解析用例，生成请求参数
│   ├── asserts.py                  # HTTP / 数据库断言
│   ├── auth_utils.py               # 鉴权工具模块(简化夹具)
│   ├── excel_utils.py              # Excel 读取
│   ├── extractor.py                # 响应提取：JSONPath / SQL / 参数
│   ├── render_obj.py               # Jinja2 模板渲染
│   └── send_request.py             # 发送 HTTP 请求
├── jmeter                          # JMeter 性能压测（脚本 + HTML 报告）
├── .env                            # 实际环境变量文件 
├── .env.example                    # 环境变量模板
├── .gitignore                      # Git 忽略文件配置
├── init_db.py                      # 数据库初始化脚本
├── pytest.ini                      # pytest 全局配置
├── requirements.txt                # 依赖清单
├── run.py                          # 一键执行入口（默认串行 + Allure 报告）
└── README.md                       # 项目说明文档
```

## Excel 用例划分

`data/用例.xlsx` 分 5 个 Sheet：

| Sheet | 场景 | 执行方式 | 说明 |
|-------|------|---------|------|
| case1 | 串行链路 | 串行 | Flask后端：接口有前后依赖，上一步返回值传给下一步 |
| case2 | 独立用例 | 并行 | Flask后端：无依赖，可并行，覆盖正向和反向场景 |
| case3 | 边界异常 | 串行 | Flask后端：边界值、非法参数，后端不支持的标记不执行 |
| case4 | 多角色状态流转 | 串行 | JavaWeb后端：admin → teacher → student 跨角色链路，数据随角色流转，强依赖顺序 |
| case5 | 越权鉴权用例 | 并行 | JavaWeb后端：垂直越权、水平越权、鉴权校验等独立用例，无依赖多进程执行 |

> case3 用于展示边界和异常场景的测试设计：
> - 当前简易后端实现了部分异常校验，有部分用例能跑通（如 `size` 超限、`status` 非法值）；
> - 其余后端不支持的用例标记为 `is_true=FALSE` 不执行，保留作为测试设计示例；
> - case3 可通过串行方式执行：将 `test_runner.py` 中 `read_excel` 的参数从 `case1` 改为 `case3`。

> case4 / case5 为适配 JavaWeb 后端新增：
> - **case4 多角色状态流转（串行）**：一条链路内依次使用 admin / teacher / student 会话，数据在角色间流转，强依赖执行顺序，必须按序执行；
> - **case5 越权鉴权用例（并行）**：单角色独立用例，相互无依赖，可通过 pytest-xdist 多进程并行提速。




## 环境要求

- Python 3.11+
- MySQL 8.0+
- Allure 命令行（生成 HTML 报告）

## 快速开始（本地部署）

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填写数据库连接信息与密钥：

```bash
cp .env.example .env
```

`.env` 关键项说明：

| 变量 | 说明 |
|------|------|
| DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME | MySQL 连接信息 |
| DB_CHARSET | 数据库字符集，默认 utf8mb4 |
| BASE_URL | 后端服务地址，默认 http://127.0.0.1:5000 |
| FLASK_HOST / FLASK_PORT | 后端服务监听地址和端口 |
| FLASK_DEBUG | 后端 debug 模式 |
| LOGIN_USER / LOGIN_PASSWORD | 自动化登录账号 |
| SECRET_KEY | JWT 密钥，需与后端一致 |
| JWT_EXPIRE | Token 过期时间（秒） |
| VAR_NAME | Excel 中 ID 提取字段的前缀 |
| EXCEL_FILE | Excel 用例文件路径 |

### 3. 初始化数据库

确保 MySQL 已启动，然后执行：

```bash
python init_db.py
```

脚本会自动完成：

- 创建数据库（默认 task_system）
- 创建 users、task 两张表
- 插入默认登录账号

### 4. 启动后端服务

```bash
python backend/simulate_back.py
```

启动成功后，访问 http://127.0.0.1:5000/health   返回 `{"status":"ok"}` 即正常。

### 5. 运行测试

另开一个终端，在项目根目录执行。

**方式一：pytest 命令（快速执行，看终端输出）**

```bash
# 串行链路（读 case1）
pytest -m "serial and flask"

# 并行正向（读 case2，4 个 worker）
pytest -n 4 -m "parallel and flask"
```

**方式二：run.py 一键执行（自动生成 Allure HTML 报告）**

```bash
# 默认执行串行链路用例（读 case1），并生成 Allure HTML 报告
python run.py
```

如需执行并行用例：

1. 注释掉 `run.py` 中串行部分
2. 取消 `run.py` 中并行部分的注释
3. 再次执行 `python run.py`

报告生成位置：

| 模式 | Allure 原始数据 | HTML 报告 |
|------|-----------------|-----------|
| 串行 | `/report/flask_serial/json` | `/report/flask_serial/html` |
| 并行 | `/report/flask_parallel/json` | `/report/flask_parallel/html` |

HTML 报告可直接用浏览器打开。如需临时启动服务查看：

```bash
# 串行
allure serve ./report/flask_serial/json

# 并行
allure serve ./report/flask_parallel/json
```

## 云端部署（阿里云 Ubuntu）
本地跑通后，我把框架部署到了阿里云 Ubuntu 服务器，并编写 Shell 脚本实现一键部署与测试

### 环境准备

```bash
apt update
apt install python3 python3-pip python3.10-venv git vim -y
apt install mysql-server -y
```
### 安装allure命令行
 
```bash
apt install default-jre -y
cd /opt
wget https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.tgz -O allure-2.27.0.tgz
tar -zxvf allure-2.27.0.tgz
ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure
allure --version
```

### 一键脚本

| 脚本 | 职责 |
|---|---|
| `scripts/init.sh` | 首次初始化：建虚拟环境、装依赖、初始化数据库 |
| `scripts/deploy.sh` | 日常部署：拉代码、重启后端、健康检查 |
| `scripts/run_test.sh` | 跑测试 + 生成 Allure 报告，支持串行/并行 |

### 使用方式

```bash
chmod 755 scripts/*.sh

./scripts/init.sh                  # 首次初始化
./scripts/deploy.sh                # 日常部署
./scripts/run_test.sh              # 串行测试 + 报告
./scripts/run_test.sh parallel     # 并行测试 + 报告
```

### 部署流程

```
SSH 登录 → git clone → 配置 .env → init.sh → deploy.sh → run_test.sh
```

## Allure 报告示例

### 串行链路（14 条）

![串行报告](docs/allure_serial.png)

### 并行独立用例（22 条）

![并行报告](docs/allure_parallel.png)

## 适配 JavaWeb 后端

> 以上为框架针对Flask靶系统的基础使用，在此基础上，框架完成对自建 JavaWeb 学生成绩管理系统的扩展适配（Spring Boot + MyBatis + MySQL），覆盖Flask靶场不具备的多角色与权限安全场景：

- **多角色状态流转（case4，串行）**：一条链路内顺序使用 admin / teacher / student 三种角色的独立会话，数据随角色流转——如管理员建班级 → 教师排课/录成绩 → 学生选课/查成绩，验证跨角色的业务状态传递，强依赖顺序，串行执行。
- **越权鉴权用例（case5，并行）**：单角色独立执行，覆盖垂直越权（学生调用管理员接口）、水平越权（教师 A 修改教师 B 数据）、未登录访问等鉴权场景，无依赖可并行。
- **多角色会话管理**：JavaWeb 使用 HttpSession 鉴权，框架用 requests.Session 为 admin / teacher / student 各维护独立会话，模拟真实角色登录态。
- **双重断言**：接口返回校验 + MySQL 落库数据校验；越权被拦截后，额外校验数据库数据未被篡改。
- **权限校验结果**：垂直/水平越权预期返回 403 拦截，并验证服务端未落库。

框架通过 `auth_utils` 抽象了鉴权差异：Flask 端 JWT、JavaWeb 端 HttpSession，两套后端复用同一套 Excel 数据驱动、断言逻辑、Allure 报告能力。


**JavaWeb 执行命令**
```bash
# case4 多角色状态流转（串行）
 pytest -m "javaweb and serial"
```
```bash
# case5 越权鉴权用例（并行，4 个 worker）
 pytest -n 4 -m "javaweb and parallel"
```
执行结果：case4 多角色流转 10 条全过，case5用例 8 条全过




## 踩坑记录

### 一、框架设计

#### 1. 并行数据清理不干净

**现象**：并行执行时，数据库残留用例产生的数据，清不干净。

**排查**：串行清理用全局变量 + `class` 级夹具，能跑通。但并行下发现两个问题：全局变量在 xdist 多进程下每个 worker 各一份，跨 worker 拿不到 ID；`class` 级 teardown 要等整个 class 跑完，并行下清理时机滞后，数据残留。

**解决**：并行清理改成 `function` 级 + 每条用例独立字典，跑完立刻清理，不依赖跨进程共享。串行保持 `class`，因为链路有依赖。

**经验**：fixture scope 要和依赖关系匹配。有依赖用 `class`，独立用 `function`。

#### 2. 提取和断言的执行顺序错误

**现象**：JDBC 数据库断言报 SQL 语法错误。

**排查**：通过日志打印渲染后的用例，观察到 `sql_check` 里 `{{ID}}` 渲染为空，SQL 变成 `WHERE id=`。排除数据库连接和 SQL 书写问题，判定是变量未赋值。进一步排查发现根因是流程顺序错了：原流程是 `渲染 → 请求 → 断言 → 提取`，但 `{{ID}}` 需要从响应提取，提取在断言之后，断言时变量还没写入。

**解决**：改成 `渲染 → 请求 → 提取 → 断言`。`render_obj` 渲染时跳过 `sql_check`，请求后先提取，再在 `jdbc_assert` 里单独渲染 `sql_check`，执行数据库校验。

**经验**：模板变量遵循「先写入，后消费」。变量取不到，先看渲染后的实际语句。

### 二、配置与安全

#### 3. 配置重复与密码明文

**现象**：数据库配置在 `config/config.py` 和 `backend/settings.py` 各写一份，密码明文。

**排查**：改数据库时经常改一处忘另一处，上传 Git 还会泄露密码。

**解决**：统一抽到根目录 `.env`，两处从环境变量读取。`.env` 不提交 Git，仓库只保留 `.env.example` 作为模板。

**经验**：配置和代码分离，敏感信息走环境变量，仓库只提交模板文件。

### 三、部署环境

#### 4. 本地跑通、云端报 Data too long

**现象**：本地 22 条全过，云端 2 条报 `pymysql.err.DataError: (1406, "Data too long for column 'task_name'")`。

**排查**：测试侧 `JSONDecodeError` → 后端返回非 JSON；查 `backend.log` 定位到 `Data too long`；对比两边表结构，本地 `VARCHAR(100)`，云端 `VARCHAR(11)`。

**根因**：`init_db.py` 字段长度写错，`CREATE TABLE IF NOT EXISTS` 不修改已存在的表，本地旧结构掩盖了错误。

**解决**：统一 `init_db.py` 定义，云端 `DROP TABLE` 后重建。

**经验**：本地跑通 ≠ 云端跑通，环境一致性必须显式验证。

## 注意事项

- 后端启动和测试运行需要在两个不同的终端。
- 数据库表名默认为 `task` 和 `users`，当前在后端 SQL 和 Excel 用例中固定。如需修改，请同步修改后端每个接口的 SQL 语句和 Excel 用例中数据库断言里的表名。
- `.env` 含密码，不要提交到 Git，仓库中只保留 `.env.example`。
- 云端部署时，Shell 脚本换行符必须是 LF，否则报 `bad interpreter: /bin/bash^M`。

## 常见问题

| 问题 | 排查方向 |
|------|----------|
| 数据库连接失败 | 检查 `.env` 中账号密码、MySQL 是否启动、端口是否被占用 |
| 表不存在 | 是否执行过 `python init_db.py` |
| 登录失败 | `users` 表中是否有 `LOGIN_USER` 账号，`.env` 与后端 `SECRET_KEY` 是否一致 |
| 并行报错 | 是否已安装 pytest-xdist |
| 云端脚本找不到 venv | 确认 `cd "$(dirname "$0")/.."` 正确，或手动 `cd` 到项目根目录 |
| 云端 `git pull` 冲突 | 用 `git fetch --all && git reset --hard origin/main` 强制同步 |