#!/bin/bash

# ENTRYPOINT ["uv", "run", "transcribe-everything"]

# ENV LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib64:${LD_LIBRARY_PATH}

export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib64:${LD_LIBRARY_PATH}

uv run transcribe-everything "$@"