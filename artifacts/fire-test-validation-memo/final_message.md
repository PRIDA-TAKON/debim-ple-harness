# MEMORANDUM & QA/QC VALIDATION AUDIT SUMMARY

**TO:** Marguerite Falk, PE — Technical Director & Reviewing Engineer (AZ PE #42798)  
**FROM:** Gordon Selby, PE — Owner & Principal Engineer (AZ PE #48213), The CFD ME  
**DATE:** October 10, 2025  
**PROJECT:** CFDME-2025-041 — Ocotillo WUI Wildfire Exposure, Phase 1  
**CLIENT:** Ocotillo Additive Structures (Attn: Trevor Buckhalter, CEO; Bianca Rennert, VP Product Marketing)  
**SUBJECT:** ASTM E119 Companion Simulation Validation Evaluation — ASME V&V 20 Assessment, Physical Test Reconciliation, Diagnostic Comparison, and Phase 1 Scope Disposition  
**DELIVERABLE FILES:**
- Primary Deliverable: `output/CFDME-2025-041_E119_validation_memo.docx`
- Convenience Copy: `output/E119_companion_simulation_validation_memo.docx`

---

### Transmittal Paragraph for Bianca Rennert (Ready to Send Today)

> *"Bianca — On the companion simulation for the Red Butte E119 burn, our governing QA procedure (CFDME-QA-VAL-002, adhering to ASME V&V 20) requires us to report model fidelity as a comparison error against the certified test of record rather than a binary validation claim, and prohibits adopting post-test adjustments without an authorized, reissued laboratory report and NIST-traceable calibration certificate. Against Red Butte's certified single-point endurance of 118 min (Report No. RBFMT-25-0918, certified by Ironwood PE Marla Kettering), our companion run predicts 131 min (continuous crossing at 130.94 min), yielding a model error of $E = +13\text{ min}$. Because this discrepancy exceeds both our firm's 10% acceptance threshold ($11.8\text{ min}$) and our combined validation uncertainty ($\pm 9\text{ min}$), the simulation cannot be characterized as validated in your launch materials or press deck. Furthermore, per ASTM E119 Section 8 and our professional standard of care, standard furnace endurance is a comparative building assembly rating and does not predict wildland-urban interface (WUI) wildfire survival; launch materials must not equate the E119 result with Sonoran buffelgrass wildfire performance."*

---

### Table 1: ASME V&V 20 Model-Error Rollup & Validation Decision Matrix

All values are derived deterministically in accordance with **CFDME Validation QA Procedure — ASME V&V 20 rev 2** (CFDME-QA-VAL-002) and ASME V&V 20-2009 (R2016).

| Parameter | Symbol / Formulation | Value | Unit | Governing Reference / Engineering Basis |
| :--- | :--- | :---: | :---: | :--- |
| **Simulation Prediction** | $S$ | **131** | $\text{min}$ | `E119_companion_sim_results.csv` (linear crossing time $130.94\text{ min}$; discrete threshold trip at $131\text{ min}$; single-point criterion governs) |
| **Certified Experimental Value** | $D$ | **118** | $\text{min}$ | Red Butte Report RBFMT-25-0918 §5.2 / Ironwood Memo IWFPE-CERT-25-0374 §2 (single-point limit at TC-6 over steel tie course) |
| **Model Comparison Error** | $E = S - D$ | **+13** | $\text{min}$ | ASME V&V 20 §1 / CFDME-QA-VAL-002 §3 ($+12.94\text{ min}$ continuous; positive sign denotes non-conservative over-prediction) |
| **Primary Acceptance Criterion** | $\|E\| \le 10\% \text{ of } D$ | **11.8** | $\text{min}$ | CFDME-QA-VAL-002 §5 ($0.10 \times 118\text{ min} = 11.8\text{ min}$ scaled tolerance band) |
| **Validation Uncertainty** | $u_{\text{val}} = \sqrt{u_{\text{num}}^2 + u_{\text{inp}}^2 + u_{\text{exp}}^2}$ | **$\pm 9$** | $\text{min}$ | CFDME-QA-VAL-002 §4 ($\pm 8.77\text{ min}$ RSS of $u_{\text{num}} = \pm 4\text{ min}$, $u_{\text{inp}} = \pm 6\text{ min}$, $u_{\text{exp}} = \pm 5\text{ min}$) |
| **Primary Criterion Test** | $\|E\| \le 11.8\text{ min}$ | **$13 > 11.8$** | $\text{min}$ | **FAILS PRIMARY CRITERION**: Model error exceeds the allowable $10\%$ tolerance band by $1.2\text{ min}$ ($1.14\text{ min}$ continuous) |
| **Secondary Uncertainty Test** | $\|E\| \le u_{\text{val}}$ | **$13 > 9$** | $\text{min}$ | **FAILS NOISE TEST**: $\|E\|$ exceeds $u_{\text{val}}$; resolved as an actionable systematic model error exceeding the noise floor |
| **Max Prediction Clearing Criterion** | $S_{\text{max}} = D + 0.10 \times D$ | **129.8** | $\text{min}$ | Upper bound clearing primary criterion ($129\text{ min}$ to nearest whole minute; $130\text{ min}$ yields $E = +12\text{ min} > 11.8\text{ min}$) |
| **Formal Validation Verdict** | Formal Decision | **FAILS** | — | **DOES NOT VALIDATE**; unqualified validation claim prohibited; report release requires Documented Finding |

---

### Detailed Engineering Audit & Technical Findings

#### 1. Assembly Equivalence & Governing Authority
- **Assembly in the Run:** CAD model of record `OAS-WUI-01_revC` (`OAS_wall_assembly_section.png` / `OAS-WUI-01_revC.FCStd`), comprising two $50\text{ mm}$ 3D-printed siliceous-aggregate concrete leaves, a $205\text{ mm}$ clear open-air cavity (no insulation, fill, membrane, or fire-stop), an overall thickness of $305\text{ mm}$ ($50/205/50\text{ mm}$), and continuous 9-gauge ($3.8\text{ mm}$ diameter) galvanized steel truss-type wire ties at $600\text{ mm}$ on-center vertical spacing with $25\text{ mm}$ embedment into each leaf, evaluated as a non-load-bearing partition.
- **Certified Geometry:** Section 2 of Red Butte Report RBFMT-25-0918 and Section 1.2 of Ironwood Certification Memo IWFPE-CERT-25-0374 tabulate the identical build: $50\text{ mm}$ leaves, $205\text{ mm}$ open cavity, $305\text{ mm}$ total thickness, siliceous aggregate, and continuous 9-gauge ($3.8\text{ mm}$) galvanized steel truss ties at $600\text{ mm}$ o.c. with $25\text{ mm}$ embedment.
- **Determination:** **YES, the assembly modeled in the run is the certified assembly.** This rests on the exact 1:1 cross-sectional correspondence of all through-wall thermal impedance layers and tie specifications. While the laboratory furnace opening was $3.05\text{ m} \times 3.05\text{ m}$ ($10\text{ ft} \times 10\text{ ft}$) and the CAD panel is $1.83\text{ m} \times 2.745\text{ m}$ ($6\text{ ft} \times 9\text{ ft}$), through-wall heat transmission and metallic tie thermal bridging are 1D/3D through-thickness mechanisms governed by cross section and tie pitch ($600\text{ mm}$ o.c.), which are identical.
- **Status of Revision D:** Trevor Buckhalter's revD geometry transmitted on 10/09/2025 (`20251009_Buckhalter_geometry_revD.eml`) adds a $610\text{ mm}$ continuous hollow parapet (total height $3355\text{ mm}$), $50\text{ mm}$ coping, and $25\text{ mm}$ drip overhang. Revision D was **not** run in the companion simulation (run on revC per CSV header and logs), was not tested at Red Butte, and falls outside Ironwood's certified rating per Section 1.2 ("Any deviation from the tabulated geometry places the assembly outside the scope of this certification").

#### 2. Governing Criterion, Crossing Times, and Section 7 Stub Status
- **ASTM E119 Endpoints (Initial Ambient $T_0 = 21.0\text{ }^\circ\text{C}$):**
  1. *Average Unexposed-Face Criterion:* Rise $\le 139.0\text{ }^\circ\text{C}$ ($250.0\text{ }^\circ\text{F}$) $\rightarrow$ Absolute limit $T_{\text{avg,limit}} = 21.0\text{ }^\circ\text{C} + 139.0\text{ }^\circ\text{C} = 160.0\text{ }^\circ\text{C}$.
  2. *Single-Point Unexposed-Face Criterion:* Rise $\le 181.0\text{ }^\circ\text{C}$ ($325.0\text{ }^\circ\text{F}$) $\rightarrow$ Absolute limit $T_{\text{max,limit}} = 21.0\text{ }^\circ\text{C} + 181.0\text{ }^\circ\text{C} = 202.0\text{ }^\circ\text{C}$.
  3. *Governing Rule:* The earlier criterion governs.
- **Simulation Crossing Times (Linear Interpolation):**
  - Single-point: At $t = 130\text{ min}$, $T = 200.5\text{ }^\circ\text{C}$; at $t = 131\text{ min}$, $T = 202.1\text{ }^\circ\text{C}$.  
    $$t_{\text{cross,single}} = 130\text{ min} + \frac{202.0 - 200.5}{202.1 - 200.5} \times 1.0\text{ min} = 130.9375\text{ min} \approx 130.94\text{ min} \quad (\mathbf{131\text{ min}}\text{ to nearest min})$$
  - Average-rise: At $t = 176\text{ min}$, $T = 159.9\text{ }^\circ\text{C}$; at $t = 177\text{ min}$, $T = 160.9\text{ }^\circ\text{C}$.  
    $$t_{\text{cross,avg}} = 176\text{ min} + \frac{160.0 - 159.9}{160.9 - 159.9} \times 1.0\text{ min} = 176.1000\text{ min} \approx 176.10\text{ min} \quad (\mathbf{176\text{ min}}\text{ to nearest min})$$
- **Governing Criterion:** The single-point criterion is reached first ($130.94\text{ min} < 176.10\text{ min}$) and **governs**.
- **Section 7 Stub Status:** In `CFDME-2025-041_Phase1_report_revB.docx`, the Section 7 stub states: *"Companion simulation predicts S = 131 min for the ASTM E119 exposure"*. **This prediction STANDS.** ($130.94\text{ min}$ rounds to $131\text{ min}$, and the discrete tripping sample is also $t = 131\text{ min}$).

#### 3. Adopted Experimental Value and Disposition on Bianca's Figure
- **Adopted Value:** **$D = 118\text{ min}$**, from Red Butte Report RBFMT-25-0918 (§5.2, single-point limit reached at TC-6) and Ironwood Memo IWFPE-CERT-25-0374 (§2).
- **Disposition on Bianca's Figure ($129\text{ min}$):** **REJECTED.** Per CFDME Validation Procedure rev 2 Section 6, client-amended numbers cannot be substituted for $D$ absent:
  1. A reissued report from the testing lab of record bearing an amendment sequence (e.g., `-R1`), signed by authorized lab signatory, stating the reason for revision;
  2. A laboratory calibration certificate covering the instrument with traceable authority; and
  3. An explicit laboratory statement that the revised figure supersedes the original.  
  *None of these exist.* Red Butte Report RBFMT-25-0918 §7 confirms all thermocouples (TC-1 to TC-10) carried active, NIST-traceable calibration certificates (`RBFMT-CAL-25-0812-TC`) valid on test day.

#### 4. Model Error, Acceptance Criterion, Uncertainty & Bound Analysis
- **Comparison Error:** $E = S - D = 131\text{ min} - 118\text{ min} = \mathbf{+13\text{ min}}$ ($+12.94\text{ min}$ continuous). Positive sign denotes simulation over-prediction (non-conservative).
- **Primary Acceptance Criterion:** $|E| \le 10\% \times D = 0.10 \times 118\text{ min} = \mathbf{11.8\text{ min}}$.  
  *Comparison:* $|E| = 13\text{ min} > 11.8\text{ min}$ $\rightarrow$ **FAILS primary acceptance criterion** by $1.2\text{ min}$.
- **Validation Uncertainty:** $u_{\text{val}} = \sqrt{4^2 + 6^2 + 5^2} = \sqrt{77} \approx \pm 8.77\text{ min} \rightarrow \mathbf{\pm 9\text{ min}}$.  
  *Comparison:* $|E| = 13\text{ min} > u_{\text{val}} = 9\text{ min}$ $\rightarrow$ Discrepancy exceeds validation noise floor; resolved as an actionable model error.
- **Largest Prediction Clearing Criterion:**  
  $$S_{\text{max}} = D + 0.10 \times D = 118\text{ min} + 11.8\text{ min} = \mathbf{129.8\text{ min}} \quad (\mathbf{129\text{ min}}\text{ to nearest whole min})$$
  *(At $S = 129\text{ min}$, $E = +11\text{ min} \le 11.8\text{ min}$; at $S = 130\text{ min}$, $E = +12\text{ min} > 11.8\text{ min}$)*.

#### 5. Two Diagnostic Multi-Source Comparisons
1. **Criteria Separation Time:**
   - Physical Test: $t_{\text{avg}} - t_{\text{single}} = 163\text{ min} - 118\text{ min} = \mathbf{45\text{ min}}$.
   - Companion Run: $t_{\text{cross,avg}} - t_{\text{cross,single}} = 176.10\text{ min} - 130.94\text{ min} = 45.16\text{ min} \rightarrow \mathbf{45\text{ min}}$ (nearest min: $176 - 131 = 45\text{ min}$).
   - *Result:* **The separation between single-point tie failure and average face failure is identical: $45\text{ min}$ vs $45\text{ min}$.**
2. **Governing Point Elevation Above Nine-Point Mean at Governance:**
   - Physical Test (at $t = 118\text{ min}$): TC-6 rise was $181.0\text{ }^\circ\text{C}$; 9-TC mean rise was $96.0\text{ }^\circ\text{C}$.  
     $$\Delta T_{\text{elev,test}} = 181.0\text{ }^\circ\text{C} - 96.0\text{ }^\circ\text{C} = \mathbf{85.0\text{ }^\circ\text{C}} \quad (\mathbf{85.0\text{ K}})$$
   - Companion Run (at $t = 130.94\text{ min}$ crossing): $T_{\text{max}} = 202.00\text{ }^\circ\text{C}$; $T_{\text{avg}} = 110.83\text{ }^\circ\text{C}$.  
     $$\Delta T_{\text{elev,sim}} = 202.00\text{ }^\circ\text{C} - 110.83\text{ }^\circ\text{C} = 91.17\text{ }^\circ\text{C} \approx \mathbf{91.2\text{ }^\circ\text{C}} \quad (\mathbf{91.2\text{ K}})$$
     *(At $t = 131\text{ min}$: $202.1\text{ }^\circ\text{C} - 110.9\text{ }^\circ\text{C} = 91.2\text{ }^\circ\text{C}$)*.
   - *Result:* **In the run, the governing point sits $91.2\text{ }^\circ\text{C}$ above the mean, compared to $85.0\text{ }^\circ\text{C}$ in the test (a delta of only $+6.2\text{ }^\circ\text{C}$).**

#### 6. Model Physics Diagnosis, Rework Identification, and Rework Status Audit
- **Diagnostic Meaning:**
  1. *Tie Conduction Physics is Sound:* The identical 45-minute separation and close hot-spot elevation ($\Delta = +6.2\text{ }^\circ\text{C}$) demonstrate that 3D conjugate conduction along the continuous steel truss ties and the localized thermal-bridge peaking mechanism are modeled with high structural fidelity.
  2. *Systemic Through-Wall Delay:* Both criteria are delayed by the exact same $+13\text{ min}$ ($131 - 118 = +13\text{ min}$ for single-point; $176 - 163 = +13\text{ min}$ for average rise). The error is a global through-thickness impedance over-prediction.
- **Where Rework Belongs:**
  - Siliceous concrete thermophysical properties: high-temperature thermal conductivity $k(T)$, volumetric heat capacity $\rho c_p(T)$, and moisture dehydration latent heat enthalpy plateau (calcium silicate hydrate dehydration at 100–300 °C carries excess effective thermal mass).
  - Cavity radiation emissivity $\epsilon$ (assumed default 0.85 vs elevated dirty/sooted emissivity) and natural convection view factors across the $205\text{ mm}$ air gap.
  - Steel tie embedment contact thermal resistance ($25\text{ mm}$ embedment into concrete).
  - Furnace exposed-face convective and radiative boundary heat flux.
- **Rework Status Audit:** **NO REWORK HAS BEEN STARTED YET.** Audits of HPC cluster accounting (`cluster_job_accounting_2025Q3.csv`), change order logs (`CFDME-2025-041_change_order_log.xlsx` has only CO-001 animation and CO-002 mesh refinement), staffing assignments (`CFDME_staffing_assignments.xlsx`), and case dictionaries (`Case/system_archive/OAS_case_setup_from_DWA.txt` is an unmodified DWA clone) confirm zero hours, compute jobs, or work orders have been allocated to E119 recalibration.

#### 7. Implications for Phase 1 Wildfire Analysis
- An over-prediction of endurance ($E = +13\text{ min}$) is non-conservative for fire safety (real physical walls transmit heat faster).
- Unqualified validation claims in the Phase 1 report or launch materials are prohibited.
- Section 7 must present the V&V 20 model-error rollup ($S = 131\text{ min}$, $D = 118\text{ min}$, $E = +13\text{ min}$, $u_{\text{val}} = \pm 9\text{ min}$) and record that the 10% criterion was not met.
- Phase 1 can only be released under a "Documented Finding" / "Released with comments" disposition.
- Downstream SOW §3.1 wildfire cases must acknowledge that physical through-wall temperatures under an advancing Sonoran buffelgrass fire front ($30.1\text{ MW}$) will likely rise faster in reality than predicted by the uncorrected solver stack.

#### 8. Scope Boundaries on Ocotillo's Wildfire Claims & Gap Closure
- **What this Exercise Establishes:** Model thermal transmission fidelity against the smooth, monotonically rising ASTM E119 standardized compartment furnace curve in a non-load-bearing configuration.
- **What it DOES NOT Establish:** Wildfire survival time, WUI performance, resistance to an advancing Sonoran buffelgrass fire front ($30.1\text{ MW}$ segment), wind-driven aerodynamic flame tilt ($5\text{--}12\text{ m/s}$), turbulent plume puffing ($0.87\text{ Hz}$), flame washing, or firebrand/ember accumulation and ignition in parapet crevices. An E119 rating cannot be converted algebraically into wildfire survival time.
- **Closing the Gap:** Physical testing under representative WUI thermal-fluid exposure (ASTM E2707/E2726, California Building Code Chapter 7A, or full-scale wind-fire burner facility testing with calibrated ember generators).
- **Mandatory Reporting Form:** Any future comparison must strictly follow ASME V&V 20 / CFDME-QA-VAL-002 §3: reporting $S$, $D$, $E = S - D$, and $u_{\text{val}}$ in a single table with units and sign; never binary yes/no or qualitative phrasing.

#### 9. Impact of Bianca's Figure, Entitlement, Stamp Language & Checklist Disposition
- **Rating Impact if Substantiated:** Measured endurance of $118\text{ min}$ falls $2\text{ min}$ short of the 2-hour ($120\text{ min}$) threshold, capping the certified rating at 1-Hour ($60\text{ min}$). If Bianca's $129\text{ min}$ figure were ever substantiated by a reissued Red Butte report, it would exceed $120\text{ min}$ ($129\text{ min} \ge 120\text{ min}$), **upgrading the certified fire-resistance rating from 1-Hour ($60\text{ min}$) to 2-Hour ($120\text{ min}$)** (a 100% rating increase).
- **Entitled Authority:** **ONLY Marla Kettering, PE (AZ PE #45106)** of Ironwood Fire Protection Engineering (or another qualified registered Fire Protection PE), acting on an official reissued laboratory report from Red Butte. Per Section 4 of Ironwood's memo: *"No other party may certify or restate this rating."* Neither The CFD ME, Gordon Selby, PE, Bianca Rennert, nor Trevor Buckhalter has legal or professional standing to alter or restate the rating.
- **Mandatory Stamp Language:**  
  $$\text{"CFD thermal analysis only. Fire-resistance rating certified separately by others."}$$
- **Peer-Review Checklist Disposition (`CFDME-2025-041_peer_review_checklist.docx`):**
  - **Item 6 CLOSES:** *"Validation reported as E ± u_val against acceptance criterion, NOT yes/no, per Validation Procedure rev 2 §3–§5"* is fully satisfied by this memo and Section 7 text.
  - **Items 2, 3, 4, 5, 7, 9, and 10 REMAIN OPEN:** Pending Froude regime documentation (Item 2), solver confirmation (Item 3), $D^*/dx$ and Pope TKE in report body (Item 4), through-wall CHT treatment documentation (Item 5), mesh build timestamp vs transmittal log cross-check (Item 7), structural windload pressure units verification (Item 9), and final reviewer sign-off (Item 10). *(Items 1 and 8 are already closed).*

---

### Appendix: Ready-to-Insert Draft Text for Section 7 of Phase 1 Report rev B

This exact text is embedded in the deliverable Word document and can be directly pasted into `CFDME-2025-041_Phase1_report_revB.docx` to replace the stub:

```markdown
7. Validation
7.1 Governing Framework and Reporting Standard
In accordance with CFDME Validation QA Procedure — ASME V&V 20 rev 2 (CFDME-QA-VAL-002), validation is reported as the model comparison error E = S - D with its combined validation uncertainty u_val, and not as a binary yes/no statement. The certified physical test of record is Red Butte Fire & Materials Testing Report No. RBFMT-25-0918 (test date 09/24/2025, certified by Ironwood Fire Protection Engineering Memorandum No. IWFPE-CERT-25-0374, Marla Kettering, PE, AZ PE #45106). The companion simulation run of record is E119_companion_sim_results.csv, modeling CAD geometry OAS-WUI-01_revC.

7.2 Thermal Transmission Endpoints and Crossing Times
Under ASTM E119 Section 8, the unexposed face is evaluated against two criteria from initial ambient T_0 = 21.0 °C: (i) average rise of nine thermocouples not to exceed 139.0 °C (limit 160.0 °C); and (ii) single-point rise not to exceed 181.0 °C (limit 202.0 °C). The earlier criterion governs. In the companion simulation, continuous linear interpolation yields a single-point crossing time of 130.94 min (nearest minute: 131 min) and an average-rise crossing time of 176.10 min (nearest minute: 176 min). The single-point criterion governs, yielding simulation prediction S = 131 min.

7.3 Model Comparison Error and Acceptance Decision
From certified test report RBFMT-25-0918 Section 5.2, single-point governance occurred at 118 min at thermocouple TC-6 (positioned over a continuous 3.8 mm steel tie course), establishing certified experimental value D = 118 min. The model comparison error is:
    E = S - D = 131 min - 118 min = +13 min
The firm's primary acceptance criterion is |E| <= 10% of D = 11.8 min. The simulation fails this criterion (|E| = 13 min > 11.8 min). Combined validation uncertainty for this assembly class is u_val = ±9 min (root-sum-square of numerical uncertainty u_num = ±4 min, input uncertainty u_inp = ±6 min, and experimental uncertainty u_exp = ±5 min). Because |E| = 13 min > u_val = 9 min, the discrepancy is resolved as an actionable model error. The positive error indicates that the CFD model over-predicts fire endurance by 13 minutes, representing a non-conservative bias.

7.4 Diagnostic Reconciliation and Model Findings
Diagnostic cross-checks confirm that the localized thermal-bridge mechanics of the steel ties are accurately modeled: the time separating single-point failure from average-rise failure is identical between test and simulation (45 min in both), and peak hot-spot elevation above the mean at governance agrees within 6.2 °C (85.0 °C test vs 91.2 °C simulation). The discrepancy is an assembly-wide through-wall transmission lag: both failure modes are shifted by exactly +13 min. Rework belongs in printed concrete high-temperature conductivity k(T), moisture dehydration enthalpy, and cavity radiation emissivity. Post-test thermocouple adjustments proposed by the client (129 min) are rejected per firm procedure Section 6 absent a reissued laboratory report.

7.5 Wildfire Scope Boundary
Per CFDME-QA-VAL-002 Section 7, validation against ASTM E119 compartment furnace data establishes model behavior under standard furnace curves and does not validate wildland-urban interface (WUI) wildfire survival. An E119 rating cannot be converted into wildfire survival time. Performance under advancing Sonoran buffelgrass fire fronts requires dedicated physical testing under transient radiant heat flux, wind-driven flame tilt, and ember attack.
```

---

### Deliverable Verification
The Word memorandum deliverable has been written directly to `output/CFDME-2025-041_E119_validation_memo.docx` (and mirrored to `output/E119_companion_simulation_validation_memo.docx`). The file has been verified in the environment (163 paragraphs, 10 styled tables, complete callout blocks, exact SI units on all quantities, and professional engineer seal and signature blocks).