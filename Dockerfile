FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
RUN export GIT_PYTHON_REFRESH=quiet
RUN apt-get update && \
        apt-get install -y libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev build-essential ffmpeg git libasound2-dev libportaudio2 && \
    rm -rf /var/lib/apt/lists/*
ENV TZ=Etc/UTC
ENV LANG=zh_CN.UTF-8
WORKDIR /app

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && pip config set install.trusted-host mirrors.aliyun.com

COPY ComfyUI /app/ComfyUI
WORKDIR /app/ComfyUI
RUN pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/x-flux-comfyui && python setup.py
RUN cd custom_nodes/ComfyUI_Qwen2-VL-Instruct && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-Manager && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui_controlnet_aux && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui-easyapi-nodes && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-KJNodes && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui_LLM_party && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/rgthree-comfy && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-FluxTrainer && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/was-node-suite-comfyui && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI_essentials && pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
RUN git clone https://github.com/PortAudio/portaudio.git && cd portaudio && ./configure && make && make install
RUN pip install --no-cache-dir minio requests certifi py-cord[voice] pyaudio moviepy==1.0.3
RUN pip install --no-cache-dir playwright && playwright install
RUN cd custom_nodes/ComfyUI-Impact-Pack && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui-art-venture && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-Diffusers-OminiControl && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-GGUF && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-VideoHelperSuite && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-HunyuanVideoWrapper && pip install --no-cache-dir -r requirements.txt




EXPOSE 8188
CMD ["python", "main.py", "--port 8188"]
