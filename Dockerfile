
# Dockerfile to create the transcribe-everything image.
# Install:
#  docker pull niteris/transcribe-everything
#  -or- docker build -t transcribe-everything .
# Examples:
#  Example 1:
#    docker pull niteris/transcribe-everything
#    docker run --rm -it niteris/transcribe-everything --help
#  Example 2:
#    docker run --rm -it -v ./rclone.conf niteris/transcribe-everything --help



# pick the CUDA version your host GPU driver supports
FROM niteris/transcribe-anything

WORKDIR /app


RUN pip install rclone-api
RUN rclone-api-install-bins

COPY . .
RUN pip install -e .

# # Get all the one time installs out of the way.
# RUN uv run transcribe-everything-init


# copy your rclone config
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh && dos2unix entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Please map in the rclone conf file.
CMD ["--help"]
