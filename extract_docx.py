# -*- coding: utf-8 -*-
import sys
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

src = r"C:\Users\17563\Downloads\任务驱动通信与端云协同规控_研究调研报告.docx"
dst = r"_report_extract.txt"
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
print("lines:", len(out))
