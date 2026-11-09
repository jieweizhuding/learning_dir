#!/usr/bin/env bash
# OpenCOOD 环境搭建脚本 —— 在 WSL2 Ubuntu-20.04 终端里执行
# 用法：复制本文件到 WSL（如 ~/setup_wsl.sh），然后 bash ~/setup_wsl.sh
set -e

echo "=== 1. 检查/安装 miniconda ==="
if [ ! -d "$HOME/miniconda3" ]; then
  wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
  bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
fi
source "$HOME/miniconda3/etc/profile.d/conda.sh"

echo "=== 2. 创建 python 3.9 环境 ==="
conda create -n opencood python=3.9 -y
conda activate opencood

echo "=== 2.5 安装 gcc（编译 box_overlaps Cython 扩展）==="
sudo apt-get update -y && sudo apt-get install -y build-essential

echo "=== 3. 安装 CUDA toolkit 11.3（提供 nvcc）==="
conda install -c nvidia cudatoolkit=11.3 -y

echo "=== 4. 安装 torch 1.10 + cu113 ==="
pip install torch==1.10.0+cu113 torchvision==0.11.0+cu113 torchaudio==0.10.0+cu113 \
  -f https://download.pytorch.org/whl/torch_stable.html

echo "=== 5. 安装 spconv 2.1.1 + 匹配的 cumm ==="
pip install spconv==2.1.1
pip install cumm==0.2.1

echo "=== 6. 克隆 OpenCOOD 到 Linux 原生文件系统（避免 /mnt/c 中文路径与跨盘性能问题）==="
cd "$HOME"
[ -d OpenCOOD ] || git clone --depth 1 https://github.com/DerrickXuNu/OpenCOOD.git
cd OpenCOOD

echo "=== 7. 安装依赖（去掉 numba 0.49，其在 py3.9 装不上且代码未用到）==="
sed '/numba/d' requirements.txt > /tmp/opencood_req.txt
pip install -r /tmp/opencood_req.txt

echo "=== 8. 编译 NMS CUDA 扩展 ==="
python opencood/utils/setup.py build_ext --inplace

echo "=== 9. 验证 ==="
python -c "import torch; print('torch', torch.__version__, 'cuda_avail', torch.cuda.is_available())"
python -c "import spconv; print('spconv', spconv.__version__)"
python -c "import opencood; print('opencood import OK')"

echo "=== ALL DONE ==="
