#!/bin/bash
set -e

cd "$(dirname "%0")/.."
source  venv/bin/active

log(){
  echo "[$(date '+%Y-%m-%d %H:%M:S')] $1"
}

START=$(date +%s)

log "------开始部署------"


log "------1.拉取代码------"
git pull

log "------2.安装依赖------"
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple -q

log "------3.重启后端------"
pkill -f simulate_back || true
nohup python backend/simulate_backe.py > simulate.log 2>&1 &
sleep2

log "------4.健康检查------"
curl -f http://127.0.0.1:5000/health || { log "后端启动失败"; exit 1; }

log "------部署完成，耗时$((END - START))秒------"

