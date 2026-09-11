# HART-120 — Flexible High-Aspect-Ratio Wing & Robust Gust-Load Alleviation

**Independent reduced-order conceptual aircraft study by Shreyas G. Chandhavar**

HART-120 is an original fictional 120-passenger-class transport concept created to study a real aerospace engineering problem:

> **How far can a higher-aspect-ratio wing improve aerodynamic efficiency before structural mass, flexibility, maneuver loads and gust loads erase the benefit — and can passive aeroelastic tailoring plus active load alleviation recover useful design space?**

This repository is intentionally physics-first. Machine learning is used only as a surrogate and screening layer; shortlisted designs are returned to the reduced-order physics model for verification.

---

## Final project result

The study starts from an AR 13.5 conventional reference configuration and closes on an **AR 15.5 technology-enabled wing** after structural sizing, fail-safe web redesign, technology-system mass accounting, aircraft-weight feedback, mission fuel estimation, ML-assisted controller screening and Monte Carlo robustness verification.

| Metric | Baseline / Requirement | Final HART-120 result |
|---|---:|---:|
| Aspect ratio | 13.5 | **15.5** |
| Wing span | 39.13 m | **41.93 m** |
| Aircraft mass | 55,000 kg | **56,416.5 kg** |
| Structural + control package | — | **6,218.69 kg** |
| Structural mass budget | 6,242.85 kg | **24.16 kg margin** |
| Induced-drag reduction | 0% | **8.36%** |
| Total cruise-drag reduction | 0% | **2.28%** |
| L/D | 18.91 | **19.85 (+4.97%)** |
| 3000-km cruise fuel | 6,234.17 kg | **6,109.06 kg** |
| Cruise fuel saving | — | **125.10 kg (2.01%)** |
| Final preview time | — | **0.070 s** |
| Sensor / processing delay | — | **0.040 s** |
| Mean envelope GLA | ≥10% objective | **15.79%** |
| 5th-percentile envelope GLA | ≥10% | **13.81%** |
| 95th-percentile controlled root moment | ≤3.729 MN·m | **3.687 MN·m** |
| Absolute load pass rate | ≥95% | **98%** |
| Envelope ≥10% GLA pass rate | ≥95% | **100%** |
| Actuator-limit pass rate | ≥95% | **100%** |
| Joint robustness | ≥95% | **98%** |
| Maximum actuator deflection | ≤15° | **13.89°** |

**Project-level conclusion:** within the assumptions of the reduced-order model, the final AR 15.5 configuration satisfies all defined conceptual design gates while retaining a positive aerodynamic and mission benefit.

---

## Engineering problem addressed

Higher aspect ratio reduces induced drag, but also increases span and structural bending demand. A more flexible wing can then become limited by:

- bending stiffness and tip deflection,
- spar-cap stress and compression buckling,
- web shear,
- maneuver and gust loads,
- dynamic amplification,
- control-surface authority,
- actuator lag, rate limits and sensing delay,
- degraded or failed load-alleviation capability,
- uncertainty in structural, aerodynamic and control parameters,
- the mass of the sensing / control / actuation system itself.

HART-120 treats these effects as one connected engineering decision chain rather than as isolated calculations.

---

## Workflow

1. Baseline aircraft and high-aspect-ratio wing definition
2. Elliptical lift distribution and spanwise shear / bending loads
3. Euler-Bernoulli flexible-wing model and stiffness calibration
4. Reduced-order spar-cap and web sizing
5. Material redistribution and stiffness-placement study
6. 2.5-g maneuver and gust load cases
7. Active load redistribution and control-authority study
8. Actuator lag, rate limit and sensor/control delay modelling
9. First-mode dynamic gust response and critical gust search
10. Preview / feedforward gust-load alleviation
11. Static aeroelastic twist and passive load redistribution
12. Compression-panel buckling screening
13. Aspect-ratio aero-structural trade
14. Passive + active load-alleviation sizing
15. Fail-safe web redesign under degraded control capability
16. Technology-system mass accounting
17. Aircraft-weight feedback into cruise drag and mission fuel
18. Physics-generated ML surrogate models
19. ML-assisted controller / design screening
20. Full-physics verification of ML finalists
21. Monte Carlo robustness study under uncertain gust, structural and control parameters
22. Final controller redesign and 300-case / 6,000-gust verification

---

## Key engineering findings

