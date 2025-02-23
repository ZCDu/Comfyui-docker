import subprocess
import pkg_resources
import sys
from packaging import specifiers, version
import argparse


def get_installed_packages():
    """
    获取当前环境中已安装的包及其版本。
    返回一个字典，键为包名，值为版本号。
    """
    installed_packages = {}
    for package in pkg_resources.working_set:
        installed_packages[package.key] = package.version
    return installed_packages


def parse_requirements(file_path):
    """
    解析 requirements.txt 文件，支持跨行依赖、条件安装和复杂版本约束。
    返回一个列表，每个元素是一个元组 (package, specifier, options)。
    """
    requirements = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    current_options = []  # 用于存储 --extra-index-url 等选项
    pending_package = None  # 用于存储上一行的包定义

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # 跳过空行和注释
            continue

        if line.startswith("--"):  # 如果是额外的选项（如 --extra-index-url）
            current_options.append(line)
            continue

        # 如果上一行有未处理的包定义，则先处理它
        # if pending_package:
        #     requirements.append(
        #         (pending_package[0], pending_package[1], current_options)
        #     )
        #     pending_package = None
        #     current_options = []

        # 处理包定义
        if ";" in line:  # 处理条件安装
            package_spec, condition = line.split(";", 1)
            package_spec = package_spec.strip()
            condition = condition.strip()
        else:
            package_spec = line
            condition = None

        # 检查条件是否满足
        if condition:
            try:
                # 替换 sys_platform 和其他可能的变量
                condition = condition.replace("sys_platform", f'"{sys.platform}"')
                if not eval(condition):
                    continue  # 条件不满足，跳过此依赖
            except Exception as e:
                print(f"条件解析失败: {condition}, 错误: {e}")
                continue

        # 处理包名和版本约束
        if "@" in package_spec or "://" in package_spec:  # 直接从 URL 或 Git 安装
            package = package_spec
            specifier = None
        elif "[" in package_spec:  # 带有额外选项的包（如 qrcode[pil]）
            package, extras = package_spec.split("[", 1)
            package = package.strip()
            extras = "[" + extras
            specifier = extras
        else:  # 普通包名和版本约束
            package_split = package_spec.split(" ", 1)
            package = package_split[0].strip()
            specifier = package_split[1].strip() if len(package_split) > 1 else None

        pending_package = (package, specifier)
        requirements.append((pending_package[0], pending_package[1], current_options))
        current_options = []

    # 处理最后一个未处理的包定义
    if pending_package:
        requirements.append((pending_package[0], pending_package[1], current_options))

    return requirements


def install_dependency(package, specifier, options):
    """
    安装或更新依赖。
    :param package: 包名。
    :param specifier: 版本约束（如 >=1.25.9）。
    :param options: 额外选项（如 --extra-index-url）。
    """
    installed_packages = get_installed_packages()
    installed_version = installed_packages.get(package.lower())

    if installed_version:
        if specifier:
            # 使用 packaging.specifiers.SpecifierSet 检查版本约束
            spec = specifiers.SpecifierSet(specifier)
            if version.parse(installed_version) in spec:
                print(f"{package} 当前版本 {installed_version} 已满足要求，跳过。")
                return
            else:
                print(f"{package} 当前版本 {installed_version} 不满足要求，重新安装...")
        else:
            print(f"{package} 已安装，未指定版本要求，跳过。")
            return

    # 安装或更新
    for single_package in ["torch", "moviepy"]:
        if package.find(single_package) != -1:
            print(f"跳过安装:{package}")
            break
        else:
            print(f"正在安装 {package} 版本 {specifier}...")
            if specifier:
                install_command = [
                    "pip",
                    "install",
                    "--no-cache-dir",
                    f"{package}{specifier}",
                ] + options
            else:
                install_command = [
                    "pip",
                    "install",
                    "--no-cache-dir",
                    package,
                ] + options
            subprocess.check_call(install_command)


def process_requirements(requirements_file):
    """
    处理 requirements.txt 文件中的依赖。
    """
    print(f"正在处理 {requirements_file}...")
    requirements = parse_requirements(requirements_file)
    for package, specifier, options in requirements:
        install_dependency(package, specifier, options)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取输入")
    parser.add_argument("files", default="requirements.txt")
    args = parser.parse_args()
    requirements_file = args.files  # 替换为你的 requirements.txt 文件路径
    process_requirements(requirements_file)
