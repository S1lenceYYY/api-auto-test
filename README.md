# 任务管理系统 · 接口自动化测试框架

基于 Python + Pytest 的接口自动化测试框架。被测对象为自建的 Flask 简易后端，用于可控构造测试场景；框架支持 Excel 数据驱动、HTTP + 数据库双重断言、串行与并行执行、Allure 可视化报告。

## 技术栈

Python 3.11+ | Pytest | pytest-xdist | Allure-Pytest | Requests | Jinja2 | openpyxl | pymysql

## 核心亮点

- **数据驱动**：用例写在 Excel 中，按场景分 Sheet 维护，新增/修改用例无需改代码。
- **双重断言**：接口返回和数据库落库结果都校验，避免“接口返回成功但数据没入库”的漏测。
- **并行执行**：基于 pytest-xdist 多进程并行，function 级后置清理，worker 间数据互不干扰。
- **动态渲染**：用例中的 `{{token}}`、`{{ID}}` 等占位符在执行时动态替换，解决接口间参数传递问题，让链路用例复用同一份 Excel。
- **场景分层**：串行链路、独立正向、边界异常三类用例分开维护，串行用例保证依赖，并行用例提升速度，边界用例展示测试设计。
- **报告可视化**：接入 Allure，用例步骤、请求响应、SQL 断言详情都可在报告中追溯。

## 踩坑记录

**1. 并行数据清理不干净**

初期并行执行时数据库残留用例数据，排查发现两个原因：

- 提取逻辑用 `if "ID" in extract` 判断，`ID_a` 这类带后缀的键被直接拦截，ID 收集不到。
- 每个 xdist worker 的 `task_id_list` 独立，跨 worker 数据互相看不见。

最终改为遍历所有键、按前缀匹配收集，并在清理前加空列表短路，避免无意义连库。

**2. 配置重复与密码明文**

项目初期数据库配置在 `config/config.py` 和 `backend/settings.py` 各写一份，且密码明文。后统一抽到根目录 `.env`，两处配置都从环境变量读取，`.env` 不提交 Git，仓库只保留 `.env.example`。

## 项目结构

```text
jkzdh封装/
├── backend/                        # 被测系统：Flask 后端
│   ├── settings.py                 # 后端配置（读 .env）
│   └── simulate_back.py            # Flask 服务入口
├── config/                         # 测试侧配置
│   └── config.py                   # 读 .env，暴露数据库/接口常量
├── data/                           # 测试数据
│   └── 用例.xlsx                   # 3 个 Sheet：串行 / 并行 / 边界
├── testcases/                      # pytest 用例代码
│   ├── test_runner.py              # 串行链路
│   └── test_parallel.py            # 独立正向并行
├── utils/                          # 工具包
│   ├── excel_utils.py              # Excel 读取
│   ├── allure_utils.py             # Allure 报告步骤与附件封装
│   ├── analyse_case.py             # 解析用例，生成请求参数
│   ├── extractor.py                # 响应提取：JSONPath / SQL / 参数
│   ├── render_obj.py               # Jinja2 模板渲染
│   ├── send_request.py             # 发送 HTTP 请求
│   └── asserts.py                  # HTTP / 数据库断言
├── init_db.py                      # 数据库初始化脚本
├── run.py                          # 一键执行入口（默认串行 + Allure 报告）
├── conftest.py                     # fixture：token、数据清理
├── pytest.ini                      # pytest 全局配置
├── requirements.txt                # 依赖清单
├── .env.example                    # 环境变量模板
└── README.md
```
## Excel 用例划分

`data/用例.xlsx` 分 3 个 Sheet：

| Sheet | 场景 | 说明 |
|-------|------|------|
| case1 | 串行链路 | 接口有前后依赖，上一步返回值传给下一步 |
| case2 | 独立正向 | 用例之间无依赖，可并行执行 |
| case3 | 边界异常 | 边界值、非法参数、越权场景，展示测试设计 |

> `case3` 用于展示异常场景的测试设计，包含边界值、非法参数、越权等用例。
> 当前简易后端仅实现正向业务，未实现参数校验和权限拦截，因此该组用例**默认不参与回归**，仅作为测试设计示例保留。
> 框架本身具备完整的异常场景执行、双重断言能力，待后端完善后可直接启用。


## 环境要求

- Python 3.11+
- MySQL 8.0+

## 快速开始

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
| LOGIN_USER / LOGIN_PASSWORD | 自动化登录账号 |
| SECRET_KEY | JWT 密钥，需与后端一致 |
| JWT_EXPIRE | Token 过期时间（秒） |
| VAR_NAME | Excel 中 ID 提取字段的前缀 |
| EXCEL_FILE | Excel 用例文件路径 |
| SHEET_NAME | 默认读取的 Sheet 名 |

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

启动成功后，访问 http://127.0.0.1:5000/health，返回 `{"status":"ok"}` 即正常。

### 5. 运行测试

另开一个终端，在项目根目录执行。

**方式一：pytest 命令（快速执行，看终端输出）**

```bash
# 串行链路（读 case1）
pytest -m serial
```
```bash
# 并行正向（读 case2，4 个 worker）
pytest -m parallel -n 4
```

**方式二：run.py  一键执行（自动生成 Allure HTML 报告）**

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
| 串行 | `report/json_report` | `report/html_report` |
| 并行 | `report/json_parallel` | `report/html_parallel` |

HTML 报告可直接用浏览器打开。如需临时启动服务查看：

串行：

```bash
allure serve ./report/json_report
```

并行：

```bash
allure serve ./report/json_parallel
```
## 注意事项

- 后端启动和测试运行需要在两个不同的终端。
- 数据库表名默认为 task 和 users。如需修改，请同步修改：
  1. `.env` 中的 TABLE_TASK / TABLE_USERS
  2. Excel 用例中数据库断言里的表名
- `.env` 含密码，不要提交到 Git，仓库中只保留 `.env.example`。
- 若使用 PyCharm，请确认项目解释器与终端 pip 指向同一个 Python 环境，避免出现“包已安装但 IDE 报未安装”的问题。

## 常见问题

| 问题 | 排查方向 |
|------|----------|
| 数据库连接失败 | 检查 `.env` 中账号密码、MySQL 是否启动、端口是否被占用 |
| 表不存在 | 是否执行过 `python init_db.py` |
| 登录失败 | users 表中是否有 LOGIN_USER 账号，`.env` 与后端 SECRET_KEY 是否一致 |
| 并行报错 | 是否已安装 pytest-xdist |
| IDE 提示包未安装 | 确认 PyCharm 解释器与终端 pip 指向同一环境 |