#!/bin/bash

# ENTRYPOINT ["uv", "run", "transcribe-everything"]

# ENV LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib64:${LD_LIBRARY_PATH}

#export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib64:/opt/conda/lib/python3.11/site-packages/nvidia/cudnn/lib:./opt/conda/lib/python3.11/site-packages/cusparselt/lib/:${LD_LIBRARY_PATH}

export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_runtime/lib64:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cudnn/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/cusparselt/lib/:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cuda_cupti/lib/:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cusparse/lib/:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cufft/lib/:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/curand/lib/:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/cublas/lib/:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/opt/conda/lib/python3.11/site-packages/nvidia/nccl/lib/:${LD_LIBRARY_PATH}

# assert that libcudnn.so.9 can be found through it's LD_LIBRARY_PATH
# assert that libcudnn.so.9 can actually be loaded by the dynamic linker
# if python3 - <<'EOF' &> /dev/null
# import ctypes
# ctypes.CDLL('libcudnn.so.9')
# EOF
# then
#     echo "✓ libcudnn.so.9 loadable"
# else
#     echo "✗ libcudnn.so.9 NOT loadable"
#     exit 1
# fi
if uv run check_linux.py
then
    echo "✓ check_linux.py"
else
    echo "✗ check_linux.py"
    exit 1
fi

uv run transcribe-everything "$@"