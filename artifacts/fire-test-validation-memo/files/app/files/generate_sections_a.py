# Module A: Memo Header, Section 1, Section 2, Section 3
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from generate_validation_memo import (
    set_cell_margins, set_cell_shading, set_cell_border, add_callout,
    format_cell, add_heading_1, add_heading_2, add_heading_3, add_para, add_bullet
)

def build_header_and_sections_1_to_3(doc):
    # Header block table
    header_table = doc.add_table(rows=7, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False
    
    col_widths = [Inches(1.8), Inches(4.7)]
    for row in header_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width
            set_cell_margins(row.cells[idx], top=60, bottom=60, left=100, right=100)
            set_cell_border(row.cells[idx], bottom=dict(val='single', sz=4, color='CBD5E1'),
                                            top=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
    
    hdr_data = [
        ("MEMORANDUM", "THE CFD MECHANICAL ENGINEER, LLC | Tucson, Arizona | AZ PE #48213"),
        ("DATE:", "October 10, 2025"),
        ("TO:", "Marguerite Falk, PE — Technical Director & Reviewing Engineer (AZ PE #42798)"),
        ("FROM:", "Gordon Selby, PE — Owner & Principal Engineer (AZ PE #48213)"),
        ("PROJECT:", "CFDME-2025-041 — Ocotillo WUI Wildfire Exposure, Phase 1"),
        ("CLIENT:", "Ocotillo Additive Structures (Attn: Trevor Buckhalter, CEO; Bianca Rennert, VP Mktg)"),
        ("SUBJECT:", "ASME V&V 20 Validation Assessment: ASTM E119 Companion Simulation — Reconciliation Against Certified Physical Test, Error Formulation, Diagnostic Comparison, and Phase 1 Scope Disposition")
    ]
    
    for r_idx, (label, val) in enumerate(hdr_data):
        row = header_table.rows[r_idx]
        if r_idx == 0:
            format_cell(row.cells[0], label, bold=True, color="0F2C59", font_size=11.0, bg_color="F1F5F9")
            format_cell(row.cells[1], val, bold=True, color="0F2C59", font_size=9.5, bg_color="F1F5F9")
        else:
            format_cell(row.cells[0], label, bold=True, color="334155", font_size=9.0)
            format_cell(row.cells[1], val, bold=False, color="1E293B", font_size=9.0)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # SECTION 1
    add_heading_1(doc, "1. Executive Summary & ASME V&V 20 Validation Rollup")
    add_para(doc, "This memorandum provides the formal engineering validation audit of the conjugate heat transfer (CHT) companion simulation executed for the Ocotillo Additive Structures (OAS) double-wythe 3D-printed concrete cavity wall assembly under standard ASTM E119 furnace exposure. This audit is conducted pursuant to the governing authority of CFDME Validation QA Procedure — ASME V&V 20 rev 2 (Document: CFDME-QA-VAL-002, effective 05/01/2025), adhering strictly to ASME V&V 20-2009 (R2016).")
    add_para(doc, "The objective of this evaluation is to provide the deterministic, auditable technical content required for Section 7 ('Validation') of the Phase 1 Draft Report (CFDME-2025-041_Phase1_report_revB.docx) and to establish the technical basis for closing Item 6 on the peer-review checklist maintained by Reviewing Engineer Marguerite Falk, PE. Under Section 3 of our governing procedure, validation shall be reported as the model comparison error E = S - D accompanied by its root-sum-square validation uncertainty u_val, and never as a qualitative or binary yes/no statement.")
    add_para(doc, "The reference dataset of record is Red Butte Fire & Materials Testing Report No. RBFMT-25-0918 (test date 09/24/2025, report issued 09/24/2025), which is formally certified by Ironwood Fire Protection Engineering Memorandum No. IWFPE-CERT-25-0374 (dated 09/29/2025, Marla Kettering, PE, AZ PE #45106). The companion simulation run of record is archived in E119_companion_sim_results.csv, modeling CAD geometry of record OAS-WUI-01_revC.")
    
    # Rollup Table
    add_heading_2(doc, "Table 1.1 — ASME V&V 20 Model-Error Rollup and Validation Decision Matrix")
    
    t1 = doc.add_table(rows=10, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    
    t1_widths = [Inches(1.8), Inches(1.3), Inches(0.9), Inches(1.1), Inches(1.4)]
    for row in t1.rows:
        for idx, width in enumerate(t1_widths):
            row.cells[idx].width = width
            set_cell_margins(row.cells[idx], top=80, bottom=80, left=100, right=100)
    
    headers = ["Validation Parameter", "Symbol / Formula", "Value", "Units", "Governing Basis / Source"]
    for idx, text in enumerate(headers):
        format_cell(t1.rows[0].cells[idx], text, bold=True, color="FFFFFF", font_size=9.0, bg_color="0F2C59")
        set_cell_border(t1.rows[0].cells[idx], bottom=dict(val='single', sz=8, color='0F2C59'))
    
    t1_rows = [
        ("Simulation Prediction", "S", "131", "min", "E119_companion_sim_results.csv (crossing at 130.94 min; single-point criterion governs)"),
        ("Certified Experimental Value", "D", "118", "min", "Red Butte Report RBFMT-25-0918 §5.2 / Ironwood Memo IWFPE-CERT-25-0374 §2 (TC-6 tie bridge)"),
        ("Model Comparison Error", "E = S - D", "+13", "min", "ASME V&V 20 §1 / CFDME-QA-VAL-002 §3 (+12.94 min continuous; positive sign = over-prediction)"),
        ("Primary Acceptance Criterion", "|E| <= 0.10 * D", "11.8", "min", "CFDME-QA-VAL-002 §5 (10% scaled tolerance band on certified experimental value D)"),
        ("Validation Uncertainty", "u_val = sqrt(u_num^2 + u_inp^2 + u_exp^2)", "+/-9", "min", "CFDME-QA-VAL-002 §4 (+/-8.77 min RSS of u_num=+/-4 min, u_inp=+/-6 min, u_exp=+/-5 min)"),
        ("Primary Criterion Test", "|E| <= 11.8 min", "13.0 > 11.8", "min", "FAILS PRIMARY CRITERION: Comparison error |E| exceeds 10% threshold by 1.2 min"),
        ("Secondary Uncertainty Test", "|E| <= u_val", "13.0 > 9.0", "min", "FAILS NOISE TEST: |E| exceeds u_val; resolved as actionable systematic model error"),
        ("Maximum Allowable S", "S_max = D + 0.10 * D", "129.8", "min", "Largest simulation prediction clearing primary criterion (129 min whole-minute limit)"),
        ("Validation Final Verdict", "Formal Status", "DOES NOT VALIDATE", "dimensionless", "Unqualified validation claim PROHIBITED under CFDME-QA-VAL-002 §5; release requires Documented Finding")
    ]
    
    for r_idx, data in enumerate(t1_rows):
        row = t1.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        if r_idx in [5, 6, 8]:
            bg = "FEF2F2" # Red tint for failures
        for c_idx, text in enumerate(data):
            is_bold = True if c_idx in [0, 2] or r_idx in [5, 6, 8] else False
            txt_color = "991B1B" if r_idx in [5, 6, 8] and c_idx in [2, 4] else "1E293B"
            format_cell(row.cells[c_idx], text, bold=is_bold, color=txt_color, font_size=8.5, bg_color=bg)
            set_cell_border(row.cells[c_idx], bottom=dict(val='single', sz=4, color='E2E8F0'),
                                              top=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    add_callout(doc, [
        "EXECUTIVE SUMMARY OF FINDINGS:",
        "1. Prediction Holds: The companion simulation prediction of S = 131 min (crossing time 130.94 min) in the Section 7 stub stands without modification.",
        "2. Experimental Anchor: The certified experimental value of record is D = 118 min (Red Butte RBFMT-25-0918, certified by Ironwood PE Marla Kettering). Bianca Rennert's informal post-test figure of 129 min is REJECTED per Section 6 of our procedure.",
        "3. Comparison Error & Tolerance Failure: The comparison error is E = +13 min. Because |E| = 13 min > 11.8 min (10% of D), the simulation FAILS the primary acceptance criterion. Furthermore, because |E| = 13 min > u_val = 9 min, the discrepancy is resolved as an actionable model error.",
        "4. Non-Conservative Physics Bias: A positive error (E = +13 min) indicates that the CFD model over-predicts fire endurance, meaning the physical assembly reaches thermal failure 13 minutes earlier than simulated. In a fire-life-safety evaluation, this represents a non-conservative error.",
        "5. Release Conditions: Phase 1 cannot be released with an unqualified validation claim. Section 7 of the report must state the numerical rollup, record the failure to validate, and document the finding."
    ], title="MANDATORY QA/QC AUDIT DETERMINATION", border_color="991B1B", bg_color="FEF2F2")

    # SECTION 2
    add_heading_1(doc, "2. Actionable Transmittal Paragraph for Bianca Rennert (Same-Day Response)")
    add_para(doc, "On October 9, 2025, Bianca Rennert (VP Product Marketing, Ocotillo Additive Structures) transmitted revised burn figures asserting a single-point endurance of 129 min based on post-test vendor calibration adjustments, requesting same-day authorization to describe the CFD simulation as 'validated against the certified test' in product launch materials scheduled for release on Friday, October 10, 2025. Per your request, below is the exact, unhedged paragraph ready for transmittal to Bianca today:")

    add_callout(doc, [
        "\"Bianca — On the companion simulation for the Red Butte E119 burn, our governing QA procedure (CFDME-QA-VAL-002, adhering to ASME V&V 20) requires us to report model fidelity as a comparison error against the certified test of record rather than a binary validation claim, and prohibits adopting post-test adjustments without an authorized, reissued laboratory report and NIST-traceable calibration certificate. Against Red Butte's certified single-point endurance of 118 min (Report No. RBFMT-25-0918, certified by Ironwood PE Marla Kettering), our companion run predicts 131 min (crossing at 130.94 min), yielding a model error of E = +13 min. Because this discrepancy exceeds both our firm's 10% acceptance threshold (11.8 min) and our combined validation uncertainty (±9 min), the simulation cannot be characterized as validated in your launch materials or press deck. Furthermore, per ASTM E119 Section 8 and our professional standard of care, standard furnace endurance is a comparative building assembly rating and does not predict wildland-urban interface (WUI) wildfire survival; launch materials must not equate the E119 result with Sonoran buffelgrass wildfire performance.\""
    ], title="RECOMMENDED TRANSMITTAL TEXT TO OCOTILLO (BIANCA RENNERT)", border_color="0F2C59", bg_color="F1F5F9")

    add_para(doc, "Engineering Basis of Transmittal: This transmittal protects both the client and The CFD ME from public and regulatory liability. Advertising a CFD model as 'validated' when the comparison error (+13 min) exceeds the governing 10% tolerance (11.8 min) violates ASME V&V 20 and our firm's licensing standard of care under Arizona law. Releasing marketing claims asserting that an E119 1-hour furnace rating confers 'wildfire survival' creates substantial tort liability in WUI residential development.")

    # SECTION 3
    add_heading_1(doc, "3. Assembly Identity & Governing Scope Authority")
    add_para(doc, "A fundamental requirement of ASME V&V 20 is establishing geometric and material equivalence between the physical test specimen and the computational domain. We have cross-checked the assembly modeled in the companion simulation against the dimensioned assembly drawing, the physical test report, and the certification memorandum.")
    
    add_heading_2(doc, "3.1 Through-Wall Cross-Sectional Geometry of Record (OAS-WUI-01_revC)")
    add_para(doc, "The through-wall cross section modeled in the companion run is documented in OAS_wall_assembly_section.png (Drawing No. OAS-WUI-01-SEC, Rev C, dated 2025-10-08; also referenced as OAS-WA-305mm-DW in the title block) and FreeCAD source file OAS-WUI-01_revC.FCStd. The through-wall build comprises:")
    add_bullet(doc, "Exposed Leaf: 50 mm thick 3D-printed concrete using a siliceous aggregate mix, cured to 28-day specification.", bold_prefix="• ")
    add_bullet(doc, "Cavity: 205 mm clear air gap between interior leaf surfaces. Open air; no insulation, no fill, no vapor barrier, and no fire-stop material.", bold_prefix="• ")
    add_bullet(doc, "Unexposed Leaf: 50 mm thick 3D-printed concrete using the same siliceous aggregate mix.", bold_prefix="• ")
    add_bullet(doc, "Overall Wall Thickness: 305 mm total thickness (50 mm + 205 mm + 50 mm).", bold_prefix="• ")
    add_bullet(doc, "Continuous Steel Wall Ties: Continuous truss-type (triangular zigzag) ties fabricated from 9-gauge (3.8 mm diameter) galvanized steel wire, installed at 600 mm on-center vertical spacing, embedded 25 mm into each concrete leaf.", bold_prefix="• ")
    add_bullet(doc, "Structural Boundary Condition: Evaluated as a non-load-bearing vertical partition.", bold_prefix="• ")

    add_heading_2(doc, "3.2 Cross-Check Against Certified Assembly of Record")
    add_para(doc, "We cross-referenced the simulation setup against Section 2 of Red Butte Test Report RBFMT-25-0918 and Section 1.2 of Ironwood Certification Memorandum IWFPE-CERT-25-0374:")
    add_bullet(doc, "Red Butte Specimen Description (§2): Confirms a 305 mm overall thickness double-wythe printed concrete wall with two 50 mm siliceous leaves, a 205 mm open-air cavity, and continuous 9-gauge (3.8 mm) galvanized steel truss ties at 600 mm vertical spacing with 25 mm embedment.", bold_prefix="1. Test Report RBFMT-25-0918: ")
    add_bullet(doc, "Ironwood Certified Geometry (§1.2): Explicitly certifies the assembly tabulated above: 50 mm wythes, 205 mm open cavity, 305 mm overall thickness, siliceous aggregate, and continuous 9-gauge (3.8 mm) galvanized truss ties at 600 mm o.c. with 25 mm embedment. Section 1.2 states: 'Any deviation from the tabulated geometry places the assembly outside the scope of this certification.'", bold_prefix="2. Certification Memo IWFPE-CERT-25-0374: ")
    add_bullet(doc, "Companion Simulation Header: E119_companion_sim_results.csv explicitly identifies the model as 'Companion simulation output — E119 furnace exposure of Ocotillo wall assembly (OAS-WUI-01_revC)'.", bold_prefix="3. Simulation Run of Record: ")

    add_heading_2(doc, "3.3 Determination on Assembly Equivalence")
    add_para(doc, "DETERMINATION: YES, the assembly modeled in the companion simulation is the exact through-wall assembly that the Ironwood certification covers.", bold_prefix="Formal Finding: ")
    add_para(doc, "What this determination rests on: This conclusion rests on the exact one-to-one correspondence of all governing through-thickness parameters: leaf thickness (50 mm each), cavity width (205 mm open air), total thickness (305 mm), concrete aggregate type (siliceous), tie wire gauge (9-gauge, 3.8 mm diameter), tie geometry (continuous triangular zigzag truss), tie vertical spacing (600 mm o.c.), tie embedment depth (25 mm each side), and absence of cavity insulation or fill.")
    add_para(doc, "Dimensional Note on Panel Face Area: The physical specimen evaluated in the Red Butte furnace was 3.05 m × 3.05 m (10 ft × 10 ft), matching the standard test frame. The CAD model OAS-WUI-01_revC represents a modular WUI field panel of 1.83 m × 2.745 m (6 ft × 9 ft). This face-dimension distinction does not alter through-wall conjugate heat transfer or metallic tie thermal-bridge conduction, because heat transmission across the cavity and through the ties is governed entirely by the through-wall cross section and vertical tie pitch (600 mm o.c.), which are identical.")

    add_heading_2(doc, "3.4 Disposition on Geometry Revision D (Parapet Addition)")
    add_para(doc, "On October 9, 2025 at 16:12 MST, Trevor Buckhalter transmitted geometry revision OAS-WUI-01_revD (20251009_Buckhalter_geometry_revD.eml), which adds a continuous 610 mm hollow parapet above the main wall (increasing total height to 3355 mm), with a 50 mm coping cap and 25 mm outer drip overhang. We confirm:")
    add_bullet(doc, "The companion simulation was executed exclusively on revision C (OAS-WUI-01_revC) and does not incorporate the parapet.", bold_prefix="• ")
    add_bullet(doc, "The Red Butte physical test evaluated revision C without a parapet.", bold_prefix="• ")
    add_bullet(doc, "Ironwood's 1-hour certification covers revision C only. Under Section 1.2 of Ironwood's memo, adding a 610 mm hollow parapet represents a geometric deviation that places revision D outside the certified fire-resistance rating. Any rating claim for revD would require physical retesting and re-certification by a registered fire-protection PE.", bold_prefix="• ")

print("Compiled generate_sections_a.py successfully.")
