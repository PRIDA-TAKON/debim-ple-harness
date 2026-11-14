An engineering resolution memorandum has been prepared and saved to [`/filesystem/CFDME-2025-041_resolution_note_revA.docx`](file:///filesystem/CFDME-2025-041_resolution_note_revA.docx). 

The note directly addresses Item 4 on Marguerite Falk's peer-review checklist ([`CFDME-2025-041_peer_review_checklist.docx`](file:///filesystem/Firm/QA/Reviews/CFDME-2025-041_peer_review_checklist.docx)) for Phase 1 Report rev B. It settles the resolution question entirely on the basis of data, logs, and mesh studies already archived on the file server—**no new simulations or mesh runs are required**.

---

### Executive Technical Summary

| Audit Item | Value of Record | QA Standard Reference & Finding |
| :--- | :--- | :--- |
| **Plume Length Scale ($D^*$)** | **$3.76\text{ m}$** (exact: $3.742\text{ m}$) | [`CFDME_QA_Verification_Standard_rev3 §2`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L26-L34); $\dot{Q} = 30.1\text{ MW}$, $T_\infty = 293.15\text{ K}$, $\rho_\infty = 1.204\text{ kg/m}^3$. |
| **Reporting Grid Cell Size ($dx$)** | **$0.5\text{ m}$** background ($0.125\text{ m}$ refined) | [`three_grid_study_outputs.txt`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/verification/three_grid_study_outputs.txt#L205-L215); `case_fine` ($11,196,000$ cells; $11,214,862$ with wall). |
| **Plume Resolution Index ($D^*/dx$)** | **$7.52$** (reported as **$7.5$**) | **COMPLIANT**: Lands in the center of the mandatory **$5 \text{ to } 10$** band ([`Standard rev 3 §5.1`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L72-L78)). |
| **Pope Resolved-TKE Fraction** | **$84\%$** ($k_{res}/(k_{res}+k_{sgs}) = 0.84$) | **COMPLIANT**: Exceeds the **$80\%$** minimum requirement ([`Standard rev 3 §5.2`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L79-L87)). |
| **Resolution Acceptance Basis** | **Dual Acceptance** (Criteria §5.1 & §5.2) | Both criteria satisfied simultaneously. **No reviewer waiver or policy decision required**. |
| **Probe Spatial Location** | $(x,y) = \text{axis}$, $z = 0.75 D^* = 2.82\text{ m}$ | Located inside the continuous buoyant flaming core within `fireRefinementZone`. |
| **Site Meteorology Impact** | $T = 35\text{–}42^\circ\text{C}$, Elev $= 730\text{ m}$ ($92.9\text{ kPa}$) | Ideal gas coupling ($\rho_\infty T_\infty = p_\infty / R$) makes $D^*$ invariant to temperature; elevation shifts $D^*$ to $3.88\text{ m}$ ($D^*/dx = 7.75$), staying in band. |
| **Checklist Item 4 Disposition** | **Currently `[ ] OPEN`** in Report rev B | **Cannot close as-is** due to appendix relegation; **closes immediately upon editorial move** of Table 6 into Section 6 body. |

---

### Detailed Findings by Question

#### 1. Plume Resolution Index, Cell Size, Plume Length Scale, and Band Compliance
* **Reporting Result**: The six SOW §3.1 production wildfire cases rest on the fine grid (`case_fine`), as designated in Section 6.3 of [`CFDME-2025-041_Phase1_report_revB.docx`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Reports/CFDME-2025-041_Phase1_report_revB.docx#L78-L79).
* **Plume Length Scale ($D^*$)**: Calculated from $\dot{Q} = 30.1\text{ MW}$ ($30,120\text{ kW}$ based on Byram fireline intensity $I = 10,040\text{ kW/m}$ over the $3.0\text{ m}$ sub-domain flaming front segment; [`CFDME-2025-041_scoping_memo_20251008.docx §5.1`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Reports/CFDME-2025-041_scoping_memo_20251008.docx#L44-L56)). Using standard reference atmosphere ($\rho_\infty = 1.204\text{ kg/m}^3$, $c_p = 1005\text{ J/(kg}\cdot\text{K)}$, $T_\infty = 293.15\text{ K}$, $g = 9.81\text{ m/s}^2$):
  $$D^* = \left( \frac{\dot{Q}}{\rho_\infty c_p T_\infty \sqrt{g}} \right)^{2/5} = \left( \frac{30.1 \times 10^6}{1.204 \times 1005 \times 293.15 \times 3.13209} \right)^{0.4} = 3.7423\text{ m} \quad (\text{recorded as } 3.76\text{ m})$$
* **Cell Size ($dx$)**: Background cell size on `case_fine` is $dx = 0.5\text{ m}$. (Note: inside the cylindrical `fireRefinementZone`, snappyHexMesh carries two additional refinement levels, bringing the local cell size to $dx_{local} = 0.125\text{ m}$; [`log.snappyHexMesh_20251009.txt`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/logs/log.snappyHexMesh_20251009.txt#L40-L55)).
* **Resolution Index ($D^*/dx$)**: Evaluated against the background grid, $D^*/dx = 3.76\text{ m} / 0.5\text{ m} = 7.52$ (reported as $7.5$).
* **Band Compliance**: [`CFDME_QA_Verification_Standard_rev3 §5.1`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L72-L78) establishes the firm's required band as $5 \le D^*/dx \le 10$. Landing at $7.5$ satisfies this requirement with a $+50\%$ margin above the minimum threshold and a $-25\%$ buffer below the upper limit. **The band is fully met.**

#### 2. Basis of Resolution Acceptance & Reviewer Decision Scope
* **Governing Basis**: Governed by [`CFDME_QA_Verification_Standard_rev3 §5`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L69-L87), which accepts either of two criteria (both preferred, either alone acceptable):
  1. *Criterion 5.1*: $D^*/dx \in [5, 10]$ (Met: $7.5$).
  2. *Criterion 5.2*: Pope resolved-TKE fraction $k_{res} / (k_{res} + k_{sgs}) \ge 0.80$ (Met: $84\%$).
* **Dual Acceptance**: The case archive ([`three_grid_study_outputs.txt`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/verification/three_grid_study_outputs.txt#L235-L250)) explicitly demonstrates **dual compliance**, meeting both criteria simultaneously.
* **Reviewer Decision**: **Nothing about this basis requires a discretionary decision, waiver, or policy interpretation from Marguerite.** Escalation under §5 is required only when a physical constraint prevents meeting a criterion; here, both pass with positive margin. Furthermore, Marguerite previously reviewed and signed off on the $D^* = 3.76\text{ m}$ / $dx = 0.5\text{ m}$ baseline in the scoping memo on 10/08/2025 ([`scoping memo §8`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Reports/CFDME-2025-041_scoping_memo_20251008.docx#L84-L88)). Her only role is routine administrative sign-off on the checklist once the reporting format is corrected.

#### 3. Spatial Probe Location and Ambient Meteorology Sensitivity
* **Probe Location vs. Plume Region**: The resolved-energy probe is at $(x, y) = \text{plume axis}$, $z = 0.75 D^* = 2.82\text{ m}$ above the fire source ([`three_grid_study_outputs.txt`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/verification/three_grid_study_outputs.txt#L198-L200)). With Byram flame length $L = 5.4\text{ m}$ and Heskestad flame height $11.5\text{ m}$, $z = 2.82\text{ m}$ sits squarely inside the continuous buoyant flaming core and inside `fireRefinementZone` (`cellZone 0`), strictly fulfilling [`Standard rev 3 §5.2`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L84-L85) ("within the buoyancy-dominated flow, not on the periphery of the domain"). The $84\%$ resolved fraction confirms the local $0.125\text{ m}$ grid captures the energy-containing turbulent scales.
* **Ambient Meteorological Representation**: The ambient values used for $D^*$ ($20.0^\circ\text{C}$, sea level, $\rho = 1.204\text{ kg/m}^3$) **do not represent the site**. SOW §3.1 and the Pima County ALERT record ([`site_met_avra_valley_2015-2024.csv`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Data/site_met_avra_valley_2015-2024.csv)) establish site summer design temperatures of $35\text{–}42^\circ\text{C}$ at an elevation of $\sim 730\text{ m}$ ($2,400\text{ ft}$).
* **Thermodynamic Impact of Site Conditions**:
  * Substituting the ideal gas equation ($\rho_\infty T_\infty = p_\infty / R_{air}$) into the $D^*$ formulation shows that **temperature alone cancels out at constant pressure**. As air warms from $20^\circ\text{C}$ to $42^\circ\text{C}$, density decreases proportionally, leaving $\rho_\infty T_\infty$ invariant ($D^* = 3.742\text{ m}$ remains unchanged at sea level).
  * Avra Valley's $730\text{ m}$ elevation lowers barometric pressure to $p_\infty \approx 92.86\text{ kPa}$ ($\sim 8.4\%$ reduction). Because $D^* \propto (p_\infty)^{-0.4}$, lower pressure slightly increases $D^*$ from $3.74\text{ m}$ to **$3.88\text{ m}$** ($+3.5\%$).
  * On the $dx = 0.5\text{ m}$ grid, this shifts $D^*/dx$ from $7.52$ to **$7.75$** (or $7.27$ if temperature were naively evaluated with uncoupled fixed density). Under all interpretations, $D^*/dx$ remains comfortably inside the mandatory $5 \text{ to } 10$ band.

#### 4. Peer-Review Checklist Closure Status & Remediation Roadmap
* **Can Item 4 Close Today As-Is?** **NO.** In [`CFDME-2025-041_Phase1_report_revB.docx`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Reports/CFDME-2025-041_Phase1_report_revB.docx#L71-L79), Section 6 contains only Table 4 (a three-grid table resembling a RANS template) and uses an appendix pointer ("Detail of the underlying LES resolution figures on that grid is given in Appendix C"). This violates [`CFDME_QA_Verification_Standard_rev3 §3 & §6`](file:///filesystem/Firm/QA/CFDME_QA_Verification_Standard_rev3.pdf#L54-L64), which expressly forbids appendix pointers for verification evidence and bars RANS-style tables from serving as primary LES verification evidence. Marguerite's refusal to close Item 4 was procedurally correct.
* **What Settles and Closes It?** A four-step editorial update to Section 6 of Report rev B, drawing solely from existing numbers in [`three_grid_study_outputs.txt`](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/verification/three_grid_study_outputs.txt):
  1. **Move Table 6 from Appendix C into Section 6 body** as Table 5 (or Table 6.1), stating $\dot{Q} = 30.1\text{ MW}$, $D^* = 3.76\text{ m}$, $dx = 0.5\text{ m}$, $D^*/dx = 7.5$, and Pope resolved-TKE $= 84\%$ at probe $z = 0.75 D^*$.
  2. **Add the mandatory single-sentence compliance statement** per §3(d): *"The Phase 1 LES resolution is accepted per CFDME QA Verification Standard rev 3 Section 5 under both the plume resolution index (D*/dx = 7.5, satisfying the 5–10 band by a +50% margin) and the Pope resolved-TKE criterion (k_res / (k_res + k_sgs) = 84%, exceeding the 80% threshold by 4 percentage points)."*
  3. **Re-label Table 4** as a secondary "Mesh Sensitivity Study," noting per Section 4 that GCI does not apply to LES because the resolved-to-modeled split changes with the mesh.
  4. **Present the updated Section 6 to Marguerite**; confirming the metrics are in the body allows her to mark Item 4 as `[X] CLOSED` on [`CFDME-2025-041_peer_review_checklist.docx`](file:///filesystem/Firm/QA/Reviews/CFDME-2025-041_peer_review_checklist.docx#L44-L45).

---

### Deliverable Verification
* **File Path**: [`/filesystem/CFDME-2025-041_resolution_note_revA.docx`](file:///filesystem/CFDME-2025-041_resolution_note_revA.docx)
* **File Integrity**: Verified non-empty ($49,307\text{ bytes}$), 79 paragraphs, 6 formatted tables, 20 structural headings.
* **Accessibility**: Passed with **0 errors and 0 warnings** via `mcp_apps_word_v2_check_accessibility`.
* **Standard of Care**: Incorporates the mandatory firm stamp block (*"CFD thermal analysis only. Fire-resistance rating certified separately by others."*), full SI unit compliance per [`CFDME_Units_SOP_rev2`](file:///filesystem/Firm/Standards/CFDME_Units_SOP_rev2.pdf), complete mathematical audit derivations, and PE signature blocks for Gordon Selby, PE (#48213) and Marguerite Falk, PE (#42798).