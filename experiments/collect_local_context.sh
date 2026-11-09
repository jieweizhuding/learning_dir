#!/usr/bin/env bash
# 在 WSL 中执行：bash experiments/collect_local_context.sh [OpenCOOD根目录]
set -euo pipefail
repo_dir="${1:-$HOME/OpenCOOD}"
output_dir="$(mktemp -d /tmp/opencood-context.XXXXXX)"
cd "$repo_dir"
for source_file in \
  opencood/models/point_pillar_v2vnet.py \
  opencood/models/sub_modules/pillar_vfe.py \
  opencood/models/sub_modules/point_pillar_scatter.py \
  opencood/models/sub_modules/base_bev_backbone.py \
  opencood/models/fuse_modules/v2v_fuse.py \
  opencood/data_utils/datasets/basedataset.py \
  opencood/data_utils/datasets/intermediate_fusion_dataset.py \
  opencood/tools/inference.py \
  opencood/tools/train_utils.py \
  opencood/hypes_yaml/yaml_utils.py; do
  if [[ -f "$source_file" ]]; then
    mkdir -p "$output_dir/$(dirname "$source_file")"
    cp -- "$source_file" "$output_dir/$source_file"
  else
    printf '%s\n' "$source_file" >> "$output_dir/missing-files.txt"
  fi
done
find "$repo_dir" -type f \( -name '*.pth' -o -name '*.pt' \) -print > "$output_dir/checkpoint-paths.txt"
free -h > "$output_dir/memory.txt"
df -h /dev/shm > "$output_dir/shared-memory.txt"
printf '收集完成：%s\n仅回传前请检查是否含有不希望分享的本地源码或路径。\n' "$output_dir"
