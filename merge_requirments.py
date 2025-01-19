import re
from packaging import version
import os


def parse_requirements_line(line):
    # 解析一行 requirements.txt 内容，返回 (package_name, specifiers)
    match = re.match(r"^([a-zA-Z0-9-_]+)((?:[<>=~!]=?[\d\w.]+,?)+)?", line.strip())
    if match:
        package_name = match.group(1)
        specifiers = match.group(2) or ""
        return package_name, specifiers
    return None, None


def get_latest_version(specifiers):
    # 获取 specifiers 中的最大版本号
    versions = []
    for specifier in specifiers.split(","):
        if specifier:
            try:
                versions.append(version.parse(specifier))
            except Exception as e:
                print(f"Error parsing version: {specifier}, error: {e}")
    if versions:
        return max(versions)
    return None


def convert_specifiers_to_greater_than_equal(specifiers):
    # 将 == 转换为 >=
    if "==" in specifiers:
        specifiers = specifiers.replace("==", ">=")
    return specifiers


def merge_requirements(main_req_file, custom_nodes_dir):
    # 存储所有依赖信息
    dependencies = {}

    def add_dependency(package_name, specifiers, index):
        if package_name not in dependencies:
            dependencies[package_name] = {
                "specifiers": specifiers,
                "has_version": bool(specifiers),
                "index": index,
            }
        else:
            current_specifiers = dependencies[package_name]["specifiers"]
            current_has_version = dependencies[package_name]["has_version"]
            current_index = dependencies[package_name]["index"]

            if current_has_version and specifiers:
                # 如果两者都有版本约束，比较版本
                current_max_version = get_latest_version(current_specifiers)
                new_max_version = get_latest_version(specifiers)

                if new_max_version and (
                    not current_max_version or new_max_version > current_max_version
                ):
                    dependencies[package_name] = {
                        "specifiers": specifiers,
                        "has_version": True,
                        "index": index,
                    }
            elif specifiers:
                # 如果当前没有版本约束，但新依赖有版本约束
                dependencies[package_name] = {
                    "specifiers": specifiers,
                    "has_version": True,
                    "index": index,
                }
            # 如果新依赖没有版本约束，则不更新

    # 处理主 requirements.txt 文件
    with open(main_req_file, "r", encoding="utf-8") as file:
        main_lines = file.readlines()

    for index, line in enumerate(main_lines):
        package_name, specifiers = parse_requirements_line(line)
        if package_name:
            add_dependency(package_name, specifiers, index)

    # 遍历 custom_nodes 目录下的每个插件
    for root, dirs, files in os.walk(custom_nodes_dir):
        if "requirements.txt" in files:
            plugin_req_file = os.path.join(root, "requirements.txt")
            with open(plugin_req_file, "r", encoding="utf-8") as file:
                plugin_lines = file.readlines()

            for index, line in enumerate(plugin_lines):
                package_name, specifiers = parse_requirements_line(line)
                if package_name:
                    add_dependency(package_name, specifiers, index + len(main_lines))

    # 过滤掉未指定版本的相同依赖
    filtered_dependencies = {}
    for package_name, info in dependencies.items():
        if info["has_version"] or not any(
            pkg == package_name and data["has_version"]
            for pkg, data in dependencies.items()
        ):
            filtered_dependencies[package_name] = info

    # 构建新的 requirements 列表
    merged_requirements = []
    deleted_indices = set()

    for index, line in enumerate(main_lines + plugin_lines):
        package_name, specifiers = parse_requirements_line(line)
        if package_name and package_name in filtered_dependencies:
            dependency_info = filtered_dependencies[package_name]
            if dependency_info["index"] == index:
                # 将 == 转换为 >=
                specifiers = convert_specifiers_to_greater_than_equal(
                    dependency_info["specifiers"]
                )
                merged_requirements.append(f"{package_name}{specifiers}\n")
            else:
                # 记录需要删除的索引
                deleted_indices.add(index)
                # 检查下一行是否包含 extra-index-url 并一同删除
                if (
                    index + 1 < len(main_lines + plugin_lines)
                    and "extra-index-url" in (main_lines + plugin_lines)[index + 1]
                ):
                    deleted_indices.add(index + 1)
        else:
            # 记录需要删除的索引
            deleted_indices.add(index)
            # 检查下一行是否包含 extra-index-url 并一同删除
            if (
                index + 1 < len(main_lines + plugin_lines)
                and "extra-index-url" in (main_lines + plugin_lines)[index + 1]
            ):
                deleted_indices.add(index + 1)

    # 添加未被删除的行到结果中
    for index, line in enumerate(main_lines + plugin_lines):
        if index not in deleted_indices:
            merged_requirements.append(line)

    with open("merged_requirements.txt", "w", encoding="utf-8") as file:
        file.writelines(merged_requirements)

    print("Merged requirements have been written to 'merged_requirements.txt'.")


if __name__ == "__main__":
    # 指定主 requirements.txt 文件路径和 custom_nodes 目录路径
    main_requirements_file = "requirements.txt"
    custom_nodes_directory = "custom_nodes"
    main_path = "./ComfyUI/"
    main_requirements_path = os.path.join(main_path, main_requirements_file)
    custom_nodes_path = os.path.join(main_path, custom_nodes_directory)

    merge_requirements(main_requirements_path, custom_nodes_path)
