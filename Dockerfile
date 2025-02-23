FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
RUN export GIT_PYTHON_REFRESH=quiet
RUN apt-get update && \
        apt-get install -y libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev build-essential ffmpeg git libasound2-dev libportaudio2 libgl1 && \
    rm -rf /var/lib/apt/lists/*
ENV TZ=Etc/UTC
ENV LANG=zh_CN.UTF-8
WORKDIR /app

# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && pip config set install.trusted-host mirrors.aliyun.com
RUN pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple && pip config set install.trusted-host mirrors.tuna.tsinghua.edu.cn

COPY requirements.txt /app/ComfyUI/requirements.txt
COPY other_requirements.txt /app/ComfyUI/other_requirements.txt
# COPY append_requirements.txt /app/ComfyUI/append_requirements.txt
COPY install_requirements.py /app/ComfyUI/install_requirements.py
COPY ComfyUI/custom_nodes/x-flux-comfyui /app/ComfyUI/custom_nodes/x-flux-comfyui
WORKDIR /app/ComfyUI
RUN python -m pip install pip==24.0 
RUN cd custom_nodes/x-flux-comfyui && python setup.py
RUN pip install --no-cache-dir llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
RUN git clone https://github.com/PortAudio/portaudio.git && cd portaudio && ./configure && make && make install
RUN python install_requirements.py requirements.txt
# RUN python install_requirements.py append_requirements.txt
RUN pip install --no-cache-dir -r other_requirements.txt
RUN pip install --no-cache-dir minio requests certifi py-cord[voice] pyaudio moviepy==1.0.3
RUN pip install --no-cache-dir playwright && playwright install
# RUN pip install git+https://github.com/WASasquatch/cstr
# RUN pip install --no-cache-dir -r extra_pakage.txt


EXPOSE 8188
CMD ["python", "main.py", "--port 8188"]
