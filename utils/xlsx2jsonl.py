# -*- coding: gbk -*-
import openpyxl
import json


def process_excel_to_jsonl(input_file_path, output_file_path):
    # Load the Excel file
    workbook = openpyxl.load_workbook(input_file_path)
    sheet = workbook['Sheet1']

    # Process the data
    data = []

    for row in sheet.iter_rows(2, sheet.max_row + 1, values_only=True):
        input_value = str(row[0])

        Strength = '{}的英雄强度是{}级，'.format(str(row[0]), str(row[1]))

        Position = '这个英雄通常情况下走{}位置，'.format(str(row[2]))

        Win_Rate = '胜率是{}，'.format(str(row[3]))

        Pick_Rate = '选取率是{}，'.format(str(row[4]))

        Ban_rate = 'ban选率是{}，'.format(str(row[5]))


        if row[6]:
            weak_against_list = row[6].replace("[", "").replace("]", "").replace("'", "").split('、')
            Weak_Against = '这个英雄不擅长对抗：' + weak_against_list[-1] + '。'

        else:
            Weak_Against = '这个英雄的弱点对手信息不可用'

        Hero_Url = '如果你想了解{}的详细天赋和出装信息，请查看如下网址{}。'.format(str(row[0]), str(row[7]))

        output_value = "".join([Strength, Position, Win_Rate, Pick_Rate, Ban_rate, Weak_Against, Hero_Url])

        conversation = {
            "system": "You are a professional LoL player, experienced professor, and world champion. "
                      "You always provide accurate, comprehensive and detailed answers to players' questions",
            "input": '我选择的英雄是{}，请给出这个英雄在当前版本的具体信息'.format(input_value),
            "output": output_value
        }
        data.append({"conversation": [conversation]})

    # Convert to JSONL format
    jsonl_data = '\n'.join(json.dumps(entry, ensure_ascii=False) for entry in data)

    # Save the output
    with open(output_file_path, 'w', encoding='gbk') as file:
        file.write(jsonl_data)

# Example usage
input_file_path = 'champions_data.xlsx'  # Path to your Excel file
output_file_path = 'processed_champions_data_gbk.jsonl'  # Desired output file path

process_excel_to_jsonl(input_file_path, output_file_path)


def convert_gbk_to_utf8(gbk_file_path, utf8_file_path):
    with open(gbk_file_path, 'r', encoding='gbk') as gbk_file, \
         open(utf8_file_path, 'w', encoding='utf-8') as utf8_file:
        for line in gbk_file:
            # 直接写入UTF-8编码的行
            utf8_file.write(line)

# 调用函数进行转换
gbk_file_path = 'processed_champions_data.jsonl'  # 替换为您的GBK文件路径
utf8_file_path = 'processed_champions_data_utf8.jsonl'  # 替换为您希望创建的UTF-8文件路径

convert_gbk_to_utf8(gbk_file_path, utf8_file_path)


