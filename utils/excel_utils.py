import openpyxl

from config.config import EXCEL_FILE


def read_excel(file_path=EXCEL_FILE, sheet_name="case1"):
    workbook = openpyxl.load_workbook(file_path)
    worksheet = workbook[sheet_name]

    data = []
    keys = [cell.value for cell in worksheet[2]]  # 第二行是字段名

    for row in worksheet.iter_rows(min_row=3, values_only=True):
        dict_data = dict(zip(keys, row))
        # 只收集 is_true 为真的用例
        if dict_data["is_true"]:
            data.append(dict_data)

    workbook.close()
    return data