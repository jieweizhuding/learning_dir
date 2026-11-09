# -*- coding: utf-8 -*-
"""向已排除方向档案追加「模型后向兼容性」近邻补充章节"""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

EAST_BODY = "宋体"
EAST_HEAD = "黑体"
BLACK = RGBColor(0, 0, 0)

def set_run(run, east=EAST_BODY, size=12, bold=False, color=None):
    run.font.name = "Times New Roman"
    rpr = run._element.get_or_add_rPr()
    rpr.get_or_add_rFonts().set(qn("w:eastAsia"), east)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color

path = r"已排除方向_新颖性复核与已有研究清单.docx"
doc = Document(path)

def heading(text):
    p = doc.add_heading(level=1)
    set_run(p.add_run(text), east=EAST_HEAD, size=14, bold=True, color=BLACK)
    return p

def body(text):
    p = doc.add_paragraph()
    set_run(p.add_run(text), size=12, color=BLACK)
    return p

heading("9. 补充近邻（2026-11-09 追加）：模型后向兼容性（ML 系统社区）")
body("适用范围：当前「模型异步演化下的协同感知与规划兼容性」候选（状态：有条件推进，未排除）。此前近邻清单仅覆盖 CV 异构协作感知，漏查了 ML 系统社区。该社区早已把「模型升级→下游兼容性退化」当作独立命题，直接威胁「单体升级导致协作退化（H1）」这一抽象命题的新颖性。")
body("已有研究：")
body("1. Bansal et al. Updates in Human-AI Teams: Understanding and Addressing the Performance/Compatibility Tradeoff. NeurIPS 2019.")
body("2. An Empirical Analysis of Backward Compatibility in Machine Learning Systems. KDD 2020. https://dl.acm.org/doi/10.1145/3394486.3403379")
body("3. Backward-Compatible Prediction Updates: A Probabilistic Approach. NeurIPS 2021. https://papers.neurips.cc/paper/2021/hash/012d9fe15b2493f21902cd55603382ec-Abstract.html")
body("4. MUSCLE: A Model Update Strategy for Compatible LLM Evolution. EMNLP 2024 Findings. https://aclanthology.org/2024.findings-emnlp.430/")
body("结论：候选方向的新颖性必须精确到「多智能体协作感知/规划中的版本演化」，并证明其失效机理与「静态异构」「异步时延」「通用模型后向不兼容」三者都不同，否则与上述文献撞车。")

doc.save(path)
print("appended")
