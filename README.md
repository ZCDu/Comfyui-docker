# 当前用到的仓库
当前用到的插件都在github.txt里, 在追加新的插件时，请按照github.txt的内容进行设置

other_requirements里都是虽然requirements里有，但是安装完之后还是找不到的python依赖

## 依赖模型
依据install-manual中的down的模型，下载到对应的位置：
1. sam -> /app/ComfyUI/models/sams/*.pth

# 执行流程
1. ./download_repo.py
2. ./merge_requirments.py 合并依赖
3. docker build (Dockerfile里使用了./install_requirements.py去安装依赖)

# 追加依赖的执行方式
1. ./append_repo.py   下载额外的仓库
2. ./append_requirements.py 合并额外的依赖到append_requirements.txt
3. 修改Dockerfile增加append——requirements.txt的安装过程, 同样使用install_requirements.py去安装依赖
4. docker build
后续如果重新拉取所有的仓库，那么就不需要在用这个追加依赖的操作，这个只要在不想重新拉全部github的时候才用
