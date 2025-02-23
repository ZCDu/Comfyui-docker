import os


def merge_requirements(base_dir, output_file):
    """
    合并指定文件夹及其子文件夹中的所有 requirements.txt 文件。
    :param base_dir: 主文件夹路径（包含 ComfyUI 和 custom_nodes）。
    :param output_file: 合并后的输出文件路径。
    """
    # 初始化一个列表来存储所有依赖项
    all_requirements = []

    # 遍历主文件夹及其子文件夹
    for root, dirs, files in os.walk(base_dir):
        if "requirements.txt" in files:
            requirements_path = os.path.join(root, "requirements.txt")
            print(f"找到 requirements.txt: {requirements_path}")
            with open(requirements_path, "r", encoding="utf-8") as file:
                # 逐行读取文件内容，并保留原始顺序
                all_requirements.extend(file.readlines())
            all_requirements.extend("\n")

            # 将所有依赖项写入输出文件
            with open(output_file, "a+", encoding="utf-8") as outfile:
                outfile.writelines(all_requirements)
            all_requirements = []
            print(f"已合并 {requirements_path} 到 {output_file}")


if __name__ == "__main__":
    # 定义主文件夹路径和输出文件路径
    comfyui_folder = "ComfyUI"  # 替换为你的 ComfyUI 文件夹路径
    output_requirements = "requirements.txt"  # 合并后的文件名

    with open(output_requirements, "w", encoding="utf-8") as file:
        file.write("")

    # 调用函数进行合并
    merge_requirements(comfyui_folder, output_requirements)
