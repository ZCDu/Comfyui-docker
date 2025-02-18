import re
import requests
import pandas as pd


def read_file_from_github(url):
    response = requests.get(url)

    if response.status_code == 200:
        response_text = response.text
        lines = response_text.splitlines()
        return lines
    else:
        url = re.sub(r"main", "master", url)
        response = requests.get(url)
        if response.status_code == 200:
            response_text = response.text
            lines = response_text.splitlines()
            return lines
        else:
            return 0


def detecting_special_case(rqs_getting_list, special_rqs_set):
    rqs_getting_list_len = len(rqs_getting_list)
    i = rqs_getting_list_len - 1
    while i >= 0:
        if bool(rqs_getting_list[i]) == False:
            rqs_getting_list.pop(i)
            i = i - 1
        elif rqs_getting_list[i][0] == "#":
            rqs_getting_list.pop(i)
            i = i - 1
        elif "sys_platform" in rqs_getting_list[i]:
            special_rqs_set.add(rqs_getting_list[i])
            rqs_getting_list.pop(i)
            i = i - 1
        elif "--extra-index" in rqs_getting_list[i]:
            str_added = rqs_getting_list[i - 1] + "\n" + rqs_getting_list[i]
            special_rqs_set.add(str_added)
            rqs_getting_list.pop(i)
            rqs_getting_list.pop(i - 1)
            i = i - 2
        elif "git+https" in rqs_getting_list[i]:
            special_rqs_set.add(rqs_getting_list[i])
            rqs_getting_list.pop(i)
            i = i - 1
        else:
            i = i - 1
    return rqs_getting_list, special_rqs_set


def check_version(s):
    return bool(re.search(r"[><=!]", s))


def min_version(old_v, new_v):
    old_list = [int(part) for part in str(old_v).split(".") if part]
    new_list = [int(part) for part in str(new_v).split(".") if part]
    max_length = max(len(old_list), len(new_list))
    old_list.extend([9] * (max_length - len(old_list)))
    new_list.extend([9] * (max_length - len(new_list)))
    for i in range(max_length):
        if old_list[i] > new_list[i]:
            return new_v
        elif old_list[i] < new_list[i]:
            return old_v
    return old_v


def max_version(old_v, new_v):
    old_list = [int(part) for part in str(old_v).split(".") if part]
    new_list = [int(part) for part in str(new_v).split(".") if part]
    max_length = max(len(old_list), len(new_list))
    old_list.extend([0] * (max_length - len(old_list)))
    new_list.extend([0] * (max_length - len(new_list)))
    for i in range(max_length):
        if old_list[i] > new_list[i]:
            return old_v
        elif old_list[i] < new_list[i]:
            return new_v
    return old_v


def split_package_info(package_str):
    # relations = ('<=', '>=', '==', '!=', '<', '>', '=')
    relations = ["<", ">", "=", "!"]
    complex_relations = ["<=", ">=", "==", "!="]
    count = 0
    for i in package_str:
        if i in relations:
            count = count + 1
    package_name = ""
    relation = ""
    version = ""
    idx_state = 0
    if count == 2:
        package_name = package_str[0]
        for i in range(len(package_str) - 1):
            if package_str[i : i + 2] in complex_relations:
                idx_state = 1
                relation = package_str[i : i + 2]
            elif idx_state == 0:
                package_name = package_name + package_str[i + 1]
            else:
                version = version + package_str[i + 1]
        package_name = package_name[:-1]
        # version=version[1:]
        return [package_name, relation, version]
    elif count == 1:
        for i in package_str:
            if i in relations:
                relation = i
                idx_state = 1
            elif idx_state == 0:
                package_name = package_name + i
            else:
                version = version + i
        return [package_name, relation, version]
    # else:
    #     return None


def changing_dic(s, pakage_version):  # 返回dict
    package_info = split_package_info(s)
    # if package_info!=None:#有版本号
    new_value = [package_info[1], package_info[2]]
    # 开始更新pakage_version字典
    # 判断是否在原字典中
    if package_info[0] in pakage_version:  # 在字典中
        # 判断值的大小关系
        original_value = pakage_version[package_info[0]]
        if new_value[0] == ">=" or new_value[0] == ">":
            pakage_version[package_info[0]] = [
                original_value[0],
                max_version(original_value[1], new_value[1]),
                original_value[2],
            ]
        # elif new_value[0]=="<="|"<":
        #     pakage_version[package_info[0]]=[min_version(original_value[0],new_value[1]),original_value[1],original_value[2]]
        # elif new_value[0]=="<=" or new_value[0]=="<":
        #     pakage_version[package_info[0]]=[original_value[0],max_version(original_value[1],new_value[1]),original_value[2]]
        elif new_value[0] == "==" or new_value[0] == "=":
            pakage_version[package_info[0]] = [
                original_value[0],
                max_version(original_value[1], new_value[1]),
                original_value[2],
            ]
        # else:#"!="
        #     pakage_version[package_info[0]]=[original_value[0],original_value[1],original_value[2].append(new_value[1])]
    else:  # 不在字典里，创建
        if new_value[0] == ">=" or new_value[0] == ">":
            pakage_version[package_info[0]] = ["99.99", new_value[1], []]
        # elif new_value[0]=="<="|"<":
        #     pakage_version[package_info[0]]=[new_value[1],'0',[]]
        elif new_value[0] == "<=" or new_value[0] == "<":
            pakage_version[package_info[0]] = ["", "", new_value[1], []]
        elif new_value[0] == "==" or new_value[0] == "=":
            pakage_version[package_info[0]] = ["99.99", new_value[1], []]
        # else:#"!="
        # pakage_version[package_info[0]]=['99.99','0',[new_value[1]]]
        else:  # "!="
            pakage_version[package_info[0]] = ["", "", []]
    return pakage_version
    # else:#无版本号
    #     return pakage_version,0


