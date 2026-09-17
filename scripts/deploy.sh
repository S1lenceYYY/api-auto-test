#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source venv/bin/activate

echo "----1.拉取代码----"
git pull

echo "----2.重启后端----"
pkill -f simulate_back || true
nohup python backend/simulate_back.py > backend.log 2>&1 &
sleep 2


echo "----3.检查后端运行----"
curl -f http://127.0.0.1:5000/health || { echo "后端启动失败"; exit 1; }

echo "----4.跑测试+生成报告----"
pytest -m serial --alluredir ./report/json_report
allure generate ./report/json_report -o .report/html_report --clean

echo "----5.部署完成----"