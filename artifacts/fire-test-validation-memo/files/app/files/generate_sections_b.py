# Module B: Sections 4, 5, 6, 7
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from generate_validation_memo import (
    set_cell_margins, set_cell_shading, set_cell_border, add_callout,
    format_cell, add_heading_1, add_heading_2, add_heading_3, add_para, add_bullet
)

def build_sections_4_to_7(doc):
    # SECTION 4
    add_heading_1(doc, "4. Governing Criterion, Crossing Times, and Section 7 Stub Status")
    add_para(doc, "ASTM E119 Section 8 prescribes two distinct thermal-transmission failure criteria for the unexposed face of a non-load-bearing wall assembly, evaluated from the initial ambient temperature T_0 = 21.0 °C:")
    add_bullet(doc, "Average Unexposed-Face Criterion: The arithmetic mean temperature rise of nine symmetrically distributed thermocouples (TC-1 through TC-9) shall not exceed 139.0 °C (250.0 °F) above initial ambient. The absolute temperature limit is: T_avg,limit = 21.0 °C + 139.0 °C = 160.0 °C.", bold_prefix="1. Average Rise Limit: ")
    add_bullet(doc, "Single-Point Unexposed-Face Criterion: The temperature rise at any single thermocouple on the unexposed face shall not exceed 181.0 °C (325.0 °F) above initial ambient. The absolute temperature limit is: T_max,limit = 21.0 °C + 181.0 °C = 202.0 °C.", bold_prefix="2. Single-Point Limit: ")
    add_para(doc, "Governing Principle: Under ASTM E119 and Section 3 of Red Butte Report RBFMT-25-0918, the earlier of the two criteria to reach its limit governs the reported fire endurance.")

    add_heading_2(doc, "4.1 Continuous Interpolation Crossing Times vs Discrete Tripping Samples")
    add_para(doc, "In accordance with your review directive, crossing times are computed as the exact continuous linear interpolation between discrete 1-minute logging intervals in E119_companion_sim_results.csv, rather than simply adopting the integer timestep that trips the threshold:")
    
    add_bullet(doc, "Single-Point Criterion Crossing: At t = 130 min, T_unexposed_max_C = 200.5 °C. At t = 131 min, T_unexposed_max_C = 202.1 °C. Linearly interpolating to the threshold of 202.0 °C:\n"
                    "t_cross,single = 130 min + [(202.0 °C - 200.5 °C) / (202.1 °C - 200.5 °C)] * (131 min - 130 min)\n"
                    "t_cross,single = 130 min + [1.5 °C / 1.6 °C] * 1.0 min = 130.9375 min ≈ 130.94 min.\n"
                    "Reported to the nearest minute per procedure: S_single = 131 min.", bold_prefix="• Single-Point Crossing: ")
    
    add_bullet(doc, "Average Unexposed-Face Criterion Crossing: At t = 176 min, T_unexposed_avg_C = 159.9 °C. At t = 177 min, T_unexposed_avg_C = 160.9 °C. Linearly interpolating to the threshold of 160.0 °C:\n"
                    "t_cross,avg = 176 min + [(160.0 °C - 159.9 °C) / (160.9 °C - 159.9 °C)] * (177 min - 176 min)\n"
                    "t_cross,avg = 176 min + [0.1 °C / 1.0 °C] * 1.0 min = 176.1000 min ≈ 176.10 min.\n"
                    "Reported to the nearest minute per procedure: S_avg = 176 min.", bold_prefix="• Average Rise Crossing: ")

    add_heading_2(doc, "4.2 Governing Criterion Determination & Section 7 Stub Status")
    add_para(doc, "GOVERNING CRITERION: The single-point criterion is reached first in the simulation (130.94 min vs 176.10 min) and therefore GOVERNS. The governing simulation prediction is S = 131 min (crossing time 130.94 min).", bold_prefix="Governance: ")
    add_para(doc, "STATUS OF SECTION 7 STUB PREDICTION: In the Phase 1 Draft Report (CFDME-2025-041_Phase1_report_revB.docx, Section 7), the stub text reads: '(To be completed. Companion simulation predicts S = 131 min for the ASTM E119 exposure; validation memo forthcoming.)'. We confirm that the prediction of S = 131 min STANDS without change. The continuous crossing time of 130.94 min rounds precisely to 131 min to the nearest minute, and the discrete sample that first exceeds the threshold is also t = 131 min (202.1 °C).", bold_prefix="Stub Disposition: ")

    # SECTION 5
    add_heading_1(doc, "5. Experimental Value Adoption & Formal Disposition on Bianca's Figure")
    add_heading_2(doc, "5.1 Certified Experimental Value Adopted (D = 118 min)")
    add_para(doc, "Per Section 6 of CFDME Validation Procedure rev 2, the experimental reference value D must be drawn strictly from the certified third-party laboratory test report of record:")
    add_bullet(doc, "Red Butte Report RBFMT-25-0918 (§5.2): Documents that unexposed thermocouple TC-6 (positioned directly over a continuous 3.8 mm truss-type steel tie course) reached the 181.0 °C single-point rise limit at 118 min after test start. At that instant, the nine-thermocouple mean rise was approximately 96.0 °C.", bold_prefix="• Test Result: ")
    add_bullet(doc, "Red Butte Report RBFMT-25-0918 (§5.3): Formally states: 'Reported endurance D = 118 min, governed by the single-point criterion at thermocouple 6.'", bold_prefix="• Lab Governance: ")
    add_bullet(doc, "Ironwood Certification Memo IWFPE-CERT-25-0374 (§2): Confirms D = 118 min as the sole governing endurance under ASTM E119, certifying the wall for a 1-hour fire-resistance rating (60 min).", bold_prefix="• Professional Certification: ")
    add_para(doc, "We formally adopt D = 118 min as the certified experimental reference value of record for this validation audit.", bold_prefix="Adopted Value: ")

    add_heading_2(doc, "5.2 Formal Disposition on Bianca Rennert's Amended Figure (129 min)")
    add_para(doc, "In her October 9, 2025 email (20251009_Rennert_revised_burn_data.eml) and accompanying spreadsheet (burn_data_original_vs_revised.csv), Bianca Rennert transmitted a 'revised' single-point endurance of 129 min, stating that Ocotillo and their thermocouple vendor applied a post-test calibration correction to TC-6. Bianca asserted that 129 min 'aligns much more closely with your simulation's 131 min, and internally we're treating that as a validation.'")
    add_para(doc, "DISPOSITION: REJECTED IN ITS ENTIRETY. Bianca Rennert's figure of 129 min is procedurally inadmissible and cannot be substituted for D under any circumstance.", bold_prefix="Formal Disposition: ")
    add_para(doc, "Governing Technical and Legal Authority: CFDME Validation Procedure rev 2, Section 6 ('Source of D') establishes an absolute rule governing third-party data integrity:")
    add_callout(doc, [
        "\"D shall be taken from the certified third-party test report of record. Client-amended values may not be substituted for D absent a reissued report from the testing laboratory of record and a calibration certificate authorizing the revision. Post-test amendments transmitted by the client but not authorized by the lab are not admissible as D... The following forms of documentation are required to substitute a revised D:",
        "1. A reissued report from the testing laboratory of record, bearing the same report number as the original with an amendment sequence (e.g., '-R1'), signed by the laboratory's authorized signatory, and stating the reason for the revision.",
        "2. A calibration certificate covering the instrument or measurement whose revision is at issue, with a date and calibration-authority reference sufficient to trace the correction.",
        "3. An explicit statement, in the reissued report, that the revised value supersedes the value in the original report for all downstream use.",
        "Absent any of the three, the original value stands. The reviewing engineer shall reject any deliverable that draws D from a client-amended figure not backed by the above documentation. A polite, specific, thermocouple-calibration explanation transmitted by a client is not a laboratory revision; the analyst shall record the client transmittal in the correspondence folder and continue to use the certified D.\""
    ], title="MANDATORY GOVERNING CLAUSE — CFDME-QA-VAL-002 SECTION 6", border_color="991B1B", bg_color="FEF2F2")

    add_para(doc, "Deficiency Audit: None of the three mandatory criteria have been satisfied:")
    add_bullet(doc, "No Reissued Lab Report: Red Butte Fire & Materials Testing has not issued an amended or reissued report (e.g., RBFMT-25-0918-R1).", bold_prefix="1. ")
    add_bullet(doc, "No Authorized Calibration Certificate: No laboratory calibration certificate exists authorizing any post-test adjustment. To the contrary, Section 7 of Red Butte's certified report confirms that thermocouple set TC-1 through TC-10 was calibrated on 2025-08-12 under NIST-traceable Certificate No. RBFMT-CAL-25-0812-TC and was fully in force on test day.", bold_prefix="2. ")
    add_bullet(doc, "No Laboratory Superseding Statement: Red Butte has made no statement superseding their published 118 min result.", bold_prefix="3. ")
    add_para(doc, "Under Arizona professional engineering statutes and firm QA policy, substituting an informal, client-preferred number for an accredited laboratory's certified result corrupts the validation baseline and constitutes engineering misrepresentation. D = 118 min stands.")

    # SECTION 6
    add_heading_1(doc, "6. Model Error Formulation, Acceptance Criterion, Uncertainty & Margin")
    add_heading_2(doc, "6.1 Deterministic Model Comparison Error (E = S - D)")
    add_para(doc, "Per ASME V&V 20 Section 1 and CFDME-QA-VAL-002 Section 3, model error is computed deterministically with sign retained:")
    add_bullet(doc, "Using integer values reported to the nearest minute:\n"
                    "E = S - D = 131 min - 118 min = +13 min.", bold_prefix="• Integer Reporting Form: ")
    add_bullet(doc, "Using exact continuous crossing times:\n"
                    "E_exact = 130.9375 min - 118.0000 min = +12.9375 min ≈ +12.94 min.\n"
                    "Both formulations yield +13 min to the nearest minute.", bold_prefix="• Continuous Formulation: ")
    add_para(doc, "Sign Significance: The positive sign (E = +13 min) indicates that the CFD companion simulation over-predicts the fire endurance of the wall assembly. In safety-critical fire engineering, predicting that a barrier survives longer than it does in physical reality represents a non-conservative model error.")

    add_heading_2(doc, "6.2 Primary Acceptance Criterion (|E| <= 10% of D)")
    add_para(doc, "Per CFDME-QA-VAL-002 Section 5, the firm's primary validation acceptance criterion is scaled to 10% of the certified experimental endurance:")
    add_bullet(doc, "Tolerance limit: 0.10 * D = 0.10 * 118 min = 11.8 min.", bold_prefix="• Allowable Error Band: ")
    add_bullet(doc, "Primary Comparison: |E| = 13 min > 11.8 min (or |12.94 min| > 11.8 min).\n"
                    "The comparison error exceeds the primary acceptance threshold by 1.2 min (or 1.14 min on continuous basis).", bold_prefix="• Acceptance Check: ")
    add_para(doc, "STATUS: FAILS PRIMARY ACCEPTANCE CRITERION.", bold_prefix="Primary Outcome: ")

    add_heading_2(doc, "6.3 Validation Uncertainty Build-Up (u_val) & Secondary Comparison")
    add_para(doc, "Per CFDME-QA-VAL-002 Section 4, the validation uncertainty u_val combines numerical, input, and experimental uncertainties via root-sum-square (RSS) for conjugate thermal E119 wall simulations:")
    add_bullet(doc, "Numerical uncertainty (discretization, iterative convergence, round-off): u_num = ±4 min.", bold_prefix="1. u_num: ")
    add_bullet(doc, "Input uncertainty (concrete k-rho-cp, cavity emissivity, tie geometry, furnace heat flux): u_inp = ±6 min.", bold_prefix="2. u_inp: ")
    add_bullet(doc, "Experimental uncertainty (Type-K TC calibration, placement, DAQ chassis per Red Butte §7): u_exp = ±5 min.", bold_prefix="3. u_exp: ")
    add_bullet(doc, "Root-Sum-Square Combination:\n"
                    "u_val = sqrt(u_num^2 + u_inp^2 + u_exp^2) = sqrt(4^2 + 6^2 + 5^2) = sqrt(16 + 36 + 25) = sqrt(77) = ±8.775 min ≈ ±8.77 min.\n"
                    "Reported to whole minutes per procedure: u_val = ±9 min.", bold_prefix="• Combined RSS Uncertainty: ")
    add_para(doc, "Secondary Comparison to u_val: Per Section 5 of our procedure, |E| is compared against u_val. Here, |E| = 13 min > u_val = 9 min. Because the model error exceeds the combined validation uncertainty, the discrepancy cannot be dismissed as measurement scatter or numerical noise floor. The error is resolved as an actionable model deficiency that must be reported.")

    add_heading_2(doc, "6.4 Maximum Prediction Clearing the Primary Criterion (S_max)")
    add_para(doc, "To establish the boundary of acceptable model behavior, we compute the largest simulation prediction that would have cleared the primary 10% criterion against D = 118 min:")
    add_bullet(doc, "Upper continuous bound: S_max = D + 0.10 * D = 118 min + 11.8 min = 129.8 min.", bold_prefix="• Continuous Limit: ")
    add_bullet(doc, "Nearest-minute integer bound: S = 129 min yields E = 129 min - 118 min = +11 min <= 11.8 min (Passes). S = 130 min yields E = 130 min - 118 min = +12 min > 11.8 min (Fails). Therefore, S_max,integer = 129 min.", bold_prefix="• Integer Limit: ")
    add_para(doc, "Analytical Insight into Client Positioning: This calculation reveals why Bianca Rennert advanced 129 min as her preferred number. An endurance of 129 min sits at the exact mathematical boundary (129.8 min) of the 10% criterion against 118 min. More importantly, if D were improperly revised to 129 min, the current simulation prediction (S = 131 min) would produce E = 131 min - 129 min = +2 min, easily clearing the criterion (|E| = 2 min <= 12.9 min) and sitting well within u_val (±9 min). However, manipulating D to force validation violates engineering ethics and governing procedure.")

    # SECTION 7
    add_heading_1(doc, "7. Multi-Source Diagnostic Comparisons: Test vs. Simulation")
    add_para(doc, "To isolate the physical root cause of the model discrepancy, we cross-evaluate two internal structural metrics between the physical test and the companion simulation:")

    add_heading_2(doc, "7.1 Diagnostic Comparison 1: Criterion Separation (Average Rise vs. Single-Point)")
    add_para(doc, "ASTM E119 tracks both the localized thermal bridge (single-point criterion) and the global field transmission (average-rise criterion). The time separation between these two criteria measures how rapidly localized thermal bridging outpaces field conduction:")
    add_bullet(doc, "In Certified Physical Test (Red Butte RBFMT-25-0918 §5.1, §5.2):\n"
                    "Average-rise criterion reached at: t_avg = 163 min.\n"
                    "Single-point criterion reached at: t_single = 118 min.\n"
                    "Test separation: Delta_t_test = 163 min - 118 min = 45 min.", bold_prefix="• Physical Test: ")
    add_bullet(doc, "In Companion Simulation (E119_companion_sim_results.csv):\n"
                    "Average-rise crossing reached at: t_cross,avg = 176.10 min (nearest minute: 176 min).\n"
                    "Single-point crossing reached at: t_cross,single = 130.94 min (nearest minute: 131 min).\n"
                    "Continuous simulation separation: Delta_t_sim = 176.10 min - 130.94 min = 45.16 min.\n"
                    "Nearest-minute simulation separation: Delta_t_sim = 176 min - 131 min = 45 min.", bold_prefix="• Companion Run: ")
    add_para(doc, "COMPARISON FINDING: The time separating the single-point failure from the average-rise failure is EXACTLY 45 min in both the physical test and the companion simulation (45 min vs 45 min).", bold_prefix="Diagnostic Result 1: ")

    add_heading_2(doc, "7.2 Diagnostic Comparison 2: Governing Point Elevation Above Nine-Point Mean")
    add_para(doc, "This metric evaluates how far the governing hot-spot temperature (over the steel tie course) sits above the nine-point field mean at the exact moment governance occurs:")
    add_bullet(doc, "In Certified Physical Test (at t = 118 min):\n"
                    "Thermocouple 6 rise: Delta_T_TC6 = 181.0 °C (absolute temperature: 21.0 °C + 181.0 °C = 202.0 °C).\n"
                    "Nine-thermocouple mean rise: Delta_T_mean = 96.0 °C (absolute temperature: 21.0 °C + 96.0 °C = 117.0 °C).\n"
                    "Test elevation above mean: Delta_T_elev,test = 181.0 °C - 96.0 °C = 85.0 °C (85.0 K).", bold_prefix="• Physical Test: ")
    add_bullet(doc, "In Companion Simulation (at governance crossing t = 130.94 min):\n"
                    "Peak unexposed temperature: T_unexposed_max_C = 202.00 °C (rise: 181.00 °C).\n"
                    "Mean unexposed temperature: T_unexposed_avg_C = 110.83 °C (rise: 89.83 °C).\n"
                    "Simulation elevation at crossing: Delta_T_elev,sim = 202.00 °C - 110.83 °C = 91.17 °C ≈ 91.2 °C (91.2 K).\n"
                    "(At discrete timestep t = 131 min: T_max = 202.1 °C, T_avg = 110.9 °C -> Delta_T_elev = 91.2 °C).", bold_prefix="• Companion Run: ")
    add_para(doc, "COMPARISON FINDING: In the simulation, the governing point sits 91.2 °C above the field mean at governance, compared to 85.0 °C in the physical test. The simulation slightly over-concentrates heat at the tie bridge by 6.2 °C (6.2 K), showing excellent agreement with test thermal peaking.", bold_prefix="Diagnostic Result 2: ")

print("Compiled generate_sections_b.py successfully.")
