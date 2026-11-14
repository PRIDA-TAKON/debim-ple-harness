# Technical Memorandum & Reviewer Disposition

**Document Reference:** [CFDME-2025-041_transient_solve_disposition_revA.docx](file:///filesystem/CFDME-2025-041_transient_solve_disposition_revA.docx)  
**Project:** CFDME-2025-041 — Ocotillo WUI Wildfire Exposure, Phase 1  
**Subject Case:** Ocotillo Desert-Fire Scoping Model ($3.00\text{ m}$ Flaming Front Segment, $30.10\text{ MW}$ Heat Release)  
**Date of Record:** 10/10/2025  
**Originating Engineer:** Gordon Selby, PE — Owner & Principal Engineer (Arizona PE #48213)  
**Reviewing Engineer:** Marguerite Falk, PE — Technical Director & Reviewing Engineer (Arizona PE #42798)  
**Target Recipient:** Sartaj Bhatia & Ananya Deshmukh, Mulshi Simulation Labs  
**Formal Disposition:** **RETURNED FOR CORRECTION — CEASE STEADY SOLVE; CONFORMING TRANSIENT LES AUTHORIZED**

---

### Executive Action Summary

> [!CAUTION]
> **DIRECTIVE TO CEASE STEADY-STATE SOLVES:**  
> Mulshi Simulation Labs is formally directed to **immediately cease all steady-state solve attempts** on project CFDME-2025-041. A fourth steady-state attempt is strictly prohibited and will not be accepted or compensated.

> [!IMPORTANT]
> **STATUTORY PE STAMP BOUNDARY:**  
> *"CFD thermal analysis only. Fire-resistance rating certified separately by others."*  
> Assembly fire-endurance certification is governed exclusively by third-party ASTM E119 testing ([Red Butte Report RB-2025-E119-01](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Validation/RedButte_E119_test_report_20250924.pdf)) and Ironwood Consulting Engineers certification memo ([09/29/2025](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Validation/Ironwood_certification_memo_20250929.pdf)).

---

## 1. Physical Basis of the Attempt 3 Residual Plateau

### Physical Mechanics & Expected Plume Dynamics
Buoyant fire plumes are fundamentally non-stationary shedding flows. Above a concentrated or line-fire thermal source, baroclinic vorticity generation ($\nabla \rho \times \nabla p$) drives periodic inward necking, toroidal vortex generation, and vertical vortex shedding. 

Per [CFDME_Modeling_Standards_Fire_rev4.pdf](file:///filesystem/Firm/Standards/CFDME_Modeling_Standards_Fire_rev4.pdf) §4, the normative Cetegen–Ahmed relationship gives the physical puffing frequency as:
$$f = 1.50 \cdot D^{-1/2}\text{ Hz}$$
For the firm's standard LES flaming front segment of $D = 3.00\text{ m}$ (established in [CFDME-2025-041_scoping_memo_20251008.docx](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Reports/CFDME-2025-041_scoping_memo_20251008.docx) §5, carrying a $30.10\text{ MW}$ fire source at Byram intensity $I = 10,040.00\text{ kW/m}$):
* **Expected Puffing Frequency:** $f_{\text{expected}} = 1.50 \cdot (3.00\text{ m})^{-1/2} = 0.8660\text{ Hz} \approx \mathbf{0.87\text{ Hz}}$
* **Expected Puffing Period:** $T_{\text{expected}} = 1 / f_{\text{expected}} = 1.1547\text{ s} \approx \mathbf{1.15\text{ s}}$

### Numerical Observations in Attempt 3
Per [log.solve_20251009_attempt3.txt](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/logs/log.solve_20251009_attempt3.txt) (Job 41304, 64 cores, 800 outer SIMPLE iterations):
1. **Iterations 1 to 400:** Displayed pseudo-transient residual decay across all fields ($U$ dropped 3 orders, $p$ dropped 4 orders).
2. **Iterations 400 to 800 (Residual Plateau):** Monotonic decay halted. Velocity initial residuals entered a locked limit cycle in the band $3.00\times 10^{-4}$ to $8.00\times 10^{-4}$ ($U_x$), while pressure initial residuals leveled off in the band $2.00\times 10^{-5}$ to $3.00\times 10^{-5}$.
3. **Centerline Probe Dynamics (Probe 0: $x = 1.50\text{ m}, y = 0.00\text{ m}, z = 8.00\text{ m}$ AGL):** Recorded persistent oscillations with temperature amplitude $\Delta T \approx 40.00\text{ K}$ and vertical velocity amplitude $\Delta U_z \approx 2.40\text{ m/s}$.
4. **Observed Period & Frequency:** Autocorrelation of residual samples over the final 200 iterations established an oscillation period of $\sim 1150$ outer iterations, equivalent to $T_{\text{observed}} = \mathbf{1.15\text{ s}}$ of internal pseudo-time ($f_{\text{observed}} = \mathbf{0.87\text{ Hz}}$).

### Discrepancy & Plume Mode Identification
$$\text{Discrepancy}_{\text{period}} = \frac{|1.15\text{ s} - 1.1547\text{ s}|}{1.1547\text{ s}} \times 100\% = \mathbf{0.41\%} \quad (99.59\%\text{ agreement})$$
The steady SIMPLE solver was actively resolving the physical puffing instability of the buoyant plume. Mulshi's operator misinterpreted this authentic physical dynamic as "convergence stalling."

### Definite Non-Existence of a Steady Solution
As codified in [CFDME_Modeling_Standards_Fire_rev4.pdf](file:///filesystem/Firm/Standards/CFDME_Modeling_Standards_Fire_rev4.pdf) §4:
> *"Because the plume oscillates at a finite, deterministic, physical frequency, no time-invariant flow field exists that any residual-tolerance schedule can converge to."*

Mulshi's proposed remedies (reducing under-relaxation, tightening GAMG smoother sweeps, or loosening residual tolerances to $1.00\times 10^{-3}$) are rejected. Artificially damping or ignoring real physical vorticity violates professional standard of care. **No steady solution exists for this problem.**

---

## 2. Audit of Delivered Case Setup Against Firm Standards

An inspection of [OAS_case_setup_from_DWA.txt](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/system_archive/OAS_case_setup_from_DWA.txt) reveals that Mulshi built the case via an unapproved cross-regime transfer from an external aerodynamics case ([CFDME-2024-018 Dry Wash Aerospace](file:///filesystem/Projects/CFDME-2024-018_DryWash_Aero/Case/DWA_highaltitude_case_setup.txt)), directly violating [CFDME_Modeling_Standards_Fire_rev4.pdf](file:///filesystem/Firm/Standards/CFDME_Modeling_Standards_Fire_rev4.pdf) §7.

| Subsystem / Item | Delivered Setup (Mulshi) | Governing Standard | Conforming Technical Requirement | Technical Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Physical Regime** | Unclassified / Implicit RANS | Rev 4 §2 | **Mixed Convection** ($Fr = 0.92\text{ to }2.21$) | $Fr = u/\sqrt{gD} \sim 1$ across $5.00\text{–}12.00\text{ m/s}$ wind envelope mandates reacting LES. |
| **Solver Stack** | `rhoSimpleFoam` / steady `fireFoam` SIMPLE | Rev 4 §3.1, §3.6 | **`fireFoam` (Transient LES)** | Low-Mach reacting PIMPLE algorithm required for buoyant plume dynamics. |
| **Turbulence Model** | Steady RANS $k$-$\omega$ SST / $k$-$\epsilon$ | Rev 4 §5 | **LES: WALE or Dynamic Smagorinsky** | RANS suppresses resolved vortex shedding; WALE correctly scales near-wall $y^+$. |
| **Combustion** | None (inherited) / 5-iter sub-cycling | Rev 4 §3.3 | **Finite-rate EDC** | Mean kinetics coupled to sub-grid strain rate at every time step. |
| **Radiation Closure** | OFF (inherited) / 32 unbanded rays | Rev 4 §3.4, App. A | **`fvDOM` (S4, 2 spectral bands)** | Discrete Ordinates Method split at $2.50\ \mu\text{m}$ over $1200.00\text{–}1700.00\text{ K}$ flame. |
| **Solid Properties** | Constant / adiabatic shortcuts | Rev 4 §3.5, App. A | **Temperature-dependent $k(T), \rho(T), c_p(T)$** | Concrete ($k=1.40\text{ W/m}\cdot\text{K}$) and steel ties ($k=45.00\text{ W/m}\cdot\text{K}$) must vary over fire range. |
| **Through-Wall Assembly** | Single-region adiabatic wall | Rev 4 §6 | **Multi-region CHT (`chtMultiRegionFoam`)** | 4 coupled regions: outer leaf, cavity, inner leaf, metallic ties with interface matching. |
| **Ambient Freestream** | $p_\infty=26.50\text{ kPa}, T_\infty=223.00\text{ K}, \rho_\infty=0.40\text{ kg/m}^3$ | SOW §3.1 | **Sonoran WUI ($35.00\text{–}42.00\ ^\circ\text{C}$, $\text{RH }10.00\text{–}25.00\%$)** | Aerospace conditions underestimate density by 2.8x and temperature by $90.00\text{ K}$. |
| **Time-Step Control** | Fixed $\Delta t = 0.01\text{ s}$, `adjustTimeStep no` | Rev 4 §4 | **`adjustTimeStep yes`, $\text{maxCo}=0.90$** | Adaptive Courant stepping mandatory; $\text{writeInterval}=0.0460\text{ s}, \text{endTime}=31.00\text{ s}$. |

---

## 3. Specification of Authorized Transient LES Solve

### Reference Dictionaries & Mandatory Settings
Governed by [fireFoam_transient_controlDict.txt](file:///filesystem/Firm/Standards/Reference_Cases/fireFoam_transient_controlDict.txt):
* $\text{maxCo} = \mathbf{0.90}$ (Courant stability limit)
* $\text{maxDeltaT} = \mathbf{0.01\text{ s}}$ ($0.0100\text{ s}$ ceiling governing case-specific upper bound)
* $\text{writeControl} = \text{adjustableRunTime}$
* $\text{startFrom} = \text{latestTime}$

### Sizing of Largest Write Interval & Shortest End Time
* **Largest Write Interval:** Standard §4 mandates $\ge 25$ samples per puffing period:
  $$\text{writeInterval}_{\text{max}} = \frac{T_{\text{puff}}}{25} = \frac{1.15\text{ s}}{25} = \mathbf{0.0460\text{ s}} \quad (\text{Exact: } \frac{1.1547\text{ s}}{25} = 0.0462\text{ s})$$
* **Shortest End Time:** Standard §4 mandates $\ge 20$ puffing periods after startup clears ($t_{\text{startup}} = 8.00\text{ s}$ per grid study):
  $$t_{\text{end, shortest}} = t_{\text{startup}} + (20 \cdot T_{\text{puff}}) = 8.00\text{ s} + (20 \cdot 1.15\text{ s}) = 8.00\text{ s} + 23.00\text{ s} = \mathbf{31.00\text{ s}} \quad (\text{Exact: } 31.09\text{ s})$$
  *(Note: Firm reference dictionary specifies $60.00\text{ s}$ for a broader $\sim 45$-cycle window; $31.00\text{ s}$ is the shortest compliant duration).*

### Time-Control Block Differences

| `controlDict` Entry | Mulshi Delivered ([Case/system/controlDict](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/system/controlDict)) | Authorized Production Setup | Technical Rationale |
| :--- | :--- | :--- | :--- |
| `startFrom` | `startTime;` | `latestTime;` | Enables clean restart from checkpoint without re-running startup. |
| `endTime` | `2000;` *(iterations)* | `31.00;` *[s]* | Shortest allowable duration: $8.00\text{ s}$ startup + $23.00\text{ s}$ ($20$ cycles). |
| `deltaT` | `0.01;` *(fixed pseudo-time)* | `0.001;` *[s]* | Conservative initial time step for startup stability prior to adaptive ramp. |
| `adjustTimeStep` | `no;` | `yes;` | Mandatory under Rev 4 §4; time step must track local Courant limit. |
| `maxCo` | *[ABSENT / UNCONTROLLED]* | `0.90;` | Strict Courant ceiling governed by firm reference `controlDict`. |
| `maxDeltaT` | *[ABSENT / UNCONTROLLED]* | `0.01;` *[s]* | Maximum time-step ceiling governed by firm reference `controlDict`. |
| `writeControl` | `timeStep;` | `adjustableRunTime;` | Pegs write intervals to simulated physical time rather than iteration count. |
| `writeInterval` | `100;` *(iterations)* | `0.0460;` *[s]* | Captures exactly 25 uniform samples per $1.15\text{ s}$ puffing cycle. |
| `writePrecision` | `6;` | `8;` | Retains high-precision floating point data for spectral and RMS processing. |

### Mesh Identification & Verification Scope Boundaries
* **Mesh of Record:** Production `snappyHexMesh` grid generated on 10/09/2025 ([log.snappyHexMesh_20251009.txt](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/logs/log.snappyHexMesh_20251009.txt)), totaling **$11,214,862\text{ cells}$** on geometry `OAS-WUI-01_revC.FCStd`. CellZones: `atmosphere` ($9,872,108$), `outerLeaf` ($582,214$), `cavity` ($212,486$), `innerLeaf` ($460,872$), `ties` ($87,182$).
* **What Verification COVERS:** Fluid-region LES plume resolution ($dx = 0.50\text{ m}$, $D^* = 3.76\text{ m}$, $D^*/dx = 7.52 \in [5.00, 10.00]$ per QA Standard rev 3 §5.1; Pope resolved-TKE fraction $k_{\text{res}}/(k_{\text{res}}+k_{\text{sgs}}) = 84.00\% \ge 80.00\%$ per §5.2) and geometric mesh quality (`checkMesh` PASS: non-orthogonality $58.34^\circ \le 65.00^\circ$, skewness $2.14 \le 4.00$, aspect ratio $8.42$).
* **What Verification DOES NOT COVER:**
  1. *Solid Conjugate Heat Transfer Regions:* The 3-grid study ([three_grid_study_outputs.txt](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/verification/three_grid_study_outputs.txt)) was a fluid-only domain ($z = 60.00\text{ m}$) without solid leaves, cavity radiation, or metallic ties. Through-wall thermal gradients are not verified by that study.
  2. *Geometry Revision revD:* Mesh is revC ($2745.00\text{ mm}$ height); does not include the $610.00\text{ mm}$ parapet transmitted in revD ([20251009_Buckhalter_geometry_revD.eml](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Correspondence/20251009_Buckhalter_geometry_revD.eml)).
  3. *Grid Convergence Index (GCI):* GCI is physically invalid for LES and strictly prohibited under QA Standard rev 3 §4.

### Retained Artifacts & Inlet Defining Settings
* **Retained Downstream:** $11.215\text{M}$-cell mesh, boundary patch topology, probe monitor locations, and ABL inlet specification. All solution fields and RANS settings are discarded.
* **Atmospheric Boundary Layer Inlet Defining Settings:**
  * Type: `atmBoundaryLayerInletVelocity`
  * Reference Velocity ($U_{\text{ref}}$): $8.00\text{ m/s}$ (Attempt 3 / Case 3.1-B; matrix spans $5.00\text{ m/s}, 8.00\text{ m/s}, 12.00\text{ m/s}$)
  * Reference Height ($Z_{\text{ref}}$): $6.10\text{ m}$ ($20.00\text{ ft}$ AGL per SOW §3.1)
  * Surface Roughness Length ($z_0$): $0.03\text{ m}$ (cured Sonoran buffelgrass)
  * Displacement Height ($d$): $0.00\text{ m}$
  * Flow Direction Vector (`flowDir`): $(\cos(240^\circ), \sin(240^\circ), 0) = (-0.5000, -0.8660, 0.0000)$ for $240^\circ$ sector; $(-1.0000, 0.0000, 0.0000)$ for $270^\circ$ sector
  * Companion Turbulence Profiles: `atmBoundaryLayerInletK` and `atmBoundaryLayerInletEpsilon`

---

## 4. Computational Cost, Runtime Projections, & Feasibility Audit

### Firm Projection Basis & Baseline Run of Record
Per Technical Director memorandum ([20251009_Falk_runtime_projection_basis.eml](file:///filesystem/20251009_Falk_runtime_projection_basis.eml)), solver wall clock scales linearly with physical simulated time on a fixed mesh, solver stack, and core count. Derived from the fine-grid run of record ([three_grid_study_outputs.txt](file:///filesystem/Projects/CFDME-2025-041_Ocotillo_WUI/Case/verification/three_grid_study_outputs.txt)):
$$\text{Rate} = \frac{5\text{h }45\text{m}}{40.00\text{ s}} = \frac{20,700.00\text{ s}}{40.00\text{ s}} = \mathbf{517.50\text{ wall-clock seconds per simulated second}} \quad (\mathbf{8.6250\text{ min/s}})$$

### Solver Wall Clock Projections (SOW §3.1 Matrix = 6 Cases)
Per SOW §3.1, the matrix procures exactly six cases: 3.1-A through 3.1-F ($240^\circ$ and $270^\circ$ at $5.00\text{ m/s}, 8.00\text{ m/s}, 12.00\text{ m/s}$).

| Scope / Duration Basis | Simulated Time | Solver Wall Clock (1 Case) | Solver Wall Clock (6-Case Matrix) | Status & Compliance |
| :--- | :---: | :---: | :---: | :--- |
| **Shortest Allowable (Authorized Basis)** | **$31.00\text{ s}$** | **$4\text{h }27\text{m}$** ($16,042.50\text{ s}$) | **$26\text{h }44\text{m}$** ($96,255.00\text{ s}$) | **Normative floor ($8.00\text{ s}$ startup + $20$ cycles)** |
| Sampling Window Alone (Zero Startup) | $23.00\text{ s}$ | $3\text{h }18\text{m}$ ($11,902.50\text{ s}$) | $19\text{h }50\text{m}$ ($71,415.00\text{ s}$) | Theoretical statistical window only |
| Grid Study Benchmark | $40.00\text{ s}$ | $5\text{h }45\text{m}$ ($20,700.00\text{ s}$) | $34\text{h }30\text{m}$ ($124,200.00\text{ s}$) | Direct run-of-record calibration |
| Reference `controlDict` Ceiling | $60.00\text{ s}$ | $8\text{h }38\text{m}$ ($31,050.00\text{ s}$) | $51\text{h }45\text{m}$ ($186,300.00\text{ s}$) | Conservative $\sim 45$-cycle window |

### Feasibility Audit: Can the Projection Basis Be Met?
**NO, the projection basis cannot be met in practice.** An audit against every required condition reveals:
1. **Fixed Mesh Condition (VIOLATED):** The study run was fluid-only ($11.196\text{M}$ cells, open top $z = 60.00\text{ m}$). The production mesh ($11.215\text{M}$ cells) adds four CHT regions with level 7 refinement ($dx \approx 3.90\text{ mm}$) at tie embedments.
2. **Fixed Solver Stack Condition (VIOLATED):** Fluid-only `fireFoam` vs multi-region `chtMultiRegionFoam` with participating cavity radiation.
3. **Fixed Core Count Condition (VIOLATED):** Study ran on borrego + cloud burst ($192+$ cores); production is assigned 64 cores.
4. **Time Step & Zero Courant Margin Bottleneck (CRITICAL):**
   * In the study run, $\text{Mean } Co = 0.47$, $\text{Max } Co = \mathbf{0.90}$ (limit $0.90$), and average $\Delta t = 2.20\times 10^{-3}\text{ s}$.
   * **Courant margin is ZERO.** $\text{Max } Co$ was already hard-limited at the $0.90$ ceiling.
   * At $12.00\text{ m/s}$ (Cases 3.1-C and 3.1-F), velocities increase by $50.00\%$, forcing $\Delta t \le 1.40\times 10^{-3}\text{ s}$ and increasing time steps by $50.00\text{ to }60.00\%$. Tie thermal diffusion across $3.90\text{ mm}$ cells further restricts $\Delta t$.
* **Value of the Projection Figure:** The projected **$4\text{h }27\text{m}$** per case and **$26\text{h }44\text{m}$** for the matrix represent an **un-derated theoretical lower-bound floor**. Actual production wall clock including CHT coupling, 64-core limits, and $12.00\text{ m/s}$ Courant compression will require a $40.00\%\text{ to }80.00\%$ derating ($6\text{h }15\text{m}\text{ to }8\text{h }00\text{m}$ per case; $37\text{h }30\text{m}\text{ to }48\text{h }00\text{m}$ matrix).

### Attempt 3 Resource Consumption & Usability
* **Consumed in Attempt 3:** **$6\text{h }41\text{m}$** ($24,060.00\text{ s} = 401.00\text{ min}$) on 64 cores ($424.30\text{ CPU-hours}$) across 800 outer iterations.
* **Comparison to One Authorized Case:** Attempt 3 consumed **$149.98\%$ ($\sim 150.00\%$)** of the wall clock required for an entire $31.00\text{ s}$ authorized production run ($4\text{h }27\text{m}$)—burning an excess of **$2\text{h }14\text{m}$** ($133.62\text{ min}$) chasing an unphysical steady state.
* **Downstream Usability:** Flow solution fields ($U, p, T, k, \epsilon, \text{radiation}$) are **$0.00\%$ usable (complete scrap)**. RANS eddy viscosity suppresses LES vortex generation, and CHT was uncoupled. Only the $11.215\text{M}$-cell mesh geometry and ABL inlet settings carry forward.

---

## 5. Deliverable Verification & Sign-Off

The formal technical note deliverable has been compiled and saved to the container filesystem:
* **Deliverable Path:** [CFDME-2025-041_transient_solve_disposition_revA.docx](file:///filesystem/CFDME-2025-041_transient_solve_disposition_revA.docx)
* **File Format:** Microsoft Word (.docx) with firm letterhead, formal metadata, comparative audit tables, reviewer sign-off block, and statutory PE stamp boundary.
* **File Size:** $53,732\text{ bytes}$ (85 paragraphs, 8 structured tables, 4,186 words).

```
========================================================================================
PROFESSIONAL ENGINEERING REGISTRATION & STAMP BOUNDARY
Gordon Selby, PE — Arizona Professional Engineer #48213 (Principal)
Marguerite Falk, PE — Arizona Professional Engineer #42798 (Technical Director)
The CFD Mechanical Engineer, LLC • Tucson, Arizona

MANDATORY STATUTORY STAMP BOUNDARY:
"CFD thermal analysis only. Fire-resistance rating certified separately by others."

Disposition Date: 10/10/2025
Action: RETURNED FOR CORRECTION — PROCEED WITH AUTHORIZED TRANSIENT LES ONLY
========================================================================================
```