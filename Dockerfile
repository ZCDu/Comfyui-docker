FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
RUN export GIT_PYTHON_REFRESH=quiet
RUN apt-get update && \
        apt-get install -y libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev build-essential ffmpeg git libasound-dev && \
    rm -rf /var/lib/apt/lists/*
ENV TZ=Etc/UTC
ENV LANG=zh_CN.UTF-8
WORKDIR /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

COPY ComfyUI /app/ComfyUI
WORKDIR /app/ComfyUI
RUN pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/x-flux-comfyui && python setup.py
RUN cd custom_nodes/ComfyUI-Manager && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui_controlnet_aux && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-Crystools && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui-easyapi-nodes && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-KJNodes && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/comfyui_LLM_party && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-VideoHelperSuite && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/rgthree-comfy && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-FluxTrainer && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-CogVideoXWrapper && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-PyramidFlowWrapper && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/was-node-suite-comfyui && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-Easy-Use && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI_essentials && pip install --no-cache-dir -r requirements.txt
RUN cd custom_nodes/ComfyUI-PuLID-Flux-Enhanced && pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
RUN git clone https://github.com/PortAudio/portaudio.git && cd portaudio && ./configure && make && make install
RUN pip install --no-cache-dir minio requests certifi discord.py pyaudio moviepy


EXPOSE 8188
CMD ["python", "main.py", "--port 8188"]
