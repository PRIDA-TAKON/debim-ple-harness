with open('generate_validation_memo.py', 'r') as f:
    text = f.read()

old_func = """def add_para(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10.0)
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    r = p.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(10.0)
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p"""

new_func = """def add_para(doc, text, bold_prefix=None, space_after=4, italic=False, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(10.0)
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.name = 'Arial'
    r.font.size = Pt(10.0)
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p"""

text = text.replace(old_func, new_func)
with open('generate_validation_memo.py', 'w') as f:
    f.write(text)

print("Updated generate_validation_memo.py successfully")
