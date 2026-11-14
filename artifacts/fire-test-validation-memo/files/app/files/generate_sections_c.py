# Module C: Sections 8, 9, 10, 11, 12, Appendix A, Appendix B
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from generate_validation_memo import (
    set_cell_margins, set_cell_shading, set_cell_border, add_callout,
    format_cell, add_heading_1, add_heading_2, add_heading_3, add_para, add_bullet
)

def build_sections_8_to_12_and_appendices(doc):
    # SECTION 8
    add_heading_1(doc, "8. Model Physics Diagnosis, Rework Identification, and Rework Status Audit")
    add_heading_2(doc, "8.1 What the Diagnostic Comparisons Say About the Model")
    add_para(doc, "Cross-referencing the two diagnostic metrics in Section 7 yields two decisive engineering conclusions regarding model physics:")
    add_bullet(doc, "Metallic Tie Thermal-Bridge Mechanics are Modeled with High Structural Fidelity: The fact that the criteria separation is identical between test and simulation (Delta_t = 45 min in both) and the temperature elevation above the mean at governance agrees within 6.2 °C (85.0 °C test vs 91.2 °C simulation) proves that the 3D conjugate conduction along the continuous steel truss ties is modeled accurately. The model correctly captures the rapid heat channeling along the steel wire and correctly reproduces the localized hot spot that trips the single-point limit 45 minutes prior to the general field average.", bold_prefix="1. Localized Thermal Bridging is Sound: ")
    add_bullet(doc, "The Model Deficiency is a Uniform, Systemic Through-Wall Transmission Delay: Examining the absolute crossing times reveals a uniform +13 min lag across the entire assembly:\n"
                    "• Single-Point Criterion: Test = 118 min, Simulation = 131 min (Delta = +13 min).\n"
                    "• Average-Rise Criterion: Test = 163 min, Simulation = 176 min (Delta = +13 min).\n"
                    "Because both the localized bridge and the broad field transmission are shifted by the exact same +13 min, the model does not suffer from a localized tie-meshing or geometric error. Rather, the entire through-thickness thermal resistance of the assembly is over-predicted.", bold_prefix="2. Uniform Through-Wall Impedance Lag: ")

    add_heading_2(doc, "8.2 Specific Areas Where Model Rework Belongs")
    add_para(doc, "To eliminate the +13 min non-conservative delay, rework must focus on the global through-wall thermal impedance chain, specifically:")
    add_bullet(doc, "Printed Concrete Thermophysical Property Calibration: The siliceous aggregate concrete leaves (50 mm each) govern bulk conduction. The temperature-dependent thermal conductivity k(T) is likely assumed too low at elevated temperatures (above 400 °C), or the volumetric heat capacity rho*cp(T) is over-estimated. Furthermore, the endothermic latent heat plateau associated with free water vaporization and calcium silicate hydrate (CSH) dehydration (100 °C to 300 °C) appears to carry excessive effective thermal mass in the solid thermophysical model, delaying heat penetration by ~13 min.", bold_prefix="1. Concrete k-rho-cp & Dehydration Kinetics: ")
    add_bullet(doc, "Cavity Radiation and Natural Convection: In a 205 mm open-air cavity at furnace temperatures, thermal radiation between the interior leaf faces is the dominant heat transfer mechanism. If the surface emissivity epsilon of the printed concrete faces was set to an uncalibrated default (e.g., epsilon = 0.85 rather than an elevated emissivity of 0.92–0.95 characteristic of dehydrated/sooted surfaces), radiant flux across the air gap is retarded. Furthermore, internal natural convection view factors and convective heat transfer coefficients across the 205 mm gap require re-benchmarking.", bold_prefix="2. Cavity Heat Transfer Dynamics: ")
    add_bullet(doc, "Tie Embedment Interface Resistance: The 25 mm embedment of the 3.8 mm galvanized wire ties into the concrete leaves was modeled with ideal thermal contact. Contact resistance or localized concrete dehydration around the embedded steel should be audited.", bold_prefix="3. Tie-Concrete Interface: ")
    add_bullet(doc, "Furnace Boundary Convective & Radiative Heat Flux: The exposed-face boundary condition should be audited to verify that the standard ASTM E119 furnace gas emissivity and convective heat transfer coefficient match Red Butte's natural-gas vertical furnace calibration.", bold_prefix="4. Exposed-Face Boundary Flux: ")

    add_heading_2(doc, "8.3 Audit of Current Rework Status")
    add_para(doc, "AUDIT RESULT: NO REWORK HAS BEEN STARTED YET.", bold_prefix="Rework Audit: ")
    add_para(doc, "To verify the state of the project file server as of today, October 10, 2025, we conducted a comprehensive audit across all firm operational and computational records:")
    add_bullet(doc, "HPC Cluster Job Logs (cluster_job_accounting_2025Q3.csv): No jobs have been submitted, queued, or run for E119 recalibration or companion run reruns on the borrego cluster or AWS cloud burst. The last CHT run remains attempt 3 from 10/09/2025.", bold_prefix="• Compute Audit: ")
    add_bullet(doc, "Change Order Log (CFDME-2025-041_change_order_log.xlsx): Only two change orders have been executed: CO-001 (post-processing animation, $2,400) and CO-002 (mesh refinement pass at wildfire front, $6,750). No change order or scope item exists for E119 model recalibration.", bold_prefix="• Contractual Audit: ")
    add_bullet(doc, "Staffing Assignments (CFDME_staffing_assignments.xlsx): Lead Engineer Gordon Selby is allocated to Phase 1 reporting; Remote Engineer Renata Ellsworth is fully committed to wildfire mesh verification and puffing plume analysis; Mulshi Simulation Labs is committed to case setups. Zero engineer-hours have been booked or assigned to companion run rework.", bold_prefix="• Staffing Audit: ")
    add_bullet(doc, "Case Setup Directory (Case/system_archive/OAS_case_setup_from_DWA.txt): The case setup remains the parent template cloned from Dry Wash Aerospace (CFDME-2024-018); through-wall thermal properties have not been modified.", bold_prefix="• Case Setup Audit: ")
    add_para(doc, "Because no new runs or tests are available and no rework has commenced, the companion run stands as evaluated, with E = +13 min.")

    # SECTION 9
    add_heading_1(doc, "9. Implications for the Rest of Phase 1")
    add_para(doc, "The failure of the companion simulation to validate under our governing procedure carries direct technical, contractual, and risk implications for the remainder of Phase 1:")
    add_bullet(doc, "Non-Conservative Thermal Bias in Wildfire Exposure: An over-prediction of E119 endurance (E = +13 min) indicates that the CFD solver stack transmits heat through the OAS wall assembly more slowly than physical reality. When this same through-wall modeling treatment is applied to the Phase 1 wildfire cases (SOW §3.1, Sonoran buffelgrass fire front at 30.1 MW), unexposed-face temperatures and internal tie temperatures will likely rise faster in reality than predicted by the simulation. The Phase 1 narrative must explicitly disclose this non-conservative bias.", bold_prefix="1. Fire-Safety Risk: ")
    add_bullet(doc, "Prohibition on Unqualified Validation Claims: Under CFDME-QA-VAL-002 Section 5, Phase 1 Report rev B cannot be released with any claim that the CFD model is 'validated against ASTM E119' or 'confirmed by certified fire testing.' Section 7 must present the V&V 20 model-error rollup (S = 131 min, D = 118 min, E = +13 min, u_val = ±9 min) and formally record that the primary 10% criterion was not met.", bold_prefix="2. Reporting Discipline: ")
    add_bullet(doc, "Peer Review Sign-Off Conditions: Technical Director Marguerite Falk, PE cannot issue an unqualified release of the Phase 1 report. The deliverable may only be released under the 'Released with comments / Documented Finding' disposition, with a formal finding documenting the +13 min model error and restricting client use.", bold_prefix="3. Reviewer Action: ")
    add_bullet(doc, "Restriction on Client Product Launch: Trevor Buckhalter's stated intent to publish headline claims ('more fire-resistant than wood-frame construction in a Sonoran WUI wildfire') citing stamped CFD validation cannot be supported by The CFD ME. Stamping an unqualified validation claim under these numbers would violate Arizona professional engineering board rules (A.A.C. R4-30-301).", bold_prefix="4. Client Impact: ")

    # SECTION 10
    add_heading_1(doc, "10. Scope Boundaries on Ocotillo's Wildfire Claims & Gap Closure")
    add_para(doc, "In accordance with CFDME Validation Procedure rev 2, Section 7 ('Scope Limitation'), this validation memo formally defines what the ASTM E119 companion simulation does and does not establish regarding Ocotillo's marketing claims:")

    add_heading_2(doc, "10.1 What the Exercise Establishes")
    add_bullet(doc, "Evaluates computational thermal transmission against the standardized, monotonically rising ASTM E119 furnace time-temperature curve in a non-load-bearing compartment partition configuration.", bold_prefix="• Standard Exposure Fidelity: ")
    add_bullet(doc, "Confirms that the 3D conjugate model correctly resolves the physical heat-channeling mechanism through continuous metallic truss ties, predicting localized thermal-bridge failure 45 minutes ahead of field average rise.", bold_prefix="• Thermal-Bridge Physics: ")

    add_heading_2(doc, "10.2 What the Exercise DOES NOT Establish")
    add_bullet(doc, "Not a Wildfire Survival Prediction: ASTM E119 is a smooth, post-flashover compartment fire curve designed to grade relative building assembly performance under repeatable laboratory conditions. A wildland-urban interface (WUI) wildfire is a wind-driven, transient, radiation-dominated fire-front event. An assembly with an E119 endurance of 118 min is NOT thereby a 'two-hour wildfire wall,' and no algebraic formula translates E119 furnace endurance into wildfire survival time.", bold_prefix="• Non-Equivalence: ")
    add_bullet(doc, "Unrepresented Wildfire Phenomena: The E119 furnace test completely omits: (i) wind-driven flame tilt and aerodynamic impingement at 5–12 m/s; (ii) peak transient radiant heat fluxes from an advancing 30.1 MW buffelgrass fire front; (iii) turbulent plume puffing (0.87 Hz) and flame washing; (iv) aerodynamic pressure differentials across the envelope; and (v) firebrand / ember accumulation and ignition in parapet crevices.", bold_prefix="• Physical Omissions: ")

    add_heading_2(doc, "10.3 What Would Close the Gap & Mandatory Reporting Form")
    add_para(doc, "Closing the gap between E119 furnace ratings and Ocotillo's Sonoran WUI wildfire claims requires physical empirical testing under representative wildland-fire exposure:")
    add_bullet(doc, "Physical Testing Requirements: Physical testing of the OAS printed wall under transient high-radiant flux and flame impingement per ASTM E2707 / ASTM E2726, California Building Code (CBC) Chapter 7A WUI standards, or full-scale wind-tunnel burner facility testing with calibrated ember generators.", bold_prefix="1. ")
    add_bullet(doc, "Future Reporting Form: Any future comparison between CFD simulation predictions and physical test data must strictly follow the ASME V&V 20 reporting form mandated by CFDME-QA-VAL-002 Section 3: S, D, E = S - D, and u_val presented in a single table with units and sign, citing certified test and run identifiers. Narrative descriptors such as 'validated,' 'confirmed,' or 'matches' are inadmissible.", bold_prefix="2. ")

    # SECTION 11
    add_heading_1(doc, "11. Fire-Resistance Rating Impact, Authority, Stamp Boundary & Checklist")
    add_heading_2(doc, "11.1 Impact of Bianca's Figure (129 min) on Certified Fire-Resistance Rating")
    add_para(doc, "We evaluated what Bianca Rennert's figure of 129 min would do to the assembly's certified fire-resistance rating IF it were ever formally substantiated by Red Butte:")
    add_bullet(doc, "Current Certification (Ironwood IWFPE-CERT-25-0374 §3): The assembly is certified for a 1-Hour Fire-Resistance Rating (60 min). Measured endurance was 118 min, which exceeds the 60-minute rung but falls 2 min short of the 120-minute threshold required for a 2-hour rating.", bold_prefix="• Current Status: ")
    add_bullet(doc, "Substantiated Rating Impact: If Red Butte were to formally reissue Report RBFMT-25-0918 with an authorized single-point endurance of 129 min, that result would exceed 120 min (129 min >= 120 min). The certified fire-resistance rating would be upgraded from 1-Hour (60 min) to 2-Hour (120 min). This represents a 100% increase in certified commercial rating.", bold_prefix="• Impact if Substantiated: ")

    add_heading_2(doc, "11.2 Statutory Entitlement to Act on Rating Certification")
    add_para(doc, "ENTITLEMENT AUTHORITY: ONLY Marla Kettering, PE (Arizona Fire Protection PE #45106), Principal of Ironwood Fire Protection Engineering (or another qualified registered Fire Protection PE), is legally entitled to issue or amend the certified fire-resistance rating, and only upon receipt of an authorized reissued test report from Red Butte Fire & Materials Testing.", bold_prefix="Legal Entitlement: ")
    add_para(doc, "Explicit Jurisdictional Boundary: Section 4 of Ironwood's certification memo explicitly states: 'Any change to the certified rating requires a reissued test report from the testing laboratory of record and a new certification issued by Ironwood Fire Protection Engineering. No other party may certify or restate this rating.'")
    add_para(doc, "Neither The CFD ME, nor Gordon Selby, PE, nor Bianca Rennert, nor Trevor Buckhalter has legal, statutory, or professional authority to alter, restate, or upgrade the certified rating.")

    add_heading_2(doc, "11.3 Mandatory Firm Stamp Language")
    add_para(doc, "Per CFDME Validation Procedure rev 2, Section 9 ('Stamp Boundary'), the firm's required stamp language on all deliverables carrying a validation claim is:")
    add_callout(doc, [
        "\"CFD thermal analysis only. Fire-resistance rating certified separately by others.\""
    ], title="MANDATORY STAMP BOUNDARY CLAUSE — CFDME-QA-VAL-002 SECTION 9", border_color="0F2C59", bg_color="F1F5F9")

    add_heading_2(doc, "11.4 Reviewer Checklist Disposition")
    add_para(doc, "Reviewing Engineer Marguerite Falk, PE maintains the quality assurance review checklist in CFDME-2025-041_peer_review_checklist.docx. On the strength of this validation memo, the disposition of all checklist items is:")
    
    t_chk = doc.add_table(rows=11, cols=4)
    t_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_chk.autofit = False
    
    chk_widths = [Inches(0.6), Inches(2.5), Inches(1.3), Inches(2.1)]
    for row in t_chk.rows:
        for idx, width in enumerate(chk_widths):
            row.cells[idx].width = width
            set_cell_margins(row.cells[idx], top=60, bottom=60, left=80, right=80)
            
    chk_headers = ["Item #", "Review Checklist Description", "Checklist Status", "Reviewer Action & Basis"]
    for idx, text in enumerate(chk_headers):
        format_cell(t_chk.rows[0].cells[idx], text, bold=True, color="FFFFFF", font_size=8.5, bg_color="0F2C59")
        set_cell_border(t_chk.rows[0].cells[idx], bottom=dict(val='single', sz=8, color='0F2C59'))
        
    chk_data = [
        ("1", "Deliverable identifies governing SOW and revision", "[X] CLOSED", "Closed in prior review cycle (SOW dated 10/08/2025 cited in §1.1)."),
        ("2", "Regime selection documented against firm modeling standard", "[ ] REMAINS OPEN", "Froude-based regime classification pending documentation in case-setup record."),
        ("3", "Solver package confirmed per Modeling Standard rev 4 §3", "[ ] REMAINS OPEN", "fireFoam solver package confirmation pending in case-setup record."),
        ("4", "Resolution basis: D*/dx and Pope TKE stated in Verification body", "[ ] REMAINS OPEN", "Verification section needs D*/dx=7.5 and Pope TKE=84% integrated into report body."),
        ("5", "Through-wall CFD treatment confirmed per Modeling Standard §6", "[ ] REMAINS OPEN", "Through-wall CHT treatment pending documentation in case-setup record."),
        ("6", "Validation reported as E ± u_val against criterion (NOT yes/no)", "[X] CLOSES VIA THIS MEMO", "CLOSED: This memo establishes Section 7 with S=131 min, D=118 min, E=+13 min, u_val=±9 min."),
        ("7", "Geometry revision tagged and matches case log", "[ ] REMAINS OPEN", "Case build log timestamp vs transmittal record check pending before sign-off."),
        ("8", "Stamp boundary respected (CFD thermal analysis only)", "[X] CLOSED", "Closed in prior review cycle (Section 9.2 contains mandatory stamp text)."),
        ("9", "Reported pressures cross-checked against boundary conditions", "[ ] REMAINS OPEN", "Structural windload pressure units check and conversion section pending per Units SOP."),
        ("10", "Reviewer sign-off and stamp block completed", "[ ] REMAINS OPEN", "Held open pending closure of Items 2, 3, 4, 5, 7, and 9.")
    ]
    
    for r_idx, data in enumerate(chk_data):
        row = t_chk.rows[r_idx + 1]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        if "CLOSES VIA" in data[2]:
            bg = "F0FDF4" # Green tint for item being closed
        for c_idx, text in enumerate(data):
            is_bold = True if c_idx in [0, 2] or "CLOSES" in text else False
            txt_color = "166534" if "CLOSES" in text else ("334155" if "[X]" in text else "1E293B")
            format_cell(row.cells[c_idx], text, bold=is_bold, color=txt_color, font_size=8.0, bg_color=bg)
            set_cell_border(row.cells[c_idx], bottom=dict(val='single', sz=4, color='E2E8F0'),
                                              top=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_para(doc, "SUMMARY: This validation memo authorizes the closure of Item 6. Items 2, 3, 4, 5, 7, 9, and 10 remain OPEN pending completion of their respective engineering verifications.", bold_prefix="Checklist Disposition Summary: ")

    # SECTION 12
    add_heading_1(doc, "12. Professional Engineer Stamp Block & Sign-Off")
    add_para(doc, "I hereby certify that this validation evaluation has been conducted in full accordance with ASME V&V 20-2009 (R2016), CFDME Validation QA Procedure rev 2 (CFDME-QA-VAL-002), and the Arizona Board of Technical Registration rules of professional conduct.")

    # Sign-off table
    t_sign = doc.add_table(rows=1, cols=2)
    t_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sign.autofit = False
    
    t_sign.rows[0].cells[0].width = Inches(3.25)
    t_sign.rows[0].cells[1].width = Inches(3.25)
    set_cell_margins(t_sign.rows[0].cells[0], top=100, bottom=100, left=120, right=120)
    set_cell_margins(t_sign.rows[0].cells[1], top=100, bottom=100, left=120, right=120)
    set_cell_border(t_sign.rows[0].cells[0], top=dict(val='single', sz=12, color='0F2C59'),
                                            bottom=dict(val='single', sz=12, color='0F2C59'),
                                            left=dict(val='single', sz=12, color='0F2C59'),
                                            right=dict(val='single', sz=12, color='0F2C59'))
    set_cell_border(t_sign.rows[0].cells[1], top=dict(val='single', sz=12, color='0F2C59'),
                                            bottom=dict(val='single', sz=12, color='0F2C59'),
                                            left=dict(val='single', sz=12, color='0F2C59'),
                                            right=dict(val='single', sz=12, color='0F2C59'))

    p_orig = t_sign.rows[0].cells[0].paragraphs[0]
    p_orig.add_run("ORIGINATING ENGINEER OF RECORD\n").bold = True
    p_orig.add_run("Gordon Selby, PE\n").bold = True
    p_orig.add_run("Owner & Principal Engineer, The CFD ME\n")
    p_orig.add_run("Arizona Professional Engineer (Mechanical) #48213\n")
    p_orig.add_run("Date: October 10, 2025\n\n")
    p_orig.add_run("[ SEAL: GORDON SELBY, PE — AZ #48213 ]\n\n").bold = True
    p_orig.add_run("Stamp Scope: CFD thermal analysis only. Fire-resistance rating certified separately by others.").italic = True

    p_rev = t_sign.rows[0].cells[1].paragraphs[0]
    p_rev.add_run("TECHNICAL REVIEWER OF RECORD\n").bold = True
    p_rev.add_run("Marguerite Falk, PE\n").bold = True
    p_rev.add_run("Technical Director & Reviewing Engineer, The CFD ME\n")
    p_rev.add_run("Arizona Professional Engineer #42798\n")
    p_rev.add_run("Date: October 10, 2025\n\n")
    p_rev.add_run("Review Disposition: [X] Released with comments (Documented Finding in §7)\n").bold = True
    p_rev.add_run("Checklist Item 6: CLOSED on strength of this memo.\n")
    p_rev.add_run("Signature: ___________________________________\n")

    doc.add_page_break()

    # APPENDIX A
    add_heading_1(doc, "Appendix A: Ready-to-Insert Draft Text for Section 7 of Phase 1 Report rev B")
    add_para(doc, "Below is the complete, formatted draft text ready for direct insertion into Section 7 ('Validation') of CFDME-2025-041_Phase1_report_revB.docx to replace the current stub and finalize report revision B:")

    add_callout(doc, [
        "7. Validation",
        "7.1 Governing Framework and Reporting Standard",
        "In accordance with CFDME Validation QA Procedure — ASME V&V 20 rev 2 (CFDME-QA-VAL-002), validation is reported as the model comparison error E = S - D with its combined validation uncertainty u_val, and not as a binary yes/no statement. The certified physical test of record is Red Butte Fire & Materials Testing Report No. RBFMT-25-0918 (test date 09/24/2025, certified by Ironwood Fire Protection Engineering Memorandum No. IWFPE-CERT-25-0374, Marla Kettering, PE, AZ PE #45106). The companion simulation run of record is E119_companion_sim_results.csv, modeling CAD geometry OAS-WUI-01_revC.",
        "",
        "7.2 Thermal Transmission Endpoints and Crossing Times",
        "Under ASTM E119 Section 8, the unexposed face is evaluated against two criteria from initial ambient T_0 = 21.0 °C: (i) average rise of nine thermocouples not to exceed 139.0 °C (limit 160.0 °C); and (ii) single-point rise not to exceed 181.0 °C (limit 202.0 °C). The earlier criterion governs. In the companion simulation, continuous linear interpolation yields a single-point crossing time of 130.94 min (nearest minute: 131 min) and an average-rise crossing time of 176.10 min (nearest minute: 176 min). The single-point criterion governs, yielding simulation prediction S = 131 min.",
        "",
        "7.3 Model Comparison Error and Acceptance Decision",
        "From certified test report RBFMT-25-0918 Section 5.2, single-point governance occurred at 118 min at thermocouple TC-6 (positioned over a continuous 3.8 mm steel tie course), establishing certified experimental value D = 118 min. The model comparison error is:",
        "    E = S - D = 131 min - 118 min = +13 min",
        "The firm's primary acceptance criterion is |E| <= 10% of D = 11.8 min. The simulation fails this criterion (|E| = 13 min > 11.8 min). Combined validation uncertainty for this assembly class is u_val = ±9 min (root-sum-square of numerical uncertainty u_num = ±4 min, input uncertainty u_inp = ±6 min, and experimental uncertainty u_exp = ±5 min). Because |E| = 13 min > u_val = 9 min, the discrepancy is resolved as an actionable model error. The positive error indicates that the CFD model over-predicts fire endurance by 13 minutes, representing a non-conservative bias.",
        "",
        "7.4 Diagnostic Reconciliation and Model Findings",
        "Diagnostic cross-checks confirm that the localized thermal-bridge mechanics of the steel ties are accurately modeled: the time separating single-point failure from average-rise failure is identical between test and simulation (45 min in both), and peak hot-spot elevation above the mean at governance agrees within 6.2 °C (85.0 °C test vs 91.2 °C simulation). The discrepancy is an assembly-wide through-wall transmission lag: both failure modes are shifted by exactly +13 min. Rework belongs in printed concrete high-temperature conductivity k(T), moisture dehydration enthalpy, and cavity radiation emissivity. Post-test thermocouple adjustments proposed by the client (129 min) are rejected per firm procedure Section 6 absent a reissued laboratory report.",
        "",
        "7.5 Wildfire Scope Boundary",
        "Per CFDME-QA-VAL-002 Section 7, validation against ASTM E119 compartment furnace data establishes model behavior under standard furnace curves and does not validate wildland-urban interface (WUI) wildfire survival. An E119 rating cannot be converted into wildfire survival time. Performance under advancing Sonoran buffelgrass fire fronts requires dedicated physical testing under transient radiant heat flux, wind-driven flame tilt, and ember attack."
    ], title="PROPOSED SECTION 7 TEXT FOR PHASE 1 REPORT REV B", border_color="0F2C59", bg_color="F8FAFC")

    # APPENDIX B
    add_heading_1(doc, "Appendix B: Time-Series Thermal Response and Crossing Interpolation Summary")
    add_para(doc, "Table B.1 reproduces key time-series intervals from E119_companion_sim_results.csv spanning the initial transient, thermal bridge heating, single-point crossing (t = 130–131 min), and average-rise crossing (t = 176–177 min):")

    t_app = doc.add_table(rows=11, cols=6)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_app.autofit = False
    
    app_widths = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]
    for row in t_app.rows:
        for idx, width in enumerate(app_widths):
            row.cells[idx].width = width
            set_cell_margins(row.cells[idx], top=60, bottom=60, left=60, right=60)
            
    app_headers = ["Time (min)", "T_exposed (°C)", "T_cavity (°C)", "T_tie (°C)", "T_unexp_avg (°C)", "T_unexp_max (°C)"]
    for idx, text in enumerate(app_headers):
        format_cell(t_app.rows[0].cells[idx], text, bold=True, color="FFFFFF", font_size=8.0, bg_color="0F2C59", align=WD_ALIGN_PARAGRAPH.RIGHT if idx > 0 else WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_border(t_app.rows[0].cells[idx], bottom=dict(val='single', sz=8, color='0F2C59'))
        
    app_data = [
        ("0", "21.0", "21.0", "21.0", "21.0", "21.0"),
        ("30", "843.0", "212.4", "121.5", "21.2", "22.8"),
        ("60", "927.0", "421.8", "184.2", "32.4", "48.6"),
        ("90", "982.0", "532.1", "228.6", "58.7", "102.4"),
        ("118", "1018.0", "598.4", "256.2", "94.2", "172.5"),
        ("130", "1028.5", "621.8", "268.4", "109.8", "200.5"),
        ("131", "1029.2", "623.1", "269.2", "110.9", "202.1"),
        ("160", "1047.8", "652.8", "291.5", "143.4", "241.5"),
        ("176", "1061.7", "659.7", "310.0", "159.9", "260.0"),
        ("177", "1062.6", "660.0", "311.1", "160.9", "261.1")
    ]
    
    for r_idx, data in enumerate(app_data):
        row = t_app.rows[r_idx + 1]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        if data[0] in ["130", "131"]:
            bg = "FEF2F2" # Single-point trip
        elif data[0] in ["176", "177"]:
            bg = "EFF6FF" # Average rise trip
        for c_idx, text in enumerate(data):
            is_bold = True if data[0] in ["130", "131", "176", "177"] and c_idx in [0, 4, 5] else False
            txt_color = "991B1B" if data[0] in ["130", "131"] and c_idx == 5 else ("1E40AF" if data[0] in ["176", "177"] and c_idx == 4 else "1E293B")
            format_cell(row.cells[c_idx], text, bold=is_bold, color=txt_color, font_size=8.0, bg_color=bg, align=WD_ALIGN_PARAGRAPH.RIGHT if c_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER)
            set_cell_border(row.cells[c_idx], bottom=dict(val='single', sz=4, color='E2E8F0'),
                                              top=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_para(doc, "Notes: Initial ambient T_0 = 21.0 °C. Single-point limit = 202.0 °C is crossed between 130 min (200.5 °C) and 131 min (202.1 °C), interpolating to 130.94 min. Average-rise limit = 160.0 °C is crossed between 176 min (159.9 °C) and 177 min (160.9 °C), interpolating to 176.10 min. All values carry SI units per CFDME Units SOP rev 2.", italic=True)

print("Compiled generate_sections_c.py successfully.")
