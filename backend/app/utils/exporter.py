import pandas as pd
import json
import os
from datetime import datetime

EXPORTS_DIR = "exports"

def export_to_json(parsed_data: dict, doc_type: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{doc_type.lower()}_{timestamp}.json"
    filepath = os.path.join(EXPORTS_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)

    return filepath


def export_to_excel(parsed_data: dict, doc_type: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{doc_type.lower()}_{timestamp}.xlsx"
    filepath = os.path.join(EXPORTS_DIR, filename)

    flat_data = {}
    for key, val in parsed_data.items():
        if isinstance(val, (str, int, float)):
            flat_data[key] = val
        elif isinstance(val, list):
            flat_data[key] = json.dumps(val)
        elif isinstance(val, dict):
            for k, v in val.items():
                flat_data[f"{key}_{k}"] = v
        else:
            flat_data[key] = str(val)

    df = pd.DataFrame([flat_data])

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=doc_type)

        # Auto adjust column widths
        worksheet = writer.sheets[doc_type]
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 4, 50)
            worksheet.column_dimensions[column].width = adjusted_width

    return filepath


def export_both(parsed_data: dict, doc_type: str) -> dict:
    json_path = export_to_json(parsed_data, doc_type)
    excel_path = export_to_excel(parsed_data, doc_type)

    return {
        "json_file": json_path,
        "excel_file": excel_path
    }