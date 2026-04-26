#!/usr/bin/env python3
"""
WBS Excel の指定タスクの進捗ステータスを更新し、draft を出力する。
Usage: python3 update_wbs.py <input_path> <output_path> <updates_json>

updates_json: '[{"no": 1, "lv2": "資料作成", "status": "Close"}]'
"""
import sys
import json
import shutil
import openpyxl


def update_wbs(input_path, output_path, updates):
    shutil.copy2(input_path, output_path)
    wb = openpyxl.load_workbook(output_path, keep_vba=True)
    ws = wb.worksheets[0]

    rows = list(ws.iter_rows(max_col=30))

    header_row_idx = None
    for i, row in enumerate(rows):
        row_vals = [cell.value for cell in row]
        row_str = [str(c) for c in row_vals if c is not None]
        if "No" in row_str and "タスク" in row_str:
            header_row_idx = i
            break

    if header_row_idx is None:
        print("ERROR: ヘッダー行が見つかりません")
        sys.exit(1)

    sub_header_row = rows[header_row_idx + 1]
    header_cells = rows[header_row_idx]

    def find_col_idx(keyword):
        for i, cell in enumerate(header_cells):
            if cell.value and keyword in str(cell.value):
                return i
        return None

    col_no = find_col_idx("No")
    col_status = find_col_idx("進捗ステータス")
    col_lv2 = None
    for i, cell in enumerate(sub_header_row):
        if cell.value and "Lv.2" in str(cell.value):
            col_lv2 = i
            break

    changed = []
    data_start = header_row_idx + 2
    for update in updates:
        for row in rows[data_start:]:
            no_val = row[col_no].value if col_no is not None else None
            lv2_val = row[col_lv2].value if col_lv2 is not None else None

            match = False
            if update.get("no") and str(no_val) == str(update["no"]):
                match = True
            if update.get("lv2") and lv2_val and update["lv2"] in str(lv2_val):
                match = True

            if match and col_status is not None:
                old_status = row[col_status].value
                row[col_status].value = update["status"]
                changed.append({
                    "task": str(lv2_val),
                    "old_status": old_status,
                    "new_status": update["status"],
                })

    wb.save(output_path)
    print(json.dumps({"changed": changed, "output": output_path}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 update_wbs.py <input> <output> <updates_json>")
        sys.exit(1)
    updates = json.loads(sys.argv[3])
    update_wbs(sys.argv[1], sys.argv[2], updates)
