#!/usr/bin/env python3
"""
WBS Excel を読み込み、タスク情報を JSON で出力する。
Usage: python3 read_wbs.py <path_to_wbs.xlsm>
"""
import sys
import json
from datetime import datetime, date
import openpyxl


def parse_date(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return None


def read_wbs(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[0]  # 第一シート固定

    rows = list(ws.iter_rows(values_only=True, max_col=30))

    # ヘッダー行を特定（"No" と "タスク" が含まれる行）
    header_row = None
    for i, row in enumerate(rows):
        row_str = [str(c) for c in row if c is not None]
        if "No" in row_str and "タスク" in row_str:
            header_row = i
            break

    if header_row is None:
        print(json.dumps({"error": "ヘッダー行が見つかりません"}))
        sys.exit(1)

    headers = list(rows[header_row])
    sub_headers = list(rows[header_row + 1]) if header_row + 1 < len(rows) else []

    def find_col(keyword):
        for i, h in enumerate(headers):
            if h is not None and keyword in str(h):
                return i
        return None

    col_no = find_col("No")
    col_assignee = find_col("担当")
    col_status = find_col("進捗ステータス")
    col_planned_hours = find_col("予定工数")

    col_lv1 = col_lv2 = col_lv3 = None
    for i, h in enumerate(sub_headers):
        if h is not None:
            if "Lv.1" in str(h):
                col_lv1 = i
            elif "Lv.2" in str(h):
                col_lv2 = i
            elif "Lv.3" in str(h):
                col_lv3 = i

    col_planned_from = col_planned_to = None
    for i, h in enumerate(headers):
        if h is not None and "予定" in str(h) and "工数" not in str(h):
            sub = sub_headers[i] if i < len(sub_headers) else None
            sub2 = sub_headers[i + 2] if i + 2 < len(sub_headers) else None
            if sub and "From" in str(sub):
                col_planned_from = i
            if sub2 and "To" in str(sub2):
                col_planned_to = i + 2
            break

    tasks = []
    data_start = header_row + 2

    for row in rows[data_start:]:
        no = row[col_no] if col_no is not None else None
        lv1 = row[col_lv1] if col_lv1 is not None else None
        lv2 = row[col_lv2] if col_lv2 is not None else None
        lv3 = row[col_lv3] if col_lv3 is not None else None
        assignee = row[col_assignee] if col_assignee is not None else None
        status = row[col_status] if col_status is not None else None
        planned_from = parse_date(row[col_planned_from]) if col_planned_from is not None else None
        planned_to = parse_date(row[col_planned_to]) if col_planned_to is not None else None
        hours = row[col_planned_hours] if col_planned_hours is not None else None

        if all(v is None for v in [no, lv1, lv2, lv3]):
            continue

        tasks.append({
            "no": no,
            "lv1": str(lv1) if lv1 else None,
            "lv2": str(lv2) if lv2 else None,
            "lv3": str(lv3) if lv3 else None,
            "assignee": str(assignee) if assignee else None,
            "status": str(status) if status else None,
            "planned_from": planned_from,
            "planned_to": planned_to,
            "planned_hours": float(hours) if hours else None,
        })

    print(json.dumps(tasks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 read_wbs.py <path>")
        sys.exit(1)
    read_wbs(sys.argv[1])
