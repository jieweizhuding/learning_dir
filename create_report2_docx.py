# -*- coding: utf-8 -*-
"""生成《任务驱动通信与端云协同规控》选题报告 docx"""
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
normal = doc.styles["Normal"]
normal.font.name = ASCII
normal.font.size = Pt(12)
normal.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), EAST_BODY)

t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(t.add_run("任务驱动通信与端云协同规控 选题报告"), east=EAST_HEAD, size=18, bold=True, color=BLACK)
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


heading("一、选题名称")
body("《面向动态网络约束的规划价值感知协作通信方法研究》")
body("英文：Planning-Value-Aware Cooperative Communication under Dynamic Network Constraints")

heading("二、研究背景与意义")
body("联网机器人/自动驾驶系统由感知、通信、预测、规划、控制构成闭环。网络带宽、时延与丢包不仅决定消息能否送达，还决定观测在决策时间窗内是否仍然有效。传统协同感知只优化检测精度与传输量，而规控更关心碰撞风险、轨迹质量、任务完成率与安全回退能力。因此，应将「信息对规划的收益」与「网络资源消耗」共同纳入研究目标。")

heading("三、国内外研究现状")
body("1. 任务导向协同框架：UniV2X（AAAI 2025）、UniMM-V2X（AAAI 2026），已有端到端规划，可作规划基线。")
body("2. 高效协同感知通信：CoSDH、mmCooper、CoST、WhisperNet、CoopTrack（CVPR/ICCV 2025–2026），通信已从固定压缩转向空间/实例/时序选择与接收方需求协调。")
body("3. 现状小结：突破口不在「能否挑选重要消息」，而在「消息对未来规划值多少钱、晚到后还有没有价值」。")

heading("四、研究内容")
body("1. 规划价值感知的信息选择（第一阶段，主）")
body("2. 时延感知的任务价值估计（第二阶段）")
body("3. 风险感知的端云规控卸载（后续扩展）")

heading("五、拟解决的关键问题")
body("主问题：", bold=True)
body("在字节预算约束下，如何按「对未来轨迹与安全的边际价值」选择要传输的协作信息，而非仅按检测置信度 / 特征强度排序？")
body("价值定义：消息 z_i 的规划边际价值 V_i = J(π 不含 z_i) − J(π 含 z_i)，其中 J 为规划代价；以轻量价值预测器逼近，联合优化规划收益与消息字节数。")

heading("六、研究方案与技术路线")
body("- 基线：UniV2X、CoSDH、WhisperNet 等；对比组 B0–B6（不协作 / 全量 / 随机 / 置信度 / 规则 / 时效 / 拟提出）")
body("- 数据：DAIR-V2X / V2X-Seq-SPD、OpenCOOD；闭环用 CARLA + 网络仿真")
body("- 指标：AP、ADE / FDE、碰撞率、成功率、字节/帧、E2E 时延")
body("- 路线：复现基线 → 受控离线实验验证「规划价值选择」假设 → CARLA 闭环")

heading("七、可行性分析")
body("- 数据 / 代码开源，可复现：DAIR-V2X、OpenCOOD、UniV2X")
body("- 算力：RTX 3060 + 冻结特征即可开展通信策略研究")
body("- 实验协议清晰：离线对比（B0–B6）→ 闭环验证，指标明确")
body("- 风险：领域拥挤；跨领域撞车（需先核验 Value of Information / Age of Information / 语义通信 / 网络化 MPC）")

heading("八、预期成果与创新点")
body("- 预期成果：一篇论文 + 开源代码")
body("- 创新点：构建可测量的「规划价值」通信目标与轻量消息排序 / 预算选择方法；报告通信量—碰撞率 / 规划误差 Pareto 曲线")

heading("九、进度安排（示例，可调整）")
body("第 1 月：阅读 UniV2X / WhisperNet / CoSDH，核验代码，跑通基线管线")
body("第 2 月：构建 B0–B4，固定通信字节预算")
body("第 3 月：按场景风险分层做误差分析，定位失败模式")
body("第 4–5 月：设计轻量规划价值估计器与预算分配策略")
body("第 6–7 月：加入时延 / 丢包 / 带宽波动，做闭环仿真")
body("第 8 月后：强基线、跨场景消融、撰写投稿")

heading("十、参考文献（精选）")
refs = [
    "UniV2X. AAAI 2025.",
    "UniMM-V2X. AAAI 2026.",
    "CoSDH. CVPR 2025.",
    "mmCooper. ICCV 2025.",
    "CoST. ICCV 2025.",
    "WhisperNet. CVPR 2026.",
    "CoopTrack. ICCV 2025.",
    "OpenCOOD / DAIR-V2X（开源代码与数据集）。",
]
for i, r in enumerate(refs, 1):
    body(f"{i}. {r}")

doc.save("任务驱动通信选题报告.docx")
print("saved")
