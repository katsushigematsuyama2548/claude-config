#!/bin/bash
# 月次 GC スクリプト — LaunchAgent から呼び出される

LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] GC 開始" >> "$LOG_DIR/gc.log"

echo "gc スキルを実行してください。~/.claude/skill-usage.jsonl を参照して各スキルの最終使用日を確認し、閾値（skills/commands=60日、agents=90日）を超えたファイルを検出して GitHub PR を作成してください。" \
  | /Users/katusigematuyama/.local/bin/claude --print \
    --dangerously-skip-permissions \
    --add-dir "$HOME/.claude" \
  >> "$LOG_DIR/gc.log" 2>> "$LOG_DIR/gc-error.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] GC 完了" >> "$LOG_DIR/gc.log"
