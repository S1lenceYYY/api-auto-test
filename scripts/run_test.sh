#!/bin/bash
set -e

cd "$(dirname "$0")/.."
source  venv/bin/activate

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

MODE=${1:-serial}
START=$(date +%s)


log "------开始跑测试(模式:$MODE)------"

if [ "$MODE" = "parallel" ]; then
    log "模式：并行（4 worker）"
    pytest -m parallel -n 4 --alluredir ./report/json_parallel
    allure generate ./report/json_parallel -o ./report/html_parallel --clean
    REPORT_DIR="./report/html_parallel"
else
    log "模式：串行"
    pytest -m serial --alluredir ./report/json_report
    allure generate ./report/json_report -o ./report/html_report --clean
    REPORT_DIR="./report/html_report"
fi


END=$(date +%s)
log "===== 测试完成，总耗时 $((END - START)) 秒 ====="
log "报告位置：$REPORT_DIR"
log "本地查看：tar 打包下载后 allure open"
log "云端查看：allure serve $REPORT_DIR -h 0.0.0.0 -p 4040"