### Higher aspect ratio is not automatically better
Induced drag decreases with AR, but structural mass and bending demand rise rapidly. In the conventional configuration, the project-level +30% structural-mass budget limited the design to approximately AR 15.0.

### Load alleviation creates usable design space
Passive aeroelastic relief plus active load alleviation extended the feasible design to **AR 15.5** under the same structural mass budget.

### Fail-safe sizing matters
The nominal load-alleviated structure became web-shear limited when active-control capability was degraded. A fail-safe web redesign added mass but kept AR 15.5 within the project budget.

### System mass can erase structural benefit
A conceptual **75 kg GLA/MLA system** was explicitly accounted for and remained below the **99.16 kg break-even allowance**.

### Mission benefit survives weight coupling
After feeding the technology mass back into aircraft weight, cruise lift, induced drag and mission fuel, the final configuration still achieved **2.28% lower total cruise drag** and **2.01% lower estimated cruise fuel** for the 3000-km study mission.

### Nominal controller performance was not enough
An early controller passed nominal physics but did not meet the project robustness target under uncertainty. The final controller was redesigned around preview and processing delay and achieved **98% joint robustness** in the final Monte Carlo verification.

---

## Machine-learning role

ML is not treated as the source of truth. It is used to accelerate engineering exploration by learning mappings from physics-generated data, screening large design spaces, ranking candidates and identifying important variables. Final candidates are always returned to the physics model.

Selected surrogate performance:

- fail-safe wingbox mass: **R² ≈ 0.997**
- cruise fuel: **R² ≈ 0.998**
- fuel-saving percentage: **R² ≈ 0.988**
- dynamic controlled root moment: **R² ≈ 0.960**
- dynamic root-moment reduction: **R² ≈ 0.935**

---

## Repository structure

```text
HART120-AeroStructural-GLA/
├── README.md
├── MODEL_LIMITATIONS.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── HART120_Flexible_Wing_Design_FINAL.ipynb
│   └── HART120_Flexible_Wing_Design_SOURCE.ipynb
├── src/
│   └── HART120_Flexible_Wing_Design.py
├── results/
│   ├── final_metrics.csv
│   ├── final_design_gates.csv
│   └── figures/
├── docs/
│   └── HART120_Engineering_Report.pdf
└── portfolio/
    ├── index.html
    ├── hart120.html
    ├── hart120-trade.svg
    └── hart120-robustness.svg
```

---

## Start here

For a quick review:

1. Read this README.
2. Open `docs/HART120_Engineering_Report.pdf` for the engineering narrative.
3. Review `results/final_metrics.csv` and `results/final_design_gates.csv` for the frozen final results.
4. Open `notebooks/HART120_Flexible_Wing_Design_FINAL.ipynb` for the complete saved analysis trail.
5. Use `src/HART120_Flexible_Wing_Design.py` if you want a script-form export of the notebook calculations.

A full clean notebook run can be computationally expensive because several Monte Carlo and controller-screening studies are included. Saved outputs are retained so the engineering trail can be reviewed without rerunning every simulation.

---

## Running locally

Python 3.10+ is recommended.

```bash
pip install -r requirements.txt
```

Then open the notebook in Jupyter or Google Colab.

---

## Scope and limitations

This is a **conceptual reduced-order engineering study**, not an aircraft certification analysis or OEM design claim. It does not replace:

- 3D CFD / RANS,
- nonlinear aeroelasticity,
- detailed composite laminate mechanics,
- shell/solid wingbox FEA,
- flutter clearance,
- CS/FAR-25 gust and maneuver substantiation,
- production flight-control-law development,
- hardware-in-the-loop testing,
- actuator thermal / reliability / redundancy qualification,
- full aircraft mission and propulsion modelling.

See [`MODEL_LIMITATIONS.md`](MODEL_LIMITATIONS.md) for the detailed boundary of the claims.

---

## Originality and IP

HART-120 is an original fictional aircraft concept created for this independent study. No proprietary OEM aircraft geometry, confidential loads, internal control laws or restricted datasets are used. The repository contains original calculations, code and project results.

---

## Author

**Shreyas G. Chandhavar**  
Mechanical Engineer · Aero-Structural Analysis · Engineering Computation  
MSc Sustainable Energy Engineering, Lund University

- Portfolio: https://shreyas-chandhavar.github.io/
- GitHub: https://github.com/shreyas-chandhavar
- LinkedIn: https://www.linkedin.com/in/shreyasgowrishankarchandhavar/
