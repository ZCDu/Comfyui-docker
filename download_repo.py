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

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # 分割仓库地址和目标路径
        parts = line.split(maxsplit=1)
        repo_url = parts[0]
        target_path = parts[1] if len(parts) > 1 else None
        repos.append((repo_url, target_path))

    return repos


def clone_repository(repo_url, base_path="ComfyUI", target_path=None, max_retries=5):
    """
    使用git clone --depth=1克隆仓库。
    :param repo_url: 仓库地址
    :param base_path: 基础路径（主文件夹）
    :param target_path: 目标路径（可选）
    :param max_retries: 最大重试次数
    """
    if target_path:
        # 如果指定了目标路径，解析路径和重命名
        full_target_path = os.path.join(base_path, "custom_nodes", target_path)
    else:
        # 如果未指定目标路径，默认克隆到基础路径下的custom_nodes目录
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        if repo_name == "ComfyUI":
            full_target_path = base_path
        else:
            full_target_path = os.path.join(base_path, "custom_nodes", repo_name)

    # 确保目标目录存在
    # os.makedirs(os.path.dirname(full_target_path), exist_ok=True)

    # 执行git clone命令，支持重试机制
    retries = 0
    while retries < max_retries:
        print(
            f"Cloning {repo_url} to {full_target_path} (Attempt {retries + 1}/{max_retries})"
        )
        try:
            subprocess.run(
                ["git", "clone", "--depth=1", repo_url, full_target_path], check=True
            )
            print(f"Successfully cloned {repo_url}")
            break
        except subprocess.CalledProcessError as e:
            retries += 1
            print(f"Failed to clone {repo_url}: {e}")
            if retries == max_retries:
                print(f"Exceeded maximum retries for {repo_url}. Skipping...")
            else:
                print("Retrying...")


if __name__ == "__main__":
    # github.txt文件路径
    github_txt_path = "github.txt"

    # 解析github.txt文件
    repos = parse_github_txt(github_txt_path)

    # 先克隆ComfyUI作为主文件夹
    comfyui_repo = repos.pop(0)  # 第一行是ComfyUI
    clone_repository(comfyui_repo[0], base_path="ComfyUI")

    # 后续克隆到ComfyUI/custom_nodes目录下
    for repo_url, target_path in repos:
        clone_repository(repo_url, base_path="ComfyUI", target_path=target_path)
