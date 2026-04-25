#!/bin/bash
# Skill ツール呼び出し時に ~/.claude/skill-usage.jsonl へ使用ログを追記する
SKILL=$(python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('skill',''))" 2>/dev/null)
if [ -n "$SKILL" ]; then
  echo "{\"skill\":\"$SKILL\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> ~/.claude/skill-usage.jsonl
fi
