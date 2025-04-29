#!/bin/bash
# This is designed to work on an Ubuntu 24.10 server
# gpu droplet from Digital Ocean which has a L40S GPu

sudo apt-get update -y
sudo apt-get install -y docker.io

sudo apt-get install -y software-properties-common
sudo add-apt-repository universe -y
sudo apt-get update -y

# 1) Pull your distro identifier (e.g. ubuntu22.04)
# NOOP

# 2) Fetch & install the GPG key
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# 3) Add the generic “stable/deb” repository, substituting your architecture
ARCH=$(dpkg --print-architecture)   # e.g. “amd64”
curl -sL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed \
      -e 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
      -e "s#\$(ARCH)#$ARCH#g" \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 4) Update & install

sudo apt-get update -y
sudo apt-get install -y nvidia-container-toolkit

sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

sudo apt-get update -y
sudo apt-get install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

# now install uv and transcribe-everything

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv venv
uv pip install transcribe-everything

# install pm2
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2

echo "#!/bin/bash" > run_transcription.sh
echo uv run transcribe-everything-run-docker dst:TorrentBooks/podcast --gpu-batch-size 80 >> run_transcription.sh
chmod +x run_transcription.sh
pm2 start run_transcription.sh --name transcribe-everything
pm2 save
pm2 startup

echo Now reboot your system to complete the installation
echo sudo reboot
echo Afterwards, run the following command to verify the installation:
echo nvidia-smi
echo If you see the NVIDIA driver version and GPU information, the installation was successful.
echo If you see an error, please check the installation steps and ensure that your GPU is supported.
echo docker run --rm --gpus all nvidia/cuda:12.2.0-runtime-ubuntu22.04 nvidia-smi
