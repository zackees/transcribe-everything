# pick the CUDA version your host GPU driver supports
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install any extra system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*



# install exactly your transcriber
RUN pip install --no-cache-dir transcribe-everything==1.5.20

RUN transcribe-everything-init

ENTRYPOINT ["transcribe-everything"]

# This path is a rclone style remote path. You must have rclone.conf file
# side by side with this program.
CMD ["dst:TorrentBooks/podcast", "--batch-size", "20"]
