import os
import datetime
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import make_memo_docx as helper

def create_memo_document():
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.different_first_page_header_footer = True

    # Color Palette
    c_navy = RGBColor(0x1B, 0x36, 0x5D)      # Primary Header Navy #1B365D
    c_slate = RGBColor(0x2C, 0x52, 0x82)     # Secondary Slate #2C5282
    c_charcoal = RGBColor(0x22, 0x22, 0x22)  # Body Charcoal #222222
    c_red = RGBColor(0xC5, 0x30, 0x30)       # Alert Red #C53030
    c_grey = RGBColor(0x55, 0x55, 0x55)      # Muted Grey #555555

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = c_charcoal
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Header / Footer for subsequent pages
    header = sections[0].header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_head = p_head.add_run("DESERT SAGE RANCH PHASE 3  |  MEMORANDUM TO CALLAWAY LAND PARTNERS  |  10/31/2026")
    r_head.font.name = 'Calibri'
    r_head.font.size = Pt(8.5)
    r_head.font.color.rgb = c_grey

    footer = sections[0].footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run("Sundial Engineering & Survey  ·  Confidential Professional Engineering Work Product  ·  Page ")
    r_foot.font.name = 'Calibri'
    r_foot.font.size = Pt(8.5)
    r_foot.font.color.rgb = c_grey
    # Add page number field via XML
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p_foot._p.append(fldSimple)

    # -------------------------------------------------------------
    # LETTERHEAD
    # -------------------------------------------------------------
    p_firm = doc.add_paragraph()
    p_firm.paragraph_format.space_after = Pt(2)
    p_firm.paragraph_format.space_before = Pt(0)
    r_firm = p_firm.add_run("SUNDIAL ENGINEERING & SURVEY")
    r_firm.font.name = 'Calibri'
    r_firm.font.size = Pt(16)
    r_firm.font.bold = True
    r_firm.font.color.rgb = c_navy

    p_subfirm = doc.add_paragraph()
    p_subfirm.paragraph_format.space_after = Pt(12)
    r_subfirm = p_subfirm.add_run("4720 South Rainbow Boulevard, Suite 210, Las Vegas, Nevada 89103  ·  (702) 555-0142  ·  NV COA #C-3874")
    r_subfirm.font.name = 'Calibri'
    r_subfirm.font.size = Pt(9)
    r_subfirm.font.color.rgb = c_grey

    # Horizontal rule
    p_rule = doc.add_paragraph()
    p_rule.paragraph_format.space_after = Pt(14)
    p_rule_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="1B365D"/></w:pBdr>')
    p_rule._p.get_or_add_pPr().append(p_rule_border)

    # Memo Title
    p_memo_title = doc.add_paragraph()
    p_memo_title.paragraph_format.space_after = Pt(12)
    r_mt = p_memo_title.add_run("MEMORANDUM")
    r_mt.font.name = 'Calibri'
    r_mt.font.size = Pt(18)
    r_mt.font.bold = True
    r_mt.font.color.rgb = c_navy

    # Memo Meta Table
    memo_table = doc.add_table(rows=5, cols=2)
    memo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    memo_table.autofit = False
    memo_table.columns[0].width = Inches(1.2)
    memo_table.columns[1].width = Inches(5.3)

    meta_data = [
        ("TO:", "Callaway Land Partners\nAttn: Garrett Nokes, Vice President of Land Development\n8880 W. Sunset Road, Suite 400, Las Vegas, NV 89148"),
        ("FROM:", "Jonathan R. Kessler, PE (Nevada PE No. 14203), Principal-in-Charge\nSundial Engineering & Survey"),
        ("DATE:", "October 31, 2026"),
        ("COPIES TO:", "Max Braddock, Project Manager, Sundial Engineering & Survey\nPriya Sarwal, PE, Civil Design Lead, Sundial Engineering & Survey\nBea Cortland, PLA (NV LA #742), Ocotillo Landscape Studio\nAdrienne Vogel, Esq., Vogel & Marsh LLP"),
        ("SUBJECT:", "DESERT SAGE RANCH PHASE 3 (JOB NO. 2201-03 / IP-26-100288 / FM-26-100290 / TM-22-500041) — ENGINEERING AUDIT OF COMMENT L-4 STREET TREE REVISION, CRITICAL PATH RESUBMITTAL FEASIBILITY FOR 11/30/2026, REQUIRED PRECONDITIONS, AND STATUTORY PRESENTATION DEADLINE RISKS UNDER NRS 278.360")
    ]

    for r_idx, (label, val) in enumerate(meta_data):
        row = memo_table.rows[r_idx]
        cell_lbl = row.cells[0]
        cell_val = row.cells[1]
        helper.set_cell_margins(cell_lbl, top=40, bottom=40, left=40, right=40)
        helper.set_cell_margins(cell_val, top=40, bottom=40, left=40, right=40)
        helper.set_cell_border(cell_lbl, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})
        helper.set_cell_border(cell_val, bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})
        
        p_l = cell_lbl.paragraphs[0]
        p_l.paragraph_format.space_before = Pt(2)
        p_l.paragraph_format.space_after = Pt(2)
        r_l = p_l.add_run(label)
        r_l.font.name = 'Calibri'
        r_l.font.size = Pt(10)
        r_l.font.bold = True
        r_l.font.color.rgb = c_navy
        
        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_before = Pt(2)
        p_v.paragraph_format.space_after = Pt(2)
        p_v.paragraph_format.line_spacing = 1.15
        r_v = p_v.add_run(val)
        r_v.font.name = 'Calibri'
        r_v.font.size = Pt(10)
        if label == "SUBJECT:":
            r_v.font.bold = True
            r_v.font.color.rgb = c_navy
        else:
            r_v.font.color.rgb = c_charcoal

    p_post_meta = doc.add_paragraph()
    p_post_meta.paragraph_format.space_after = Pt(8)
    p_meta_rule = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="1B365D"/></w:pBdr>')
    p_post_meta._p.get_or_add_pPr().append(p_meta_rule)

    print("Header and metadata constructed.")
    return doc

doc = create_memo_document()
doc.save("output/test_memo.docx")
print("Saved test docx")
