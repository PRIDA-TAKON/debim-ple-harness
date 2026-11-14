# 13.8 kV Site Distribution Conveyance Study — Final Deliverable Summary
**Solicitation:** FA4610-26-R-0031 | **Project:** PCSFA 24-0117  
**Installation:** Pacific Crest Space Force Annex, Los Angeles County, CA  
**Primary Deliverable:** [`output/submission.zip`](file:///filesystem/final_batch4__electrical_task12_conveyance_study__blind/output/submission.zip)  
**Root Contents:**
1. [`conveyance_study.xlsx`](file:///filesystem/final_batch4__electrical_task12_conveyance_study__blind/output/conveyance_study.xlsx) (11 fully populated sheets matching template with live formulas)
2. [`conveyance_study_report.md`](file:///filesystem/final_batch4__electrical_task12_conveyance_study__blind/output/conveyance_study_report.md) (Comprehensive 35% Design Study Report)

---

### 1. Key Verified Results & Recommendations

| Item | Feeder Circuit Description | Recommended Type | Cable / Conductor Size & Sets | Route Length (LF) | Direct Cost ($) | Contract Cost ($) | Total Project Cost ($) | Unit Cost ($/LF) | Selection Status & Technical Basis |
|:---|:---|:---:|:---:|---:|---:|---:|---:|---:|:---|
| **C01** | SS-1 Feeder F1 to MB-1 MSG-A (Primary) | **CEDB** | 2 sets (3x 1/C 500 kcmil AL) | 927.2 | $233,595.26 | $297,849.36 | $330,568.11 | **$356.52** | **Governed by IEDS 4.2 & UFC 3-550-01 3-11.2.1.** Sole permitted underground method inside industrial core; includes 80 LF HDD under Mission Dr (48" cover) and MH-01/MH-02. |
| **C02** | SS-1 Feeder F2 to MB-1 MSG-B (Secondary) | **CEDB** | 2 sets (3x 1/C 500 kcmil AL) | 1,182.3 | $280,050.61 | $357,082.99 | $396,308.56 | **$335.20** | **Governed by IEDS 4.2 & 4.4.** Bus B redundancy feeder routed independently (>20 ft separation from C01); includes 80 LF HDD under Mission Dr and MH-03/MH-04. |
| **C03** | SS-1 Feeder F3 to CUP-1 SWG-C1 | **CEDB** | 1 set (3x 1/C 500 kcmil AL) | 490.0 | $84,352.31 | $107,554.76 | $119,369.65 | **$243.61** | **Governed by IEDS 4.2 & 4.8.** CEDB across Parking Lot P-1; includes 150 LF structurally reinforced envelope (4 No. 4 bars + No. 3 ties) and MH-05. |
| **C04** | CUP-1 Feeder CF-2 to Lift Station LS-2 | **CEDB** | 1 set (3x 1/C 250 kcmil AL) | 1,327.0 | $260,519.67 | $332,179.75 | $368,669.70 | **$277.82** | **Governed by IEDS 4.2 & 4.3.** Includes 80 LF HDD under Mission Dr, 120 LF deep HDD (120" cover) under Drainage Channel DC-1, dewatering near B-10, and MH-06 to MH-10. |
| **C05** | MB-1 MSG-A to Unit Substation USS-A1 | **RMC** | 1 set (3x 1/C 500 kcmil AL) | 400.0 | $82,464.82 | $105,148.08 | $116,698.60 | **$291.75** | **Governed by IEDS 5.1 & NEC 300.37.** RMC inside MB-1 Corridor COR-1; EMT prohibited for >600 V; cable tray prohibited due to <18" ceiling space and SCIF IT-1 10-ft keep-out zone. |
| **C06** | SS-1 Feeder F4 to Gate House GH-1 | **OH** | 1 set (250 kcmil risers / 1/0 ACSR Raven) | 1,978.0 | $89,590.88 | $114,234.28 | $126,782.91 | **$64.10** | **Governed by IEDS 4.1 & RFP 1.5.** Located along south boundary (y=220) outside industrial polygon. OH is fully permitted and saves **$301,823.37 (70.4%)** vs CEDB ($428,606.28). |
| **C07** | CUP-1 Feeder CF-1 to Warehouse W-3 | **CEDB** | 1 set (3x 1/C 250 kcmil AL) | 680.0 | $157,968.31 | $201,420.01 | $223,546.00 | **$328.74** | **Governed by IEDS 4.2 & 4.5.** CEDB with 40 LF Jack-and-Bore (JB) crossing under active rail spur RR-SPUR-2 (two 5" RGS conduits at 42" cover) and MH-11 to MH-13. |
| **TOTAL** | **Entire 13.8 kV Distribution Package** | — | — | **6,984.5 LF** | **$1,188,541.86** | **$1,515,469.23** | **$1,681,943.52** | **$240.81** | **All 34 alternatives evaluated and priced across 636 bottom-up takeoff lines.** |

---

### 2. Engineering Calculations & Design Basis

1. **Short-Circuit Conductor Withstand Verification:**
   - **Fault Level & Duration:** 25.1 kA symmetrical, 0.16 s backup clearing time (Protective Device Settings Schedule Rev D & IEDS 2.4).
   - **ICEA P-32-382 / Onderdonk Formulation:** Minimum thermal threshold for aluminum with 90°C XLPE insulation ($T_2 = 250^\circ\text{C}$) is **213.5 kcmil**. 4/0 AWG AL (211.6 kcmil) fails; **250 kcmil AL is the statutory network minimum**, dictating the conductor sizes for C04, C06 risers, and C07 despite lighter operating currents.
2. **Thermal Ampacity Modeling:**
   - Ductbank ratings modeled per Neher-McGrath / NEC 310.60 ($\rho = 90^\circ\text{C}\cdot\text{cm/W}$, 20°C ambient earth). C01/C02 at 100% LF yield 335 A/set (total 670 A > 640 A / 560 A load). C03, C04, C07 at 75% LF yield 410 A/set and 300 A/set.
   - C05 indoor RMC derated for 40°C ambient yields 245 A (> 200 A load). C06 1/0 ACSR 'Raven' evaluated per IEEE 738 (40°C ambient, 2 ft/s wind) yields 242 A (> 40 A load).
3. **Cable Pulling Mechanics (All 23 Pulls Verified):**
   - **Tension:** Pulling eye limit $0.008 \times \text{cmil} \times N$ (12,000 lb for 500 kcmil; 6,000 lb for 250 kcmil). Max observed tension across all pulls is 1,760.3 lb (C01-P3), well below limits.
   - **Sidewall Bearing Pressure (SWBP):** Governed by approved submittal SUB-33 71 02-07 limit of **600 lb/ft** (superseding catalog 1,000 lb/ft). Max observed SWBP is 153.9 lb/ft on C05 interior conduit bend, well within limits.
   - **Conduit Fill & Jam Ratio:** All duct fills are $\le 39.0\%$ (under the NEC 40% threshold); clearance and jam ratios avoid critical jamming windows.

---

### 3. Estimating Basis, Cost Model & Live Formulas

1. **Labor Classification & Prevailing Wages:**
   - Priced bottom-up using **CA20260022 Mod 5** (effective 2026-08-06 per 29 CFR 1.6(c)(2)(ii)(A)).
   - Loaded rates in `LaborRates` use live formulas: `=D{idx}*(1+F{idx})+E{idx}` applying payroll taxes and workers' comp (Class 7538: 20.39%, Class 5190: 15.77%, Class 6218: 19.00%) strictly to base wages.
2. **Markup Hierarchy & Markups Table:**
   - **JOOH:** 9.50% (`Markups!$B$2`)
   - **HOOH:** 4.50% (`Markups!$B$3`) applied to Direct + JOOH
   - **Profit:** 7.9714% (`Markups!$B$4`) calculated via UFC 3-740-05 11-2.2 weighted guidelines ($4.2M job size, 15-month duration, 30% subcontracting)
   - **Performance & Payment Bond:** Effective rate **1.24043%** (`Markups!$B$5`) derived from Sierra Surety Class B graduated rate on $1,468,431.67 base sum + 3% surcharge for 15-month performance period ($18,214.85 premium)
   - **Escalation to Midpoint (2027-08-18):** Factor **1.019388** (`Markups!$B$6`) per UFS 3-701-01 Table 4-2 daily interpolation
   - **Design Contingency:** 5.00% (`Markups!$B$7`)
   - **SIOH:** 5.70% (`Markups!$B$8`) applied per UFC 3-740-05 13-3.2 to Contract Cost + Contingency
   - **Area Cost Factor:** Prohibited on bottom-up estimates per UFS 3-701-01 4-1.1; set to **1.000** (`Markups!$B$9`)
3. **Live Formulas in Alternatives:**
   - Columns K through U dynamically recompute from underlying labor, equipment, material, and subcontract columns and `Markups!$B$2:$B$8`, ensuring full auditability.

---

### 4. GFE Findings Resolved & Applied (7 Formal Defect Logs)

- **`FIND-01` (SS-1 Feeder F1 Pickup):** E-001 showed 560 A; Settings Schedule Rev D increased to 640 A for MB-1 Phase 2. Governed by Settings Schedule Rev D per IEDS 1.3 order of precedence.
- **`FIND-02` (Soil Classification & Dewatering):** GEO Table 2 listed B-7 and B-10 as OSHA Type B; primary boring logs show cohesionless SP/SM sands with water at 4.0 ft and 3.0 ft. Governed by boring logs and 29 CFR 1926 Subpart P App A (reclassified as OSHA Type C with dewatering).
- **`FIND-03` (Prohibition of Area Cost Factor):** Gov Estimate Template applied ACF of 1.16; UFS 3-701-01 4-1.1 strictly forbids applying ACF to local bottom-up estimates. Corrected to 1.0.
- **`FIND-04` (Water Main W-12 Clearance):** C-101 indicated W-12 at 72" depth; SUE-24-0117 QL-A potholing (TH-1/TH-2) revealed actual depth of 56" (16" shallower). Governed by SUE survey.
- **`FIND-05` (Retained Tree T-208 Protection):** C-101 omitted retained 14" Jacaranda T-208 at (170, 395). Governed by tree survey TS-24-0117; jogged C06 underground route east to x=195 to protect the 14-ft TPZ.
- **`FIND-06` (Tape-Shield SWBP Restriction):** Catalog TD-15AL-133 cited 1,000 lb/ft; approved submittal SUB-33 71 02-07 restricted tape shield to 600 lb/ft. Governed by approved submittal.
- **`FIND-07` (Wage Determination Revision):** Attachment J-3 contained superseded Mod 2; applied Mod 5 published 2026-08-06 (>10 days before bid opening) pursuant to 29 CFR 1.6(c)(2)(ii)(A).

---

### 5. Deliverable Archive Verification

Verification of [`output/submission.zip`](file:///filesystem/final_batch4__electrical_task12_conveyance_study__blind/output/submission.zip):
```
Archive:  output/submission.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
    55023  2026-11-14 04:33   conveyance_study.xlsx
    50701  2026-11-14 04:37   conveyance_study_report.md
---------                     -------
   105724                     2 files
```
All deliverables are verified, non-empty, and compliant with all RFP specifications and governing criteria.