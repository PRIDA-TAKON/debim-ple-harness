### Executive Engineering Summary

**Project:** Cattail Run Data Campus — Phase 1 Foundation Package (`AV-CR-2604`)  
**Client:** Ardent Vale Infrastructure LLC  
**Jurisdiction:** Loudoun County, Virginia  
**Deliverable Archive:** `/filesystem/dc_structural__foundation_strategy__blind/output/submission.zip`

---

### Key Verified Results & Campus Strategy

1. **Campus Optimization Programme & Rig Allocation:**
   - **Improved Spread Footings over Rammed Aggregate Piers (4 Pads):** `CR-P1`, `CR-P2`, `CR-P4`, and `CR-P6`.
   - **Shallow Spread Footings Alone (2 Pads):** `CR-P3` and `CR-P5`.
   - **Rig Mobilisation:** Exactly **2 rigs mobilised** ($80,000 lump sum). Each rig serves at most 2 pads within the milestone window per Kettleridge terms:
     - **Rig 1:** Serves `CR-P1` and `CR-P2`.
     - **Rig 2:** Serves `CR-P4` and `CR-P6`.
   - **Verification Testing:** 1 production modulus test per improved pad ($9,500/EA, 4 tests total = $38,000).
   - **Campus Total Foundation Cost:** **$417,335.12** (including $80,000 rig mobilisation, concrete, reinforcement, excavation, backfill, aggregate piers, geosynthetic platform, and modulus tests).

2. **Frost Depth & Governing Climate Normals:**
   - Governing cooperative station USC00444909 (Lincoln, VA): Current 1981–2010 NOAA NCEI normals yield a 100-year Air-Freezing Index of **556 °F-days** (exceeding the Loudoun County AHJ Amendment 3 threshold of 500 °F-days). The 1951–1980 product (416 °F-days) was set aside per RFI-007.
   - Governing foundation bearing depth: **$D_f = 42\text{ in} = 3.50\text{ ft}$** below finished grade campus-wide in Stratum I residual soils.
   - Piezometer groundwater depths range from 8.0 ft to 21.0 ft ($> D_f$), resulting in **0 construction dewatering days**.

3. **Geotechnical Capacity & Tolerable Movement:**
   - **Bearing Capacity:** Evaluated using UFC 3-220-20 Section 5-3 general bearing capacity formulation with Brinch Hansen factors ($N_c = 22.25, N_q = 11.85, N_\gamma = 7.94$) and groundwater corrections. Required factors of safety per UFC 3-220-01 Table 2-3:
     - `CR-P1`, `CR-P2`, `CR-P3`, `CR-P6`: $\text{FS} = 3.5$ (Light Industrial, Public)
     - `CR-P4`: $\text{FS} = 3.0$ (Apartments, Office)
     - `CR-P5`: $\text{FS} = 2.5$ (Warehouse)
   - **Total Settlement:** Discretised layered elastic compression (0.25 ft increments to $\max(4B, 40\text{ ft})$, 2:1 stress distribution). All 36 foundations achieve $s_{tot} \le 1.0\text{ inch}$.
   - **Angular Distortion:** Adjacent unit differential settlements strictly comply with the UFC 3-220-01 limit: $\Delta s / \text{span} \le 1/500 = 0.0020\text{ rad}$ across all spans (including the critical 5.0 ft span between F5 and W1).

4. **Concrete Durability & Material Assignments:**
   - Measured water-soluble sulfate concentrations per GDR Rev 2 assign exposure classes per EM 1110-2-2000 Table 2-2 and UFGS 03 30 00:
     - `CR-P1` (0.14% $\text{SO}_4$, S1): $f'_c = 4000\text{ psi}$, $\max w/cm = 0.50$ ($196/CY)
     - `CR-P2` (0.23% $\text{SO}_4$, S2): $f'_c = 4500\text{ psi}$, $\max w/cm = 0.45$ ($211/CY)
     - `CR-P3` (0.07% $\text{SO}_4$, S0): $f'_c = 4000\text{ psi}$, $\max w/cm = 0.50$ ($196/CY)
     - `CR-P4` (0.11% $\text{SO}_4$, S1): $f'_c = 4000\text{ psi}$, $\max w/cm = 0.50$ ($196/CY)
     - `CR-P5` (0.05% $\text{SO}_4$, S0, but exterior loading apron F3 freeze-thaw): $f'_c = 5000\text{ psi}$, $\max w/cm = 0.40$ ($228/CY)
     - `CR-P6` (0.26% $\text{SO}_4$, S2): $f'_c = 4500\text{ psi}$, $\max w/cm = 0.45$ ($211/CY)

5. **Shear-Wall Footing (W1) Stability:**
   - Overturning eccentricity under service load: $e = 6.94\text{ in}$ to $7.52\text{ in} \le L/6 = 48.0\text{ in}$ (well within middle third).
   - Net uplift factor of safety under lateral wind: $\text{FS}_{uplift} \ge 3.00 \ge 1.50$.
   - Sliding factor of safety: $\text{FS}_{sliding} \ge 2.69 \ge 2.00$ ($\delta = \frac{2}{3}\phi = 17.33^\circ$, passive earth pressure halved).

---

### Deliverables Verified Inside `output/submission.zip`

The final archive contains exactly the six required files at the root:

| Deliverable File | Format / Template | Verification Status |
| :--- | :--- | :--- |
| **`foundation_geometry.json`** | UTF-8 JSON (BIM Standard Rev 2) | Conforms to schema; all 36 foundations populated; dimensions in 3-in increments; zero `null`s; W1 stability parameters included. |
| **`ground_improvement_plan.json`** | UTF-8 JSON (BIM Standard Rev 2) | 2 rigs assigned; 4 improved pads; $n_s = 10.0$; pier dia 30 in; pad depths and linear feet match geometry. |
| **`foundation_schedule.xlsx`** | Owner Excel Template | Exactly 36 rows; 19 columns matching template headers; 100% numerical consistency with geometry JSON. |
| **`foundation_feasibility_matrix.md`** | Markdown Table & Narrative | Complete pad-by-pad demand, bearing check, settlement, W1 stability, and cost comparison for both alternatives. |
| **`constraint_register.xlsx`** | Owner Excel Template | 72 substantive rows ($\le 96$ limit); governing clauses cited; cancelled/superseded documents marked as set aside. |
| **`design_basis.md`** | Fenced JSON block + Narrative | Valid JSON header; comprehensive narrative addressing governing criteria, analysis methods, and mobilisation rationale. |