#!/bin/bash
set -e

cd "$(dirname "$0")/.."

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "------开始初始化------"

log "------创建虚拟环境------"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    log "虚拟环境创建完成"
else
    log "虚拟环境已存在，跳过"
fi

source venv/bin/activate

log "------安装依赖------"
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple -q
log "依赖安装完成"

log "------检查 .env------"
if [ ! -f ".env" ]; then
    cp .env.example .env
    log "已从模板创建 .env，请手动填写真实值后重新执行"
    exit 1
fi
log ".env 已存在"

log "------初始化数据库------"
python init_db.py

log "===== 初始化完成 ====="