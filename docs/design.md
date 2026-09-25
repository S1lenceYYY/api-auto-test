## 框架设计

### 1. 六层架构

框架分为六层，每层职责单一：

| 层级 | 职责 | 核心类 |
|------|------|--------|
| 上下文层 | 数据存储与传递 | `Context` |
| 数据层 | Excel 读取 + Jinja2 渲染 | `DataProvider` |
| 执行层 | HTTP 请求发送 + 参数清理 | `HttpClient` |
| 提取层 | 响应 / 数据库双通道提取 | `DataExtractor` |
| 断言层 | HTTP 响应 + 数据库落库断言 | `AssertionEngine` |
| 协调层 | 流程编排 + 依赖注入 | `BaseRunner` |

- 多项目复用：Flask 和 JavaWeb 共用 `BaseRunner.execute()`。

### 2. 工具层与框架层的分工

- **工具层（`utils/`）**：单一职责的具体动作，如 `render_obj`、`send_request`、`http_assert`。
- **框架层（`framework.py`）**：流程编排和分层架构。

框架层调用工具层，工具层不依赖框架层。

### 3. 串行 / 并行 Context 策略

| 场景 | Context scope | 原因 |
|------|---------------|------|
| 并行用例 | `function` | 每条用例独立，互不依赖 |
| 串行链路 | `class` | 类内共享，链路数据传递 |

`pytest-xdist` 多进程下，每个 Worker 有独立的 Fixture 实例，天然隔离。

### 4. 两阶段渲染

- **请求前渲染**：URL、Headers、JSON Body。
- **断言前渲染**：SQL 断言字段。

`sql_check` 里的 `{{ID}}` 需要在请求后提取，请求前渲染时变量还不存在，所以 `render_obj` 跳过 `sql_check`，等 `DataExtractor` 提取后再在 `jdbc_assert` 里单独渲染。

## 踩坑记录


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
