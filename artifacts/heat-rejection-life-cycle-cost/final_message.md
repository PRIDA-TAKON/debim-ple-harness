# Condenser Water Heat Rejection Replacement — Papago Federal Center, Phoenix, Arizona
**95% Construction Documents QA/QC Engineering Audit & Final Deliverables**
**Mechanical Engineer of Record / Plant Designer**

---

### Executive Deliverable Notice
The complete deliverable package has been compiled, rigorously verified against all project standards and deliverable schemas, and packaged into the required archive at:
`/filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/submission.zip`

The archive contains all eight required project deliverables:
1. [`CT_SCHEDULE_CUP.dxf`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/CT_SCHEDULE_CUP.dxf) — Courthouse Central Utility Plant schedule sheet and roof layout.
2. [`CT_SCHEDULE_ANNEX.dxf`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/CT_SCHEDULE_ANNEX.dxf) — Data Annex Plant schedule sheet and roof layout.
3. [`CT_SCHEDULE_LAB.dxf`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/CT_SCHEDULE_LAB.dxf) — Laboratory Wing Plant schedule sheet and roof layout.
4. [`CT_CALC_CUP.xlsx`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/CT_CALC_CUP.xlsx) — Courthouse Central Utility Plant 5-sheet engineering calculation workbook.
5. [`CT_CALC_ANNEX.xlsx`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/CT_CALC_ANNEX.xlsx) — Data Annex Plant 5-sheet engineering calculation workbook.
6. [`CT_CALC_LAB.xlsx`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/CT_CALC_LAB.xlsx) — Laboratory Wing Plant 5-sheet engineering calculation workbook.
7. [`constraint_register.csv`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/constraint_register.csv) — 55 verified project requirements across 28 constraint families, citing only active governing authorities.
8. [`design_basis.md`](file:///filesystem/final_batch4__mechanical_task3_ct_heat_lcc__blind/output/design_basis.md) — Comprehensive technical design basis, conflict reconciliations, and margin audit.

---

### Key Verified Results & Selections

| Plant | Selected Configuration | Design Flow & Setpoints | Max Allowable COC | Peak Electrical Demand | Annual Makeup vs. Allocation | Life-Cycle Net Savings | Governing Constraint & Margin |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **CUP** | **4 $\times$ CTX-0600-S**<br>SS-304 / DE-2 / Premium Eff | **1,800.0 gpm** (450 gpm/cell)<br>$CWS_{min}=65.0$ °F, Offset $=12.0$ °F<br>Sched $CWS=86.0$ °F, Range $=13.0$ °F | **4.14**<br>(PSI $\ge 5.60$ at $CWR=98.02$ °F) | **508.84 kW**<br>(Spare: 528.0 kW) | **8,100.2 kgal/yr**<br>(Alloc: 10,300.0 kgal) | **$279,819.15**<br>(LCC: $5,683,849.89) | `structural capacity`<br>(relative margin **0.0250**) |
| **ANNEX** | **4 $\times$ CTX-0600-S**<br>SS-304 / DE-2 / Premium Eff | **1,800.0 gpm** (450 gpm/cell)<br>$CWS_{min}=75.0$ °F, Offset $=11.0$ °F<br>Sched $CWS=86.0$ °F, Range $=14.0$ °F | **4.00**<br>(PSI $\ge 5.60$ at $CWR=99.38$ °F) | **559.58 kW**<br>(Spare: 590.0 kW) | **11,705.1 kgal/yr**<br>(Alloc: 12,600.0 kgal) | **$310,882.10**<br>(LCC: $7,791,697.78) | `tower capability`<br>(relative margin **0.0510**) |
| **LAB** | **3 $\times$ CTX-0900-S**<br>SS-304 / DE-2 / Premium Eff | **2,130.0 gpm** (710 gpm/cell)<br>$CWS_{min}=65.0$ °F, Offset $=9.5$ °F<br>Sched $CWS=87.0$ °F, Range $=14.0$ °F | **3.93**<br>(PSI $\ge 5.60$ at $CWR=100.05$ °F) | **640.98 kW**<br>(Spare: 641.14 kW) | **15,085.6 kgal/yr**<br>(Alloc: 17,400.0 kgal) | **$299,608.80**<br>(LCC: $7,957,532.74) | `electrical capacity`<br>(relative margin **0.0003**) |
| **Campus** | **11 Cells Total** | — | — | — | **34,890.9 kgal/yr** | **$890,310.05** | — |

---

### Core Engineering Basis & Quality Control Audit Trail

1. **Hierarchy of Truth & Governing Authorities (Conflict Reconciliation)**:
   * `CONFLICT 1: ADOPTED UFC 3-410-01 paragraph 2-4.2.4 | SET ASIDE GSA PBS-P100 paragraph 5.3.1`  
     *Basis*: DC-02 paragraph 2 assigns outdoor design conditions to UFC 3-410-01. UFC 3-410-01 paragraph 2-4.2.4 dictates tower sizing based on the 1.0% annual wet bulb plus a mandatory +5.0 °F safety adder. Station analysis of Phoenix Sky Harbor Airport LCD (2022–2024, mean pressure 28.7221 inHg / 97,264 Pa) establishes the 1.0% Twb as 75.0 °F, yielding a governing **80.0 °F design wet bulb**, and 0.4% Twb of 76.0 °F yielding an **81.0 °F redundancy wet bulb**. Winter 99.6% dry bulb is 41.0 °F (> 32 °F freeze threshold; no basin heater required).
   * `CONFLICT 2: ADOPTED UFM 3-230-13 5 February 2026 | SET ASIDE UFC 3-230-13 2023`  
     *Basis*: UFM 3-230-13 cancels and supersedes UFC 3-230-13 (2023). Governs water treatment, silica limits (150 ppm circulating ceiling), and Practical (Puckorius) Scaling Index closed-form equations ($pH_{eq} = 1.485 \log_{10}(TA) + 4.54$).
   * `CONFLICT 3: ADOPTED M-401 Revision C | SET ASIDE M-401 Revision B`  
     *Basis*: Revision C fixes heat rejection equipment zones and architectural outdoor air intake positions, superseding Revision B.

2. **Electrical Infrastructure & Motor Control Centers**:
   * Spare capacity verified against panel schedule E-601 Rev C: MCC-R1 = 528.0 kW; MCC-R2 = 590.0 kW; MCC-R3 = 660.0 kW less 18.86 kW for dedicated laboratory exhaust fans EF-L1/L2/L3 (per RFI-034 response) = **641.1373 kW**.
   * Peak coincident demand across all 180 scenario bins (8,760 hours) strictly complies with available bus capacity without service upgrades. On LAB, electrical capacity binds with a relative margin of 0.0003 (PCD = 640.975 kW vs. 641.1373 kW limit).

3. **Water Chemistry, Purveyor Allocations & Sewer Discharge**:
   * Evaluated under the **SATURATED-EXIT** formulation adopting the moist-air energy and mass balance of the project's reference simulation engine.
   * Controlling cycles of concentration are bound by the Puckorius Scaling Index (PSI $\ge 5.60$) evaluated at the achieved design CWR temperature for each plant.
   * Annual makeup is well within allocations (PW-LTR-014 and PW-LTR-019 Amendment 1: ANNEX = 12,600 kgal/yr; CUP = 10,300 kgal/yr; LAB = 17,400 kgal/yr). Peak day makeup and blowdown sewer discharges strictly comply with municipal discharge limits.

4. **Structural Framing & Roof Clearances**:
   * Support frame dimensions and operating weights verified against S-401 Rev C framing zones:
     * CUP: CTX-0600-S (117.0 psf) bears in CUP-S1 (126 psf) and CUP-S2 (120 psf), yielding governing structural margin of 0.0250.
     * ANNEX: CTX-0600-S (117.0 psf) bears in ANNEX-S1 (128 psf) and ANNEX-S2 (124 psf).
     * LAB: CTX-0900-S (116.67 psf) bears entirely within LAB-S1 (126 psf, ending at $X=70.0$ ft prior to the $X=74.0$ ft zone boundary).
   * All cells provide $\ge 6.0$ ft inlet face clearances and $\ge 25.0$ ft separation from outdoor air intakes (CUP = 34 ft, ANNEX = 36 ft, LAB = 42 ft).

5. **Life-Cycle Economics & Net Savings Optimization**:
   * Calculated in constant 1 October 2025 dollars over a 26-year study period (1-year construction + 25-year service period) at the 3.0% DOE real discount rate.
   * Discount factors: $UPV^*_{elec} = 15.335223$, $UPV_{nonfuel} = 16.905969$, $UPV^*_{water} = 21.777005$.
   * Option SS-304 (Type 304 stainless steel basin and casing) yields a 25-year service life, eliminating replacement costs and salvage residual, producing maximum life-cycle net savings totaling **$890,310.05** across the campus.