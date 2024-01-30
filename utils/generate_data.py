# -*- coding: utf-8 -*-


def duplicate_jsonl_lines(original_file_path, new_file_path, num_copies):
    """
    复制jsonl文件中的每一行指定次数，并写入到新的jsonl文件中。

    :param original_file_path: 原始jsonl文件的路径
    :param new_file_path: 新jsonl文件的路径
    :param num_copies: 每行要复制的次数
    """
    with open(original_file_path, 'r', encoding='utf-8') as original_file, \
            open(new_file_path, 'w', encoding='utf-8') as new_file:
        for line in original_file:
            for _ in range(num_copies):
                new_file.write(line)


# 使用示例
if __name__ == "__main__":
    # 原始jsonl文件路径
    original_file_path = './processed_champions_data_utf8.jsonl'

    # 新jsonl文件的路径
    new_file_path = './champions_data_50.jsonl'

    # 调用函数复制每行内容150遍
    duplicate_jsonl_lines(original_file_path, new_file_path, 50)