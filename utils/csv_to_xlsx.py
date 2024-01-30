# import pandas as pd
#
# # 读取CSV文件
# csv_file = './champions_data.csv'  # 替换为你的CSV文件路径
# df = pd.read_csv(csv_file, delimiter='\t', encoding='utf-8')
#
# # 保存为Excel文件
# excel_file = './champions_data.xlsx'  # 替换为你想要保存的Excel文件路径
# df.to_excel(excel_file, index=False, encoding='utf-8')
#
# print(f"CSV文件已成功转换为Excel文件：{excel_file}")

import pandas as pd


def convert_csv_to_xlsx(csv_file, xlsx_file):
    # Read the CSV data
    data = pd.read_csv(csv_file, delimiter=',', encoding='gbk')

    # Write the dataframe object into XLSX file
    data.to_excel(xlsx_file, index=None, header=True)

    print("CSV file has been converted to XLSX file successfully.")


# replace 'your_data.csv' and 'output.xlsx' with your actual CSV file name and desired output XLSX file name
convert_csv_to_xlsx('./champions_data.csv', './champions_data.xlsx')