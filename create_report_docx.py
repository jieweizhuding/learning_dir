# -*- coding: utf-8 -*-
"""生成《事件相机三维重建》选题报告 docx"""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

EAST_BODY = "宋体"
EAST_HEAD = "黑体"
ASCII = "Times New Roman"
BLACK = RGBColor(0, 0, 0)


def set_run(run, east=EAST_BODY, ascii_font=ASCII, size=12, bold=False, color=None):
    run.font.name = ascii_font
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), east)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


doc = Document()

# Normal 样式默认中文字体
normal = doc.styles["Normal"]
normal.font.name = ASCII
normal.font.size = Pt(12)
normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), EAST_BODY)

# 标题
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(t.add_run("事件相机三维重建 选题报告"), east=EAST_HEAD, size=18, bold=True, color=BLACK)
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(sub.add_run("（暂定选题 · 计算机技术专业）"), size=12, color=BLACK)


def heading(text):
    p = doc.add_heading(level=1)
    run = p.add_run(text)
    set_run(run, east=EAST_HEAD, size=14, bold=True, color=BLACK)
    return p


def body(text, bold=False):
    p = doc.add_paragraph()
    set_run(p.add_run(text), size=12, bold=bold, color=BLACK)
    return p


# 一、选题名称
heading("一、选题名称")
body("基于事件相机的三维场景重建方法研究")

# 二、研究背景与意义
heading("二、研究背景与意义")
body("事件相机（Event Camera，又称动态视觉传感器 DVS）是一种仿生视觉传感器，仅输出像素级的异步亮度变化事件，而非固定帧率的图像。相比传统 RGB 相机，它具有微秒级时间分辨率、高动态范围（>120 dB）、无运动模糊、低功耗与低延迟等优势，特别适合高速运动、低照度/大动态范围以及资源受限的移动平台（无人机、机器人、自动驾驶等）。")
body("三维重建是计算机视觉的基础任务之一。传统基于帧的相机在高速运动或低照度场景下容易出现运动模糊或曝光不足，导致重建失败；事件相机天然适配这些极端场景，因此“事件相机三维重建”成为兼具前沿性与应用价值的研究方向。其意义在于为极端光照与高速运动场景提供鲁棒、低延迟的三维感知能力，支撑机器人、AR/VR 与自动驾驶等应用。")

# 三、国内外研究现状
heading("三、国内外研究现状")
body("当前研究大致沿三条技术路线演进：")
body("1. 事件 SLAM / 视觉里程计：如 EVO、ESVO、Ultimate SLAM 等，多为稀疏或半稠密重建，属于早期工作。")
body("2. 事件神经辐射场（Event NeRF）：EventNeRF（CVPR 2023）、E-NeRF（ICCV 2023）等，将神经辐射场引入事件相机，从运动事件相机恢复稠密场景，是当前代表性路线。")
body("3. 事件 3D 高斯泼溅（Event 3DGS）：Event3DGS、EvGGS 等（2024–2025），训练更快、可编辑、支持跨场景泛化，是当前最前沿方向。")
body("相关综述（如 A Survey of 3D Reconstruction with Event Cameras, 2025）表明：该领域正从稀疏走向稠密、从单场景拟合走向跨场景泛化，但仍处于早期，公开基线较少、尚未收敛。")

# 四、研究内容
heading("四、研究内容")
body("1. 事件数据预处理与噪声抑制；")
body("2. 事件驱动的神经渲染重建（NeRF / 3DGS）；")
body("3. 单目尺度估计与稠密深度恢复；")
body("4.（可选）跨传感器 / 跨场景泛化与多模态融合。")

# 五、拟解决的关键问题
heading("五、拟解决的关键问题")
body("主问题：", bold=True)
body("在事件数据稀疏、含噪声、且缺乏绝对强度信息的条件下，如何实现鲁棒、稠密、可泛化的三维场景重建？")
body("可拆解子问题：")
body("1. 噪声与稀疏事件下的稳定优化与训练；")
body("2. 单目事件的尺度不确定性与稠密几何恢复；")
body("3. 跨传感器、跨场景的泛化能力。")

# 六、研究方案与技术路线
heading("六、研究方案与技术路线")
body("- 基线复现：EventNeRF、Event3DGS；")
body("- 数据：MVSEC、DSEC、TUM-VIE 及合成事件数据（如 E-3DGS）；")
body("- 指标：PSNR / SSIM / LPIPS（新视角合成）、深度误差、位姿误差；")
body("- 技术栈：PyTorch + 开源 NeRF / 3DGS 代码；")
body("- 路线：复现基线 → 定位一个具体缺口（噪声鲁棒 / 泛化 / 尺度恢复）→ 提出改进方法 → 实验验证与对比。")

# 七、可行性分析
heading("七、可行性分析")
body("- 数据公开：MVSEC、DSEC、TUM-VIE 等数据集可用；")
body("- 开源基线存在：EventNeRF、Event3DGS 等可复现（数量较少但可自实现部分模块）；")
body("- 算力：单场景 NeRF / 3DGS 单卡可训；")
body("- 风险：事件相机成像模型存在概念门槛；公开基线较少，需自行实现部分内容。")

# 八、预期成果与创新点
heading("八、预期成果与创新点")
body("- 预期成果：一篇论文（新视角合成 / 深度估计方向）、开源代码与预训练模型；")
body("- 创新点：在噪声鲁棒、跨场景泛化或单目尺度恢复等具体点提出新方法。")

# 九、进度安排
heading("九、进度安排（示例，可调整）")
body("第 1–3 月：补事件相机与神经渲染基础，复现 EventNeRF / Event3DGS；")
body("第 4–8 月：确定具体研究问题，提出方法并完成主体实验；")
body("第 9–12 月：整理结果，撰写并投稿论文。")

# 十、参考文献
heading("十、参考文献（精选）")
refs = [
    "Zhu et al. The Multivehicle Stereo Event Camera Dataset (MVSEC). IJRR, 2018.",
    "Gehrig et al. DSEC: A Stereo Event Camera Dataset for Driving Scenarios. CVPR, 2021.",
    "Klenk et al. TUM-VIE: Visual-Inertial Event Dataset. 2021.",
    "Rudnev et al. EventNeRF: Neural Radiance Fields from a Single Colour Event Camera. CVPR, 2023.",
    "Klenk et al. E-NeRF: Neural Radiance Fields from a Moving Event Camera. ICCV, 2023.",
    "Zhou et al. ESVO: Event-based Stereo Visual Odometry. TPAMI, 2021.",
    "Wang et al. Event3DGS: Event-based 3D Gaussian Splatting for Fast Egomotion. 2024.",
    "Wang et al. EvGGS: A Collaborative Learning Framework for Event-based Generalizable Gaussian Splatting. 2024.",
    "A Survey of 3D Reconstruction with Event Cameras. arXiv:2505.08438, 2025.",
]
for i, r in enumerate(refs, 1):
    body(f"{i}. {r}")

doc.save("事件相机三维重建选题报告.docx")
print("saved")
