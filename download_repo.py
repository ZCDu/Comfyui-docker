import os
import subprocess
import time


def clone_github_projects(file_path):
    # 首先，检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，请检查文件路径。")
        return
    first_project = False
    with open(file_path, 'r') as file:
        for line in file:
            project_url = line.strip()  # 去除行末的换行符
            project_name = project_url.split('/')[-1].strip('.git')  # 获取项目名称
            while True:
                try:
                    # 尝试克隆项目
                    if first_project is not True:
                        first_project = True
                        subprocess.check_call(['git', 'clone', project_url, "--depth=1"])
                        print(f"成功克隆项目: {project_url}")
                        first_project_path = project_name
                        # 创建 custom 文件夹
                        custom_folder = os.path.join(first_project_path, 'custom_nodes')
                        os.makedirs(custom_folder, exist_ok=True)
                    else:
                        subprocess.check_call(['git', 'clone', project_url, os.path.join(first_project_path,"custom_nodes",project_name), "--depth=1"])
                    break
                except subprocess.CalledProcessError:
                    print(f"克隆项目 {project_url} 失败，正在重试...")
                    time.sleep(2)  # 等待 2 秒后重试


if __name__ == "__main__":
    clone_github_projects('github.txt')
