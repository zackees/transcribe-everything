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

# This path is a rclone style remote path. You must have rclone.conf file
# side by side with this program.
CMD ["--help"]
