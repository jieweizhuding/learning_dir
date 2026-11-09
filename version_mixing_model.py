# -*- coding: utf-8 -*-
"""
版本混用模型补丁（草案 · 未在 WSL 验证）
修改自 opencood/models/point_pillar_intermediate.py

设计：把「版本」定义为单体感知编码器 pillar_vfe；
      不同智能体用不同版本 (v1/v2) 的 pillar_vfe，共享 scatter + backbone（融合与检测头）。
智能体序号 = voxel_coords[:, 0]（OpenCOOD 中间融合数据集里每个智能体的 voxel 坐标第 0 维为其序号）。

用法：
  1) 把本文件放到 OpenCOOD/opencood/models/ 下（或 import 本类）。
  2) 从两个 checkpoint（同架构不同训练阶段）各取 pillar_vfe 权重，用 load_encoder_weights 载入。
  3) 推理时按版本组合传入 version_assign（长度=智能体数，0 用 v1、1 用 v2）。
"""
import torch
import torch.nn as nn

from opencood.models.sub_modules.pillar_vfe import PillarVFE
from opencood.models.sub_modules.point_pillar_scatter import PointPillarScatter
from opencood.models.sub_modules.att_bev_backbone import AttBEVBackbone


def _strip_prefix(state_dict, prefix='pillar_vfe.'):
    """从完整模型 state_dict 中抽取 pillar_vfe 部分。"""
    out = {}
    for k, v in state_dict.items():
        if k.startswith(prefix):
            out[k[len(prefix):]] = v
    return out


class PointPillarIntermediateVersionMix(nn.Module):
    def __init__(self, args):
        super().__init__()
        cfg_pvfe = args['pillar_vfe']
        self.pillar_vfe_v1 = PillarVFE(cfg_pvfe, num_point_features=4,
                                       voxel_size=args['voxel_size'],
                                       point_cloud_range=args['lidar_range'])
        self.pillar_vfe_v2 = PillarVFE(cfg_pvfe, num_point_features=4,
                                       voxel_size=args['voxel_size'],
                                       point_cloud_range=args['lidar_range'])
        self.scatter = PointPillarScatter(args['point_pillar_scatter'])
        self.backbone = AttBEVBackbone(args['base_bev_backbone'], 64)
        self.cls_head = nn.Conv2d(128 * 3, args['anchor_number'], kernel_size=1)
        self.reg_head = nn.Conv2d(128 * 3, 7 * args['anchor_num'], kernel_size=1)

    def load_encoder_weights(self, v1_ckpt_state, v2_ckpt_state):
        """v1/v2 为完整 checkpoint 的 state_dict（含 pillar_vfe. 前缀），自动抽取。"""
        self.pillar_vfe_v1.load_state_dict(_strip_prefix(v1_ckpt_state))
        self.pillar_vfe_v2.load_state_dict(_strip_prefix(v2_ckpt_state))

    def forward(self, data_dict, version_assign=None):
        """
        version_assign: None  -> 全部智能体用 v1（等价原单编码器行为）
                        list   -> 长度=智能体数，元素 0(v1)/1(v2)
        """
        voxel_features = data_dict['processed_lidar']['voxel_features']
        voxel_coords = data_dict['processed_lidar']['voxel_coords']
        voxel_num_points = data_dict['processed_lidar']['voxel_num_points']
        record_len = data_dict['record_len']

        if version_assign is None:
            batch_dict = {'voxel_features': voxel_features,
                          'voxel_coords': voxel_coords,
                          'voxel_num_points': voxel_num_points,
                          'record_len': record_len}
            batch_dict = self.pillar_vfe_v1(batch_dict)
        else:
            agent_ids = torch.unique(voxel_coords[:, 0])  # 升序，与 record_len 顺序一致
            pillar_list = []
            for i, aid in enumerate(agent_ids):
                mask = voxel_coords[:, 0] == aid
                sub = {'voxel_features': voxel_features[mask],
                       'voxel_coords': voxel_coords[mask],
                       'voxel_num_points': voxel_num_points[mask]}
                enc = self.pillar_vfe_v1 if int(version_assign[i]) == 0 \
                    else self.pillar_vfe_v2
                sub = enc(sub)
                pillar_list.append(sub['pillar_features'])
            pillar_features = torch.cat(pillar_list, dim=0)
            batch_dict = {'pillar_features': pillar_features,
                          'voxel_coords': voxel_coords,
                          'record_len': record_len}

        batch_dict = self.scatter(batch_dict)
        batch_dict = self.backbone(batch_dict)

        spatial_features_2d = batch_dict['spatial_features_2d']
        psm = self.cls_head(spatial_features_2d)
        rm = self.reg_head(spatial_features_2d)
        return {'psm': psm, 'rm': rm}
