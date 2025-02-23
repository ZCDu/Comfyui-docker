import os


def parse_github_txt(file_path):
    """
    解析github.txt文件，提取需要查找的文件夹信息。
    返回一个列表，每个元素是一个元组 (repo_name, target_path)。
    如果没有指定目标路径，则target_path为None。
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    folders = []
    start_parsing = False

    for line in lines:
        line = line.strip()
        if line.startswith("# 新增"):
            start_parsing = True
            continue

        if start_parsing and line:
            # 分割仓库地址和目标路径
            parts = line.split(maxsplit=1)
            repo_url = parts[0]
            target_path = parts[1] if len(parts) > 1 else None

            # 提取仓库名或指定的目标路径
            if target_path:
                folder_path = target_path
            else:
                folder_path = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
            folders.append(folder_path)

    return folders


def merge_requirements(
    folders, base_path="ComfyUI/custom_nodes", output_file="append_requirements.txt"
):
    """
    根据解析出的文件夹信息，查找每个文件夹下的requirements.txt文件，
    并将其内容按顺序合并到output_file中。
    :param folders: 包含文件夹路径的列表
    :param base_path: 基础路径
    :param output_file: 输出文件名
    """
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write("")
        print(f"执行前清空{output_file}")

    merged_content = []

    for folder in folders:
        requirements_path = os.path.join(base_path, folder, "requirements.txt")
        if os.path.exists(requirements_path):
            print(f"Found requirements.txt in {folder}")
            with open(requirements_path, "r", encoding="utf-8") as req_file:
                content = req_file.read().strip()
                if content:
                    merged_content.append(content)
        else:
            print(f"No requirements.txt found in {folder}")

        merged_content.append("\n")
        # 将合并的内容写入输出文件
        with open(output_file, "a", encoding="utf-8") as out_file:
            out_file.write("\n".join(merged_content))
            print(f"Merged {requirements_path} saved to {output_file}")
        merged_content = []


if __name__ == "__main__":
    # github.txt文件路径
    github_txt_path = "github.txt"

    # 解析github.txt文件
    folders = parse_github_txt(github_txt_path)

    # 合并requirements.txt文件
    merge_requirements(folders)
