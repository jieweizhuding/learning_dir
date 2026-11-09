# -*- coding: utf-8 -*-
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

def iter_blocks(doc):
    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, doc)
        elif child.tag == qn('w:tbl'):
            yield Table(child, doc)

def dump(src, dst):
    doc = Document(src)
    out = []
    for b in iter_blocks(doc):
        if isinstance(b, Paragraph):
            t = b.text.strip()
            if t:
                out.append(t)
        else:
            out.append("=== TABLE ===")
            for row in b.rows:
                cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
                out.append(" | ".join(cells))
            out.append("=== END TABLE ===")
    open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    print(dst, "lines:", len(out))

dump(r"C:\Users\17563\Downloads\候选方向_模型异步演化与协作规划兼容性_研究报告.docx", r"候选方向提取.txt")
dump(r"C:\Users\17563\Downloads\已排除方向_新颖性复核与已有研究清单 - 副本.docx", r"已排除方向提取.txt")