if __name__ == "__main__":
    dependencies_list = []
    requirements_list = []
    requirements_no_list = []
    install_dir = "install.sh"  # 读取install.sh的路径
    requirements_save_dir = "requirements.txt"  # 保存requirements.txt的路径
    extra_pakage_save_dir = (
        "extra_pakage.txt"  # extra_pakage.txt，就是那些指定cu121的路径
    )

    with open(install_dir, "r") as f:
        # with open('install.sh', 'r') as f:
        contents = f.readlines()
    for i in range(len(contents)):
        c_n = contents[i]
        c_n = c_n[10:]
        c_n = c_n.split(".")[0] + c_n.split(".")[1]
        repo = c_n[18:]
        dependencies_list.append(
            "https://raw.githubusercontent.com/{}/main/requirements.txt".format(repo)
        )
        # print(i)
    for i in dependencies_list:
        require_lines = read_file_from_github(i)
        if require_lines == 0:
            requirements_no_list.append(i)
        else:
            for j in require_lines:
                requirements_list.append(j.replace(" ", ""))
    special_rqs_set = set()
    requirements_list, special_rqs_set = detecting_special_case(
        requirements_list, special_rqs_set
    )
    # 将带有版本要求，就是带有比较符号的存入字典
    pakage_version = {}  # {package:[<num,>num,!=[num]]}
    pakage_no_version = set()
    for i in requirements_list:
        if check_version(i):  # 带有比较符号
            pakage_version = changing_dic(i, pakage_version)
        else:
            pakage_no_version.add(i)

    # 处理git，将依赖的依赖导入pakage_no_version中
    dependencies_list = []
    requirements_list = []
    for i in special_rqs_set.copy():
        if "git+http" in i:
            repo = i[23:-4]
            dependencies_list.append(
                "https://raw.githubusercontent.com/{}/main/requirements.txt".format(
                    repo
                )
            )
            special_rqs_set.remove(i)
    for i in dependencies_list:
        require_lines = read_file_from_github(i)
        if require_lines == 0:
            requirements_no_list.append(i)
        else:
            for j in require_lines:
                requirements_list.append(j.replace(" ", ""))
    for i in requirements_list:
        pakage_no_version.add(i)

    # 将没有版本号的存入
    for i in pakage_no_version:
        if i not in pakage_version:
            pakage_version[i] = ["", "", []]

    # 将extra-index从special_rqs_set移动到extra_pakage，并且在pakage_version中移除对应的包
    extra_pakage = set()
    for i in special_rqs_set.copy():
        if "extra-index" in i:
            pakage_name, pakage_info = i.splitlines()
            extra_pakage.add(i)

            # pakage_name.pop(i)
            special_rqs_set.remove(i)
            if pakage_name in pakage_version:
                pakage_version.pop(pakage_name)

    # 处理platform
    for i in special_rqs_set.copy():
        if "win32" in i or "darwin" in i:
            special_rqs_set.remove(i)

    # 准备打印str
    requirements_print_str = ""
    for i in pakage_version:
        if bool(pakage_version[i][1]) == False:
            requirements_print_str += i
            requirements_print_str += "\n"
        else:
            requirements_print_str += i
            requirements_print_str += ">="
            requirements_print_str += pakage_version[i][1]
            requirements_print_str += "\n"
    for i in special_rqs_set:
        requirements_print_str += i
        requirements_print_str += "\n"
    requirements_print_str = requirements_print_str[:-1]
    with open(requirements_save_dir, "w", encoding="utf-8") as file:
        # 写入字符串
        file.write(requirements_print_str)

    # 打印extra_pakage
    requirements_print_str = ""
    for i in extra_pakage:
        requirements_print_str = requirements_print_str + i
        requirements_print_str = requirements_print_str + "\n"
    requirements_print_str = requirements_print_str[:-1]
    with open(extra_pakage_save_dir, "w", encoding="utf-8") as file:
        # 写入字符串
        file.write(requirements_print_str)
    # special_rqs_set
    pass
