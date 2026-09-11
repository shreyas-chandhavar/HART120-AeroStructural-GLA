# HART-120 — Flexible High-Aspect-Ratio Wing & Robust Gust-Load Alleviation

**Independent reduced-order conceptual aircraft study** by **Shreyas G. Chandhavar**

HART-120 is an original fictional 120-passenger-class transport concept created to investigate a real aerospace engineering problem:

> **How far can a higher-aspect-ratio wing improve aerodynamic efficiency before structural mass, flexibility and gust/maneuver loads erase the benefit — and can passive aeroelastic tailoring plus active load alleviation recover useful design space?**

This repository is not a generic ML exercise. The workflow starts from first-principles engineering models, uses ML only as a fast surrogate/screening layer, and returns shortlisted designs to the physics model for verification.

---

## Why this problem matters

Increasing wing aspect ratio reduces induced drag, but also increases span and root bending demand. A lighter, more flexible wing can then become limited by:

- global bending stiffness and tip deflection,
- spar-cap stress and compression buckling,
- web shear,
- maneuver loads,
- gust loads and dynamic amplification,
- control-surface authority and actuator dynamics,
- degraded or failed load-alleviation systems,
- uncertainty in structural, aerodynamic and control parameters,
- the mass of the load-alleviation system itself.

HART-120 treats these effects as one connected engineering decision chain rather than isolated calculations.

---

## Final frozen configuration

| Metric | Baseline / Requirement | Final HART-120 result |
|---|---:|---:|
| Aspect ratio | 13.5 | **15.5** |
| Wing span | 39.13 m | **41.93 m** |
| Aircraft mass | 55,000 kg | **56,416.5 kg** |
| Final structural + control package | — | **6,218.69 kg** |
| Structural mass budget | 6,242.85 kg | **24.16 kg margin** |
| Induced-drag reduction | 0% | **8.36%** |
| Total cruise-drag reduction | 0% | **2.28%** |
| L/D | 18.91 | **19.85 (+4.97%)** |
| 3000-km cruise fuel | 6,234.17 kg | **6,109.06 kg** |
| Cruise fuel saving | — | **125.10 kg (2.01%)** |
| Final preview time | — | **0.070 s** |
| Sensor / processing delay | — | **0.040 s** |
| Effective timing lead | — | **0.030 s** |
| Mean envelope GLA | ≥10% project objective | **15.79%** |
| 5th-percentile envelope GLA | ≥10% | **13.81%** |
| 95th-percentile controlled root moment | ≤3.729 MN·m | **3.687 MN·m** |
| Absolute load pass rate | ≥95% | **98%** |
| Envelope ≥10% GLA pass rate | ≥95% | **100%** |
| Actuator-limit pass rate | ≥95% | **100%** |
| Joint robustness | ≥95% | **98%** |
| Maximum actuator deflection | ≤15° | **13.89°** |

**Project-level result:** the final AR 15.5 configuration satisfies all defined conceptual design gates in the reduced-order model.

---

## Engineering workflow

### 1. Baseline aerodynamic and structural model
A fictional aircraft requirement set is used to derive wing area, span and chord distribution. An elliptical reference lift distribution is integrated to obtain shear force and bending moment.

### 2. Flexible-wing calibration
A spanwise stiffness distribution is represented using Euler-Bernoulli beam mechanics. Root stiffness is calibrated to a project-level tip-deflection target.

### 3. Simplified wingbox sizing
Equivalent spar-cap area and web thickness are sized from stiffness, bending stress and shear requirements. The model is deliberately reduced order and reports **spar-cap + web mass**, not total wing mass.

### 4. Structural material redistribution
Equal-mass stiffness-placement tests show that inboard material is substantially more effective at reducing global tip deflection than outboard material. A fixed-mass redistribution study demonstrates that structural layout can improve performance before adding mass.

### 5. Maneuver and gust load cases
The model adds a 2.5-g maneuver case and vertical-gust loading. Active load redistribution is introduced while preserving total lift.

### 6. Control authority and actuator dynamics
Required lift redistribution is converted to control demand. Actuator lag, control delay, rate limit and surface-deflection constraints are introduced.

### 7. Dynamic gust response
A first-mode flexible-wing model is used to study dynamic amplification and critical gust gradients.

### 8. Preview / feedforward gust-load alleviation
The study evaluates whether preview sensing can create enough timing lead to reduce root bending moment before the gust fully loads the wing.

### 9. Static aeroelastic tailoring
An idealized torsional wingbox model estimates passive washout and associated spanwise load redistribution.

### 10. Compression buckling screening
Spar-cap and panel buckling checks are added to prevent a stiffness-only design from being presented as complete structural sizing.

### 11. Aspect-ratio trade
AR = 13.5–18 is explored. Higher AR reduces induced drag but rapidly increases structural mass in the conventional configuration.

### 12. Passive + active load alleviation
A technology-enabled wing combines passive aeroelastic relief with active maneuver-load redistribution and is compared against the conventional wing under the same project-level constraints.

### 13. Fail-safe sizing and system mass
Degraded / failed control cases reveal web shear as a limiting condition. The web is resized fail-safe, and the mass of the GLA/MLA sensing, control and actuation system is accounted for.

