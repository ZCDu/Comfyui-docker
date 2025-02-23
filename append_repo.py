import os
import subprocess


def parse_github_txt(file_path):
    """
    解析github.txt文件，提取需要克隆的仓库信息。
    返回一个列表，每个元素是一个元组 (repo_url, target_path)。
    如果没有指定目标路径，则target_path为None。
    """
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    repos = []
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
            repos.append((repo_url, target_path))

    return repos


def clone_repositories(repos, default_base_path="ComfyUI/custom_nodes"):
    """
    根据解析出的仓库信息，克隆仓库到指定位置。
    :param repos: 包含仓库信息的列表 [(repo_url, target_path), ...]
    :param default_base_path: 默认的基础路径
    """
    for repo_url, target_path in repos:
        if target_path:
            # 如果指定了目标路径，解析路径和重命名
            target_dir, rename = os.path.split(target_path)
            full_target_path = os.path.join(default_base_path, target_dir, rename)
        else:
            # 如果未指定目标路径，默认克隆到基础路径下
            repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
            full_target_path = os.path.join(default_base_path, repo_name)

        # 确保目标目录存在
        os.makedirs(os.path.dirname(full_target_path), exist_ok=True)

        # 执行git clone命令
        print(f"Cloning {repo_url} to {full_target_path}")
        try:
            subprocess.run(["git", "clone", repo_url, full_target_path], check=True)
            print(f"Successfully cloned {repo_url}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo_url}: {e}")


if __name__ == "__main__":
    # github.txt文件路径
    github_txt_path = "github.txt"

    # 解析github.txt文件
    repos = parse_github_txt(github_txt_path)

    # 克隆仓库
    clone_repositories(repos)
