import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
# remove default sheet
wb.remove(wb.active)

# Styles
font_title = Font(name='Calibri', size=16, bold=True, color='1B365D')
font_subtitle = Font(name='Calibri', size=11, italic=True, color='555555')
font_sec_hdr = Font(name='Calibri', size=13, bold=True, color='1B365D')
font_tbl_hdr = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
font_bold = Font(name='Calibri', size=11, bold=True)
font_regular = Font(name='Calibri', size=11)
font_italic = Font(name='Calibri', size=10, italic=True)

fill_hdr = PatternFill(start_color='1B365D', end_color='1B365D', fill_type='solid')
fill_subhdr = PatternFill(start_color='2C5282', end_color='2C5282', fill_type='solid')
fill_zebra = PatternFill(start_color='F7FAFC', end_color='F7FAFC', fill_type='solid')
fill_highlight = PatternFill(start_color='EBF8FF', end_color='EBF8FF', fill_type='solid')
fill_alert = PatternFill(start_color='FFF5F5', end_color='FFF5F5', fill_type='solid')
font_alert = Font(name='Calibri', size=11, bold=True, color='C53030')

border_thin = Side(border_style="thin", color="CBD5E0")
border_all = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
border_top_thick = Border(top=Side(border_style="medium", color="1B365D"))
border_total = Border(top=Side(border_style="thin", color="1B365D"), bottom=Side(border_style="double", color="1B365D"))

# -------------------------------------------------------------------------
# Tab 1: L-4 Street Tree Audit
# -------------------------------------------------------------------------
ws1 = wb.create_sheet(title="L-4 Street Tree Audit")
ws1.views.sheetView[0].showGridLines = True

ws1.cell(1, 1, "DESERT SAGE RANCH PHASE 3 — JOB NO. 2201-03").font = font_title
ws1.cell(2, 1, "Technical Audit: Comment L-4 Street Frontage Tree Requirements vs. Current Landscape Plans").font = font_subtitle

headers1 = [
    "Frontage Segment", "Applicable Classification", "Linear Feet (LF)", 
    "Code Standard (CCC 30.64.030(k))", "Trees Shown (Sheet L-2)", 
    "Trees Demanded (Comment L-4)", "Deficit / Delta (Trees)", 
    "Physical & Spatial Constraints Identified"
]

