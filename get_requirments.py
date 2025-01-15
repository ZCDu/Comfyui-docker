import os
import re


def get_requirements_files(folder_path):
    requirements_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "requirements.txt":
                requirements_files.append(os.path.join(root, file))
    return requirements_files


def merge_and_deduplicate_files(file_list, output_file):
    seen = set()
    with open(output_file, 'w') as outfile:
        for file_path in file_list:
            with open(file_path, 'r') as infile:
                for line in infile:
                    stripped_line = remove_version(line.strip())
                    if stripped_line not in seen:
                        seen.add(stripped_line)
                        outfile.write(stripped_line + '\n')


def remove_version(line):
    # 使用正则表达式匹配包名部分，去除版本号
    pattern = re.compile(r'^([a-zA-Z0-9\-_]+)')
    match = pattern.search(line)
    if match:
        return match.group(1)
    return line


# 调用函数，传入文件夹路径
folder_path = "./"
output_file = "merged_requirements.txt"
requirements_files = get_requirements_files(folder_path)
merge_and_deduplicate_files(requirements_files, output_file)
