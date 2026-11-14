import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from generate_sections_a import build_header_and_sections_1_to_3
from generate_sections_b import build_sections_4_to_7
from generate_sections_c import build_sections_8_to_12_and_appendices

doc = docx.Document()

# Set standard page margins (1.0 inch all around)
for sec in doc.sections:
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)
    
    # Configure Header and Footer
    header = sec.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run("THE CFD ME | CFDME-2025-041 | E119 Companion Simulation Validation Memo | rev 1")
    hr.font.name = 'Arial'
    hr.font.size = Pt(8.5)
    hr.font.color.rgb = RGBColor(100, 116, 139)
    
    footer = sec.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    fr1 = fp.add_run("CONFIDENTIAL & PROPRIETARY — THE CFD MECHANICAL ENGINEER, LLC")
    fr1.font.name = 'Arial'
    fr1.font.size = Pt(8.5)
    fr1.font.color.rgb = RGBColor(100, 116, 139)

print("Building Document Sections...")
build_header_and_sections_1_to_3(doc)
build_sections_4_to_7(doc)
build_sections_8_to_12_and_appendices(doc)

os.makedirs('output', exist_ok=True)
out_path1 = 'output/CFDME-2025-041_E119_validation_memo.docx'
out_path2 = 'output/E119_companion_simulation_validation_memo.docx'

doc.save(out_path1)
doc.save(out_path2)

print(f"Successfully generated {out_path1} ({os.path.getsize(out_path1)} bytes)")
print(f"Successfully generated {out_path2} ({os.path.getsize(out_path2)} bytes)")