### 14. Aircraft-level mission closure
The added aircraft mass is fed back into cruise lift, induced drag, total drag, L/D and a Breguet-type cruise fuel estimate.

### 15. Physics-generated ML surrogates
Thousands of design cases are generated from the physics model. Random-forest surrogates are trained for structural, aerodynamic and mission outputs.

### 16. ML-assisted controller search
The surrogate screens large controller-design spaces quickly. ML is used for candidate screening only; finalists are re-evaluated using the transient physics model.

### 17. Robustness and uncertainty
Monte Carlo studies perturb gust amplitude, frequency, damping, actuator dynamics, control effectiveness and sensing/processing timing.

### 18. Final controller redesign
The original controller fails the 95% robustness target. Preview and delay are redesigned, then a final 300-case / 6,000-gust full-physics verification is run.

---

## Key engineering findings

### Higher aspect ratio is not automatically better
At constant wing area, induced drag falls as AR increases, but span and structural bending demand increase. In this model, an unconstrained push toward AR 18 incurs a very large simplified wingbox penalty.

### Load alleviation creates usable design space
Under the project’s +30% structural-mass budget, the highest conventional configuration is AR 15.0, while the technology-enabled configuration reaches **AR 15.5**.

### Fail-safe sizing matters
A nominal load-alleviated structure was not acceptable under full control loss because the web became shear-governing. A fail-safe redesign added mass but kept AR 15.5 within the structural budget.

### System mass can erase an elegant structural result
The project explicitly closes the mass of forward gust sensing, flight-control computing, actuator increment, power electronics, wiring and integration allowance. The selected **75 kg** conceptual GLA/MLA system remains below the **99.16 kg** break-even allowance.

### Mission benefit survives weight coupling
After adding the structural/control package to aircraft mass, the final AR 15.5 configuration still shows:

- **8.36%** lower induced drag,
- **2.28%** lower total cruise drag,
- **4.97%** higher L/D,
- **2.01%** lower estimated cruise fuel for the 3000-km study mission.

### Nominal control performance is not enough
The first selected controller did not meet the project robustness objective under uncertainty. The final controller uses:

- preview time = **0.070 s**,
- sensor/processing delay = **0.040 s**,
- effective lead = **0.030 s**.

It achieves **98% joint robustness** in the final 300-case Monte Carlo verification.

---

## Machine learning role

ML is not treated as the source of truth.

The project uses ML to:
1. learn surrogate mappings from physics-generated design data,
2. screen large design spaces,
3. rank candidate configurations,
4. identify important variables,
5. reduce the number of expensive transient simulations.

Final shortlisted designs are returned to the physics model for verification.

Selected surrogate results:
- fail-safe wingbox mass: **R² ≈ 0.997**
- cruise fuel: **R² ≈ 0.998**
- fuel-saving percentage: **R² ≈ 0.988**
- dynamic controlled root moment: **R² ≈ 0.960**
- dynamic root-moment reduction: **R² ≈ 0.935**

---

## Repository structure

```text
HART120/
├── README.md
├── LICENSE
├── MODEL_LIMITATIONS.md
├── requirements.txt
├── notebooks/
│   └── HART120_Flexible_Wing_Design_FINAL.ipynb
├── src/
│   └── HART120_Flexible_Wing_Design.py
├── results/
│   ├── final_metrics.csv
│   ├── final_design_gates.csv
│   └── figures/
└── docs/
    ├── HART120_Engineering_Report.docx
    └── HART120_Engineering_Report.pdf
```

---

## Running the notebook

Python 3.10+ is recommended.

```bash
pip install -r requirements.txt
```

Open the notebook in Jupyter or Google Colab.

The notebook contains several Monte Carlo and controller-screening studies. A full clean run can be computationally expensive. The saved notebook outputs preserve the final study results so the complete engineering trail can be reviewed without rerunning every simulation.

---

## Assumptions and limitations

This is a **conceptual reduced-order study**, not an aircraft certification analysis.

The model does not replace:
- 3D CFD / RANS / high-fidelity aerodynamics,
- geometrically nonlinear aeroelasticity,
- detailed composite laminate mechanics,
- shell/solid wingbox FEA,
- flutter clearance,
- CS/FAR-25 certification gust and maneuver substantiation,
- detailed flight-control-law design,
- hardware-in-the-loop testing,
- actuator thermal / reliability / redundancy qualification,
- full aircraft mission and propulsion modelling.

See [`MODEL_LIMITATIONS.md`](MODEL_LIMITATIONS.md) for the detailed boundary of the claims.

---

## Originality and IP note

HART-120 is an original fictional aircraft concept created for this independent study. No proprietary OEM aircraft geometry, internal company loads, control laws or confidential datasets are used. The repository contains original code, calculations and project results.

---

## Author

**Shreyas G. Chandhavar**  
Mechanical Engineer · Aero-Structural Analysis · Engineering Computation  
MSc Sustainable Energy Engineering, Lund University

- Portfolio: https://shreyas-chandhavar.github.io/
- GitHub: https://github.com/shreyas-chandhavar
- LinkedIn: https://www.linkedin.com/in/shreyasgowrishankarchandhavar/
