# pick the CUDA version your host GPU driver supports
FROM pytorch/pytorch:2.6.0-cuda12.6-cudnn9-runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -y

# install any extra system deps
RUN apt-get install -y build-essential
RUN apt-get install -y curl

RUN distribution=$(. /etc/os-release;echo  $ID$VERSION_ID)  && \
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -  && \
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list

# RUN apt-get install -y docker.io nvidia-container-toolkit    

RUN apt-get update -y
RUN apt-get install -y nvidia-container-toolkit

RUN mkdir -p /etc/docker

RUN nvidia-ctk runtime configure --runtime=docker

RUN pip install uv

# RUN pip install --no-cache-dir transcribe-everything
RUN uv venv
RUN uv pip install transcribe-everything

# Force install ffmpeg
RUN uv run static_ffmpeg -version


# Install the transcriber.
RUN uv pip install transcribe-everything==1.5.20

# Get all the one time installs out of the way.
RUN uv run transcribe-everything-init

# copy your rclone config
COPY rclone.conf .

ENTRYPOINT ["uv", "run", "transcribe-everything"]

# This path is a rclone style remote path. You must have rclone.conf file
# side by side with this program.
CMD ["dst:TorrentBooks/podcast", "--batch-size", "20"]

# 