#打开excel文件
#选择表
#读数据操作
#关闭表
#zip()函数可以把迭代对象打包成一个个元组，dict（zip（key，value）），形式与用例一样
import openpyxl
import  os

from config.config import EXCEL_FILE


def read_excel(file_path=EXCEL_FILE,sheet_name="case1"):
    # # 获取当前 excel_utils.py 文件所在目录
    # cur_path = os.path.abspath(__file__)
    # utils_dir = os.path.dirname(cur_path)
    # # 向上一层到达项目根目录 F:\jkzdh5.2
    # root_dir = os.path.dirname(utils_dir)
    # # Excel在 data 文件夹
    # excel_file = os.path.join(root_dir, "data", "用例.xlsx")

    workbook = openpyxl.load_workbook(file_path)
    worksheet=workbook[sheet_name]
    data=[]#空列表，用于组转字典
    keys=[cell.value for cell in worksheet[2]]#拿key行，也是表的第2行
    for row in worksheet.iter_rows (min_row=3,values_only=True):
        dict_data= dict(zip(keys,row))
        #如果读取的is_true 的值为TRUE，则append，反之则不减少不必要的资源消耗
        if dict_data["is_true"]:
            data.append(dict_data)
    workbook.close()
    return data