ws1.cell(4, 1, "Table 1.1: Frontage Breakdown and Tree Quantity Reconciliation").font = font_sec_hdr
for c, h in enumerate(headers1, 1):
    cell = ws1.cell(5, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data1 = [
    ["Windmill Lane (Phase 3 Extension)", "Arterial / HOA Landscape Strip", 2560, "1 tree / 20 LF (Medium Canopy)", 34, 128, 94, "Driveways, sight visibility zones (SVZs), storm drain Line A, curb inlets"],
    ["Interior Collector (Both Sides)", "Collector / HOA Landscape Strip", 1180, "1 tree / 20 LF (Medium Canopy)", 16, 59, 43, "Driveway cuts (Lots 1-60), streetlight foundations (24 poles), hydrants"],
    ["Rainbow Boulevard Entry (East Side)", "Arterial / Entry Treatment", 420, "1 tree / 20 LF (Medium Canopy)", 8, 21, 13, "Sight triangle at entry intersection, monument island sign clear zone"],
]

for r, row in enumerate(data1, 6):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws1.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if c in [3, 5, 6, 7]:
            cell.alignment = Alignment(horizontal="right")
        elif c == 4:
            cell.alignment = Alignment(horizontal="center")

# Total Row
ws1.cell(9, 1, "Total Dedicated Street Frontage").font = font_bold
ws1.cell(9, 2, "—").alignment = Alignment(horizontal="center")
ws1.cell(9, 3, 4160).font = font_bold
ws1.cell(9, 3).alignment = Alignment(horizontal="right")
ws1.cell(9, 4, "1 tree / 20 LF").alignment = Alignment(horizontal="center")
ws1.cell(9, 5, 58).font = font_bold
ws1.cell(9, 5).alignment = Alignment(horizontal="right")
ws1.cell(9, 6, 208).font = font_bold
ws1.cell(9, 6).alignment = Alignment(horizontal="right")
ws1.cell(9, 7, 150).font = font_bold
ws1.cell(9, 7).alignment = Alignment(horizontal="right")
ws1.cell(9, 8, "Rigid 20-ft spacing physically impossible without canopy clustering/substitution").font = font_bold

for c in range(1, 9):
    ws1.cell(9, c).border = border_total

# Overall Plant Schedule Impact
ws1.cell(11, 1, "Table 1.2: Total Landscape Tree Schedule Reconciliation (Sheet L-1 vs. Resubmittal)").font = font_sec_hdr

headers1_2 = ["Tree Category / Location", "Species (Palette)", "Size", "Current Plan (L-1)", "Revised Plan", "Net Change", "Irrigation Circuit"]
for c, h in enumerate(headers1_2, 1):
    cell = ws1.cell(12, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_subhdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data1_2 = [
    ["Street Frontages (Windmill / Collector / Rainbow)", "Chilopsis / Parkinsonia / Prosopis", "24-inch box", 58, 208, 150, "Dedicated drip / bubbler circuit"],
    ["Entry Monument Island (Rainbow Blvd)", "Pistacia lentiscus x atlantica", "24-inch box", 6, 6, 0, "Separate 3/4-inch meter circuit"],
    ["Common-Area Park (Parcel A)", "Ulmus parvifolia 'True Green'", "36-inch box", 10, 10, 0, "Dedicated bubbler / 1.5-inch meter"],
]

for r, row in enumerate(data1_2, 13):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws1.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if c in [4, 5, 6]:
            cell.alignment = Alignment(horizontal="right")

# Total row
ws1.cell(16, 1, "Total Trees Across All Common Areas").font = font_bold
ws1.cell(16, 2, "—").alignment = Alignment(horizontal="center")
ws1.cell(16, 3, "—").alignment = Alignment(horizontal="center")
ws1.cell(16, 4, 74).font = font_bold
ws1.cell(16, 4).alignment = Alignment(horizontal="right")
ws1.cell(16, 5, 224).font = font_bold
ws1.cell(16, 5).alignment = Alignment(horizontal="right")
ws1.cell(16, 6, 150).font = font_bold
ws1.cell(16, 6).alignment = Alignment(horizontal="right")
ws1.cell(16, 7, "+202.7% increase in total project tree count").font = font_italic

for c in range(1, 8):
    ws1.cell(16, c).border = border_total

for col in ws1.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws1.column_dimensions[col_letter].width = max(max_len + 3, 12)
ws1.column_dimensions['A'].width = 38
ws1.column_dimensions['H'].width = 45

# -------------------------------------------------------------------------
# Tab 2: Water Budget Scenarios
# -------------------------------------------------------------------------
ws2 = wb.create_sheet(title="Water Budget Comparison")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(1, 1, "DESERT SAGE RANCH PHASE 3 — JOB NO. 2201-03").font = font_title
ws2.cell(2, 1, "Landscape Water Budget Audit: Impact of Comment L-4 (+150 Trees) and Turf Regulatory Options").font = font_subtitle

ws2.cell(4, 1, "Table 2.1: Annual Irrigation Demand Comparison Across Regulatory Scenarios").font = font_sec_hdr

headers2 = [
    "Hydrozone / Landscape Component", "Area / Qty Unit", "Application Rate", 
    "Baseline Plan (08/21 Submittal)", "Scenario 1: Add 150 Trees (Turf Unchanged)", 
    "Scenario 2: Add 150 Trees + Convert Turf to Desert Drip", "Notes & Methodology Basis"
]

for c, h in enumerate(headers2, 1):
    cell = ws2.cell(5, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data2 = [
    ["HZ-1: Common-Area Park Turf (Parcel A)", "18,400 SF", "5.5 ft/yr (Spray)", 2.3232, 2.3232, 0.4224, "Scenario 2 converts 18,400 SF sod to drip desert planting @ 1.0 ft/yr"],
    ["HZ-2: Common-Area Drip Planting (Shrubs/Mulch)", "22,200 SF", "1.0 ft/yr (In-line drip)", 0.5096, 0.5096, 0.5096, "Streetscape strips, park perimeter, entry monument"],
    ["HZ-3a: Street Frontage Trees", "58 vs. 208 EA", "2,000 gal/tree/yr", 0.3560, 1.2767, 1.2767, "300,000 gal/yr added by 150 street trees (325,851 gal/ac-ft)"],
    ["HZ-3b: Entry Monument Trees", "6 EA", "2,000 gal/tree/yr", 0.0368, 0.0368, 0.0368, "Pistacia lentiscus canopy trees"],
    ["HZ-3c: Park Interior Shade Trees", "10 EA", "2,000 gal/tree/yr", 0.0614, 0.0614, 0.0614, "Ulmus parvifolia shade canopy at bench nodes"],
]

for r, row in enumerate(data2, 6):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws2.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if c in [4, 5, 6]:
            cell.alignment = Alignment(horizontal="right")
            cell.number_format = '0.00'

# Subtotals
ws2.cell(11, 1, "Total Trees Annual Water Demand").font = font_bold
ws2.cell(11, 2, "74 vs. 224 EA").alignment = Alignment(horizontal="center")
ws2.cell(11, 3, "2,000 gal/tree/yr").alignment = Alignment(horizontal="center")
ws2.cell(11, 4, 0.4542).number_format = '0.00'
ws2.cell(11, 4).font = font_bold
ws2.cell(11, 5, 1.3748).number_format = '0.00'
ws2.cell(11, 5).font = font_bold
ws2.cell(11, 6, 1.3748).number_format = '0.00'
ws2.cell(11, 6).font = font_bold
ws2.cell(11, 7, "Tree demand increases by 0.9207 ac-ft/yr (+202.7%)").font = font_italic
for c in range(1, 8):
    ws2.cell(11, c).border = border_all

# Total Annual Applied Water
ws2.cell(12, 1, "TOTAL ANNUAL IRRIGATION DEMAND (AFY)").font = font_bold
ws2.cell(12, 2, "40,600 SF / 224 Trees").alignment = Alignment(horizontal="center")
ws2.cell(12, 3, "SNWA Standard").alignment = Alignment(horizontal="center")
ws2.cell(12, 4, 3.2871).number_format = '0.00'
ws2.cell(12, 4).font = font_bold
ws2.cell(12, 5, 4.2077).number_format = '0.00'
ws2.cell(12, 5).font = font_bold
ws2.cell(12, 6, 2.3069).number_format = '0.00'
ws2.cell(12, 6).font = font_bold
ws2.cell(12, 7, "Scenario 1: +28.0% demand surge | Scenario 2: -29.8% net reduction").font = font_bold
for c in range(1, 8):
    ws2.cell(12, c).border = border_total

# Net Variance vs Baseline
ws2.cell(14, 1, "Variance vs. Baseline Submittal (AFY)").font = font_bold
ws2.cell(14, 4, 0.0).number_format = '0.00'
ws2.cell(14, 5, 0.9207).number_format = '+0.00'
ws2.cell(14, 5).font = font_alert
ws2.cell(14, 6, -0.9802).number_format = '-0.00'
ws2.cell(14, 6).font = font_bold
ws2.cell(14, 7, "Turf conversion offsets tree water demand and generates 0.98 AFY surplus").font = font_italic

for col in ws2.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws2.column_dimensions[col_letter].width = max(max_len + 3, 12)
ws2.column_dimensions['A'].width = 38
ws2.column_dimensions['G'].width = 45

# -------------------------------------------------------------------------
# Tab 3: Cost and Bond Escalation
# -------------------------------------------------------------------------
ws3 = wb.create_sheet(title="Cost and Bond Impact")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(1, 1, "DESERT SAGE RANCH PHASE 3 — JOB NO. 2201-03").font = font_title
ws3.cell(2, 1, "Performance Bond and Engineer's Estimate Audit: Impact of L-4 Street Tree Revision").font = font_subtitle

ws3.cell(4, 1, "Table 3.1: Section 6 Landscape & Irrigation Line-Item Adjustments").font = font_sec_hdr

headers3 = ["Item No.", "Description", "Unit", "Unit Price ($)", "Current Qty", "Current Extended ($)", "Revised Qty", "Revised Extended ($)", "Delta ($)"]
for c, h in enumerate(headers3, 1):
    cell = ws3.cell(5, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data3 = [
    ["7.09", "Tree, 24-inch box, planted, staked, and mulched (street frontage)", "EA", 485.00, 64, 31040.00, 214, 103790.00, 72750.00],
    ["7.10", "Tree, 36-inch box, planted, staked, and mulched (park shade)", "EA", 1150.00, 10, 11500.00, 10, 11500.00, 0.00],
    ["7.16", "Cool-season turf sod, Kentucky bluegrass/rye, on prepared grade", "SF", 2.15, 18400, 39560.00, 18400, 39560.00, 0.00],
    ["7.41", "Drip tubing, subsurface, 12-inch o.c. emitters, in prepared bed", "SF", 0.65, 55000, 35750.00, 55000, 35750.00, 0.00],
    ["7.42", "Point-source drip emitter assembly, per tree or shrub", "EA", 12.50, 750, 9375.00, 900, 11250.00, 1875.00],
    ["Other", "Balance of Section 6 items (soil prep, mulch, cobble, controllers, valves)", "LS", "Various", 1, 262115.00, 1, 262115.00, 0.00],
]

for r, row in enumerate(data3, 6):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws3.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if c in [4, 6, 8, 9]:
            cell.alignment = Alignment(horizontal="right")
            if isinstance(val, (int, float)):
                cell.number_format = '$#,##0.00'
        elif c in [5, 7]:
            cell.alignment = Alignment(horizontal="right")

# Section 6 Subtotal
ws3.cell(12, 1, "Section 6").font = font_bold
ws3.cell(12, 2, "Section 6 Subtotal — Landscape and Irrigation").font = font_bold
ws3.cell(12, 6, 389340.00).number_format = '$#,##0.00'
ws3.cell(12, 6).font = font_bold
ws3.cell(12, 8, 463965.00).number_format = '$#,##0.00'
ws3.cell(12, 8).font = font_bold
ws3.cell(12, 9, 74625.00).number_format = '$#,##0.00'
ws3.cell(12, 9).font = font_bold
for c in range(1, 10):
    ws3.cell(12, c).border = border_total

# Bonding Summary Table
ws3.cell(14, 1, "Table 3.2: Performance Bond Escalation and Statutory Rounding").font = font_sec_hdr

headers3_2 = ["Bond Component / Cost Element", "Current Estimate (10/10/2026)", "Revised Estimate (L-4 Revision)", "Variance ($)", "Basis / Clark County Bonding Criteria"]
for c, h in enumerate(headers3_2, 1):
    cell = ws3.cell(15, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_subhdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data3_2 = [
    ["Civil Construction Subtotal (Sections 1-5, 7-8)", 4467225.75, 4467225.75, 0.00, "Earthwork, storm drain, streets, wet utilities, dry utilities, survey, traffic"],
    ["Landscape Construction Subtotal (Section 6)", 389340.00, 463965.00, 74625.00, "Reflects 150 additional 24-inch box trees and drip emitters"],
    ["Total Construction Subtotal", 4856565.75, 4931190.75, 74625.00, "Sum of all improvement plan line items"],
    ["Mobilization, Bonds, Insurance (LS)", 350000.00, 350000.00, 0.00, "Lump sum allowance per schedule"],
    ["Contingency (LS)", 150000.00, 150000.00, 0.00, "Lump sum allowance per schedule"],
    ["Raw Total Estimate of Probable Cost", 5356565.75, 5431190.75, 74625.00, "Exact mathematical sum prior to rounding"],
]

for r, row in enumerate(data3_2, 16):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws3.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if c in [2, 3, 4]:
            cell.alignment = Alignment(horizontal="right")
            cell.number_format = '$#,##0.00'

# Bond Total
ws3.cell(22, 1, "PHASE 3 PERFORMANCE BOND TOTAL").font = font_bold
ws3.cell(22, 2, 5357000.00).number_format = '$#,##0.00'
ws3.cell(22, 2).font = font_bold
ws3.cell(22, 3, 5432000.00).number_format = '$#,##0.00'
ws3.cell(22, 3).font = font_bold
ws3.cell(22, 4, 75000.00).number_format = '$#,##0.00'
ws3.cell(22, 4).font = font_alert
ws3.cell(22, 5, "Rounded up to next $1,000 per Sched. Sec. 12.02. Mandatory surety update.").font = font_bold
for c in range(1, 6):
    ws3.cell(22, c).border = border_total

for col in ws3.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws3.column_dimensions[col_letter].width = max(max_len + 3, 12)
ws3.column_dimensions['A'].width = 36
ws3.column_dimensions['B'].width = 42
ws3.column_dimensions['E'].width = 45

# -------------------------------------------------------------------------
# Tab 4: Resubmittal Tracker Audit
# -------------------------------------------------------------------------
ws4 = wb.create_sheet(title="Tracker & Prerequisites Audit")
ws4.views.sheetView[0].showGridLines = True

ws4.cell(1, 1, "DESERT SAGE RANCH PHASE 3 — JOB NO. 2201-03").font = font_title
ws4.cell(2, 1, "Resubmittal Tracker Status Audit: Critical Path Preconditions and Inter-Discipline Dependencies").font = font_subtitle

ws4.cell(4, 1, "Table 4.1: Audit of Open Resubmittal Tracker Items and Governing Preconditions").font = font_sec_hdr

headers4 = ["Discipline", "Ref", "Reviewer / Authority", "Tracker Due", "Status as of 10/31", "Critical Path Precondition Required Before Resubmittal"]
for c, h in enumerate(headers4, 1):
    cell = ws4.cell(5, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data4 = [
    ["Mapping / Stat.", "M-1", "Comprehensive Planning (Marchetti)", "11/06/2026", "OPEN / URGENT", "Provide written confirmation of Ph 1/2 recording (12/23/2024, Bk 175, Pg 60); obtain Department letter confirming statutory deadline is 12/23/2026."],
    ["Landscape / Code", "L-2", "Public Works (Yeoman) / SNWA", "11/22/2026", "PENDING CLIENT", "Callaway must elect park amenities (playground) or desert conversion. Vogel SF exemption letter is legally ineffective under SNWA Bulletin WRC-2024-07."],
    ["Landscape / Code", "L-3", "Public Works (Yeoman) / Comp Plan", "11/22/2026", "PENDING CLIENT", "Coordinate revised compliance note citing CCC 30.64.030(j) and SNWA definitions; pre-clear with Marchetti to avoid Condition 14 TAB design review."],
    ["Landscape / Code", "L-4", "Public Works (Yeoman)", "11/22/2026", "OPEN / CLASHES", "Cross-check 208 tree locations against driveways, SVZs, Line A storm drain, and 20-ft dry utility easement; recalculate water budget (+0.92 AFY)."],
    ["Landscape / Seal", "L-1", "Public Works (Yeoman)", "11/22/2026", "IN PROGRESS", "Bea Cortland, PLA (NV LA #742) must sign and seal sheets L-1 through L-4."],
    ["Landscape / Curb", "L-5", "Public Works (Yeoman)", "11/22/2026", "IN PROGRESS", "Dimension face-of-curb planting setbacks and confirm 10-ft turf curb setback on L-2."],
    ["Landscape / Sched", "L-6", "Public Works (Yeoman)", "11/22/2026", "IN PROGRESS", "Reconcile plant schedule quantities on L-1 with plan-plotted symbols on L-2/L-3."],
    ["Utilities / Sewer", "U-2", "CCWRD (Vince Alarid)", "11/06/2026", "EXPIRED", "CCWRD Capacity Confirmation CCWRD-SCC-2025-1187 expired on 09/30/2026. Renewal must be filed immediately; condition precedent to plan approval."],
    ["Utilities / Water", "U-2", "LVVWD (Carmen Whitfield)", "11/06/2026", "CURRENT", "LVVWD Will-Serve valid through 07/22/2028; verify increased tree irrigation volume does not exceed commitment or require meter upsizing."],
    ["Utilities / Dry", "U-1", "Sagebrush Utility Design", "11/22/2026", "IN PROGRESS", "Reconcile joint trench with storm drain on C-8 and ensure no tree pits encroach into recorded 20-ft private utility easement along north boundary."],
    ["Fire Access", "F-1", "CCFD (Capt. Emmett Roark)", "11/10/2026", "SCHEDULED", "Execute coordination call on 11/10 to confirm permanent two-point access compliance."],
    ["Civil / Drainage", "G-3", "RFCD / Dale Yeoman", "11/22/2026", "IN PROGRESS", "Reconcile C-9 basin summary to 6.4 ac-ft master drainage allocation."],
    ["Civil / Grading", "G-8", "NDEP / Dale Yeoman", "11/22/2026", "OPEN", "Provide stand-alone ESC sheet citing NDEP General Permit NVR100000 and active NOI."],
    ["Survey / Map", "M-4", "Silver Butte Title / Co. Surveyor", "11/06/2026", "CURRENT", "Plot Schedule B exceptions from Title Report SBT-2026-04188 (current through 01/01/2027)."],
    ["Survey / Map", "M-5", "Callaway Land Partners", "11/13/2026", "PENDING CLIENT", "Obtain authorized signatory and current Nevada statutory notary form for Owner's Dedication."],
    ["Surety / Bond", "A-6", "Surety Broker / Callaway", "11/13/2026", "OPEN", "Update Engineer's Estimate to $5,432,000.00 and issue bond rider for execution."],
]

for r, row in enumerate(data4, 6):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws4.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if c == 5 and "EXPIRED" in str(val):
            cell.font = font_alert
            cell.fill = fill_alert
        elif c == 5 and "OPEN" in str(val):
            cell.font = font_bold

for col in ws4.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws4.column_dimensions[col_letter].width = max(max_len + 3, 12)
ws4.column_dimensions['A'].width = 18
ws4.column_dimensions['C'].width = 30
ws4.column_dimensions['F'].width = 50

# -------------------------------------------------------------------------
# Tab 5: Calendar and Review Scenarios
# -------------------------------------------------------------------------
ws5 = wb.create_sheet(title="Schedule Scenarios & Runway")
ws5.views.sheetView[0].showGridLines = True

ws5.cell(1, 1, "DESERT SAGE RANCH PHASE 3 — JOB NO. 2201-03").font = font_title
ws5.cell(2, 1, "Critical Path Schedule Analysis: Resubmittal Dates vs. Statutory Expiration (NRS 278.360)").font = font_subtitle

ws5.cell(4, 1, "Table 5.1: Review Turnaround Scenarios (Business Days Accounting for County Holidays)").font = font_sec_hdr

headers5 = [
    "Resubmittal Date", "Internal QC Freeze", "10 Business Days (Expedited)", 
    "12 Business Days", "15 Business Days (Target)", "20 Business Days (Standard CC-PW)", 
    "Recordation Viability vs. 12/18 Target", "Statutory Compliance vs. 12/23 Cliff"
]

for c, h in enumerate(headers5, 1):
    cell = ws5.cell(5, c, h)
    cell.font = font_tbl_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data5 = [
    ["Fri 11/13/2026", "Fri 11/06/2026", "Tue 12/01/2026", "Thu 12/03/2026", "Tue 12/08/2026", "Tue 12/15/2026", "FEASIBLE — 3 days margin to 12/18", "COMPLIANT — 8 days margin to 12/23"],
    ["Mon 11/16/2026", "Wed 11/11/2026", "Wed 12/02/2026", "Fri 12/04/2026", "Wed 12/09/2026", "Wed 12/16/2026", "FEASIBLE — 2 days margin to 12/18", "COMPLIANT — 7 days margin to 12/23"],
    ["Fri 11/20/2026", "Fri 11/13/2026", "Tue 12/08/2026", "Thu 12/10/2026", "Tue 12/15/2026", "Tue 12/22/2026", "FEASIBLE under 15-day review (12/15)", "COMPLIANT — 1-day margin under 20-day"],
    ["Mon 11/23/2026", "Wed 11/18/2026", "Wed 12/09/2026", "Fri 12/11/2026", "Wed 12/16/2026", "Wed 12/23/2026", "UNLIKELY — requires 12-day turnaround", "BORDERLINE — 0 days margin under 20-day"],
    ["Mon 11/30/2026", "Sun 11/22/2026", "Mon 12/14/2026", "Wed 12/16/2026", "Mon 12/21/2026", "Tue 12/29/2026", "FATAL under standard 20-day review", "NON-COMPLIANT — Map terminates on 12/23!"],
]

for r, row in enumerate(data5, 6):
    fill = fill_zebra if r % 2 == 0 else PatternFill(fill_type=None)
    for c, val in enumerate(row, 1):
        cell = ws5.cell(r, c, val)
        cell.font = font_regular
        cell.fill = fill
        cell.border = border_all
        if r == 10: # 11/30 row
            cell.fill = fill_alert
            if c in [7, 8]:
                cell.font = font_alert
        elif r == 8: # 11/20 row
            cell.fill = fill_highlight
            if c in [7, 8]:
                cell.font = font_bold

for col in ws5.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws5.column_dimensions[col_letter].width = max(max_len + 3, 12)
ws5.column_dimensions['A'].width = 18
ws5.column_dimensions['G'].width = 38
ws5.column_dimensions['H'].width = 42

wb.save("output/TECHNICAL_AUDIT_L4_LANDSCAPE_AND_TRACKER.xlsx")
print("Saved output/TECHNICAL_AUDIT_L4_LANDSCAPE_AND_TRACKER.xlsx successfully!")
