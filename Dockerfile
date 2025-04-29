# pick the CUDA version your host GPU driver supports
FROM pytorch/pytorch:2.6.0-cuda12.6-cudnn9-runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -y

# install any extra system deps
RUN apt-get install -y build-essential
RUN apt-get install -y curl dos2unix


RUN distribution=$(. /etc/os-release;echo  $ID$VERSION_ID)  && \
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -  && \
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list

# RUN apt-get install -y docker.io nvidia-container-toolkit    

RUN apt-get update -y
RUN apt-get install -y nvidia-container-toolkit

RUN mkdir -p /etc/docker

RUN nvidia-ctk runtime configure --runtime=docker

RUN pip install transcribe-anything>=3.0.10

COPY entrypoint.sh /app/entrypoint.sh
COPY check_linux_shared_libraries.py /app/check_linux_shared_libraries.py

RUN /bin/bash /app/entrypoint.sh --only-check-shared-libs && transcribe-anything-init-insane


COPY . .
RUN uv pip install -e .

# # Get all the one time installs out of the way.
# RUN uv run transcribe-everything-init


# copy your rclone config
COPY rclone.conf .
RUN chmod +x entrypoint.sh && dos2unix entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# This path is a rclone style remote path. You must have rclone.conf file
# side by side with this program.
CMD ["dst:TorrentBooks/podcast", "--batch-size", "20"]
