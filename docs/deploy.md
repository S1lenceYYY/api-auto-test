## 云端部署（阿里云 Ubuntu）

本地跑通后，框架已部署至阿里云 Ubuntu 服务器，并编写 Shell 脚本实现一键部署与测试。

### 环境准备

```bash
apt update
apt install python3 python3-pip python3-venv git vim -y
apt install mysql-server -y
```

# Allure 依赖 Java 运行时
```bash
apt install default-jre -y
```

# 下载并安装 Allure 2.27.0

```bash
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
./scripts/run_test.sh              # 串行测试 + 报告(flask)
./scripts/run_test.sh parallel     # 并行测试 + 报告(flask)
```

### 部署流程

```
SSH 登录 → git clone → 配置 .env → init.sh → deploy.sh → run_test.sh
```