# 当前用到的仓库
https://github.com/chrisgoringe/cg-use-everywhere.git
https://github.com/sipherxyz/comfyui-art-venture.git
https://github.com/kijai/ComfyUI-CogVideoXWrapper.git
https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes.git
https://github.com/huggingface/controlnet_aux.git
https://github.com/crystian/ComfyUI-Crystools.git
https://github.com/pythongosssss/ComfyUI-Custom-Scripts.git
https://github.com/lldacing/comfyui-easyapi-nodes.git
https://github.com/yolain/ComfyUI-Easy-Use.git
https://github.com/cubiq/ComfyUI_essentials.git
https://github.com/kijai/ComfyUI-FluxTrainer.git
https://github.com/ali-vilab/In-Context-LoRA.git
https://github.com/kijai/ComfyUI-KJNodes.git
https://github.com/heshengtao/comfyui_LLM_party.git
https://github.com/ltdrdata/ComfyUI-Manager.git
https://github.com/shadowcz007/comfyui-mixlab-nodes.git
https://github.com/sipie800/ComfyUI-PuLID-Flux-Enhanced.git
https://github.com/kijai/ComfyUI-PyramidFlowWrapper.git
https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git
https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
https://github.com/rgthree/rgthree-comfy.git
https://github.com/WASasquatch/was-node-suite-comfyui.git
https://github.com/XLabs-AI/x-flux-comfyui.git

https://github.com/kaibioinfo/ComfyUI_AdvancedRefluxControl

# Impack-Pack
https://github.com/ltdrdata/ComfyUI-Impact-Pack
需要在该分支下git 依赖的分支
```shell
git clone https://github.com/ltdrdata/ComfyUI-Impact-Subpack impact_subpack
```
## 依赖模型
依据install-manual中的down的模型，下载到对应的位置：
1. sam -> /app/ComfyUI/models/sams/*.pth

# 执行流程
1. ./download_repo.py
2. ./get_requirments.py
3. docker build
