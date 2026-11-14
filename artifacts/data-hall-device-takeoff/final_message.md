### Engineering Deliverables & QA/QC Audit Summary

**Deliverable Archive:** [`output/submission.zip`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/submission.zip)  
**Project:** Meridian Data Center — Phase 1, Data Hall 1 (`ec_0205_d100`)  
**Priced Basket Total:** **`$15,615.87`** (Re-priced sum of attribution extended prices)  
**Total Purchased Value:** **`$17,980.45`** (Including Owner's 5% spare stock and whole carton rounding)  

---

### 1. Key Verified Results

#### Device Census & Takeoff Summary (193 Total Units)
*Exact integer derivation per conventions C1–C9; zero tolerance applied.*

| Type Mark | Scheduled Description | Count | Governing Basis / Sheets |
|:---|:---|---:|:---|
| **`R1`** | RECEPTACLE, DUPLEX, 20 A, 125 V, WALL-MOUNTED | **38** | [E-201](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-201_power_and_device_plan_1.png) (7), [E-202](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-202_power_and_device_plan_2.png) (10), [E-203](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-203_power_and_device_plan_3.png) (2), [E-204](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-204_power_and_device_plan_4.png) (0), [E-231](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-231_enlarged_electrical_plans.png) (9), [E-232](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-232_enlarged_electrical_plans.png) (6), [E-233](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-233_enlarged_electrical_plans.png) (4) |
| **`R2`** | RECEPTACLE, QUADRAPLEX, 20 A, 125 V, WALL-MOUNTED | **8** | E-201 (2 added via [ADD-02](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/addenda/ADD-02_addendum_two.md)), E-232 (3), E-233 (3) |
| **`R3`** | RECEPTACLE, DUPLEX, GFCI, 20 A | **8** | E-231 (3), E-232 (3), E-233 (2) |
| **`R4`** | RECEPTACLE, DUPLEX, ISOLATED GROUND, 20 A, 125 V | **6** | E-202 (4), E-233 (2) |
| **`R5`** | RECEPTACLE, DUPLEX, WEATHER-RESISTANT | **8** | E-201 (4 drawn), E-202 (4 via Keynote <2> at CRAH-01..04) |
| **`R6`** | RECEPTACLE, DUPLEX, EMERGENCY BRANCH, 20 A, 125 V | **4** | E-201 (1), E-203 (1), E-231 (1), E-233 (1) |
| **`R7`** | BOX, OUTLET, FLOOR, TWO-GANG, IN ACCESS FLOOR | **6** | E-232 (3 via Keynote <3>), E-233 (3 via Keynote <3> at PDUs) |
| **`R8`** | RECEPTACLE, SINGLE, 50 A, 250 V, WALL-MOUNTED | **0** | Legend entry with zero instances across set (C4 / E-03) |
| **`J1`** | BOX, JUNCTION, 100 MM SQUARE, CONCEALED | **32** | E-201 (11), E-202 (7), E-203 (7), E-204 (2), E-231 (4), E-232 (1) |
| **`P1`** | BOX, PULL, 300 X 300 X 150 MM, SURFACE | **6** | E-201 (1), E-202 (1), E-203 (1), E-231 (1), E-232 (1), E-233 (1) |
| **`F1`** | APPLIANCE, NOTIFICATION, VISIBLE, WALL-MOUNTED | **12** | [E-211](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-211_fire_alarm_device_plan.png) (8 via Keynote <1> exterior walls; 4 via Keynote <4> exit doors) |
| **`F2`** | APPLIANCE, NOTIFICATION, AUDIBLE-VISIBLE, WALL | **4** | E-211 (1), E-231 (2), E-233 (1) |
| **`F3`** | STATION, MANUAL, FIRE ALARM, WALL-MOUNTED | **3** | E-211 (2), E-233 (1) |
| **`F4`** | DETECTOR, SMOKE, PHOTOELECTRIC, CEILING | **6** | E-211 (6) |
| **`F5`** | DETECTOR, SMOKE, PHOTOELECTRIC, ACCESS FLOOR | **25** | E-211 (25 in 5x5 grid) |
| **`F6`** | DETECTOR, SMOKE, PROJECTED BEAM, WALL | **0** | Legend entry with zero instances across set (C4 / E-03) |
| **`D1`** | DETECTOR, SMOKE, DUCT, FURNISHED UNDER DIV 23 | **27** | E-211 (25 supply ducts), E-231 (1), E-232 (1) |
| **TOTAL** | | **193** | |

---

### 2. Engineering Basis & Method of Compliance

1. **Hierarchy of Truth & Governing Addenda (C6 / E-07):**
   - [ADD-02](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/addenda/ADD-02_addendum_two.md) (2026-08-07) postdates all drawing Rev 2 issues (2026-07-27). In Bay A1 on E-201, 3 duplex receptacles (`R1`) were deleted; the first two from the south were replaced with quadraplex receptacles (`R2`), the third deleted without replacement, and junction boxes (`J1`) retained.
2. **Match Lines & Enlarged Plan Boundaries (C1, C7 / E-05, E-08):**
   - Devices crossing quadrant match lines (Grid Line 2 and Grid Line B) were counted strictly on their home quadrant plan; far-side depictions were treated as reference only (General Note 2).
   - Electrical Entry and PDU Gallery zones cross-referenced to enlarged views were counted exclusively from [E-231](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-231_enlarged_electrical_plans.png), [E-232](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-232_enlarged_electrical_plans.png), and [E-233](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-233_enlarged_electrical_plans.png) (General Note 4).
3. **Condition Assignment Precedence (C8 / E-11):**
   - *Tier 1 Precedence ([E-002](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/E-002_device_and_mounting_schedule.md)):* `EMERGENCY` branch for `R6` (4 units); `IG` for `R4` (6 units); `ACCESS-FLOOR` for `R7` (6 units) and `F5` (25 units); `CEILING` for `F4` (6 units) and `D1` (27 units).
   - *Tier 2 Precedence ([A-102](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/drawings/A-102_partition_and_finish_plan.png)):* `DAMP` hatch for CRAH condensate aprons (`R5`, 8 units).
   - *Tier 3 Precedence (Wall Centerline):* P1 = `DRY-STUD` (124 units), P2 = `DRY-MASONRY` (11 units), P3 = `RATED-2HR` (25 units).
   - *While-in-Use Hood Directive:* Per task instruction, while-in-use hoods are noted in `basis.md` but carry no bill line item as none exist in the catalogue.
4. **Assembly Specification & Pricing Band Alignment (E-12, E-18–E-21):**
   - Division 26 05 33, 26 20 00, 28 31 76, and 07 84 00 specifications were cross-referenced with [`device_catalogue_2026.md`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/product_data/device_catalogue_2026.md).
   - All 25 fire-rated boxes in partition P3 include listed intumescent pads (`ACC-FIRESTOP-PAD`), qualifying for Price Band 2 (24–199) at **$94.06/EA**.
   - Duct detectors (`D1`) carry installation labor only (`INS-DUCT-DET`) with zero material cost per Spec 28 31 76 para 1.3.
   - Owner's 5% spare stock was applied and rounded up to the nearest whole carton per [`price_list_2026Q2.md`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/product_data/price_list_2026Q2.md).
5. **Unresolved Symbols Audit (E-04, E-04b):**
   - Confirmed zero (0) unscheduled symbols exist across all drawing sheets; every plan instance mapped to scheduled legend marks.

---

### 3. Deliverables Generated & Verified

The following files were generated directly in [`output/`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/) and archived into [`output/submission.zip`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/submission.zip):
- [`takeoff.csv`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/takeoff.csv): 17 rows (one per scheduled mark, exact descriptions and integer counts).
- [`locations.csv`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/locations.csv): 119 rows aggregated by structural grid bay (`sheet, type_mark, grid_bay, condition, count`).
- [`bom.csv`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/bom.csv): 68 attribution rows (Basket Total: **`$15,615.87`**) and 18 purchase rows with `(PURCHASE)` and `(STOCK)` (Purchase Total: **`$17,980.45`**).
- [`register.csv`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/register.csv): 23 rows covering every criteria clause E-01 through E-22 (including E-04b) with source citations and compliance mechanisms.
- [`basis.md`](file:///filesystem/final_batch4__electrical_task17_ec_0205_d100__blind/output/basis.md): Comprehensive engineering narrative documenting conventions C1–C9, governing issues, condition matrix, code citations, spare-stock/carton arithmetic, and zero-unresolved audit.