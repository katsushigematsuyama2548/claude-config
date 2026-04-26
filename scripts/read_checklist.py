#!/usr/bin/env python3
"""
Usage: python3 read_checklist.py <工程名> [--file <path>] [--timing <タイミング>]
Output: JSON array of checklist items for the given phase

Examples:
  python3 read_checklist.py 要件定義 --file .claude/docs/templates/checklist.xlsx
  python3 read_checklist.py 設計 --timing フェーズ終了時
"""

import sys
import json
import argparse
import openpyxl


def read_checklist(file_path: str, phase: str, timing_filter: str = None) -> list:
    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb["チェックシート"]

    current_phase = None
    current_timing = None
    current_summary = None
    results = []
    in_phase = False

    for row in ws.iter_rows(min_row=5, values_only=True):
        cell_phase = row[2]
        cell_timing = row[3]
        cell_summary = row[4]
        cell_content = row[5]
        cell_no = row[1]

        if cell_phase and not str(cell_phase).startswith("="):
            current_phase = cell_phase
            in_phase = current_phase == phase

        if in_phase and not in_phase and results:
            break

        if not in_phase:
            if results:
                break
            continue

        if cell_timing and not str(cell_timing).startswith("="):
            current_timing = cell_timing
        if cell_summary and not str(cell_summary).startswith("="):
            current_summary = cell_summary

        if not cell_content:
            continue

        if timing_filter and current_timing != timing_filter:
            continue

        results.append({
            "no": cell_no,
            "timing": current_timing,
            "summary": current_summary,
            "content": str(cell_content).strip(),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="チェックリストの指定工程を出力する")
    parser.add_argument("phase", help="工程名（例: 要件定義, 設計, 開発・UT）")
    parser.add_argument(
        "--file",
        default=".claude/docs/templates/checklist.xlsx",
        help="チェックリストファイルパス（デフォルト: .claude/docs/templates/checklist.xlsx）",
    )
    parser.add_argument(
        "--timing",
        default=None,
        help="タイミングフィルタ（例: フェーズ開始時, フェーズ終了時）",
    )
    args = parser.parse_args()

    items = read_checklist(args.file, args.phase, args.timing)

    if not items:
        print(json.dumps([], ensure_ascii=False))
        sys.exit(0)

    print(json.dumps(items, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
