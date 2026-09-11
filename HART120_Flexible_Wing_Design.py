"""
HART-120 Flexible High-Aspect-Ratio Wing Design and Robust GLA Study
Exported from the final Jupyter/Colab notebook.
Reduced-order conceptual design study; not certification-level analysis.
"""

# %% [notebook cell 0]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% [notebook cell 1]
# ---------------------------------------------
# HART-120 — Aircraft Design Requirements
# ---------------------------------------------

mass_design = 55_000       # kg
g = 9.81                   # m/s^2

mach_cruise = 0.76
altitude_cruise = 11_000   # m

rho_cruise = 0.364         # kg/m^3
a_cruise = 295.0           # m/s

CL_cruise = 0.52

AR_baseline = 13.5
taper_ratio = 0.30
sweep_deg = 25.0

oswald_e = 0.85

# %% [notebook cell 2]
# Cruise speed
V_cruise = mach_cruise * a_cruise

# Aircraft weight
W_design = mass_design * g

# Required wing area
S_wing = (2 * W_design) / (rho_cruise * V_cruise**2 * CL_cruise)

# Baseline wingspan
b_wing = np.sqrt(AR_baseline * S_wing)

# %% [notebook cell 3]
print("HART-120 BASELINE WING")
print("----------------------")
print(f"Cruise velocity: {V_cruise:.2f} m/s")
print(f"Design weight: {W_design/1000:.2f} kN")
print(f"Wing area: {S_wing:.2f} m^2")
print(f"Wing span: {b_wing:.2f} m")
print(f"Aspect ratio: {AR_baseline:.2f}")

# %% [notebook cell 4]
# ---------------------------------------------
# HART-120 — Baseline Wing Planform
# ---------------------------------------------

c_root = (2 * S_wing) / (b_wing * (1 + taper_ratio))
c_tip = taper_ratio * c_root

print(f"Root chord: {c_root:.2f} m")
print(f"Tip chord: {c_tip:.2f} m")

# %% [notebook cell 5]
n_stations = 51

y = np.linspace(0, b_wing / 2, n_stations)

# %% [notebook cell 6]
print("Number of stations:", len(y))
print("Root position:", y[0], "m")
print("Tip position:", y[-1], "m")

# %% [notebook cell 7]
chord = c_root - (c_root - c_tip) * (y / (b_wing / 2))
print("Root chord from array:", chord[0], "m")
print("Tip chord from array:", chord[-1], "m")

# %% [notebook cell 8]
plt.figure(figsize=(8, 5))

plt.plot(y, chord, linewidth=2)

plt.xlabel("Spanwise Position, y [m]")
plt.ylabel("Local Chord, c(y) [m]")
plt.title("HART-120 Spanwise Chord Distribution")

plt.grid(True)
plt.show()

# %% [notebook cell 9]
# ---------------------------------------------
# HART-120 — Reference Aerodynamic Loading
# ---------------------------------------------

elliptical_shape = np.sqrt(1 - ( y / (b_wing/ 2) )**2)
print("Root shape value:", elliptical_shape[0])
print("Tip shape value:", elliptical_shape[-1])

# %% [notebook cell 10]
L_half = W_design / 2

shape_integral = np.trapezoid(elliptical_shape, y)
lift_scale = L_half / shape_integral
lift_per_span = lift_scale * elliptical_shape
print(f"Required half-wing lift: {L_half/1000:.2f} kN")
print(f"Root lift per span: {lift_per_span[0]/1000:.2f} kN/m")
print(f"Tip lift per span: {lift_per_span[-1]/1000:.2f} kN/m")
L_half_check = np.trapezoid(lift_per_span, y)

print(f"Integrated half-wing lift: {L_half_check/1000:.2f} kN")

# %% [notebook cell 11]
plt.figure(figsize=(8, 5))

plt.plot(y, lift_per_span / 1000, linewidth=2)

plt.xlabel("Spanwise Position, y [m]")
plt.ylabel("Lift per Unit Span, L'(y) [kN/m]")
plt.title("HART-120 Elliptical Lift Distribution")

plt.grid(True)
plt.show()

# %% [notebook cell 12]
shear_force = np.zeros_like(y)
for i in range(len(y)):
    shear_force[i] = np.trapezoid(lift_per_span[i:], y[i:])
print(f"Root shear force: {shear_force[0]/1000:.2f} kN")
print(f"Tip shear force: {shear_force[-1]/1000:.2f} kN")

# %% [notebook cell 13]
plt.figure(figsize=(8, 5))

plt.plot(y, shear_force / 1000, linewidth=2)

plt.xlabel("Spanwise Position, y [m]")
plt.ylabel("Shear Force, V(y) [kN]")
plt.title("HART-120 Wing Shear Force Distribution")

plt.grid(True)
plt.show()

# %% [notebook cell 14]
bending_moment = np.zeros_like(y)

for i in range(len(y)):
    bending_moment[i] = np.trapezoid(shear_force[i:], y[i:])
print(f"Root bending moment: {bending_moment[0]/1e6:.2f} MN·m")
print(f"Tip bending moment: {bending_moment[-1]/1e6:.2f} MN·m")

# %% [notebook cell 15]
plt.figure(figsize=(8, 5))

plt.plot(y, bending_moment / 1e6, linewidth=2)

plt.xlabel("Spanwise Position, y [m]")
plt.ylabel("Bending Moment, M(y) [MN·m]")
plt.title("HART-120 Wing Bending Moment Distribution")

plt.grid(True)
plt.show()

# %% [notebook cell 16]
stiffness_shape = (chord / c_root)**3
print(f"Root stiffness ratio: {stiffness_shape[0]:.3f}")
print(f"Tip stiffness ratio: {stiffness_shape[-1]:.3f}")

# %% [notebook cell 17]
tip_deflection_ratio_target = 0.05

tip_deflection_target = tip_deflection_ratio_target * (b_wing / 2)
print(f"Target tip deflection: {tip_deflection_target:.3f} m")

# %% [notebook cell 18]
EI_root_trial = 1.0e9   # N·m^2
EI_trial = EI_root_trial * stiffness_shape
print(f"Trial root EI: {EI_trial[0]/1e9:.3f} GN·m^2")
print(f"Trial tip EI: {EI_trial[-1]/1e9:.3f} GN·m^2")

# %% [notebook cell 19]
curvature_trial = bending_moment / EI_trial
print(f"Root curvature: {curvature_trial[0]:.6f} 1/m")
print(f"Tip curvature: {curvature_trial[-1]:.6f} 1/m")

# %% [notebook cell 20]
slope_trial = np.zeros_like(y)
for i in range(1, len(y)):
    slope_trial[i] = np.trapezoid(curvature_trial[:i+1], y[:i+1])
print(f"Root slope: {slope_trial[0]:.6f} rad")
print(f"Tip slope: {slope_trial[-1]:.6f} rad")

# %% [notebook cell 21]
deflection_trial = np.zeros_like(y)
for i in range(1, len(y)):
    deflection_trial[i] = np.trapezoid(slope_trial[:i+1], y[:i+1])
print(f"Root deflection: {deflection_trial[0]:.4f} m")
print(f"Trial tip deflection: {deflection_trial[-1]:.4f} m")
print(f"Target tip deflection: {tip_deflection_target:.4f} m")

# %% [notebook cell 22]
EI_root = EI_root_trial * (deflection_trial[-1] / tip_deflection_target)
print(f"Calibrated root EI: {EI_root/1e9:.3f} GN·m^2")
EI = EI_root * stiffness_shape
print(f"Final root EI: {EI[0]/1e9:.3f} GN·m^2")
print(f"Final tip EI: {EI[-1]/1e9:.3f} GN·m^2")

# %% [notebook cell 23]
curvature = bending_moment / EI
slope = np.zeros_like(y)

for i in range(1, len(y)):
    slope[i] = np.trapezoid(curvature[:i+1], y[:i+1])

deflection = np.zeros_like(y)

for i in range(1, len(y)):
    deflection[i] = np.trapezoid(slope[:i+1], y[:i+1])

print(f"Final tip slope: {slope[-1]:.6f} rad")
print(f"Final tip deflection: {deflection[-1]:.4f} m")
print(f"Target tip deflection: {tip_deflection_target:.4f} m")

# %% [notebook cell 24]
plt.figure(figsize=(8, 5))

plt.plot(y, deflection, linewidth=2)

plt.xlabel("Spanwise Position, y [m]")
plt.ylabel("Vertical Deflection, w(y) [m]")
plt.title("HART-120 Baseline Wing Deflection")

plt.grid(True)
plt.show()

# %% [notebook cell 25]
tip_deflection = deflection[-1]
tip_slope = slope[-1]
root_bending_moment = bending_moment[0]
tip_deflection_ratio = tip_deflection / (b_wing / 2)
print("HART-120 FLEXIBLE WING BASELINE")
print("--------------------------------")
print(f"Root bending moment: {root_bending_moment/1e6:.3f} MN·m")
print(f"Tip slope: {tip_slope:.5f} rad")
print(f"Tip deflection: {tip_deflection:.3f} m")
print(f"Tip deflection ratio: {tip_deflection_ratio*100:.2f} %")
print(f"Root EI: {EI_root/1e9:.3f} GN·m^2")

# %% [notebook cell 26]
# ---------------------------------------------
# HART-120 — Simplified Wingbox Model
# ---------------------------------------------

E_eq = 70e9       # Pa
rho_eq = 1600     # kg/m^3
I_required = EI / E_eq
print(f"Required root I: {I_required[0]:.6f} m^4")
print(f"Required tip I: {I_required[-1]:.6f} m^4")

# %% [notebook cell 27]
thickness_ratio = 0.12
box_height_fraction = 0.80
airfoil_thickness = thickness_ratio * chord
box_height = box_height_fraction * airfoil_thickness
print(f"Root airfoil thickness: {airfoil_thickness[0]:.3f} m")
print(f"Root wingbox height: {box_height[0]:.3f} m")

print(f"Tip airfoil thickness: {airfoil_thickness[-1]:.3f} m")
print(f"Tip wingbox height: {box_height[-1]:.3f} m")

# %% [notebook cell 28]
A_cap = (2 * I_required) / (box_height**2)
print(f"Root spar-cap area: {A_cap[0]*1e4:.2f} cm^2")
print(f"Tip spar-cap area: {A_cap[-1]*1e4:.2f} cm^2")

# %% [notebook cell 29]
sigma_cap = bending_moment / (A_cap * box_height)
print(f"Root spar-cap stress: {sigma_cap[0]/1e6:.2f} MPa")
print(f"Maximum spar-cap stress: {np.max(sigma_cap)/1e6:.2f} MPa")
print(f"Tip spar-cap stress: {sigma_cap[-1]/1e6:.2f} MPa")

# %% [notebook cell 30]
cap_mass_per_span = 2 * A_cap * rho_eq
print(f"Root cap mass per span: {cap_mass_per_span[0]:.2f} kg/m")
print(f"Tip cap mass per span: {cap_mass_per_span[-1]:.2f} kg/m")

# %% [notebook cell 31]
m_caps_half = np.trapezoid(cap_mass_per_span, y)

m_caps_total = 2 * m_caps_half

print(f"Half-wing spar-cap mass: {m_caps_half:.2f} kg")
print(f"Total spar-cap mass, both wings: {m_caps_total:.2f} kg")

# %% [notebook cell 32]
cap_mass_fraction = m_caps_total / mass_design

print(f"Spar-cap mass fraction: {cap_mass_fraction*100:.2f} %")

# %% [notebook cell 33]
tau_allow = 40e6      # Pa
web_thickness_required = shear_force / (2 * tau_allow * box_height)
print(f"Required root web thickness: {web_thickness_required[0]*1000:.2f} mm")
print(f"Required mid-span web thickness: {web_thickness_required[len(y)//2]*1000:.2f} mm")
print(f"Required tip web thickness: {web_thickness_required[-1]*1000:.2f} mm")

# %% [notebook cell 34]
web_thickness_min = 2.5e-3   # m

web_thickness = np.maximum(web_thickness_required, web_thickness_min)
print(f"Final root web thickness: {web_thickness[0]*1000:.2f} mm")
print(f"Final mid-span web thickness: {web_thickness[len(y)//2]*1000:.2f} mm")
print(f"Final tip web thickness: {web_thickness[-1]*1000:.2f} mm")

# %% [notebook cell 35]
web_mass_per_span = 2 * web_thickness * box_height * rho_eq

print(f"Root web mass per span: {web_mass_per_span[0]:.2f} kg/m")
print(f"Mid-span web mass per span: {web_mass_per_span[len(y)//2]:.2f} kg/m")
print(f"Tip web mass per span: {web_mass_per_span[-1]:.2f} kg/m")

# %% [notebook cell 36]
m_web_half = np.trapezoid(web_mass_per_span, y)

m_web_total = 2 * m_web_half

print(f"Half-wing web mass: {m_web_half:.2f} kg")
print(f"Total web mass, both wings: {m_web_total:.2f} kg")

# %% [notebook cell 37]
m_wingbox_total = m_caps_total + m_web_total

wingbox_mass_fraction = m_wingbox_total / mass_design

print(f"Total simplified wingbox mass: {m_wingbox_total:.2f} kg")
print(f"Wingbox mass fraction: {wingbox_mass_fraction*100:.2f} %")

# %% [notebook cell 38]
cap_fraction_wingbox = m_caps_total / m_wingbox_total
web_fraction_wingbox = m_web_total / m_wingbox_total

print(f"Spar-cap contribution: {cap_fraction_wingbox*100:.2f} %")
print(f"Shear-web contribution: {web_fraction_wingbox*100:.2f} %")

# %% [notebook cell 39]
wingbox_mass_per_span = cap_mass_per_span + web_mass_per_span



print(f"Root wingbox mass per span: {wingbox_mass_per_span[0]:.2f} kg/m")

print(f"Mid-span wingbox mass per span: {wingbox_mass_per_span[len(y)//2]:.2f} kg/m")

print(f"Tip wingbox mass per span: {wingbox_mass_per_span[-1]:.2f} kg/m")

# %% [notebook cell 40]
plt.figure(figsize=(8, 5))



plt.plot(y, wingbox_mass_per_span, linewidth=2)



plt.xlabel("Spanwise Position, y [m]")

plt.ylabel("Wingbox Mass per Unit Span [kg/m]")

plt.title("HART-120 Spanwise Wingbox Mass Distribution")



plt.grid(True)

plt.show()

# %% [notebook cell 41]
stiffness_factors = np.linspace(0.7, 1.30, 13)
print("Stiffness factors:")
print(stiffness_factors)

# %% [notebook cell 42]
tip_deflection_results = []

for factor in stiffness_factors:

    EI_candidate = factor * EI
    curvature_candidate = bending_moment / EI_candidate

    slope_candidate = np.zeros_like(y)

    for i in range(1, len(y)):
        slope_candidate[i] = np.trapezoid(
            curvature_candidate[:i+1],
            y[:i+1]
        )

    deflection_candidate = np.zeros_like(y)

    for i in range(1, len(y)):
        deflection_candidate[i] = np.trapezoid(
            slope_candidate[:i+1],
            y[:i+1]
        )

    tip_deflection_results.append(deflection_candidate[-1])

tip_deflection_results = np.array(tip_deflection_results)

print("Tip deflections [m]:")
print(tip_deflection_results)

# %% [notebook cell 43]
max_stress_results = []
wingbox_mass_results = []

for factor in stiffness_factors:

    EI_candidate = factor * EI

    I_candidate = EI_candidate / E_eq

    A_cap_candidate = (2 * I_candidate) / (box_height**2)

    sigma_candidate = bending_moment / (
        A_cap_candidate * box_height
    )

    cap_mass_per_span_candidate = (
        2 * A_cap_candidate * rho_eq
    )

    m_caps_half_candidate = np.trapezoid(
        cap_mass_per_span_candidate,
        y
    )

    m_caps_total_candidate = 2 * m_caps_half_candidate

    m_wingbox_candidate = (
        m_caps_total_candidate + m_web_total
    )

    max_stress_results.append(np.max(sigma_candidate))

    wingbox_mass_results.append(m_wingbox_candidate)

max_stress_results = np.array(max_stress_results)
wingbox_mass_results = np.array(wingbox_mass_results)
print("Maximum spar-cap stresses [MPa]:")
print(max_stress_results / 1e6)

print("\nWingbox masses [kg]:")
print(wingbox_mass_results)

# %% [notebook cell 44]
deflection_limit = tip_deflection_target

feasible_deflection = tip_deflection_results <= deflection_limit

print("Deflection-feasible designs:")
print(feasible_deflection)

feasible_masses = wingbox_mass_results[feasible_deflection]

minimum_feasible_mass = np.min(feasible_masses)

print(f"Minimum feasible uniform wingbox mass: {minimum_feasible_mass:.2f} kg")

# %% [notebook cell 45]
eta = y / (b_wing / 2)

inner_region = eta < 0.35
mid_region = (eta >= 0.35) & (eta < 0.70)
outer_region = eta >= 0.70
print("Inner stations:", np.sum(inner_region))
print("Mid stations:", np.sum(mid_region))
print("Outer stations:", np.sum(outer_region))
print("Total stations:", np.sum(inner_region) + np.sum(mid_region) + np.sum(outer_region))

# %% [notebook cell 46]
m_caps_inner = np.trapezoid(cap_mass_per_span[inner_region], y[inner_region])

m_caps_mid = np.trapezoid(cap_mass_per_span[mid_region], y[mid_region])

m_caps_outer = np.trapezoid(cap_mass_per_span[outer_region], y[outer_region])

print(f"Inner-region cap mass: {m_caps_inner:.2f} kg")
print(f"Mid-region cap mass: {m_caps_mid:.2f} kg")
print(f"Outer-region cap mass: {m_caps_outer:.2f} kg")

print(f"Regional mass sum: {m_caps_inner + m_caps_mid + m_caps_outer:.2f} kg")
print(f"Original half-wing cap mass: {m_caps_half:.2f} kg")

# %% [notebook cell 47]
dy = y[1] - y[0]

integration_weights = np.full_like(y, dy)

integration_weights[0] *= 0.5
integration_weights[-1] *= 0.5

# %% [notebook cell 48]
m_caps_inner_corrected = np.sum(
    cap_mass_per_span[inner_region] * integration_weights[inner_region]
)

m_caps_mid_corrected = np.sum(
    cap_mass_per_span[mid_region] * integration_weights[mid_region]
)

m_caps_outer_corrected = np.sum(
    cap_mass_per_span[outer_region] * integration_weights[outer_region]
)
regional_mass_sum_corrected = (
    m_caps_inner_corrected
    + m_caps_mid_corrected
    + m_caps_outer_corrected
)

print(f"Corrected inner cap mass: {m_caps_inner_corrected:.2f} kg")
print(f"Corrected mid cap mass: {m_caps_mid_corrected:.2f} kg")
print(f"Corrected outer cap mass: {m_caps_outer_corrected:.2f} kg")
print(f"Corrected regional sum: {regional_mass_sum_corrected:.2f} kg")
print(f"Original half-wing cap mass: {m_caps_half:.2f} kg")

# %% [notebook cell 49]
added_mass_half = 100.0   # kg per half-wing

inner_stiffness_factor = 1 + (added_mass_half / m_caps_inner_corrected)
mid_stiffness_factor = 1 + (added_mass_half / m_caps_mid_corrected)
outer_stiffness_factor = 1 + (added_mass_half / m_caps_outer_corrected)

print(f"Inner-region stiffness multiplier: {inner_stiffness_factor:.4f}")
print(f"Mid-region stiffness multiplier: {mid_stiffness_factor:.4f}")
print(f"Outer-region stiffness multiplier: {outer_stiffness_factor:.4f}")

# %% [notebook cell 50]
# ---------------------------------------------
# HART-120 — Equal-Mass Stiffness Placement Test
# ---------------------------------------------

EI_inner_test = EI.copy()
EI_mid_test = EI.copy()
EI_outer_test = EI.copy()

# Apply regional stiffness increases
EI_inner_test[inner_region] *= inner_stiffness_factor
EI_mid_test[mid_region] *= mid_stiffness_factor
EI_outer_test[outer_region] *= outer_stiffness_factor


def calculate_tip_deflection(EI_input):

    curvature_temp = bending_moment / EI_input

    slope_temp = np.zeros_like(y)

    for i in range(1, len(y)):
        slope_temp[i] = np.trapezoid(
            curvature_temp[:i+1],
            y[:i+1]
        )

    deflection_temp = np.zeros_like(y)

    for i in range(1, len(y)):
        deflection_temp[i] = np.trapezoid(
            slope_temp[:i+1],
            y[:i+1]
        )

    return deflection_temp[-1]


tip_deflection_inner = calculate_tip_deflection(EI_inner_test)
tip_deflection_mid = calculate_tip_deflection(EI_mid_test)
tip_deflection_outer = calculate_tip_deflection(EI_outer_test)


print("CHECK THAT STIFFNESS ACTUALLY CHANGED")
print("-------------------------------------")
print("Inner EI change:", np.max(np.abs(EI_inner_test - EI)))
print("Mid EI change:", np.max(np.abs(EI_mid_test - EI)))
print("Outer EI change:", np.max(np.abs(EI_outer_test - EI)))

print("\nHART-120 EQUAL-MASS STIFFNESS PLACEMENT TEST")
print("--------------------------------------------")
print(f"Baseline tip deflection: {tip_deflection:.8f} m")
print(f"+100 kg inner region: {tip_deflection_inner:.8f} m")
print(f"+100 kg mid region: {tip_deflection_mid:.8f} m")
print(f"+100 kg outer region: {tip_deflection_outer:.8f} m")
print(f"+100 kg outer region: {tip_deflection_outer:.8f} m")

# %% [notebook cell 51]
deflection_reduction_inner = tip_deflection - tip_deflection_inner
deflection_reduction_mid = tip_deflection - tip_deflection_mid
deflection_reduction_outer = tip_deflection - tip_deflection_outer

print(f"Inner-region reduction: {deflection_reduction_inner*1000:.2f} mm")
print(f"Mid-region reduction: {deflection_reduction_mid*1000:.2f} mm")
print(f"Outer-region reduction: {deflection_reduction_outer*1000:.2f} mm")

# %% [notebook cell 52]
redistributed_mass = 100.0   # kg per half-wing

inner_factor_redistributed = 1 + (
    redistributed_mass / m_caps_inner_corrected
)

outer_factor_redistributed = 1 - (
    redistributed_mass / m_caps_outer_corrected
)

print(f"Inner redistribution factor: {inner_factor_redistributed:.4f}")
print(f"Outer redistribution factor: {outer_factor_redistributed:.4f}")

# %% [notebook cell 53]
EI_redistributed = EI.copy()

EI_redistributed[inner_region] *= inner_factor_redistributed
EI_redistributed[outer_region] *= outer_factor_redistributed
tip_deflection_redistributed = calculate_tip_deflection(EI_redistributed)

print(f"Baseline tip deflection: {tip_deflection:.4f} m")
print(f"Redistributed tip deflection: {tip_deflection_redistributed:.4f} m")

# %% [notebook cell 54]
I_redistributed = EI_redistributed / E_eq

A_cap_redistributed = (2 * I_redistributed) / (box_height**2)

sigma_redistributed = bending_moment / (
    A_cap_redistributed * box_height
)

max_stress_redistributed = np.max(sigma_redistributed)
max_stress_index = np.argmax(sigma_redistributed)

print(f"Baseline maximum stress: {np.max(sigma_cap)/1e6:.2f} MPa")
print(f"Redistributed maximum stress: {max_stress_redistributed/1e6:.2f} MPa")
print(f"Maximum stress location: {y[max_stress_index]:.2f} m")

# %% [notebook cell 55]
cap_mass_per_span_redistributed = 2 * A_cap_redistributed * rho_eq

m_caps_half_redistributed = np.sum(
    cap_mass_per_span_redistributed * integration_weights
)

mass_difference = (
    m_caps_half_redistributed - m_caps_half
)

baseline_outer_max_stress = np.max(
    sigma_cap[outer_region]
)

redistributed_outer_max_stress = np.max(
    sigma_redistributed[outer_region]
)

print(f"Baseline half-wing cap mass: {m_caps_half:.2f} kg")
print(f"Redistributed half-wing cap mass: {m_caps_half_redistributed:.2f} kg")
print(f"Cap-mass difference: {mass_difference:.4f} kg")

print(f"Baseline outer-region max stress: {baseline_outer_max_stress/1e6:.2f} MPa")
print(f"Redistributed outer-region max stress: {redistributed_outer_max_stress/1e6:.2f} MPa")

# %% [notebook cell 56]
mass_reduction_factor = tip_deflection_redistributed / tip_deflection_target

EI_mass_reduced = mass_reduction_factor * EI_redistributed

print(f"Required stiffness scaling factor: {mass_reduction_factor:.4f}")

# %% [notebook cell 57]
tip_deflection_mass_reduced = calculate_tip_deflection(EI_mass_reduced)

I_mass_reduced = EI_mass_reduced / E_eq

A_cap_mass_reduced = (2 * I_mass_reduced) / (box_height**2)

sigma_mass_reduced = bending_moment / (
    A_cap_mass_reduced * box_height
)

cap_mass_per_span_mass_reduced = (
    2 * A_cap_mass_reduced * rho_eq
)

m_caps_half_mass_reduced = np.sum(
    cap_mass_per_span_mass_reduced * integration_weights
)

m_caps_total_mass_reduced = 2 * m_caps_half_mass_reduced

m_wingbox_mass_reduced = (
    m_caps_total_mass_reduced + m_web_total
)

wingbox_mass_saving = (
    m_wingbox_total - m_wingbox_mass_reduced
)

wingbox_mass_saving_percent = (
    wingbox_mass_saving / m_wingbox_total
) * 100

print("HART-120 REDISTRIBUTED MASS-REDUCED DESIGN")
print("-----------------------------------------")

print(f"Baseline wingbox mass: {m_wingbox_total:.2f} kg")
print(f"Mass-reduced wingbox mass: {m_wingbox_mass_reduced:.2f} kg")
print(f"Wingbox mass saving: {wingbox_mass_saving:.2f} kg")
print(f"Wingbox mass saving: {wingbox_mass_saving_percent:.2f} %")

print()

print(f"Target tip deflection: {tip_deflection_target:.4f} m")
print(f"Final tip deflection: {tip_deflection_mass_reduced:.4f} m")

print()

print(f"Baseline max stress: {np.max(sigma_cap)/1e6:.2f} MPa")
print(f"Final max stress: {np.max(sigma_mass_reduced)/1e6:.2f} MPa")

# %% [notebook cell 58]
load_factor_maneuver = 2.5

lift_per_span_maneuver = load_factor_maneuver * lift_per_span

L_half_maneuver = np.trapezoid(lift_per_span_maneuver, y)

print(f"1-g half-wing lift: {L_half/1000:.2f} kN")
print(f"2.5-g half-wing lift: {L_half_maneuver/1000:.2f} kN")

# %% [notebook cell 59]
shear_force_maneuver = np.zeros_like(y)

for i in range(len(y)):
    shear_force_maneuver[i] = np.trapezoid(lift_per_span_maneuver[i:], y[i:])
print(f"2.5-g root shear force: {shear_force_maneuver[0]/1000:.2f} kN")
print(f"2.5-g tip shear force: {shear_force_maneuver[-1]/1000:.2f} kN")

# %% [notebook cell 60]
bending_moment_maneuver = np.zeros_like(y)



for i in range(len(y)):

    bending_moment_maneuver[i] = np.trapezoid(shear_force_maneuver[i:], y[i:] )



print(f"2.5-g root bending moment: {bending_moment_maneuver[0]/1e6:.3f} MN·m")

print(f"2.5-g tip bending moment: {bending_moment_maneuver[-1]/1e6:.3f} MN·m")

# %% [notebook cell 61]
sigma_maneuver = bending_moment_maneuver / (A_cap_mass_reduced * box_height)

max_stress_maneuver = np.max(sigma_maneuver)
max_stress_maneuver_index = np.argmax(sigma_maneuver)

print(f"1-g final max stress: {np.max(sigma_mass_reduced)/1e6:.2f} MPa")
print(f"2.5-g max stress: {max_stress_maneuver/1e6:.2f} MPa")
print(f"Critical span location: {y[max_stress_maneuver_index]:.2f} m")

# %% [notebook cell 62]
curvature_maneuver = (
    bending_moment_maneuver / EI_mass_reduced
)

slope_maneuver = np.zeros_like(y)

for i in range(1, len(y)):
    slope_maneuver[i] = np.trapezoid(
        curvature_maneuver[:i+1],
        y[:i+1]
    )

deflection_maneuver = np.zeros_like(y)

for i in range(1, len(y)):
    deflection_maneuver[i] = np.trapezoid(
        slope_maneuver[:i+1],
        y[:i+1]
    )

tip_deflection_maneuver = deflection_maneuver[-1]

print(f"1-g final tip deflection: {tip_deflection_mass_reduced:.4f} m")
print(f"2.5-g maneuver tip deflection: {tip_deflection_maneuver:.4f} m")
print(
    f"2.5-g deflection / half-span: "
    f"{100 * tip_deflection_maneuver / (b_wing/2):.2f} %"
)

# %% [notebook cell 63]
gust_velocity = 10.0       # m/s
lift_curve_slope = 2 * np.pi   # rad^-1
gust_angle_rad = np.arctan(gust_velocity / V_cruise)



gust_angle_deg = np.degrees(gust_angle_rad)



print(f"Gust velocity: {gust_velocity:.1f} m/s")

print(f"Incremental gust angle: {gust_angle_deg:.3f} deg")

# %% [notebook cell 64]
delta_Cl_gust = lift_curve_slope * gust_angle_rad

print(f"Incremental gust lift coefficient: {delta_Cl_gust:.4f}")

delta_lift_per_span_gust = (
    0.5
    * rho_cruise
    * V_cruise**2
    * chord
    * delta_Cl_gust
)

delta_L_half_gust = np.trapezoid(
    delta_lift_per_span_gust,
    y
)

print(f"Incremental half-wing gust lift: {delta_L_half_gust/1000:.2f} kN")

# %% [notebook cell 65]
lift_per_span_gust_total = lift_per_span + delta_lift_per_span_gust

L_half_gust_total = np.trapezoid(lift_per_span_gust_total,y)

gust_load_factor = L_half_gust_total / L_half

print(f"1-g half-wing lift: {L_half/1000:.2f} kN")
print(f"Incremental gust lift: {delta_L_half_gust/1000:.2f} kN")
print(f"Total gust half-wing lift: {L_half_gust_total/1000:.2f} kN")
print(f"Equivalent gust load factor: {gust_load_factor:.3f} g")

# %% [notebook cell 66]
shear_force_gust = np.zeros_like(y)



for i in range(len(y)):

    shear_force_gust[i] = np.trapezoid(lift_per_span_gust_total[i:],y[i:])

print(f"Gust root shear force: {shear_force_gust[0]/1000:.2f} kN")

print(f"Gust tip shear force: {shear_force_gust[-1]/1000:.2f} kN")

# %% [notebook cell 67]
bending_moment_gust = np.zeros_like(y)

for i in range(len(y)):
    bending_moment_gust[i] = np.trapezoid(shear_force_gust[i:] , y[i:])

print(f"1-g root bending moment: {bending_moment[0]/1e6:.3f} MN·m")
print(f"Gust root bending moment: {bending_moment_gust[0]/1e6:.3f} MN·m")
print(f"2.5-g root bending moment: {bending_moment_maneuver[0]/1e6:.3f} MN·m")

# %% [notebook cell 68]
sigma_gust = bending_moment_gust / (
    A_cap_mass_reduced * box_height
)

max_stress_gust = np.max(sigma_gust)
max_stress_gust_index = np.argmax(sigma_gust)

print(f"1-g max stress: {np.max(sigma_mass_reduced)/1e6:.2f} MPa")
print(f"Gust max stress: {max_stress_gust/1e6:.2f} MPa")
print(f"2.5-g max stress: {max_stress_maneuver/1e6:.2f} MPa")
print(f"Gust critical location: {y[max_stress_gust_index]:.2f} m")


curvature_gust = bending_moment_gust / EI_mass_reduced

slope_gust = np.zeros_like(y)

for i in range(1, len(y)):
    slope_gust[i] = np.trapezoid(
        curvature_gust[:i+1],
        y[:i+1]
    )

deflection_gust = np.zeros_like(y)

for i in range(1, len(y)):
    deflection_gust[i] = np.trapezoid(
        slope_gust[:i+1],
        y[:i+1]
    )

tip_deflection_gust = deflection_gust[-1]

print(f"1-g tip deflection: {tip_deflection_mass_reduced:.4f} m")
print(f"Gust tip deflection: {tip_deflection_gust:.4f} m")
print(f"2.5-g tip deflection: {tip_deflection_maneuver:.4f} m")

# %% [notebook cell 69]
inboard_gla_region = eta <= 0.40
outboard_gla_region = ((eta >= 0.65) & (eta <= 0.95))
load_shift_fraction = 0.25
lift_shift = load_shift_fraction * delta_L_half_gust
print(f"Load shifted per half-wing: {lift_shift/1000:.2f} kN")

# %% [notebook cell 70]
# -------------------------------------------------
# HART-120 — Gust Load Alleviation
# Zero-net-lift spanwise load redistribution
# -------------------------------------------------

inboard_gla_region = eta <= 0.40

outboard_gla_region = (
    (eta >= 0.65) &
    (eta <= 0.95)
)

load_shift_fraction = 0.25

lift_shift = (
    load_shift_fraction
    * delta_L_half_gust
)

print(f"Load shifted per half-wing: {lift_shift/1000:.2f} kN")


# Create control-effect shapes
inboard_shape = np.zeros_like(y)
outboard_shape = np.zeros_like(y)

inboard_shape[inboard_gla_region] = 1.0
outboard_shape[outboard_gla_region] = 1.0


# Integrate each shape so it can be normalized
inboard_shape_integral = np.trapezoid(
    inboard_shape,
    y
)

outboard_shape_integral = np.trapezoid(
    outboard_shape,
    y
)


# Add lift inboard and remove exactly the same lift outboard
delta_lift_per_span_gla = (
    lift_shift
    * inboard_shape
    / inboard_shape_integral

    -

    lift_shift
    * outboard_shape
    / outboard_shape_integral
)


# Verify zero net change in lift
net_gla_lift_change = np.trapezoid(
    delta_lift_per_span_gla,
    y
)

print(
    f"Net GLA lift change: "
    f"{net_gla_lift_change/1000:.6f} kN"
)


# Apply redistribution to original gust load
lift_per_span_gust_gla = (
    lift_per_span_gust_total
    + delta_lift_per_span_gla
)

L_half_gust_gla = np.trapezoid(
    lift_per_span_gust_gla,
    y
)

print()
print(f"Original gust half-wing lift: {L_half_gust_total/1000:.2f} kN")
print(f"GLA gust half-wing lift: {L_half_gust_gla/1000:.2f} kN")

# %% [notebook cell 71]
# -------------------------------------------------
# HART-120 — Gust Load Alleviation
# Shear force and bending moment after redistribution
# -------------------------------------------------

shear_force_gla = np.zeros_like(y)

for i in range(len(y)):
    shear_force_gla[i] = np.trapezoid(
        lift_per_span_gust_gla[i:],
        y[i:]
    )


bending_moment_gla = np.zeros_like(y)

for i in range(len(y)):
    bending_moment_gla[i] = np.trapezoid(
        shear_force_gla[i:],
        y[i:]
    )


root_moment_reduction = (
    bending_moment_gust[0]
    - bending_moment_gla[0]
)

root_moment_reduction_percent = (
    root_moment_reduction
    / bending_moment_gust[0]
) * 100


print(f"Original gust root shear: {shear_force_gust[0]/1000:.2f} kN")
print(f"GLA gust root shear: {shear_force_gla[0]/1000:.2f} kN")

print()

print(f"Original gust root moment: {bending_moment_gust[0]/1e6:.3f} MN·m")
print(f"GLA gust root moment: {bending_moment_gla[0]/1e6:.3f} MN·m")

print()

print(f"Root moment reduction: {root_moment_reduction/1e6:.3f} MN·m")
print(f"Root moment reduction: {root_moment_reduction_percent:.2f} %")

# %% [notebook cell 72]
# -------------------------------------------------
# HART-120 — GLA Structural Response
# Stress and deflection after gust-load alleviation
# -------------------------------------------------

# GLA stress
sigma_gla = bending_moment_gla / (
    A_cap_mass_reduced * box_height
)

max_stress_gla = np.max(sigma_gla)
max_stress_gla_index = np.argmax(sigma_gla)

stress_reduction_percent = (
    (max_stress_gust - max_stress_gla)
    / max_stress_gust
) * 100


print(f"Original gust max stress: {max_stress_gust/1e6:.2f} MPa")
print(f"GLA gust max stress: {max_stress_gla/1e6:.2f} MPa")
print(f"Stress reduction: {stress_reduction_percent:.2f} %")
print(f"Critical location: {y[max_stress_gla_index]:.2f} m")


# GLA curvature
curvature_gla = (
    bending_moment_gla / EI_mass_reduced
)

# GLA slope
slope_gla = np.zeros_like(y)

for i in range(1, len(y)):
    slope_gla[i] = np.trapezoid(
        curvature_gla[:i+1],
        y[:i+1]
    )


# GLA deflection
deflection_gla = np.zeros_like(y)

for i in range(1, len(y)):
    deflection_gla[i] = np.trapezoid(
        slope_gla[:i+1],
        y[:i+1]
    )

tip_deflection_gla = deflection_gla[-1]

deflection_reduction_percent = (
    (tip_deflection_gust - tip_deflection_gla)
    / tip_deflection_gust
) * 100


print()
print(f"Original gust tip deflection: {tip_deflection_gust:.4f} m")
print(f"GLA gust tip deflection: {tip_deflection_gla:.4f} m")
print(f"Tip deflection reduction: {deflection_reduction_percent:.2f} %")

# %% [notebook cell 73]
# -------------------------------------------------
# HART-120 — GLA Load-Shift Sensitivity Study
# Sweep 0–60% of incremental gust load
# -------------------------------------------------

import pandas as pd

load_shift_fractions = np.linspace(0.0, 0.60, 13)

root_moment_gla_results = []
max_stress_gla_results = []
tip_deflection_gla_results = []
root_shear_gla_results = []
total_half_lift_gla_results = []
min_span_load_results = []
net_lift_change_results = []


for fraction in load_shift_fractions:

    # Amount of incremental gust lift redistributed
    lift_shift_test = (
        fraction * delta_L_half_gust
    )

    # Zero-net-lift redistribution
    delta_lift_per_span_gla_test = (
        lift_shift_test
        * inboard_shape
        / inboard_shape_integral

        -

        lift_shift_test
        * outboard_shape
        / outboard_shape_integral
    )

    # New total gust loading
    lift_per_span_gla_test = (
        lift_per_span_gust_total
        + delta_lift_per_span_gla_test
    )

    # Total half-wing lift
    L_half_gla_test = np.trapezoid(
        lift_per_span_gla_test,
        y
    )

    # Check net lift conservation
    net_lift_change_test = (
        L_half_gla_test
        - L_half_gust_total
    )

    # -----------------------------
    # Shear force
    # -----------------------------
    shear_test = np.zeros_like(y)

    for i in range(len(y)):
        shear_test[i] = np.trapezoid(
            lift_per_span_gla_test[i:],
            y[i:]
        )

    # -----------------------------
    # Bending moment
    # -----------------------------
    moment_test = np.zeros_like(y)

    for i in range(len(y)):
        moment_test[i] = np.trapezoid(
            shear_test[i:],
            y[i:]
        )

    # -----------------------------
    # Stress
    # -----------------------------
    stress_test = (
        moment_test
        / (A_cap_mass_reduced * box_height)
    )

    # -----------------------------
    # Deflection
    # -----------------------------
    curvature_test = (
        moment_test / EI_mass_reduced
    )

    slope_test = np.zeros_like(y)

    for i in range(1, len(y)):
        slope_test[i] = np.trapezoid(
            curvature_test[:i+1],
            y[:i+1]
        )

    deflection_test = np.zeros_like(y)

    for i in range(1, len(y)):
        deflection_test[i] = np.trapezoid(
            slope_test[:i+1],
            y[:i+1]
        )

    # Store results
    root_moment_gla_results.append(
        moment_test[0]
    )

    max_stress_gla_results.append(
        np.max(stress_test)
    )

    tip_deflection_gla_results.append(
        deflection_test[-1]
    )

    root_shear_gla_results.append(
        shear_test[0]
    )

    total_half_lift_gla_results.append(
        L_half_gla_test
    )

    min_span_load_results.append(
        np.min(lift_per_span_gla_test)
    )

    net_lift_change_results.append(
        net_lift_change_test
    )


# Convert to arrays
root_moment_gla_results = np.array(root_moment_gla_results)
max_stress_gla_results = np.array(max_stress_gla_results)
tip_deflection_gla_results = np.array(tip_deflection_gla_results)
root_shear_gla_results = np.array(root_shear_gla_results)
total_half_lift_gla_results = np.array(total_half_lift_gla_results)
min_span_load_results = np.array(min_span_load_results)
net_lift_change_results = np.array(net_lift_change_results)


# -------------------------------------------------
# Performance reductions
# -------------------------------------------------

moment_reduction_percent = (
    (
        bending_moment_gust[0]
        - root_moment_gla_results
    )
    / bending_moment_gust[0]
) * 100


stress_reduction_percent = (
    (
        max_stress_gust
        - max_stress_gla_results
    )
    / max_stress_gust
) * 100


deflection_reduction_percent = (
    (
        tip_deflection_gust
        - tip_deflection_gla_results
    )
    / tip_deflection_gust
) * 100


# -------------------------------------------------
# Simple physical feasibility check
# Avoid negative upward spanwise loading
# -------------------------------------------------

load_distribution_feasible = (
    min_span_load_results >= 0.0
)


# -------------------------------------------------
# Results table
# -------------------------------------------------

gla_results_df = pd.DataFrame({

    "Load_Shift_%":
        load_shift_fractions * 100,

    "Root_Shear_kN":
        root_shear_gla_results / 1000,

    "Root_Moment_MNm":
        root_moment_gla_results / 1e6,

    "Moment_Reduction_%":
        moment_reduction_percent,

    "Max_Stress_MPa":
        max_stress_gla_results / 1e6,

    "Stress_Reduction_%":
        stress_reduction_percent,

    "Tip_Deflection_m":
        tip_deflection_gla_results,

    "Deflection_Reduction_%":
        deflection_reduction_percent,

    "Minimum_Local_Load_kNm":
        min_span_load_results / 1000,

    "Net_Lift_Change_kN":
        net_lift_change_results / 1000,

    "Load_Distribution_Feasible":
        load_distribution_feasible
})


print(
    gla_results_df.round(3).to_string(index=False)
)


# -------------------------------------------------
# Find best feasible load-shift fraction
# -------------------------------------------------

feasible_indices = np.where(
    load_distribution_feasible
)[0]

best_index = feasible_indices[
    np.argmin(
        root_moment_gla_results[
            feasible_indices
        ]
    )
]


best_fraction = (
    load_shift_fractions[best_index]
)

best_root_moment = (
    root_moment_gla_results[best_index]
)

best_stress = (
    max_stress_gla_results[best_index]
)

best_tip_deflection = (
    tip_deflection_gla_results[best_index]
)


print()
print("HART-120 GLA SENSITIVITY — BEST FEASIBLE CASE")
print("---------------------------------------------")

print(
    f"Load shift fraction: "
    f"{best_fraction*100:.1f} %"
)

print(
    f"Root bending moment: "
    f"{best_root_moment/1e6:.3f} MN·m"
)

print(
    f"Root moment reduction: "
    f"{moment_reduction_percent[best_index]:.2f} %"
)

print(
    f"Maximum stress: "
    f"{best_stress/1e6:.2f} MPa"
)

print(
    f"Stress reduction: "
    f"{stress_reduction_percent[best_index]:.2f} %"
)

print(
    f"Tip deflection: "
    f"{best_tip_deflection:.4f} m"
)

print(
    f"Tip deflection reduction: "
    f"{deflection_reduction_percent[best_index]:.2f} %"
)

print(
    f"Minimum local span load: "
    f"{min_span_load_results[best_index]/1000:.2f} kN/m"
)

print(
    f"Net lift change: "
    f"{net_lift_change_results[best_index]/1000:.6f} kN"
)

# %% [notebook cell 74]
# -------------------------------------------------
# HART-120 — Maneuver Load Alleviation Sensitivity
# Redistribute part of the incremental 2.5-g load
# while preserving total maneuver lift
# -------------------------------------------------

# Incremental maneuver load above the 1-g condition
delta_lift_per_span_maneuver = (
    lift_per_span_maneuver - lift_per_span
)

delta_L_half_maneuver = np.trapezoid(
    delta_lift_per_span_maneuver,
    y
)

print(
    f"Incremental maneuver half-wing lift above 1-g: "
    f"{delta_L_half_maneuver/1000:.2f} kN"
)


# Sweep maneuver load redistribution
maneuver_shift_fractions = np.linspace(0.0, 0.30, 31)

mla_root_moment_results = []
mla_max_stress_results = []
mla_tip_deflection_results = []
mla_root_shear_results = []
mla_total_lift_results = []
mla_min_local_load_results = []
mla_net_lift_change_results = []


for fraction in maneuver_shift_fractions:

    # Amount of incremental maneuver lift shifted
    lift_shift_mla = (
        fraction * delta_L_half_maneuver
    )

    # Zero-net-lift redistribution
    delta_lift_per_span_mla = (
        lift_shift_mla
        * inboard_shape
        / inboard_shape_integral

        -

        lift_shift_mla
        * outboard_shape
        / outboard_shape_integral
    )

    # Alleviated maneuver load distribution
    lift_per_span_mla = (
        lift_per_span_maneuver
        + delta_lift_per_span_mla
    )

    # Total half-wing maneuver lift
    L_half_mla = np.trapezoid(
        lift_per_span_mla,
        y
    )

    net_lift_change_mla = (
        L_half_mla - L_half_maneuver
    )


    # ---------------------------------------------
    # Shear force
    # ---------------------------------------------

    shear_mla = np.zeros_like(y)

    for i in range(len(y)):
        shear_mla[i] = np.trapezoid(
            lift_per_span_mla[i:],
            y[i:]
        )


    # ---------------------------------------------
    # Bending moment
    # ---------------------------------------------

    moment_mla = np.zeros_like(y)

    for i in range(len(y)):
        moment_mla[i] = np.trapezoid(
            shear_mla[i:],
            y[i:]
        )


    # ---------------------------------------------
    # Stress
    # ---------------------------------------------

    stress_mla = (
        moment_mla
        / (A_cap_mass_reduced * box_height)
    )


    # ---------------------------------------------
    # Curvature
    # ---------------------------------------------

    curvature_mla = (
        moment_mla / EI_mass_reduced
    )


    # ---------------------------------------------
    # Slope
    # ---------------------------------------------

    slope_mla = np.zeros_like(y)

    for i in range(1, len(y)):
        slope_mla[i] = np.trapezoid(
            curvature_mla[:i+1],
            y[:i+1]
        )


    # ---------------------------------------------
    # Deflection
    # ---------------------------------------------

    deflection_mla = np.zeros_like(y)

    for i in range(1, len(y)):
        deflection_mla[i] = np.trapezoid(
            slope_mla[:i+1],
            y[:i+1]
        )


    # ---------------------------------------------
    # Store results
    # ---------------------------------------------

    mla_root_shear_results.append(
        shear_mla[0]
    )

    mla_root_moment_results.append(
        moment_mla[0]
    )

    mla_max_stress_results.append(
        np.max(stress_mla)
    )

    mla_tip_deflection_results.append(
        deflection_mla[-1]
    )

    mla_total_lift_results.append(
        L_half_mla
    )

    mla_min_local_load_results.append(
        np.min(lift_per_span_mla)
    )

    mla_net_lift_change_results.append(
        net_lift_change_mla
    )


# Convert lists to NumPy arrays
mla_root_shear_results = np.array(
    mla_root_shear_results
)

mla_root_moment_results = np.array(
    mla_root_moment_results
)

mla_max_stress_results = np.array(
    mla_max_stress_results
)

mla_tip_deflection_results = np.array(
    mla_tip_deflection_results
)

mla_total_lift_results = np.array(
    mla_total_lift_results
)

mla_min_local_load_results = np.array(
    mla_min_local_load_results
)

mla_net_lift_change_results = np.array(
    mla_net_lift_change_results
)


# -------------------------------------------------
# Performance reductions
# -------------------------------------------------

mla_moment_reduction_percent = (
    (
        bending_moment_maneuver[0]
        - mla_root_moment_results
    )
    / bending_moment_maneuver[0]
) * 100


mla_stress_reduction_percent = (
    (
        max_stress_maneuver
        - mla_max_stress_results
    )
    / max_stress_maneuver
) * 100


mla_deflection_reduction_percent = (
    (
        tip_deflection_maneuver
        - mla_tip_deflection_results
    )
    / tip_deflection_maneuver
) * 100


# -------------------------------------------------
# Physical feasibility
# Prevent negative upward local loading
# -------------------------------------------------

mla_feasible = (
    mla_min_local_load_results >= -1e-6
)


# -------------------------------------------------
# Results table
# -------------------------------------------------

mla_results_df = pd.DataFrame({

    "Load_Shift_%":
        maneuver_shift_fractions * 100,

    "Root_Shear_kN":
        mla_root_shear_results / 1000,

    "Root_Moment_MNm":
        mla_root_moment_results / 1e6,

    "Moment_Reduction_%":
        mla_moment_reduction_percent,

    "Max_Stress_MPa":
        mla_max_stress_results / 1e6,

    "Stress_Reduction_%":
        mla_stress_reduction_percent,

    "Tip_Deflection_m":
        mla_tip_deflection_results,

    "Deflection_Reduction_%":
        mla_deflection_reduction_percent,

    "Minimum_Local_Load_kNm":
        mla_min_local_load_results / 1000,

    "Net_Lift_Change_kN":
        mla_net_lift_change_results / 1000,

    "Feasible":
        mla_feasible
})


print(
    mla_results_df.round(3).to_string(index=False)
)


# -------------------------------------------------
# Best feasible maneuver-load-alleviation case
# -------------------------------------------------

feasible_indices_mla = np.where(
    mla_feasible
)[0]

best_mla_index = feasible_indices_mla[
    np.argmin(
        mla_root_moment_results[
            feasible_indices_mla
        ]
    )
]


best_mla_fraction = (
    maneuver_shift_fractions[best_mla_index]
)

best_mla_root_moment = (
    mla_root_moment_results[best_mla_index]
)

best_mla_stress = (
    mla_max_stress_results[best_mla_index]
)

best_mla_tip_deflection = (
    mla_tip_deflection_results[best_mla_index]
)


print()
print("HART-120 MANEUVER LOAD ALLEVIATION — BEST FEASIBLE CASE")
print("-------------------------------------------------------")

print(
    f"Load shift fraction: "
    f"{best_mla_fraction*100:.1f} %"
)

print(
    f"Root bending moment: "
    f"{best_mla_root_moment/1e6:.3f} MN·m"
)

print(
    f"Root moment reduction: "
    f"{mla_moment_reduction_percent[best_mla_index]:.2f} %"
)

print(
    f"Maximum stress: "
    f"{best_mla_stress/1e6:.2f} MPa"
)

print(
    f"Stress reduction: "
    f"{mla_stress_reduction_percent[best_mla_index]:.2f} %"
)

print(
    f"Tip deflection: "
    f"{best_mla_tip_deflection:.4f} m"
)

print(
    f"Tip deflection reduction: "
    f"{mla_deflection_reduction_percent[best_mla_index]:.2f} %"
)

print(
    f"Minimum local load: "
    f"{mla_min_local_load_results[best_mla_index]/1000:.3f} kN/m"
)

print(
    f"Net lift change: "
    f"{mla_net_lift_change_results[best_mla_index]/1000:.6f} kN"
)

# %% [notebook cell 75]
# -------------------------------------------------
# HART-120 — Wing-Web Load Envelope
# Compare uncontrolled vs active-load-alleviated cases
# -------------------------------------------------

def calculate_shear_and_moment(load_per_span):

    shear = np.zeros_like(y)

    for i in range(len(y)):
        shear[i] = np.trapezoid(
            load_per_span[i:],
            y[i:]
        )

    moment = np.zeros_like(y)

    for i in range(len(y)):
        moment[i] = np.trapezoid(
            shear[i:],
            y[i:]
        )

    return shear, moment


# -------------------------------------------------
# Reconstruct BEST GLA case
# -------------------------------------------------

lift_shift_best_gla = (
    best_fraction
    * delta_L_half_gust
)

delta_lift_best_gla = (
    lift_shift_best_gla
    * inboard_shape
    / inboard_shape_integral

    -

    lift_shift_best_gla
    * outboard_shape
    / outboard_shape_integral
)

lift_best_gla = (
    lift_per_span_gust_total
    + delta_lift_best_gla
)

shear_best_gla, moment_best_gla = (
    calculate_shear_and_moment(
        lift_best_gla
    )
)


# -------------------------------------------------
# Reconstruct BEST maneuver-load-alleviation case
# -------------------------------------------------

lift_shift_best_mla = (
    best_mla_fraction
    * delta_L_half_maneuver
)

delta_lift_best_mla = (
    lift_shift_best_mla
    * inboard_shape
    / inboard_shape_integral

    -

    lift_shift_best_mla
    * outboard_shape
    / outboard_shape_integral
)

lift_best_mla = (
    lift_per_span_maneuver
    + delta_lift_best_mla
)

shear_best_mla, moment_best_mla = (
    calculate_shear_and_moment(
        lift_best_mla
    )
)


# -------------------------------------------------
# Web shear stress using CURRENT web thickness
#
# tau = V / (2 * t_web * h_box)
# -------------------------------------------------

tau_cruise = np.abs(shear_force) / (
    2 * web_thickness * box_height
)

tau_gust = np.abs(shear_force_gust) / (
    2 * web_thickness * box_height
)

tau_gla = np.abs(shear_best_gla) / (
    2 * web_thickness * box_height
)

tau_maneuver = np.abs(shear_force_maneuver) / (
    2 * web_thickness * box_height
)

tau_mla = np.abs(shear_best_mla) / (
    2 * web_thickness * box_height
)


# -------------------------------------------------
# Summary table
# -------------------------------------------------

web_load_cases = pd.DataFrame({

    "Load_Case": [
        "1-g Cruise",
        "10 m/s Gust",
        "Gust + GLA",
        "2.5-g Maneuver",
        "Maneuver + MLA"
    ],

    "Root_Shear_kN": [
        shear_force[0] / 1000,
        shear_force_gust[0] / 1000,
        shear_best_gla[0] / 1000,
        shear_force_maneuver[0] / 1000,
        shear_best_mla[0] / 1000
    ],

    "Root_Moment_MNm": [
        bending_moment[0] / 1e6,
        bending_moment_gust[0] / 1e6,
        moment_best_gla[0] / 1e6,
        bending_moment_maneuver[0] / 1e6,
        moment_best_mla[0] / 1e6
    ],

    "Max_Web_Shear_MPa": [
        np.max(tau_cruise) / 1e6,
        np.max(tau_gust) / 1e6,
        np.max(tau_gla) / 1e6,
        np.max(tau_maneuver) / 1e6,
        np.max(tau_mla) / 1e6
    ]
})

print("HART-120 WEB LOAD-CASE CHECK")
print("----------------------------")
print(
    web_load_cases.round(3).to_string(index=False)
)


# -------------------------------------------------
# UNCONTROLLED design shear envelope
# Cruise + Gust + Maneuver
# -------------------------------------------------

shear_envelope_uncontrolled = np.maximum.reduce([
    np.abs(shear_force),
    np.abs(shear_force_gust),
    np.abs(shear_force_maneuver)
])


# -------------------------------------------------
# CONTROLLED design shear envelope
# Cruise + best GLA + best MLA
# -------------------------------------------------

shear_envelope_controlled = np.maximum.reduce([
    np.abs(shear_force),
    np.abs(shear_best_gla),
    np.abs(shear_best_mla)
])


# -------------------------------------------------
# Required web thickness
#
# t_web = V / (2 * tau_allow * h_box)
# -------------------------------------------------

web_thickness_uncontrolled_required = (
    shear_envelope_uncontrolled
    / (2 * tau_allow * box_height)
)

web_thickness_controlled_required = (
    shear_envelope_controlled
    / (2 * tau_allow * box_height)
)


# Apply minimum manufacturing gauge
web_thickness_uncontrolled = np.maximum(
    web_thickness_uncontrolled_required,
    web_thickness_min
)

web_thickness_controlled = np.maximum(
    web_thickness_controlled_required,
    web_thickness_min
)


# -------------------------------------------------
# Web mass
# Two webs per wing
# -------------------------------------------------

web_mass_per_span_uncontrolled = (
    2
    * web_thickness_uncontrolled
    * box_height
    * rho_eq
)

web_mass_per_span_controlled = (
    2
    * web_thickness_controlled
    * box_height
    * rho_eq
)


m_web_half_uncontrolled = np.trapezoid(
    web_mass_per_span_uncontrolled,
    y
)

m_web_half_controlled = np.trapezoid(
    web_mass_per_span_controlled,
    y
)


m_web_total_uncontrolled = (
    2 * m_web_half_uncontrolled
)

m_web_total_controlled = (
    2 * m_web_half_controlled
)


web_mass_saving_control = (
    m_web_total_uncontrolled
    - m_web_total_controlled
)

web_mass_saving_control_percent = (
    web_mass_saving_control
    / m_web_total_uncontrolled
) * 100


# -------------------------------------------------
# Output
# -------------------------------------------------

print()
print("HART-120 WEB SIZING — LOAD ENVELOPE")
print("-----------------------------------")

print(
    f"Original 1-g-sized web mass: "
    f"{m_web_total:.2f} kg"
)

print(
    f"Uncontrolled load-envelope web mass: "
    f"{m_web_total_uncontrolled:.2f} kg"
)

print(
    f"Controlled load-envelope web mass: "
    f"{m_web_total_controlled:.2f} kg"
)

print(
    f"Web mass saving from load alleviation: "
    f"{web_mass_saving_control:.2f} kg"
)

print(
    f"Web mass saving from load alleviation: "
    f"{web_mass_saving_control_percent:.2f} %"
)

print()

print(
    f"Uncontrolled root web thickness: "
    f"{web_thickness_uncontrolled[0]*1000:.2f} mm"
)

print(
    f"Controlled root web thickness: "
    f"{web_thickness_controlled[0]*1000:.2f} mm"
)

print(
    f"Minimum web gauge: "
    f"{web_thickness_min*1000:.2f} mm"
)

# %% [notebook cell 76]
# -------------------------------------------------
# HART-120 — Spar-Cap Sizing Against Load Envelope
# Compare uncontrolled vs active-load-alleviated wing
# -------------------------------------------------

# Uncontrolled bending-moment envelope
moment_envelope_uncontrolled = np.maximum.reduce([
    np.abs(bending_moment),
    np.abs(bending_moment_gust),
    np.abs(bending_moment_maneuver)
])


# Controlled bending-moment envelope
moment_envelope_controlled = np.maximum.reduce([
    np.abs(bending_moment),
    np.abs(moment_best_gla),
    np.abs(moment_best_mla)
])


# -------------------------------------------------
# Effective spar-cap design allowable sweep
# -------------------------------------------------

sigma_allow_values = np.arange(
    180e6,
    301e6,
    10e6
)


uncontrolled_cap_mass_results = []
controlled_cap_mass_results = []

uncontrolled_wingbox_mass_results = []
controlled_wingbox_mass_results = []

cap_mass_saving_results = []
wingbox_mass_saving_results = []

cap_mass_saving_percent_results = []
wingbox_mass_saving_percent_results = []


for sigma_allow_design in sigma_allow_values:

    # -------------------------------------------------
    # Strength-required spar-cap area
    #
    # sigma = M / (A * h)
    #
    # Therefore:
    # A_required = M / (sigma_allow * h)
    # -------------------------------------------------

    A_cap_strength_uncontrolled = (
        moment_envelope_uncontrolled
        / (sigma_allow_design * box_height)
    )

    A_cap_strength_controlled = (
        moment_envelope_controlled
        / (sigma_allow_design * box_height)
    )


    # -------------------------------------------------
    # Final design must satisfy BOTH:
    #
    # 1. stiffness requirement
    # 2. strength requirement
    #
    # Current A_cap_mass_reduced is our
    # stiffness-driven minimum area.
    # -------------------------------------------------

    A_cap_design_uncontrolled = np.maximum(
        A_cap_mass_reduced,
        A_cap_strength_uncontrolled
    )

    A_cap_design_controlled = np.maximum(
        A_cap_mass_reduced,
        A_cap_strength_controlled
    )


    # -------------------------------------------------
    # Cap mass per unit span
    # Two caps per wing
    # -------------------------------------------------

    cap_mass_per_span_uncontrolled = (
        2
        * A_cap_design_uncontrolled
        * rho_eq
    )

    cap_mass_per_span_controlled = (
        2
        * A_cap_design_controlled
        * rho_eq
    )


    # -------------------------------------------------
    # Total cap mass — both wings
    # -------------------------------------------------

    m_caps_half_uncontrolled = np.sum(
        cap_mass_per_span_uncontrolled
        * integration_weights
    )

    m_caps_half_controlled = np.sum(
        cap_mass_per_span_controlled
        * integration_weights
    )


    m_caps_total_uncontrolled = (
        2 * m_caps_half_uncontrolled
    )

    m_caps_total_controlled = (
        2 * m_caps_half_controlled
    )


    # -------------------------------------------------
    # Total simplified wingbox mass
    #
    # Caps + previously envelope-sized webs
    # -------------------------------------------------

    m_wingbox_uncontrolled_envelope = (
        m_caps_total_uncontrolled
        + m_web_total_uncontrolled
    )

    m_wingbox_controlled_envelope = (
        m_caps_total_controlled
        + m_web_total_controlled
    )


    # -------------------------------------------------
    # Mass benefit from active load alleviation
    # -------------------------------------------------

    cap_mass_saving = (
        m_caps_total_uncontrolled
        - m_caps_total_controlled
    )

    wingbox_mass_saving = (
        m_wingbox_uncontrolled_envelope
        - m_wingbox_controlled_envelope
    )


    cap_mass_saving_percent = (
        cap_mass_saving
        / m_caps_total_uncontrolled
    ) * 100

    wingbox_mass_saving_percent = (
        wingbox_mass_saving
        / m_wingbox_uncontrolled_envelope
    ) * 100


    # Store results
    uncontrolled_cap_mass_results.append(
        m_caps_total_uncontrolled
    )

    controlled_cap_mass_results.append(
        m_caps_total_controlled
    )

    uncontrolled_wingbox_mass_results.append(
        m_wingbox_uncontrolled_envelope
    )

    controlled_wingbox_mass_results.append(
        m_wingbox_controlled_envelope
    )

    cap_mass_saving_results.append(
        cap_mass_saving
    )

    wingbox_mass_saving_results.append(
        wingbox_mass_saving
    )

    cap_mass_saving_percent_results.append(
        cap_mass_saving_percent
    )

    wingbox_mass_saving_percent_results.append(
        wingbox_mass_saving_percent
    )


# Convert to NumPy arrays
uncontrolled_cap_mass_results = np.array(
    uncontrolled_cap_mass_results
)

controlled_cap_mass_results = np.array(
    controlled_cap_mass_results
)

uncontrolled_wingbox_mass_results = np.array(
    uncontrolled_wingbox_mass_results
)

controlled_wingbox_mass_results = np.array(
    controlled_wingbox_mass_results
)

cap_mass_saving_results = np.array(
    cap_mass_saving_results
)

wingbox_mass_saving_results = np.array(
    wingbox_mass_saving_results
)

cap_mass_saving_percent_results = np.array(
    cap_mass_saving_percent_results
)

wingbox_mass_saving_percent_results = np.array(
    wingbox_mass_saving_percent_results
)


# -------------------------------------------------
# Results table
# -------------------------------------------------

load_alleviation_mass_df = pd.DataFrame({

    "Allowable_Stress_MPa":
        sigma_allow_values / 1e6,

    "Uncontrolled_Cap_Mass_kg":
        uncontrolled_cap_mass_results,

    "Controlled_Cap_Mass_kg":
        controlled_cap_mass_results,

    "Cap_Mass_Saving_kg":
        cap_mass_saving_results,

    "Cap_Mass_Saving_%":
        cap_mass_saving_percent_results,

    "Uncontrolled_Wingbox_Mass_kg":
        uncontrolled_wingbox_mass_results,

    "Controlled_Wingbox_Mass_kg":
        controlled_wingbox_mass_results,

    "Wingbox_Mass_Saving_kg":
        wingbox_mass_saving_results,

    "Wingbox_Mass_Saving_%":
        wingbox_mass_saving_percent_results
})


print("HART-120 LOAD ALLEVIATION — STRUCTURAL MASS BENEFIT")
print("---------------------------------------------------")

print(
    load_alleviation_mass_df
    .round(2)
    .to_string(index=False)
)

# %% [notebook cell 77]
# -------------------------------------------------
# HART-120 — Control Authority Assessment
# Convert required load redistribution into
# equivalent local change in lift coefficient
# -------------------------------------------------

q_cruise = (
    0.5
    * rho_cruise
    * V_cruise**2
)


# -------------------------------------------------
# BEST GUST LOAD ALLEVIATION CASE
# -------------------------------------------------

delta_Cl_gla_distribution = (
    delta_lift_best_gla
    / (q_cruise * chord)
)


max_positive_delta_Cl_gla = np.max(
    delta_Cl_gla_distribution
)

max_negative_delta_Cl_gla = np.min(
    delta_Cl_gla_distribution
)


# -------------------------------------------------
# BEST MANEUVER LOAD ALLEVIATION CASE
# -------------------------------------------------

delta_Cl_mla_distribution = (
    delta_lift_best_mla
    / (q_cruise * chord)
)


max_positive_delta_Cl_mla = np.max(
    delta_Cl_mla_distribution
)

max_negative_delta_Cl_mla = np.min(
    delta_Cl_mla_distribution
)


# -------------------------------------------------
# Output
# -------------------------------------------------

print("HART-120 CONTROL AUTHORITY REQUIREMENT")
print("--------------------------------------")

print(f"Dynamic pressure: {q_cruise/1000:.2f} kPa")

print()

print("GUST LOAD ALLEVIATION")
print(
    f"Maximum positive ΔCl: "
    f"{max_positive_delta_Cl_gla:.3f}"
)

print(
    f"Maximum negative ΔCl: "
    f"{max_negative_delta_Cl_gla:.3f}"
)

print()

print("MANEUVER LOAD ALLEVIATION")
print(
    f"Maximum positive ΔCl: "
    f"{max_positive_delta_Cl_mla:.3f}"
)

print(
    f"Maximum negative ΔCl: "
    f"{max_negative_delta_Cl_mla:.3f}"
)


# -------------------------------------------------
# Spanwise control-demand plots
# -------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    delta_Cl_gla_distribution
)

plt.axhline(
    0.0,
    linestyle="--"
)

plt.xlabel("Normalized Half-Span, η")
plt.ylabel("Required ΔCl")
plt.title(
    "HART-120 — Gust Load Alleviation Control Demand"
)

plt.grid(True)
plt.show()


plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    delta_Cl_mla_distribution
)

plt.axhline(
    0.0,
    linestyle="--"
)

plt.xlabel("Normalized Half-Span, η")
plt.ylabel("Required ΔCl")
plt.title(
    "HART-120 — Maneuver Load Alleviation Control Demand"
)

plt.grid(True)
plt.show()

# %% [notebook cell 78]
# ============================================================
# HART-120 — CONTROL-AUTHORITY-CONSTRAINED LOAD ALLEVIATION
#
# Improvements over previous model:
# 1. Smooth spanwise control influence instead of step changes
# 2. Explicit maximum |ΔCl| constraint
# 3. Non-negative local lift constraint
# 4. Zero-net-lift redistribution maintained
# 5. Gust and maneuver cases evaluated separately
#
# NOTE:
# ΔCl limits below are sensitivity values, NOT certification limits.
# ============================================================


# ------------------------------------------------------------
# 1. Smooth control influence functions
# ------------------------------------------------------------

def smooth_control_shape(eta, start, end):

    shape = np.zeros_like(eta)

    mask = (
        (eta >= start)
        & (eta <= end)
    )

    xi = (
        (eta[mask] - start)
        / (end - start)
    )

    # Smooth sine-shaped aerodynamic influence
    shape[mask] = np.sin(
        np.pi * xi
    )

    return shape


# Generic conceptual control zones
inboard_shape_smooth = smooth_control_shape(
    eta,
    0.00,
    0.40
)

outboard_shape_smooth = smooth_control_shape(
    eta,
    0.65,
    0.95
)


# Normalize influence functions
inboard_smooth_integral = np.trapezoid(
    inboard_shape_smooth,
    y
)

outboard_smooth_integral = np.trapezoid(
    outboard_shape_smooth,
    y
)


print("SMOOTH CONTROL INFLUENCE CHECK")
print("------------------------------")

print(
    f"Inboard shape integral: "
    f"{inboard_smooth_integral:.4f} m"
)

print(
    f"Outboard shape integral: "
    f"{outboard_smooth_integral:.4f} m"
)


# ------------------------------------------------------------
# 2. Structural-response helper function
# ------------------------------------------------------------

def calculate_structural_response(
    load_distribution
):

    # Shear
    shear = np.zeros_like(y)

    for i in range(len(y)):
        shear[i] = np.trapezoid(
            load_distribution[i:],
            y[i:]
        )


    # Bending moment
    moment = np.zeros_like(y)

    for i in range(len(y)):
        moment[i] = np.trapezoid(
            shear[i:],
            y[i:]
        )


    # Spar-cap stress
    stress = (
        moment
        / (
            A_cap_mass_reduced
            * box_height
        )
    )


    # Curvature
    curvature = (
        moment
        / EI_mass_reduced
    )


    # Slope
    slope = np.zeros_like(y)

    for i in range(1, len(y)):
        slope[i] = np.trapezoid(
            curvature[:i+1],
            y[:i+1]
        )


    # Deflection
    deflection = np.zeros_like(y)

    for i in range(1, len(y)):
        deflection[i] = np.trapezoid(
            slope[:i+1],
            y[:i+1]
        )


    return (
        shear,
        moment,
        stress,
        deflection
    )


# ------------------------------------------------------------
# 3. Load-alleviation evaluation function
# ------------------------------------------------------------

def evaluate_load_alleviation(
    base_load_distribution,
    incremental_half_lift,
    shift_fractions,
    deltaCl_limit
):

    # Uncontrolled structural response
    (
        shear_base,
        moment_base,
        stress_base,
        deflection_base
    ) = calculate_structural_response(
        base_load_distribution
    )


    base_root_moment = (
        moment_base[0]
    )

    base_max_stress = (
        np.max(stress_base)
    )

    base_tip_deflection = (
        deflection_base[-1]
    )


    results = []


    for fraction in shift_fractions:

        # ----------------------------------------------------
        # Amount of aerodynamic load redistributed
        # ----------------------------------------------------

        lift_shift_candidate = (
            fraction
            * incremental_half_lift
        )


        # ----------------------------------------------------
        # Smooth zero-net-lift redistribution
        # ----------------------------------------------------

        delta_lift_candidate = (

            lift_shift_candidate
            * inboard_shape_smooth
            / inboard_smooth_integral

            -

            lift_shift_candidate
            * outboard_shape_smooth
            / outboard_smooth_integral
        )


        # ----------------------------------------------------
        # Equivalent control demand
        #
        # ΔCl = ΔL' / (q c)
        # ----------------------------------------------------

        deltaCl_candidate = (
            delta_lift_candidate
            / (
                q_cruise
                * chord
            )
        )


        max_abs_deltaCl = np.max(
            np.abs(
                deltaCl_candidate
            )
        )


        # ----------------------------------------------------
        # Controlled aerodynamic loading
        # ----------------------------------------------------

        controlled_load = (
            base_load_distribution
            + delta_lift_candidate
        )


        # ----------------------------------------------------
        # Zero-net-lift validation
        # ----------------------------------------------------

        net_lift_change = np.trapezoid(
            delta_lift_candidate,
            y
        )


        # ----------------------------------------------------
        # Local loading constraint
        # ----------------------------------------------------

        minimum_local_load = np.min(
            controlled_load
        )


        # ----------------------------------------------------
        # Structural response
        # ----------------------------------------------------

        (
            shear_controlled,
            moment_controlled,
            stress_controlled,
            deflection_controlled
        ) = calculate_structural_response(
            controlled_load
        )


        root_moment = (
            moment_controlled[0]
        )

        max_stress = np.max(
            stress_controlled
        )

        tip_deflection = (
            deflection_controlled[-1]
        )


        # ----------------------------------------------------
        # Performance improvements
        # ----------------------------------------------------

        moment_reduction = (
            (
                base_root_moment
                - root_moment
            )
            / base_root_moment
        ) * 100


        stress_reduction = (
            (
                base_max_stress
                - max_stress
            )
            / base_max_stress
        ) * 100


        deflection_reduction = (
            (
                base_tip_deflection
                - tip_deflection
            )
            / base_tip_deflection
        ) * 100


        # ----------------------------------------------------
        # Feasibility constraints
        # ----------------------------------------------------

        authority_feasible = (
            max_abs_deltaCl
            <= deltaCl_limit + 1e-10
        )

        loading_feasible = (
            minimum_local_load
            >= -1e-6
        )

        feasible = (
            authority_feasible
            and loading_feasible
        )


        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------

        results.append({

            "Load_Shift_%":
                fraction * 100,

            "Root_Shear_kN":
                shear_controlled[0] / 1000,

            "Root_Moment_MNm":
                root_moment / 1e6,

            "Moment_Reduction_%":
                moment_reduction,

            "Max_Stress_MPa":
                max_stress / 1e6,

            "Stress_Reduction_%":
                stress_reduction,

            "Tip_Deflection_m":
                tip_deflection,

            "Deflection_Reduction_%":
                deflection_reduction,

            "Max_Abs_DeltaCl":
                max_abs_deltaCl,

            "Minimum_Local_Load_kNm":
                minimum_local_load / 1000,

            "Net_Lift_Change_kN":
                net_lift_change / 1000,

            "Authority_Feasible":
                authority_feasible,

            "Loading_Feasible":
                loading_feasible,

            "Overall_Feasible":
                feasible
        })


    results_df = pd.DataFrame(
        results
    )


    # --------------------------------------------------------
    # Best feasible solution
    # --------------------------------------------------------

    feasible_df = results_df[
        results_df[
            "Overall_Feasible"
        ]
    ]


    best_index = (
        feasible_df[
            "Root_Moment_MNm"
        ].idxmin()
    )


    best_result = (
        results_df.loc[
            best_index
        ]
    )


    return (
        results_df,
        best_result
    )


# ------------------------------------------------------------
# 4. Control-authority sensitivity values
#
# These are conceptual sensitivity limits,
# not regulatory/certification values.
# ------------------------------------------------------------

deltaCl_authority_limits = np.array([
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    1.00,
    1.20
])


# Fine load-shift sweeps
gust_shift_sweep = np.linspace(
    0.0,
    0.60,
    121
)

maneuver_shift_sweep = np.linspace(
    0.0,
    0.40,
    161
)


authority_summary = []


# ------------------------------------------------------------
# 5. Sweep control authority
# ------------------------------------------------------------

for deltaCl_limit in deltaCl_authority_limits:

    # -------------------------
    # Gust
    # -------------------------

    gust_control_df, gust_best = (
        evaluate_load_alleviation(
            lift_per_span_gust_total,
            delta_L_half_gust,
            gust_shift_sweep,
            deltaCl_limit
        )
    )


    # -------------------------
    # Maneuver
    # -------------------------

    maneuver_control_df, maneuver_best = (
        evaluate_load_alleviation(
            lift_per_span_maneuver,
            delta_L_half_maneuver,
            maneuver_shift_sweep,
            deltaCl_limit
        )
    )


    authority_summary.append({

        "DeltaCl_Limit":
            deltaCl_limit,

        "Gust_Best_Shift_%":
            gust_best[
                "Load_Shift_%"
            ],

        "Gust_Root_Moment_MNm":
            gust_best[
                "Root_Moment_MNm"
            ],

        "Gust_Moment_Reduction_%":
            gust_best[
                "Moment_Reduction_%"
            ],

        "Gust_Max_Stress_MPa":
            gust_best[
                "Max_Stress_MPa"
            ],

        "Gust_Tip_Deflection_m":
            gust_best[
                "Tip_Deflection_m"
            ],

        "Gust_Max_Abs_DeltaCl":
            gust_best[
                "Max_Abs_DeltaCl"
            ],

        "Maneuver_Best_Shift_%":
            maneuver_best[
                "Load_Shift_%"
            ],

        "Maneuver_Root_Moment_MNm":
            maneuver_best[
                "Root_Moment_MNm"
            ],

        "Maneuver_Moment_Reduction_%":
            maneuver_best[
                "Moment_Reduction_%"
            ],

        "Maneuver_Max_Stress_MPa":
            maneuver_best[
                "Max_Stress_MPa"
            ],

        "Maneuver_Tip_Deflection_m":
            maneuver_best[
                "Tip_Deflection_m"
            ],

        "Maneuver_Max_Abs_DeltaCl":
            maneuver_best[
                "Max_Abs_DeltaCl"
            ]
    })


authority_summary_df = pd.DataFrame(
    authority_summary
)


# ------------------------------------------------------------
# 6. Print results
# ------------------------------------------------------------

print()
print(
    "HART-120 CONTROL-AUTHORITY-CONSTRAINED "
    "LOAD ALLEVIATION"
)

print(
    "------------------------------------------------"
)

print(
    authority_summary_df
    .round(3)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 7. Plot — attainable load redistribution
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    deltaCl_authority_limits,
    authority_summary_df[
        "Gust_Best_Shift_%"
    ],
    marker="o",
    label="Gust"
)

plt.plot(
    deltaCl_authority_limits,
    authority_summary_df[
        "Maneuver_Best_Shift_%"
    ],
    marker="o",
    label="Maneuver"
)

plt.xlabel(
    "Maximum Allowed |ΔCl|"
)

plt.ylabel(
    "Best Feasible Load Redistribution (%)"
)

plt.title(
    "HART-120 — Control Authority vs "
    "Achievable Load Redistribution"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 8. Plot — root bending-moment benefit
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    deltaCl_authority_limits,
    authority_summary_df[
        "Gust_Moment_Reduction_%"
    ],
    marker="o",
    label="Gust"
)

plt.plot(
    deltaCl_authority_limits,
    authority_summary_df[
        "Maneuver_Moment_Reduction_%"
    ],
    marker="o",
    label="Maneuver"
)

plt.xlabel(
    "Maximum Allowed |ΔCl|"
)

plt.ylabel(
    "Root Bending Moment Reduction (%)"
)

plt.title(
    "HART-120 — Load Alleviation Benefit "
    "Under Control-Authority Limits"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 79]
# ============================================================
# HART-120 — CONTROL SURFACE DEFLECTION AUTHORITY STUDY
#
# Convert aerodynamic control demand ΔCl into equivalent
# control-surface deflection:
#
# ΔCl = (dCl/dδ) * δ
#
# Sensitivity study only — effectiveness values are conceptual,
# not tied to a specific aircraft/control surface.
# ============================================================


# ------------------------------------------------------------
# 1. Control-surface effectiveness sensitivity
# ΔCl generated per degree of surface deflection
# ------------------------------------------------------------

control_effectiveness_values = np.array([
    0.02,
    0.03,
    0.04,
    0.05,
    0.06
])  # ΔCl / degree


# Maximum actuator/control-surface deflection
deflection_limits_deg = np.array([
    5.0,
    10.0,
    15.0,
    20.0
])


control_surface_results = []


# ------------------------------------------------------------
# 2. Sweep effectiveness and deflection limits
# ------------------------------------------------------------

for cl_delta_per_deg in control_effectiveness_values:

    for delta_limit_deg in deflection_limits_deg:

        # Maximum achievable aerodynamic authority
        deltaCl_limit_surface = (
            cl_delta_per_deg
            * delta_limit_deg
        )


        # ----------------------------------------------------
        # Gust case
        # ----------------------------------------------------

        gust_surface_df, gust_surface_best = (
            evaluate_load_alleviation(
                lift_per_span_gust_total,
                delta_L_half_gust,
                gust_shift_sweep,
                deltaCl_limit_surface
            )
        )


        # ----------------------------------------------------
        # Maneuver case
        # ----------------------------------------------------

        maneuver_surface_df, maneuver_surface_best = (
            evaluate_load_alleviation(
                lift_per_span_maneuver,
                delta_L_half_maneuver,
                maneuver_shift_sweep,
                deltaCl_limit_surface
            )
        )


        # ----------------------------------------------------
        # Required actual deflection for best cases
        # ----------------------------------------------------

        gust_required_deflection_deg = (
            gust_surface_best[
                "Max_Abs_DeltaCl"
            ]
            / cl_delta_per_deg
        )

        maneuver_required_deflection_deg = (
            maneuver_surface_best[
                "Max_Abs_DeltaCl"
            ]
            / cl_delta_per_deg
        )


        # ----------------------------------------------------
        # Store results
        # ----------------------------------------------------

        control_surface_results.append({

            "dCl_dDelta_per_deg":
                cl_delta_per_deg,

            "Deflection_Limit_deg":
                delta_limit_deg,

            "DeltaCl_Authority":
                deltaCl_limit_surface,

            "Gust_Load_Shift_%":
                gust_surface_best[
                    "Load_Shift_%"
                ],

            "Gust_Root_Moment_MNm":
                gust_surface_best[
                    "Root_Moment_MNm"
                ],

            "Gust_Moment_Reduction_%":
                gust_surface_best[
                    "Moment_Reduction_%"
                ],

            "Gust_Required_Deflection_deg":
                gust_required_deflection_deg,

            "Maneuver_Load_Shift_%":
                maneuver_surface_best[
                    "Load_Shift_%"
                ],

            "Maneuver_Root_Moment_MNm":
                maneuver_surface_best[
                    "Root_Moment_MNm"
                ],

            "Maneuver_Moment_Reduction_%":
                maneuver_surface_best[
                    "Moment_Reduction_%"
                ],

            "Maneuver_Required_Deflection_deg":
                maneuver_required_deflection_deg
        })


control_surface_df = pd.DataFrame(
    control_surface_results
)


# ------------------------------------------------------------
# 3. Print table
# ------------------------------------------------------------

print()
print(
    "HART-120 CONTROL-SURFACE AUTHORITY STUDY"
)

print(
    "----------------------------------------"
)

print(
    control_surface_df
    .round(3)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 4. Find best configuration under <= 15 deg deflection
# ------------------------------------------------------------

practical_deflection_limit = 15.0

candidate_configs = control_surface_df[
    control_surface_df[
        "Deflection_Limit_deg"
    ] <= practical_deflection_limit
]


best_gust_surface_index = (
    candidate_configs[
        "Gust_Root_Moment_MNm"
    ].idxmin()
)

best_maneuver_surface_index = (
    candidate_configs[
        "Maneuver_Root_Moment_MNm"
    ].idxmin()
)


best_gust_surface = (
    control_surface_df.loc[
        best_gust_surface_index
    ]
)

best_maneuver_surface = (
    control_surface_df.loc[
        best_maneuver_surface_index
    ]
)


# ------------------------------------------------------------
# 5. Best-case outputs
# ------------------------------------------------------------

print()
print(
    "BEST GUST CONTROL-SURFACE CONFIGURATION"
)
print(
    "---------------------------------------"
)

print(
    f"dCl/dδ: "
    f"{best_gust_surface['dCl_dDelta_per_deg']:.3f} per deg"
)

print(
    f"Allowed deflection: "
    f"{best_gust_surface['Deflection_Limit_deg']:.1f} deg"
)

print(
    f"Required deflection: "
    f"{best_gust_surface['Gust_Required_Deflection_deg']:.2f} deg"
)

print(
    f"Load redistribution: "
    f"{best_gust_surface['Gust_Load_Shift_%']:.1f} %"
)

print(
    f"Root moment reduction: "
    f"{best_gust_surface['Gust_Moment_Reduction_%']:.2f} %"
)


print()
print(
    "BEST MANEUVER CONTROL-SURFACE CONFIGURATION"
)
print(
    "-------------------------------------------"
)

print(
    f"dCl/dδ: "
    f"{best_maneuver_surface['dCl_dDelta_per_deg']:.3f} per deg"
)

print(
    f"Allowed deflection: "
    f"{best_maneuver_surface['Deflection_Limit_deg']:.1f} deg"
)

print(
    f"Required deflection: "
    f"{best_maneuver_surface['Maneuver_Required_Deflection_deg']:.2f} deg"
)

print(
    f"Load redistribution: "
    f"{best_maneuver_surface['Maneuver_Load_Shift_%']:.1f} %"
)

print(
    f"Root moment reduction: "
    f"{best_maneuver_surface['Maneuver_Moment_Reduction_%']:.2f} %"
)


# ------------------------------------------------------------
# 6. Plot — Gust benefit vs available surface deflection
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

for effectiveness in control_effectiveness_values:

    subset = control_surface_df[
        control_surface_df[
            "dCl_dDelta_per_deg"
        ] == effectiveness
    ]

    plt.plot(
        subset["Deflection_Limit_deg"],
        subset["Gust_Moment_Reduction_%"],
        marker="o",
        label=f"dCl/dδ = {effectiveness:.02f}/deg"
    )

plt.xlabel(
    "Maximum Control Surface Deflection (deg)"
)

plt.ylabel(
    "Gust Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — Gust Alleviation vs Control Surface Authority"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 7. Plot — Maneuver benefit vs available surface deflection
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

for effectiveness in control_effectiveness_values:

    subset = control_surface_df[
        control_surface_df[
            "dCl_dDelta_per_deg"
        ] == effectiveness
    ]

    plt.plot(
        subset["Deflection_Limit_deg"],
        subset["Maneuver_Moment_Reduction_%"],
        marker="o",
        label=f"dCl/dδ = {effectiveness:.02f}/deg"
    )

plt.xlabel(
    "Maximum Control Surface Deflection (deg)"
)

plt.ylabel(
    "Maneuver Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — Maneuver Alleviation vs Control Surface Authority"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 80]
# ============================================================
# HART-120 — DYNAMIC GUST + ACTUATOR RESPONSE
#
# Industrial problem addressed:
# A static controller may show good load alleviation, but a real
# actuator has finite response time, rate limit and deflection limit.
#
# This reduced-order model checks whether the control surface can
# react quickly enough during a transient 1-cosine gust.
#
# NOTE:
# This is a conceptual dynamic sensitivity model, not a
# certification gust model.
# ============================================================


# ------------------------------------------------------------
# 1. Selected control-surface configuration
# ------------------------------------------------------------

cl_delta_selected = 0.06        # ΔCl per degree
max_deflection_deg = 15.0       # deg

best_gust_shift_fraction = 0.39

best_gust_required_deflection = (
    best_gust_surface[
        "Gust_Required_Deflection_deg"
    ]
)

print("SELECTED GUST CONTROL SYSTEM")
print("----------------------------")

print(
    f"Control effectiveness: "
    f"{cl_delta_selected:.3f} ΔCl/deg"
)

print(
    f"Maximum deflection: "
    f"{max_deflection_deg:.1f} deg"
)

print(
    f"Static required deflection: "
    f"{best_gust_required_deflection:.2f} deg"
)

print(
    f"Static gust load redistribution: "
    f"{best_gust_shift_fraction*100:.1f} %"
)


# ------------------------------------------------------------
# 2. Reconstruct full static GLA redistribution
# ------------------------------------------------------------

full_gust_lift_shift = (
    best_gust_shift_fraction
    * delta_L_half_gust
)

delta_lift_gla_full = (

    full_gust_lift_shift
    * inboard_shape_smooth
    / inboard_smooth_integral

    -

    full_gust_lift_shift
    * outboard_shape_smooth
    / outboard_smooth_integral
)


# ------------------------------------------------------------
# 3. Define transient 1-cosine gust
#
# Gust distance = 2H
# Peak gust occurs at distance H
# ------------------------------------------------------------

gust_gradient_H = 60.0     # m
gust_peak_velocity = 10.0  # m/s

gust_duration = (
    2 * gust_gradient_H
    / V_cruise
)

dt = 0.002

time = np.arange(
    0.0,
    gust_duration + dt,
    dt
)

distance = (
    V_cruise * time
)


gust_velocity_time = (
    gust_peak_velocity
    / 2
    * (
        1
        - np.cos(
            np.pi
            * distance
            / gust_gradient_H
        )
    )
)


# Ensure zero outside gust region
gust_velocity_time[
    distance > 2 * gust_gradient_H
] = 0.0


gust_scale_time = (
    gust_velocity_time
    / gust_peak_velocity
)


print()
print("DYNAMIC GUST")
print("------------")

print(
    f"Gust gradient H: "
    f"{gust_gradient_H:.1f} m"
)

print(
    f"Aircraft speed: "
    f"{V_cruise:.2f} m/s"
)

print(
    f"Gust duration: "
    f"{gust_duration:.3f} s"
)

print(
    f"Peak gust velocity: "
    f"{np.max(gust_velocity_time):.2f} m/s"
)


# ------------------------------------------------------------
# 4. Actuator dynamic assumptions
# ------------------------------------------------------------

actuator_time_constant = 0.12   # seconds
actuator_rate_limit = 80.0      # deg/s
sensor_control_delay = 0.04     # seconds


delay_steps = int(
    sensor_control_delay / dt
)


# ------------------------------------------------------------
# 5. Gust control command
# ------------------------------------------------------------

command_deflection = (
    best_gust_required_deflection
    * gust_scale_time
)

command_deflection = np.clip(
    command_deflection,
    -max_deflection_deg,
    max_deflection_deg
)


# Add control-system delay
delayed_command = np.zeros_like(
    command_deflection
)

if delay_steps > 0:

    delayed_command[delay_steps:] = (
        command_deflection[:-delay_steps]
    )

else:

    delayed_command[:] = (
        command_deflection
    )


# ------------------------------------------------------------
# 6. First-order actuator + rate limit
#
# dδ/dt = (δ_command - δ_actual) / tau
# ------------------------------------------------------------

actual_deflection = np.zeros_like(
    time
)


for k in range(1, len(time)):

    desired_rate = (
        delayed_command[k]
        - actual_deflection[k-1]
    ) / actuator_time_constant

    limited_rate = np.clip(
        desired_rate,
        -actuator_rate_limit,
        actuator_rate_limit
    )

    actual_deflection[k] = (
        actual_deflection[k-1]
        + limited_rate * dt
    )

    actual_deflection[k] = np.clip(
        actual_deflection[k],
        -max_deflection_deg,
        max_deflection_deg
    )


# ------------------------------------------------------------
# 7. Convert actuator response into achieved GLA authority
# ------------------------------------------------------------

actuator_authority_ratio = (
    actual_deflection
    / best_gust_required_deflection
)

actuator_authority_ratio = np.clip(
    actuator_authority_ratio,
    0.0,
    1.0
)


# ------------------------------------------------------------
# 8. Dynamic structural response
# ------------------------------------------------------------

root_moment_uncontrolled_time = []
root_moment_controlled_time = []

root_shear_uncontrolled_time = []
root_shear_controlled_time = []

max_stress_uncontrolled_time = []
max_stress_controlled_time = []

tip_deflection_uncontrolled_time = []
tip_deflection_controlled_time = []


for k in range(len(time)):

    gust_scale = (
        gust_scale_time[k]
    )


    # --------------------------------------------------------
    # Instantaneous gust loading without control
    # --------------------------------------------------------

    load_uncontrolled = (
        lift_per_span
        + gust_scale
        * delta_lift_per_span_gust
    )


    # --------------------------------------------------------
    # Desired GLA redistribution scales with gust intensity
    # --------------------------------------------------------

    ideal_control_load = (
        gust_scale
        * delta_lift_gla_full
    )


    # --------------------------------------------------------
    # Actual load redistribution limited by actuator response
    # --------------------------------------------------------

    if gust_scale > 1e-8:

        tracking_ratio = (
            actuator_authority_ratio[k]
            / gust_scale
        )

        tracking_ratio = np.clip(
            tracking_ratio,
            0.0,
            1.0
        )

    else:

        tracking_ratio = 0.0


    actual_control_load = (
        tracking_ratio
        * ideal_control_load
    )


    load_controlled = (
        load_uncontrolled
        + actual_control_load
    )


    # --------------------------------------------------------
    # Structural response — uncontrolled
    # --------------------------------------------------------

    (
        shear_u,
        moment_u,
        stress_u,
        deflection_u
    ) = calculate_structural_response(
        load_uncontrolled
    )


    # --------------------------------------------------------
    # Structural response — controlled
    # --------------------------------------------------------

    (
        shear_c,
        moment_c,
        stress_c,
        deflection_c
    ) = calculate_structural_response(
        load_controlled
    )


    # Store
    root_shear_uncontrolled_time.append(
        shear_u[0]
    )

    root_shear_controlled_time.append(
        shear_c[0]
    )

    root_moment_uncontrolled_time.append(
        moment_u[0]
    )

    root_moment_controlled_time.append(
        moment_c[0]
    )

    max_stress_uncontrolled_time.append(
        np.max(stress_u)
    )

    max_stress_controlled_time.append(
        np.max(stress_c)
    )

    tip_deflection_uncontrolled_time.append(
        deflection_u[-1]
    )

    tip_deflection_controlled_time.append(
        deflection_c[-1]
    )


# ------------------------------------------------------------
# 9. Convert results to arrays
# ------------------------------------------------------------

root_shear_uncontrolled_time = np.array(
    root_shear_uncontrolled_time
)

root_shear_controlled_time = np.array(
    root_shear_controlled_time
)

root_moment_uncontrolled_time = np.array(
    root_moment_uncontrolled_time
)

root_moment_controlled_time = np.array(
    root_moment_controlled_time
)

max_stress_uncontrolled_time = np.array(
    max_stress_uncontrolled_time
)

max_stress_controlled_time = np.array(
    max_stress_controlled_time
)

tip_deflection_uncontrolled_time = np.array(
    tip_deflection_uncontrolled_time
)

tip_deflection_controlled_time = np.array(
    tip_deflection_controlled_time
)


# ------------------------------------------------------------
# 10. Peak dynamic results
# ------------------------------------------------------------

peak_moment_uncontrolled = np.max(
    root_moment_uncontrolled_time
)

peak_moment_controlled = np.max(
    root_moment_controlled_time
)

dynamic_moment_reduction = (
    (
        peak_moment_uncontrolled
        - peak_moment_controlled
    )
    / peak_moment_uncontrolled
) * 100


peak_stress_uncontrolled = np.max(
    max_stress_uncontrolled_time
)

peak_stress_controlled = np.max(
    max_stress_controlled_time
)

dynamic_stress_reduction = (
    (
        peak_stress_uncontrolled
        - peak_stress_controlled
    )
    / peak_stress_uncontrolled
) * 100


peak_deflection_uncontrolled = np.max(
    tip_deflection_uncontrolled_time
)

peak_deflection_controlled = np.max(
    tip_deflection_controlled_time
)

dynamic_deflection_reduction = (
    (
        peak_deflection_uncontrolled
        - peak_deflection_controlled
    )
    / peak_deflection_uncontrolled
) * 100


# ------------------------------------------------------------
# 11. Output
# ------------------------------------------------------------

print()
print("HART-120 DYNAMIC GUST LOAD ALLEVIATION")
print("--------------------------------------")

print(
    f"Actuator time constant: "
    f"{actuator_time_constant:.3f} s"
)

print(
    f"Rate limit: "
    f"{actuator_rate_limit:.1f} deg/s"
)

print(
    f"Control delay: "
    f"{sensor_control_delay:.3f} s"
)

print(
    f"Peak actuator deflection: "
    f"{np.max(actual_deflection):.2f} deg"
)

print()

print(
    f"Peak uncontrolled root moment: "
    f"{peak_moment_uncontrolled/1e6:.3f} MN·m"
)

print(
    f"Peak controlled root moment: "
    f"{peak_moment_controlled/1e6:.3f} MN·m"
)

print(
    f"Dynamic root-moment reduction: "
    f"{dynamic_moment_reduction:.2f} %"
)

print()

print(
    f"Peak uncontrolled stress: "
    f"{peak_stress_uncontrolled/1e6:.2f} MPa"
)

print(
    f"Peak controlled stress: "
    f"{peak_stress_controlled/1e6:.2f} MPa"
)

print(
    f"Dynamic stress reduction: "
    f"{dynamic_stress_reduction:.2f} %"
)

print()

print(
    f"Peak uncontrolled tip deflection: "
    f"{peak_deflection_uncontrolled:.4f} m"
)

print(
    f"Peak controlled tip deflection: "
    f"{peak_deflection_controlled:.4f} m"
)

print(
    f"Dynamic tip-deflection reduction: "
    f"{dynamic_deflection_reduction:.2f} %"
)


# ------------------------------------------------------------
# 12. Plot — gust profile
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time,
    gust_velocity_time
)

plt.xlabel("Time (s)")
plt.ylabel("Vertical Gust Velocity (m/s)")
plt.title("HART-120 — 1-Cosine Gust Profile")
plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 13. Plot — commanded vs actual control-surface motion
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time,
    command_deflection,
    label="Commanded"
)

plt.plot(
    time,
    actual_deflection,
    label="Actual"
)

plt.xlabel("Time (s)")
plt.ylabel("Control Surface Deflection (deg)")
plt.title("HART-120 — Actuator Dynamic Response")
plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 14. Plot — dynamic root bending moment
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time,
    root_moment_uncontrolled_time / 1e6,
    label="Uncontrolled"
)

plt.plot(
    time,
    root_moment_controlled_time / 1e6,
    label="Active GLA"
)

plt.xlabel("Time (s)")
plt.ylabel("Root Bending Moment (MN·m)")
plt.title("HART-120 — Dynamic Gust Root Bending Moment")
plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 15. Plot — dynamic tip deflection
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time,
    tip_deflection_uncontrolled_time,
    label="Uncontrolled"
)

plt.plot(
    time,
    tip_deflection_controlled_time,
    label="Active GLA"
)

plt.xlabel("Time (s)")
plt.ylabel("Tip Deflection (m)")
plt.title("HART-120 — Dynamic Gust Wing Deflection")
plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 81]
# ============================================================
# HART-120 — CORRECTED DYNAMIC GUST + ACTUATOR RESPONSE
#
# Actual aerodynamic control load now follows the ACTUAL
# control-surface deflection directly.
# ============================================================


# ------------------------------------------------------------
# Storage
# ------------------------------------------------------------

root_moment_uncontrolled_time = []
root_moment_controlled_time = []

root_shear_uncontrolled_time = []
root_shear_controlled_time = []

max_stress_uncontrolled_time = []
max_stress_controlled_time = []

tip_deflection_uncontrolled_time = []
tip_deflection_controlled_time = []

net_lift_controlled_time = []


# ------------------------------------------------------------
# Time marching
# ------------------------------------------------------------

for k in range(len(time)):

    gust_scale = gust_scale_time[k]


    # --------------------------------------------------------
    # Uncontrolled instantaneous gust loading
    # --------------------------------------------------------

    load_uncontrolled = (
        lift_per_span
        + gust_scale
        * delta_lift_per_span_gust
    )


    # --------------------------------------------------------
    # Actual actuator authority
    #
    # 0   -> no load redistribution
    # 1   -> full static GLA redistribution
    # --------------------------------------------------------

    actual_control_scale = (
        actual_deflection[k]
        / best_gust_required_deflection
    )


    # --------------------------------------------------------
    # Aerodynamic load generated by actual surface motion
    # --------------------------------------------------------

    actual_control_load = (
        actual_control_scale
        * delta_lift_gla_full
    )


    # --------------------------------------------------------
    # Controlled wing loading
    # --------------------------------------------------------

    load_controlled = (
        load_uncontrolled
        + actual_control_load
    )


    # --------------------------------------------------------
    # Structural response — uncontrolled
    # --------------------------------------------------------

    (
        shear_u,
        moment_u,
        stress_u,
        deflection_u
    ) = calculate_structural_response(
        load_uncontrolled
    )


    # --------------------------------------------------------
    # Structural response — controlled
    # --------------------------------------------------------

    (
        shear_c,
        moment_c,
        stress_c,
        deflection_c
    ) = calculate_structural_response(
        load_controlled
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    root_shear_uncontrolled_time.append(
        shear_u[0]
    )

    root_shear_controlled_time.append(
        shear_c[0]
    )

    root_moment_uncontrolled_time.append(
        moment_u[0]
    )

    root_moment_controlled_time.append(
        moment_c[0]
    )

    max_stress_uncontrolled_time.append(
        np.max(stress_u)
    )

    max_stress_controlled_time.append(
        np.max(stress_c)
    )

    tip_deflection_uncontrolled_time.append(
        deflection_u[-1]
    )

    tip_deflection_controlled_time.append(
        deflection_c[-1]
    )

    net_lift_controlled_time.append(
        np.trapezoid(
            load_controlled,
            y
        )
    )


# ------------------------------------------------------------
# Convert to arrays
# ------------------------------------------------------------

root_shear_uncontrolled_time = np.array(
    root_shear_uncontrolled_time
)

root_shear_controlled_time = np.array(
    root_shear_controlled_time
)

root_moment_uncontrolled_time = np.array(
    root_moment_uncontrolled_time
)

root_moment_controlled_time = np.array(
    root_moment_controlled_time
)

max_stress_uncontrolled_time = np.array(
    max_stress_uncontrolled_time
)

max_stress_controlled_time = np.array(
    max_stress_controlled_time
)

tip_deflection_uncontrolled_time = np.array(
    tip_deflection_uncontrolled_time
)

tip_deflection_controlled_time = np.array(
    tip_deflection_controlled_time
)

net_lift_controlled_time = np.array(
    net_lift_controlled_time
)


# ------------------------------------------------------------
# Peak results
# ------------------------------------------------------------

peak_moment_uncontrolled = np.max(
    root_moment_uncontrolled_time
)

peak_moment_controlled = np.max(
    root_moment_controlled_time
)

dynamic_moment_reduction = (
    (
        peak_moment_uncontrolled
        - peak_moment_controlled
    )
    / peak_moment_uncontrolled
) * 100


peak_stress_uncontrolled = np.max(
    max_stress_uncontrolled_time
)

peak_stress_controlled = np.max(
    max_stress_controlled_time
)

dynamic_stress_reduction = (
    (
        peak_stress_uncontrolled
        - peak_stress_controlled
    )
    / peak_stress_uncontrolled
) * 100


peak_deflection_uncontrolled = np.max(
    tip_deflection_uncontrolled_time
)

peak_deflection_controlled = np.max(
    tip_deflection_controlled_time
)

dynamic_deflection_reduction = (
    (
        peak_deflection_uncontrolled
        - peak_deflection_controlled
    )
    / peak_deflection_uncontrolled
) * 100


# ------------------------------------------------------------
# Peak locations in time
# ------------------------------------------------------------

peak_moment_u_index = np.argmax(
    root_moment_uncontrolled_time
)

peak_moment_c_index = np.argmax(
    root_moment_controlled_time
)


# ------------------------------------------------------------
# Output
# ------------------------------------------------------------

print()
print("HART-120 CORRECTED DYNAMIC GUST LOAD ALLEVIATION")
print("------------------------------------------------")

print(
    f"Peak actuator deflection: "
    f"{np.max(actual_deflection):.2f} deg"
)

print()

print(
    f"Peak uncontrolled root moment: "
    f"{peak_moment_uncontrolled/1e6:.3f} MN·m"
)

print(
    f"Peak controlled root moment: "
    f"{peak_moment_controlled/1e6:.3f} MN·m"
)

print(
    f"Dynamic root-moment reduction: "
    f"{dynamic_moment_reduction:.2f} %"
)

print()

print(
    f"Uncontrolled moment peak time: "
    f"{time[peak_moment_u_index]:.3f} s"
)

print(
    f"Controlled moment peak time: "
    f"{time[peak_moment_c_index]:.3f} s"
)

print()

print(
    f"Peak uncontrolled stress: "
    f"{peak_stress_uncontrolled/1e6:.2f} MPa"
)

print(
    f"Peak controlled stress: "
    f"{peak_stress_controlled/1e6:.2f} MPa"
)

print(
    f"Dynamic stress reduction: "
    f"{dynamic_stress_reduction:.2f} %"
)

print()

print(
    f"Peak uncontrolled tip deflection: "
    f"{peak_deflection_uncontrolled:.4f} m"
)

print(
    f"Peak controlled tip deflection: "
    f"{peak_deflection_controlled:.4f} m"
)

print(
    f"Dynamic tip-deflection reduction: "
    f"{dynamic_deflection_reduction:.2f} %"
)

print()

print(
    f"Maximum root-shear difference: "
    f"{np.max(np.abs(
        root_shear_controlled_time
        - root_shear_uncontrolled_time
    ))/1000:.6f} kN"
)

# %% [notebook cell 82]
# ============================================================
# HART-120 — FIRST-MODE FLEXIBLE-WING DYNAMIC GUST RESPONSE
#
# Adds:
# 1. First bending mode
# 2. Generalized modal mass
# 3. Generalized modal stiffness
# 4. Structural damping
# 5. Newmark-beta transient integration
# 6. Extended post-gust response
# 7. Dynamic GLA vs uncontrolled comparison
#
# Reduced-order conceptual aeroelastic model
# ============================================================


# ------------------------------------------------------------
# 1. Extended simulation time
# Allow wing and actuator to respond AFTER gust passes
# ------------------------------------------------------------

post_gust_time = 2.0       # s

time_dyn = np.arange(
    0.0,
    gust_duration + post_gust_time + dt,
    dt
)

distance_dyn = (
    V_cruise * time_dyn
)


# ------------------------------------------------------------
# 2. Rebuild 1-cosine gust over extended time
# ------------------------------------------------------------

gust_velocity_dyn = np.zeros_like(
    time_dyn
)

gust_active = (
    distance_dyn <= 2 * gust_gradient_H
)

gust_velocity_dyn[gust_active] = (
    gust_peak_velocity
    / 2
    * (
        1
        - np.cos(
            np.pi
            * distance_dyn[gust_active]
            / gust_gradient_H
        )
    )
)

gust_scale_dyn = (
    gust_velocity_dyn
    / gust_peak_velocity
)


# ------------------------------------------------------------
# 3. Control-surface command over extended time
# ------------------------------------------------------------

command_deflection_dyn = (
    best_gust_required_deflection
    * gust_scale_dyn
)

command_deflection_dyn = np.clip(
    command_deflection_dyn,
    -max_deflection_deg,
    max_deflection_deg
)


# ------------------------------------------------------------
# 4. Sensor/control delay
# ------------------------------------------------------------

delay_steps_dyn = int(
    sensor_control_delay / dt
)

delayed_command_dyn = np.zeros_like(
    command_deflection_dyn
)

if delay_steps_dyn > 0:

    delayed_command_dyn[
        delay_steps_dyn:
    ] = command_deflection_dyn[
        :-delay_steps_dyn
    ]

else:

    delayed_command_dyn[:] = (
        command_deflection_dyn
    )


# ------------------------------------------------------------
# 5. Actuator dynamics
# ------------------------------------------------------------

actual_deflection_dyn = np.zeros_like(
    time_dyn
)

for k in range(1, len(time_dyn)):

    desired_rate = (
        delayed_command_dyn[k]
        - actual_deflection_dyn[k-1]
    ) / actuator_time_constant

    limited_rate = np.clip(
        desired_rate,
        -actuator_rate_limit,
        actuator_rate_limit
    )

    actual_deflection_dyn[k] = (
        actual_deflection_dyn[k-1]
        + limited_rate * dt
    )

    actual_deflection_dyn[k] = np.clip(
        actual_deflection_dyn[k],
        -max_deflection_deg,
        max_deflection_deg
    )


# ------------------------------------------------------------
# 6. First cantilever bending mode
#
# Uniform Euler-Bernoulli cantilever mode used as an
# admissible shape for the variable-stiffness HART-120 wing.
# ------------------------------------------------------------

half_span = (
    b_wing / 2
)

eta_mode = (
    y / half_span
)

lambda_1 = 1.875104068711961

sigma_mode = (
    np.cosh(lambda_1)
    + np.cos(lambda_1)
) / (
    np.sinh(lambda_1)
    + np.sin(lambda_1)
)


phi = (
    np.cosh(
        lambda_1 * eta_mode
    )
    -
    np.cos(
        lambda_1 * eta_mode
    )
    -
    sigma_mode
    * (
        np.sinh(
            lambda_1 * eta_mode
        )
        -
        np.sin(
            lambda_1 * eta_mode
        )
    )
)


# Normalize mode so tip amplitude = 1
phi = (
    phi / phi[-1]
)


# ------------------------------------------------------------
# 7. Analytical second derivative of mode shape
# ------------------------------------------------------------

phi_tip_raw = (
    np.cosh(lambda_1)
    -
    np.cos(lambda_1)
    -
    sigma_mode
    * (
        np.sinh(lambda_1)
        -
        np.sin(lambda_1)
    )
)


phi_second = (
    (lambda_1 / half_span)**2
    * (
        np.cosh(
            lambda_1 * eta_mode
        )
        +
        np.cos(
            lambda_1 * eta_mode
        )
        -
        sigma_mode
        * (
            np.sinh(
                lambda_1 * eta_mode
            )
            +
            np.sin(
                lambda_1 * eta_mode
            )
        )
    )
    / phi_tip_raw
)


# ------------------------------------------------------------
# 8. Dynamic wingbox mass distribution
#
# Spar caps + controlled-envelope webs
# ------------------------------------------------------------

dynamic_mass_per_span = (
    cap_mass_per_span_mass_reduced
    + web_mass_per_span_controlled
)


# ------------------------------------------------------------
# 9. Generalized modal mass
#
# M* = integral m(y) phi(y)^2 dy
# ------------------------------------------------------------

modal_mass = np.trapezoid(
    dynamic_mass_per_span
    * phi**2,
    y
)


# ------------------------------------------------------------
# 10. Generalized modal stiffness
#
# K* = integral EI(y) [phi''(y)]^2 dy
# ------------------------------------------------------------

modal_stiffness = np.trapezoid(
    EI_mass_reduced
    * phi_second**2,
    y
)


# ------------------------------------------------------------
# 11. Natural frequency
# ------------------------------------------------------------

omega_n = np.sqrt(
    modal_stiffness
    / modal_mass
)

frequency_hz = (
    omega_n
    / (2 * np.pi)
)


# ------------------------------------------------------------
# 12. Structural damping
# ------------------------------------------------------------

damping_ratio = 0.03

modal_damping = (
    2
    * damping_ratio
    * omega_n
    * modal_mass
)


print()
print("HART-120 FIRST BENDING MODE")
print("---------------------------")

print(
    f"Generalized modal mass: "
    f"{modal_mass:.2f} kg"
)

print(
    f"Generalized modal stiffness: "
    f"{modal_stiffness/1e6:.2f} MN/m"
)

print(
    f"Estimated first bending frequency: "
    f"{frequency_hz:.3f} Hz"
)

print(
    f"Structural damping ratio: "
    f"{damping_ratio*100:.1f} %"
)


# ------------------------------------------------------------
# 13. Build time-dependent generalized aerodynamic forces
# ------------------------------------------------------------

generalized_force_uncontrolled = np.zeros_like(
    time_dyn
)

generalized_force_controlled = np.zeros_like(
    time_dyn
)


for k in range(len(time_dyn)):

    # Incremental gust loading relative to 1-g equilibrium
    incremental_gust_load = (
        gust_scale_dyn[k]
        * delta_lift_per_span_gust
    )


    # Actual control authority
    control_scale = (
        actual_deflection_dyn[k]
        / best_gust_required_deflection
    )


    # Actual aerodynamic redistribution
    incremental_control_load = (
        control_scale
        * delta_lift_gla_full
    )


    # Uncontrolled generalized force
    generalized_force_uncontrolled[k] = np.trapezoid(
        incremental_gust_load
        * phi,
        y
    )


    # Controlled generalized force
    generalized_force_controlled[k] = np.trapezoid(
        (
            incremental_gust_load
            + incremental_control_load
        )
        * phi,
        y
    )


# ------------------------------------------------------------
# 14. Newmark-beta solver
#
# M q_ddot + C q_dot + K q = Q(t)
# ------------------------------------------------------------

def newmark_beta_response(
    force,
    mass,
    damping,
    stiffness,
    dt,
    beta=0.25,
    gamma=0.50
):

    n = len(force)

    displacement = np.zeros(n)
    velocity = np.zeros(n)
    acceleration = np.zeros(n)


    acceleration[0] = (
        force[0]
        - damping * velocity[0]
        - stiffness * displacement[0]
    ) / mass


    a0 = 1.0 / (
        beta * dt**2
    )

    a1 = gamma / (
        beta * dt
    )

    a2 = 1.0 / (
        beta * dt
    )

    a3 = (
        1.0 / (2.0 * beta)
        - 1.0
    )

    a4 = (
        gamma / beta
        - 1.0
    )

    a5 = (
        dt
        * (
            gamma / (2.0 * beta)
            - 1.0
        )
    )


    effective_stiffness = (
        stiffness
        + a0 * mass
        + a1 * damping
    )


    for k in range(n - 1):

        effective_force = (
            force[k+1]

            + mass
            * (
                a0 * displacement[k]
                + a2 * velocity[k]
                + a3 * acceleration[k]
            )

            + damping
            * (
                a1 * displacement[k]
                + a4 * velocity[k]
                + a5 * acceleration[k]
            )
        )


        displacement[k+1] = (
            effective_force
            / effective_stiffness
        )


        acceleration[k+1] = (
            a0
            * (
                displacement[k+1]
                - displacement[k]
            )
            - a2 * velocity[k]
            - a3 * acceleration[k]
        )


        velocity[k+1] = (
            velocity[k]
            + dt
            * (
                (1.0 - gamma)
                * acceleration[k]
                + gamma
                * acceleration[k+1]
            )
        )


    return (
        displacement,
        velocity,
        acceleration
    )


# ------------------------------------------------------------
# 15. Solve uncontrolled response
# ------------------------------------------------------------

(
    modal_displacement_uncontrolled,
    modal_velocity_uncontrolled,
    modal_acceleration_uncontrolled
) = newmark_beta_response(

    generalized_force_uncontrolled,

    modal_mass,

    modal_damping,

    modal_stiffness,

    dt
)


# ------------------------------------------------------------
# 16. Solve controlled response
# ------------------------------------------------------------

(
    modal_displacement_controlled,
    modal_velocity_controlled,
    modal_acceleration_controlled
) = newmark_beta_response(

    generalized_force_controlled,

    modal_mass,

    modal_damping,

    modal_stiffness,

    dt
)


# ------------------------------------------------------------
# 17. Static calibration of first-mode displacement
#
# Compare modal static response to exact beam static response
# for the previously solved 10 m/s gust.
# ------------------------------------------------------------

generalized_force_peak_static = np.trapezoid(
    delta_lift_per_span_gust
    * phi,
    y
)


modal_static_tip_increment = (
    generalized_force_peak_static
    / modal_stiffness
)


exact_static_tip_increment = (
    tip_deflection_gust
    - tip_deflection_mass_reduced
)


tip_response_scale = (
    exact_static_tip_increment
    / modal_static_tip_increment
)


# ------------------------------------------------------------
# 18. Static calibration of root bending moment
# ------------------------------------------------------------

modal_root_moment_per_unit_q = (
    EI_mass_reduced[0]
    * abs(
        phi_second[0]
    )
)


modal_static_root_increment = (
    modal_root_moment_per_unit_q
    * modal_static_tip_increment
)


exact_static_root_increment = (
    bending_moment_gust[0]
    - bending_moment[0]
)


root_moment_response_scale = (
    exact_static_root_increment
    / modal_static_root_increment
)


print()
print("FIRST-MODE STATIC CALIBRATION")
print("-----------------------------")

print(
    f"Exact beam gust tip increment: "
    f"{exact_static_tip_increment:.4f} m"
)

print(
    f"Raw first-mode static increment: "
    f"{modal_static_tip_increment:.4f} m"
)

print(
    f"Tip-response calibration factor: "
    f"{tip_response_scale:.3f}"
)

print(
    f"Root-moment calibration factor: "
    f"{root_moment_response_scale:.3f}"
)


# ------------------------------------------------------------
# 19. Reconstruct dynamic tip motion
# ------------------------------------------------------------

dynamic_tip_increment_uncontrolled = (
    modal_displacement_uncontrolled
    * tip_response_scale
)

dynamic_tip_increment_controlled = (
    modal_displacement_controlled
    * tip_response_scale
)


dynamic_tip_total_uncontrolled = (
    tip_deflection_mass_reduced
    + dynamic_tip_increment_uncontrolled
)

dynamic_tip_total_controlled = (
    tip_deflection_mass_reduced
    + dynamic_tip_increment_controlled
)


# ------------------------------------------------------------
# 20. Reconstruct dynamic root bending moment
# ------------------------------------------------------------

dynamic_root_increment_uncontrolled = (
    modal_root_moment_per_unit_q
    * modal_displacement_uncontrolled
    * root_moment_response_scale
)

dynamic_root_increment_controlled = (
    modal_root_moment_per_unit_q
    * modal_displacement_controlled
    * root_moment_response_scale
)


dynamic_root_total_uncontrolled = (
    bending_moment[0]
    + dynamic_root_increment_uncontrolled
)

dynamic_root_total_controlled = (
    bending_moment[0]
    + dynamic_root_increment_controlled
)


# ------------------------------------------------------------
# 21. Dynamic root spar-cap stress
# ------------------------------------------------------------

dynamic_root_stress_uncontrolled = (
    dynamic_root_total_uncontrolled
    / (
        A_cap_mass_reduced[0]
        * box_height[0]
    )
)

dynamic_root_stress_controlled = (
    dynamic_root_total_controlled
    / (
        A_cap_mass_reduced[0]
        * box_height[0]
    )
)


# ------------------------------------------------------------
# 22. Peak results
# ------------------------------------------------------------

peak_dynamic_tip_u = np.max(
    dynamic_tip_total_uncontrolled
)

peak_dynamic_tip_c = np.max(
    dynamic_tip_total_controlled
)


peak_dynamic_root_u = np.max(
    dynamic_root_total_uncontrolled
)

peak_dynamic_root_c = np.max(
    dynamic_root_total_controlled
)


peak_dynamic_stress_u = np.max(
    dynamic_root_stress_uncontrolled
)

peak_dynamic_stress_c = np.max(
    dynamic_root_stress_controlled
)


first_mode_tip_reduction = (
    (
        peak_dynamic_tip_u
        - peak_dynamic_tip_c
    )
    / peak_dynamic_tip_u
) * 100


first_mode_moment_reduction = (
    (
        peak_dynamic_root_u
        - peak_dynamic_root_c
    )
    / peak_dynamic_root_u
) * 100


first_mode_stress_reduction = (
    (
        peak_dynamic_stress_u
        - peak_dynamic_stress_c
    )
    / peak_dynamic_stress_u
) * 100


# Dynamic amplification relative to quasi-static gust
dynamic_amplification_tip = (
    peak_dynamic_tip_u
    / tip_deflection_gust
)

dynamic_amplification_moment = (
    peak_dynamic_root_u
    / bending_moment_gust[0]
)


# ------------------------------------------------------------
# 23. Peak times
# ------------------------------------------------------------

tip_peak_u_index = np.argmax(
    dynamic_tip_total_uncontrolled
)

tip_peak_c_index = np.argmax(
    dynamic_tip_total_controlled
)

moment_peak_u_index = np.argmax(
    dynamic_root_total_uncontrolled
)

moment_peak_c_index = np.argmax(
    dynamic_root_total_controlled
)


# ------------------------------------------------------------
# 24. Output summary
# ------------------------------------------------------------

print()
print(
    "HART-120 FIRST-MODE DYNAMIC GUST RESPONSE"
)

print(
    "-----------------------------------------"
)

print(
    f"First bending frequency: "
    f"{frequency_hz:.3f} Hz"
)

print(
    f"Gust duration: "
    f"{gust_duration:.3f} s"
)

print(
    f"Peak actual actuator deflection: "
    f"{np.max(actual_deflection_dyn):.2f} deg"
)

print()

print(
    f"Quasi-static uncontrolled tip: "
    f"{tip_deflection_gust:.4f} m"
)

print(
    f"Dynamic uncontrolled tip: "
    f"{peak_dynamic_tip_u:.4f} m"
)

print(
    f"Dynamic controlled tip: "
    f"{peak_dynamic_tip_c:.4f} m"
)

print(
    f"Dynamic tip reduction: "
    f"{first_mode_tip_reduction:.2f} %"
)

print(
    f"Tip dynamic amplification factor: "
    f"{dynamic_amplification_tip:.3f}"
)

print()

print(
    f"Quasi-static gust root moment: "
    f"{bending_moment_gust[0]/1e6:.3f} MN·m"
)

print(
    f"Dynamic uncontrolled root moment: "
    f"{peak_dynamic_root_u/1e6:.3f} MN·m"
)

print(
    f"Dynamic controlled root moment: "
    f"{peak_dynamic_root_c/1e6:.3f} MN·m"
)

print(
    f"Dynamic root-moment reduction: "
    f"{first_mode_moment_reduction:.2f} %"
)

print(
    f"Root-moment dynamic amplification factor: "
    f"{dynamic_amplification_moment:.3f}"
)

print()

print(
    f"Dynamic uncontrolled root stress: "
    f"{peak_dynamic_stress_u/1e6:.2f} MPa"
)

print(
    f"Dynamic controlled root stress: "
    f"{peak_dynamic_stress_c/1e6:.2f} MPa"
)

print(
    f"Dynamic stress reduction: "
    f"{first_mode_stress_reduction:.2f} %"
)

print()

print(
    f"Uncontrolled tip peak time: "
    f"{time_dyn[tip_peak_u_index]:.3f} s"
)

print(
    f"Controlled tip peak time: "
    f"{time_dyn[tip_peak_c_index]:.3f} s"
)

print(
    f"Uncontrolled moment peak time: "
    f"{time_dyn[moment_peak_u_index]:.3f} s"
)

print(
    f"Controlled moment peak time: "
    f"{time_dyn[moment_peak_c_index]:.3f} s"
)

print()

print(
    f"Final actuator deflection: "
    f"{actual_deflection_dyn[-1]:.4f} deg"
)


# ------------------------------------------------------------
# 25. Plot first bending mode
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta_mode,
    phi
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Normalized First-Mode Amplitude"
)

plt.title(
    "HART-120 — Assumed First Bending Mode"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 26. Plot extended gust + actuator response
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time_dyn,
    command_deflection_dyn,
    label="Commanded"
)

plt.plot(
    time_dyn,
    actual_deflection_dyn,
    label="Actual"
)

plt.xlabel("Time (s)")
plt.ylabel(
    "Control Surface Deflection (deg)"
)

plt.title(
    "HART-120 — Extended Actuator Response"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 27. Dynamic wing-tip response
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time_dyn,
    dynamic_tip_total_uncontrolled,
    label="Uncontrolled"
)

plt.plot(
    time_dyn,
    dynamic_tip_total_controlled,
    label="Active GLA"
)

plt.axhline(
    tip_deflection_mass_reduced,
    linestyle="--",
    label="1-g Equilibrium"
)

plt.xlabel("Time (s)")
plt.ylabel("Wing Tip Deflection (m)")

plt.title(
    "HART-120 — First-Mode Dynamic Gust Deflection"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 28. Dynamic root bending moment
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time_dyn,
    dynamic_root_total_uncontrolled / 1e6,
    label="Uncontrolled"
)

plt.plot(
    time_dyn,
    dynamic_root_total_controlled / 1e6,
    label="Active GLA"
)

plt.axhline(
    bending_moment[0] / 1e6,
    linestyle="--",
    label="1-g Equilibrium"
)

plt.xlabel("Time (s)")
plt.ylabel(
    "Root Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — First-Mode Dynamic Root Bending Moment"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 29. Dynamic root stress
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    time_dyn,
    dynamic_root_stress_uncontrolled / 1e6,
    label="Uncontrolled"
)

plt.plot(
    time_dyn,
    dynamic_root_stress_controlled / 1e6,
    label="Active GLA"
)

plt.xlabel("Time (s)")
plt.ylabel(
    "Root Spar-Cap Stress (MPa)"
)

plt.title(
    "HART-120 — Dynamic Root Stress"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 83]
# ============================================================
# HART-120 — GUST GRADIENT / DYNAMIC RESONANCE SENSITIVITY
#
# Industrial problem:
# Different gust lengths excite a flexible wing differently.
# A controller that works for one gust may perform poorly for
# another.
#
# This sweep identifies:
# - Critical gust gradient
# - Maximum dynamic amplification
# - Controlled vs uncontrolled peak loads
# - GLA effectiveness across gust scales
# ============================================================


# ------------------------------------------------------------
# 1. Gust-gradient sweep
# ------------------------------------------------------------

gust_gradient_values = np.arange(
    10.0,
    201.0,
    10.0
)   # m


gust_gradient_results = []


# ------------------------------------------------------------
# 2. Loop through gust gradients
# ------------------------------------------------------------

for H_test in gust_gradient_values:

    # --------------------------------------------------------
    # Gust duration
    # --------------------------------------------------------

    gust_duration_test = (
        2 * H_test
        / V_cruise
    )

    post_time_test = 2.0

    time_test = np.arange(
        0.0,
        gust_duration_test
        + post_time_test
        + dt,
        dt
    )

    distance_test = (
        V_cruise
        * time_test
    )


    # --------------------------------------------------------
    # 1-cosine gust
    # --------------------------------------------------------

    gust_velocity_test = np.zeros_like(
        time_test
    )

    gust_active_test = (
        distance_test
        <= 2 * H_test
    )

    gust_velocity_test[
        gust_active_test
    ] = (

        gust_peak_velocity
        / 2

        * (

            1

            - np.cos(

                np.pi
                * distance_test[
                    gust_active_test
                ]
                / H_test
            )
        )
    )


    gust_scale_test = (
        gust_velocity_test
        / gust_peak_velocity
    )


    # --------------------------------------------------------
    # Control command
    # --------------------------------------------------------

    command_test = (
        best_gust_required_deflection
        * gust_scale_test
    )

    command_test = np.clip(
        command_test,
        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Sensor / controller delay
    # --------------------------------------------------------

    delay_steps_test = int(
        sensor_control_delay
        / dt
    )

    delayed_command_test = np.zeros_like(
        command_test
    )

    if delay_steps_test > 0:

        delayed_command_test[
            delay_steps_test:
        ] = command_test[
            :-delay_steps_test
        ]

    else:

        delayed_command_test[:] = (
            command_test
        )


    # --------------------------------------------------------
    # Actuator dynamics
    # --------------------------------------------------------

    actuator_test = np.zeros_like(
        time_test
    )

    for k in range(
        1,
        len(time_test)
    ):

        desired_rate_test = (

            delayed_command_test[k]
            - actuator_test[k-1]

        ) / actuator_time_constant


        limited_rate_test = np.clip(

            desired_rate_test,

            -actuator_rate_limit,

            actuator_rate_limit
        )


        actuator_test[k] = (

            actuator_test[k-1]

            + limited_rate_test
            * dt
        )


        actuator_test[k] = np.clip(

            actuator_test[k],

            -max_deflection_deg,

            max_deflection_deg
        )


    # --------------------------------------------------------
    # Generalized aerodynamic forces
    # --------------------------------------------------------

    # Modal force produced by the full 10 m/s gust increment
    Q_gust_peak = np.trapezoid(

        delta_lift_per_span_gust
        * phi,

        y
    )


    # Modal force produced by full static GLA redistribution
    Q_control_full = np.trapezoid(

        delta_lift_gla_full
        * phi,

        y
    )


    # Time-dependent uncontrolled generalized load
    Q_uncontrolled_test = (

        gust_scale_test
        * Q_gust_peak
    )


    # Time-dependent control authority
    control_scale_test = (

        actuator_test
        / best_gust_required_deflection
    )


    # Controlled generalized load
    Q_controlled_test = (

        Q_uncontrolled_test

        + control_scale_test
        * Q_control_full
    )


    # --------------------------------------------------------
    # Modal dynamics — uncontrolled
    # --------------------------------------------------------

    (
        q_uncontrolled_test,
        qdot_uncontrolled_test,
        qddot_uncontrolled_test

    ) = newmark_beta_response(

        Q_uncontrolled_test,

        modal_mass,

        modal_damping,

        modal_stiffness,

        dt
    )


    # --------------------------------------------------------
    # Modal dynamics — controlled
    # --------------------------------------------------------

    (
        q_controlled_test,
        qdot_controlled_test,
        qddot_controlled_test

    ) = newmark_beta_response(

        Q_controlled_test,

        modal_mass,

        modal_damping,

        modal_stiffness,

        dt
    )


    # --------------------------------------------------------
    # Dynamic wing-tip response
    # --------------------------------------------------------

    tip_uncontrolled_test = (

        tip_deflection_mass_reduced

        + q_uncontrolled_test
        * tip_response_scale
    )


    tip_controlled_test = (

        tip_deflection_mass_reduced

        + q_controlled_test
        * tip_response_scale
    )


    # --------------------------------------------------------
    # Dynamic root bending moment
    # --------------------------------------------------------

    root_moment_uncontrolled_test = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_uncontrolled_test
        * root_moment_response_scale
    )


    root_moment_controlled_test = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_controlled_test
        * root_moment_response_scale
    )


    # --------------------------------------------------------
    # Root stress
    # --------------------------------------------------------

    root_stress_uncontrolled_test = (

        root_moment_uncontrolled_test

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    root_stress_controlled_test = (

        root_moment_controlled_test

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Peak values
    # --------------------------------------------------------

    peak_root_moment_u = np.max(
        root_moment_uncontrolled_test
    )

    peak_root_moment_c = np.max(
        root_moment_controlled_test
    )


    peak_tip_u = np.max(
        tip_uncontrolled_test
    )

    peak_tip_c = np.max(
        tip_controlled_test
    )


    peak_stress_u = np.max(
        root_stress_uncontrolled_test
    )

    peak_stress_c = np.max(
        root_stress_controlled_test
    )


    # --------------------------------------------------------
    # Dynamic amplification
    # --------------------------------------------------------

    moment_DAF = (

        peak_root_moment_u
        / bending_moment_gust[0]
    )


    tip_DAF = (

        peak_tip_u
        / tip_deflection_gust
    )


    # --------------------------------------------------------
    # Active-control benefit
    # --------------------------------------------------------

    moment_reduction_test = (

        (
            peak_root_moment_u
            - peak_root_moment_c
        )

        / peak_root_moment_u

    ) * 100


    tip_reduction_test = (

        (
            peak_tip_u
            - peak_tip_c
        )

        / peak_tip_u

    ) * 100


    stress_reduction_test = (

        (
            peak_stress_u
            - peak_stress_c
        )

        / peak_stress_u

    ) * 100


    # --------------------------------------------------------
    # Gust characteristic frequency
    #
    # Approximate inverse of gust duration
    # --------------------------------------------------------

    gust_characteristic_frequency = (

        1.0
        / gust_duration_test
    )


    frequency_ratio = (

        gust_characteristic_frequency
        / frequency_hz
    )


    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    gust_gradient_results.append({

        "Gust_H_m":
            H_test,

        "Gust_Duration_s":
            gust_duration_test,

        "Approx_Gust_Frequency_Hz":
            gust_characteristic_frequency,

        "Frequency_Ratio":
            frequency_ratio,

        "Peak_Root_Moment_Uncontrolled_MNm":
            peak_root_moment_u / 1e6,

        "Peak_Root_Moment_Controlled_MNm":
            peak_root_moment_c / 1e6,

        "Root_Moment_DAF":
            moment_DAF,

        "Root_Moment_Reduction_%":
            moment_reduction_test,

        "Peak_Stress_Uncontrolled_MPa":
            peak_stress_u / 1e6,

        "Peak_Stress_Controlled_MPa":
            peak_stress_c / 1e6,

        "Stress_Reduction_%":
            stress_reduction_test,

        "Peak_Tip_Uncontrolled_m":
            peak_tip_u,

        "Peak_Tip_Controlled_m":
            peak_tip_c,

        "Tip_DAF":
            tip_DAF,

        "Tip_Reduction_%":
            tip_reduction_test,

        "Peak_Actuator_Deflection_deg":
            np.max(actuator_test)
    })


# ------------------------------------------------------------
# 3. DataFrame
# ------------------------------------------------------------

gust_gradient_df = pd.DataFrame(
    gust_gradient_results
)


print()
print(
    "HART-120 GUST-GRADIENT DYNAMIC SENSITIVITY"
)

print(
    "------------------------------------------"
)

print(

    gust_gradient_df
    .round(3)
    .to_string(index=False)

)


# ------------------------------------------------------------
# 4. Critical uncontrolled dynamic load case
# ------------------------------------------------------------

critical_moment_index = (

    gust_gradient_df[
        "Peak_Root_Moment_Uncontrolled_MNm"
    ].idxmax()
)


critical_tip_index = (

    gust_gradient_df[
        "Peak_Tip_Uncontrolled_m"
    ].idxmax()
)


critical_DAF_index = (

    gust_gradient_df[
        "Root_Moment_DAF"
    ].idxmax()
)


critical_moment_case = (

    gust_gradient_df.loc[
        critical_moment_index
    ]
)


critical_tip_case = (

    gust_gradient_df.loc[
        critical_tip_index
    ]
)


critical_DAF_case = (

    gust_gradient_df.loc[
        critical_DAF_index
    ]
)


# ------------------------------------------------------------
# 5. Summary
# ------------------------------------------------------------

print()
print(
    "HART-120 CRITICAL DYNAMIC GUST CASE"
)

print(
    "-----------------------------------"
)

print(
    f"Critical gust gradient H: "
    f"{critical_moment_case['Gust_H_m']:.1f} m"
)

print(
    f"Gust duration: "
    f"{critical_moment_case['Gust_Duration_s']:.3f} s"
)

print(
    f"Peak uncontrolled root moment: "
    f"{critical_moment_case['Peak_Root_Moment_Uncontrolled_MNm']:.3f} MN·m"
)

print(
    f"Peak controlled root moment: "
    f"{critical_moment_case['Peak_Root_Moment_Controlled_MNm']:.3f} MN·m"
)

print(
    f"GLA root-moment reduction: "
    f"{critical_moment_case['Root_Moment_Reduction_%']:.2f} %"
)

print(
    f"Dynamic amplification factor: "
    f"{critical_moment_case['Root_Moment_DAF']:.3f}"
)

print()

print(
    f"Critical uncontrolled stress: "
    f"{critical_moment_case['Peak_Stress_Uncontrolled_MPa']:.2f} MPa"
)

print(
    f"Controlled stress: "
    f"{critical_moment_case['Peak_Stress_Controlled_MPa']:.2f} MPa"
)

print()

print(
    f"Critical tip-deflection gradient H: "
    f"{critical_tip_case['Gust_H_m']:.1f} m"
)

print(
    f"Maximum uncontrolled tip deflection: "
    f"{critical_tip_case['Peak_Tip_Uncontrolled_m']:.4f} m"
)

print()

print(
    f"Maximum DAF occurs at H: "
    f"{critical_DAF_case['Gust_H_m']:.1f} m"
)

print(
    f"Maximum root-moment DAF: "
    f"{critical_DAF_case['Root_Moment_DAF']:.3f}"
)


# ------------------------------------------------------------
# 6. Plot — root bending moment vs gust gradient
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(

    gust_gradient_values,

    gust_gradient_df[
        "Peak_Root_Moment_Uncontrolled_MNm"
    ],

    marker="o",

    label="Uncontrolled"
)

plt.plot(

    gust_gradient_values,

    gust_gradient_df[
        "Peak_Root_Moment_Controlled_MNm"
    ],

    marker="o",

    label="Active GLA"
)

plt.xlabel(
    "Gust Gradient H (m)"
)

plt.ylabel(
    "Peak Root Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — Critical Gust Gradient Search"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 7. Plot — dynamic amplification
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(

    gust_gradient_values,

    gust_gradient_df[
        "Root_Moment_DAF"
    ],

    marker="o"
)

plt.axhline(
    1.0,
    linestyle="--"
)

plt.xlabel(
    "Gust Gradient H (m)"
)

plt.ylabel(
    "Root Moment Dynamic Amplification Factor"
)

plt.title(
    "HART-120 — Gust Dynamic Amplification"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 8. Plot — GLA effectiveness
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(

    gust_gradient_values,

    gust_gradient_df[
        "Root_Moment_Reduction_%"
    ],

    marker="o"
)

plt.xlabel(
    "Gust Gradient H (m)"
)

plt.ylabel(
    "Peak Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — GLA Effectiveness Across Gust Gradients"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 9. Plot — actuator demand
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(

    gust_gradient_values,

    gust_gradient_df[
        "Peak_Actuator_Deflection_deg"
    ],

    marker="o"
)

plt.axhline(
    max_deflection_deg,
    linestyle="--",
    label="Deflection limit"
)

plt.xlabel(
    "Gust Gradient H (m)"
)

plt.ylabel(
    "Peak Control Surface Deflection (deg)"
)

plt.title(
    "HART-120 — Actuator Demand vs Gust Gradient"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 84]
# ============================================================
# HART-120 — CRITICAL-GUST ACTUATOR REQUIREMENT STUDY
#
# Purpose:
# Determine how sensor delay, actuator time constant, and
# actuator rate limit affect GLA performance at the critical
# H = 40 m gust.
#
# Outputs:
# - dynamic root moment reduction
# - peak stress
# - tip deflection
# - actuator demand
# - combinations meeting a project-level performance target
#
# NOTE:
# The target reduction is a project design objective,
# not a certification requirement.
# ============================================================


# ------------------------------------------------------------
# 1. Critical gust identified by previous sweep
# ------------------------------------------------------------

critical_H = float(
    critical_moment_case["Gust_H_m"]
)

critical_gust_duration = (
    2 * critical_H / V_cruise
)

post_gust_time_control = 2.0

time_control = np.arange(
    0.0,
    critical_gust_duration
    + post_gust_time_control
    + dt,
    dt
)

distance_control = (
    V_cruise * time_control
)


# ------------------------------------------------------------
# 2. Critical 1-cosine gust
# ------------------------------------------------------------

gust_velocity_control = np.zeros_like(
    time_control
)

critical_gust_active = (
    distance_control
    <= 2 * critical_H
)

gust_velocity_control[
    critical_gust_active
] = (
    gust_peak_velocity
    / 2
    * (
        1
        - np.cos(
            np.pi
            * distance_control[
                critical_gust_active
            ]
            / critical_H
        )
    )
)

gust_scale_control = (
    gust_velocity_control
    / gust_peak_velocity
)


# ------------------------------------------------------------
# 3. Full gust and control generalized forces
# ------------------------------------------------------------

Q_gust_peak_control = np.trapezoid(
    delta_lift_per_span_gust
    * phi,
    y
)

Q_control_full = np.trapezoid(
    delta_lift_gla_full
    * phi,
    y
)


# ------------------------------------------------------------
# 4. Uncontrolled critical-gust response
# ------------------------------------------------------------

Q_uncontrolled_control = (
    gust_scale_control
    * Q_gust_peak_control
)

(
    q_uncontrolled_control,
    qdot_uncontrolled_control,
    qddot_uncontrolled_control
) = newmark_beta_response(
    Q_uncontrolled_control,
    modal_mass,
    modal_damping,
    modal_stiffness,
    dt
)


root_moment_uncontrolled_control = (
    bending_moment[0]
    + modal_root_moment_per_unit_q
    * q_uncontrolled_control
    * root_moment_response_scale
)


tip_uncontrolled_control = (
    tip_deflection_mass_reduced
    + q_uncontrolled_control
    * tip_response_scale
)


peak_root_moment_uncontrolled_control = np.max(
    root_moment_uncontrolled_control
)

peak_tip_uncontrolled_control = np.max(
    tip_uncontrolled_control
)


# ------------------------------------------------------------
# 5. Actuator parameter sweep
# ------------------------------------------------------------

time_constant_values = np.array([
    0.04,
    0.06,
    0.08,
    0.10,
    0.12,
    0.16,
    0.20
])

sensor_delay_values = np.array([
    0.00,
    0.02,
    0.04,
    0.06,
    0.08
])

rate_limit_values = np.array([
    40.0,
    60.0,
    80.0,
    120.0,
    160.0
])


# Project-level performance objective
target_root_moment_reduction = 10.0   # %


actuator_requirement_results = []


# ------------------------------------------------------------
# 6. Sweep all actuator combinations
# ------------------------------------------------------------

for tau_actuator in time_constant_values:

    for delay_actuator in sensor_delay_values:

        for rate_actuator in rate_limit_values:

            # ------------------------------------------------
            # Control command
            # ------------------------------------------------

            command_test = (
                best_gust_required_deflection
                * gust_scale_control
            )

            command_test = np.clip(
                command_test,
                -max_deflection_deg,
                max_deflection_deg
            )


            # ------------------------------------------------
            # Sensor / controller delay
            # ------------------------------------------------

            delay_steps_test = int(
                round(
                    delay_actuator / dt
                )
            )

            delayed_command_test = np.zeros_like(
                command_test
            )

            if delay_steps_test > 0:

                delayed_command_test[
                    delay_steps_test:
                ] = command_test[
                    :-delay_steps_test
                ]

            else:

                delayed_command_test[:] = (
                    command_test
                )


            # ------------------------------------------------
            # Actuator response
            # ------------------------------------------------

            actuator_test = np.zeros_like(
                time_control
            )


            for k in range(
                1,
                len(time_control)
            ):

                desired_rate = (
                    delayed_command_test[k]
                    - actuator_test[k-1]
                ) / tau_actuator


                actual_rate = np.clip(
                    desired_rate,
                    -rate_actuator,
                    rate_actuator
                )


                actuator_test[k] = (
                    actuator_test[k-1]
                    + actual_rate * dt
                )


                actuator_test[k] = np.clip(
                    actuator_test[k],
                    -max_deflection_deg,
                    max_deflection_deg
                )


            # ------------------------------------------------
            # Actual aerodynamic control authority
            # ------------------------------------------------

            control_scale_test = (
                actuator_test
                / best_gust_required_deflection
            )


            # ------------------------------------------------
            # Controlled generalized forcing
            # ------------------------------------------------

            Q_controlled_test = (
                Q_uncontrolled_control
                + control_scale_test
                * Q_control_full
            )


            # ------------------------------------------------
            # Structural dynamics
            # ------------------------------------------------

            (
                q_controlled_test,
                qdot_controlled_test,
                qddot_controlled_test
            ) = newmark_beta_response(
                Q_controlled_test,
                modal_mass,
                modal_damping,
                modal_stiffness,
                dt
            )


            # ------------------------------------------------
            # Root bending moment
            # ------------------------------------------------

            root_moment_controlled_test = (
                bending_moment[0]
                + modal_root_moment_per_unit_q
                * q_controlled_test
                * root_moment_response_scale
            )


            # ------------------------------------------------
            # Tip deflection
            # ------------------------------------------------

            tip_controlled_test = (
                tip_deflection_mass_reduced
                + q_controlled_test
                * tip_response_scale
            )


            # ------------------------------------------------
            # Root stress
            # ------------------------------------------------

            root_stress_controlled_test = (
                root_moment_controlled_test
                / (
                    A_cap_mass_reduced[0]
                    * box_height[0]
                )
            )


            # ------------------------------------------------
            # Peak responses
            # ------------------------------------------------

            peak_root_moment_controlled = np.max(
                root_moment_controlled_test
            )

            peak_tip_controlled = np.max(
                tip_controlled_test
            )

            peak_root_stress_controlled = np.max(
                root_stress_controlled_test
            )


            # ------------------------------------------------
            # GLA benefit
            # ------------------------------------------------

            root_moment_reduction = (
                (
                    peak_root_moment_uncontrolled_control
                    - peak_root_moment_controlled
                )
                / peak_root_moment_uncontrolled_control
            ) * 100


            tip_reduction = (
                (
                    peak_tip_uncontrolled_control
                    - peak_tip_controlled
                )
                / peak_tip_uncontrolled_control
            ) * 100


            # ------------------------------------------------
            # Performance target
            # ------------------------------------------------

            meets_target = (
                root_moment_reduction
                >= target_root_moment_reduction
            )


            # ------------------------------------------------
            # Store
            # ------------------------------------------------

            actuator_requirement_results.append({

                "Time_Constant_s":
                    tau_actuator,

                "Sensor_Delay_s":
                    delay_actuator,

                "Rate_Limit_deg_s":
                    rate_actuator,

                "Peak_Actuator_Deflection_deg":
                    np.max(
                        np.abs(
                            actuator_test
                        )
                    ),

                "Peak_Root_Moment_MNm":
                    peak_root_moment_controlled / 1e6,

                "Root_Moment_Reduction_%":
                    root_moment_reduction,

                "Peak_Root_Stress_MPa":
                    peak_root_stress_controlled / 1e6,

                "Peak_Tip_Deflection_m":
                    peak_tip_controlled,

                "Tip_Deflection_Reduction_%":
                    tip_reduction,

                "Meets_10pct_Target":
                    meets_target
            })


# ------------------------------------------------------------
# 7. DataFrame
# ------------------------------------------------------------

actuator_requirement_df = pd.DataFrame(
    actuator_requirement_results
)


print()
print(
    "HART-120 CRITICAL-GUST ACTUATOR REQUIREMENT STUDY"
)

print(
    "------------------------------------------------"
)

print(
    f"Critical gust H: "
    f"{critical_H:.1f} m"
)

print(
    f"Critical gust duration: "
    f"{critical_gust_duration:.3f} s"
)

print(
    f"Uncontrolled peak root moment: "
    f"{peak_root_moment_uncontrolled_control/1e6:.3f} MN·m"
)

print(
    f"Project target reduction: "
    f"{target_root_moment_reduction:.1f} %"
)


# ------------------------------------------------------------
# 8. Feasible actuator combinations
# ------------------------------------------------------------

feasible_actuator_df = (
    actuator_requirement_df[
        actuator_requirement_df[
            "Meets_10pct_Target"
        ]
    ]
    .copy()
)


print()
print(
    f"Total actuator configurations tested: "
    f"{len(actuator_requirement_df)}"
)

print(
    f"Configurations meeting target: "
    f"{len(feasible_actuator_df)}"
)


# ------------------------------------------------------------
# 9. Best dynamic performance
# ------------------------------------------------------------

best_performance_index = (
    actuator_requirement_df[
        "Root_Moment_Reduction_%"
    ].idxmax()
)

best_performance_case = (
    actuator_requirement_df.loc[
        best_performance_index
    ]
)


print()
print(
    "BEST DYNAMIC LOAD-ALLEVIATION PERFORMANCE"
)

print(
    "-----------------------------------------"
)

print(
    f"Actuator time constant: "
    f"{best_performance_case['Time_Constant_s']:.3f} s"
)

print(
    f"Sensor delay: "
    f"{best_performance_case['Sensor_Delay_s']:.3f} s"
)

print(
    f"Rate limit: "
    f"{best_performance_case['Rate_Limit_deg_s']:.1f} deg/s"
)

print(
    f"Peak surface deflection: "
    f"{best_performance_case['Peak_Actuator_Deflection_deg']:.2f} deg"
)

print(
    f"Peak root moment: "
    f"{best_performance_case['Peak_Root_Moment_MNm']:.3f} MN·m"
)

print(
    f"Root moment reduction: "
    f"{best_performance_case['Root_Moment_Reduction_%']:.2f} %"
)

print(
    f"Peak root stress: "
    f"{best_performance_case['Peak_Root_Stress_MPa']:.2f} MPa"
)

print(
    f"Peak tip deflection: "
    f"{best_performance_case['Peak_Tip_Deflection_m']:.4f} m"
)


# ------------------------------------------------------------
# 10. Minimum rate limit achieving target
# ------------------------------------------------------------

if len(feasible_actuator_df) > 0:

    minimum_required_rate = (
        feasible_actuator_df[
            "Rate_Limit_deg_s"
        ].min()
    )


    min_rate_cases = (
        feasible_actuator_df[
            feasible_actuator_df[
                "Rate_Limit_deg_s"
            ] == minimum_required_rate
        ]
    )


    best_min_rate_index = (
        min_rate_cases[
            "Root_Moment_Reduction_%"
        ].idxmax()
    )

    best_min_rate_case = (
        actuator_requirement_df.loc[
            best_min_rate_index
        ]
    )


    print()
    print(
        "LOWEST RATE-LIMIT CONFIGURATION MEETING TARGET"
    )

    print(
        "----------------------------------------------"
    )

    print(
        f"Rate limit: "
        f"{best_min_rate_case['Rate_Limit_deg_s']:.1f} deg/s"
    )

    print(
        f"Time constant: "
        f"{best_min_rate_case['Time_Constant_s']:.3f} s"
    )

    print(
        f"Sensor delay: "
        f"{best_min_rate_case['Sensor_Delay_s']:.3f} s"
    )

    print(
        f"Root moment reduction: "
        f"{best_min_rate_case['Root_Moment_Reduction_%']:.2f} %"
    )


# ------------------------------------------------------------
# 11. Maximum sensor delay still meeting target
# ------------------------------------------------------------

if len(feasible_actuator_df) > 0:

    maximum_feasible_delay = (
        feasible_actuator_df[
            "Sensor_Delay_s"
        ].max()
    )


    max_delay_cases = (
        feasible_actuator_df[
            feasible_actuator_df[
                "Sensor_Delay_s"
            ] == maximum_feasible_delay
        ]
    )


    best_max_delay_index = (
        max_delay_cases[
            "Root_Moment_Reduction_%"
        ].idxmax()
    )

    best_max_delay_case = (
        actuator_requirement_df.loc[
            best_max_delay_index
        ]
    )


    print()
    print(
        "MAXIMUM TESTED SENSOR DELAY MEETING TARGET"
    )

    print(
        "------------------------------------------"
    )

    print(
        f"Sensor delay: "
        f"{best_max_delay_case['Sensor_Delay_s']:.3f} s"
    )

    print(
        f"Time constant: "
        f"{best_max_delay_case['Time_Constant_s']:.3f} s"
    )

    print(
        f"Rate limit: "
        f"{best_max_delay_case['Rate_Limit_deg_s']:.1f} deg/s"
    )

    print(
        f"Root moment reduction: "
        f"{best_max_delay_case['Root_Moment_Reduction_%']:.2f} %"
    )


# ------------------------------------------------------------
# 12. Maximum actuator time constant meeting target
# ------------------------------------------------------------

if len(feasible_actuator_df) > 0:

    maximum_feasible_tau = (
        feasible_actuator_df[
            "Time_Constant_s"
        ].max()
    )


    max_tau_cases = (
        feasible_actuator_df[
            feasible_actuator_df[
                "Time_Constant_s"
            ] == maximum_feasible_tau
        ]
    )


    best_max_tau_index = (
        max_tau_cases[
            "Root_Moment_Reduction_%"
        ].idxmax()
    )

    best_max_tau_case = (
        actuator_requirement_df.loc[
            best_max_tau_index
        ]
    )


    print()
    print(
        "SLOWEST TESTED ACTUATOR MEETING TARGET"
    )

    print(
        "--------------------------------------"
    )

    print(
        f"Time constant: "
        f"{best_max_tau_case['Time_Constant_s']:.3f} s"
    )

    print(
        f"Sensor delay: "
        f"{best_max_tau_case['Sensor_Delay_s']:.3f} s"
    )

    print(
        f"Rate limit: "
        f"{best_max_tau_case['Rate_Limit_deg_s']:.1f} deg/s"
    )

    print(
        f"Root moment reduction: "
        f"{best_max_tau_case['Root_Moment_Reduction_%']:.2f} %"
    )


# ------------------------------------------------------------
# 13. Sensitivity plot — time constant
# Fixed delay = 0.04 s and rate = 80 deg/s
# ------------------------------------------------------------

tau_plot_df = actuator_requirement_df[
    (
        actuator_requirement_df[
            "Sensor_Delay_s"
        ] == 0.04
    )
    &
    (
        actuator_requirement_df[
            "Rate_Limit_deg_s"
        ] == 80.0
    )
]


plt.figure(figsize=(8, 5))

plt.plot(
    tau_plot_df[
        "Time_Constant_s"
    ],
    tau_plot_df[
        "Root_Moment_Reduction_%"
    ],
    marker="o"
)

plt.axhline(
    target_root_moment_reduction,
    linestyle="--",
    label="Project target"
)

plt.xlabel(
    "Actuator Time Constant (s)"
)

plt.ylabel(
    "Critical-Gust Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — GLA Sensitivity to Actuator Response Time"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 14. Sensitivity plot — sensor delay
# Fixed tau = 0.08 s and rate = 80 deg/s
# ------------------------------------------------------------

delay_plot_df = actuator_requirement_df[
    (
        actuator_requirement_df[
            "Time_Constant_s"
        ] == 0.08
    )
    &
    (
        actuator_requirement_df[
            "Rate_Limit_deg_s"
        ] == 80.0
    )
]


plt.figure(figsize=(8, 5))

plt.plot(
    delay_plot_df[
        "Sensor_Delay_s"
    ],
    delay_plot_df[
        "Root_Moment_Reduction_%"
    ],
    marker="o"
)

plt.axhline(
    target_root_moment_reduction,
    linestyle="--",
    label="Project target"
)

plt.xlabel(
    "Sensor / Control Delay (s)"
)

plt.ylabel(
    "Critical-Gust Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — GLA Sensitivity to Control Delay"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 15. Sensitivity plot — actuator rate limit
# Fixed tau = 0.08 s and delay = 0.02 s
# ------------------------------------------------------------

rate_plot_df = actuator_requirement_df[
    (
        actuator_requirement_df[
            "Time_Constant_s"
        ] == 0.08
    )
    &
    (
        actuator_requirement_df[
            "Sensor_Delay_s"
        ] == 0.02
    )
]


plt.figure(figsize=(8, 5))

plt.plot(
    rate_plot_df[
        "Rate_Limit_deg_s"
    ],
    rate_plot_df[
        "Root_Moment_Reduction_%"
    ],
    marker="o"
)

plt.axhline(
    target_root_moment_reduction,
    linestyle="--",
    label="Project target"
)

plt.xlabel(
    "Actuator Rate Limit (deg/s)"
)

plt.ylabel(
    "Critical-Gust Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — GLA Sensitivity to Actuator Rate Limit"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 16. Feasibility map
# Fixed actuator rate = 80 deg/s
# ------------------------------------------------------------

feasibility_map = np.zeros(
    (
        len(time_constant_values),
        len(sensor_delay_values)
    )
)


for i, tau_value in enumerate(
    time_constant_values
):

    for j, delay_value in enumerate(
        sensor_delay_values
    ):

        case = actuator_requirement_df[
            (
                actuator_requirement_df[
                    "Time_Constant_s"
                ] == tau_value
            )
            &
            (
                actuator_requirement_df[
                    "Sensor_Delay_s"
                ] == delay_value
            )
            &
            (
                actuator_requirement_df[
                    "Rate_Limit_deg_s"
                ] == 80.0
            )
        ]

        feasibility_map[i, j] = (
            case[
                "Root_Moment_Reduction_%"
            ].iloc[0]
        )


plt.figure(figsize=(8, 5))

image = plt.imshow(
    feasibility_map,
    origin="lower",
    aspect="auto",
    extent=[
        sensor_delay_values[0],
        sensor_delay_values[-1],
        time_constant_values[0],
        time_constant_values[-1]
    ]
)

plt.colorbar(
    image,
    label="Root Moment Reduction (%)"
)

plt.xlabel(
    "Sensor / Control Delay (s)"
)

plt.ylabel(
    "Actuator Time Constant (s)"
)

plt.title(
    "HART-120 — Critical-Gust Control Performance Map"
)

plt.show()

# %% [notebook cell 85]
# ============================================================
# HART-120 — GUST PREVIEW / FEEDFORWARD CONTROL STUDY
#
# Industrial problem:
# Sensor + control delay can make active GLA ineffective or
# even increase structural loads because the control action
# arrives at the wrong phase of the wing response.
#
# Proposed solution:
# Use forward gust preview so the control surface begins
# responding BEFORE the gust reaches the wing.
#
# Conceptual reduced-order preview-control study.
# ============================================================


# ------------------------------------------------------------
# 1. Use the critical gust identified previously
# ------------------------------------------------------------

preview_H = 40.0

preview_gust_duration = (
    2 * preview_H
    / V_cruise
)

preview_post_time = 2.0

time_preview = np.arange(
    0.0,
    preview_gust_duration
    + preview_post_time
    + dt,
    dt
)

distance_preview_time = (
    V_cruise * time_preview
)


# ------------------------------------------------------------
# 2. Critical 1-cosine gust
# ------------------------------------------------------------

gust_velocity_preview = np.zeros_like(
    time_preview
)

gust_active_preview = (
    distance_preview_time
    <= 2 * preview_H
)

gust_velocity_preview[
    gust_active_preview
] = (
    gust_peak_velocity
    / 2
    * (
        1
        - np.cos(
            np.pi
            * distance_preview_time[
                gust_active_preview
            ]
            / preview_H
        )
    )
)

gust_scale_preview = (
    gust_velocity_preview
    / gust_peak_velocity
)


# ------------------------------------------------------------
# 3. Baseline actuator / control system
#
# Use the original dynamic-control assumptions
# ------------------------------------------------------------

preview_actuator_tau = 0.12      # s
preview_rate_limit = 80.0        # deg/s
preview_control_delay = 0.04     # s


# ------------------------------------------------------------
# 4. Gust preview-time sweep
# ------------------------------------------------------------

preview_time_values = np.arange(
    0.0,
    0.121,
    0.01
)


preview_results = []


# ------------------------------------------------------------
# 5. Uncontrolled generalized force
# ------------------------------------------------------------

Q_gust_peak_preview = np.trapezoid(
    delta_lift_per_span_gust
    * phi,
    y
)

Q_control_full_preview = np.trapezoid(
    delta_lift_gla_full
    * phi,
    y
)


Q_uncontrolled_preview = (
    gust_scale_preview
    * Q_gust_peak_preview
)


# ------------------------------------------------------------
# 6. Solve uncontrolled dynamic response once
# ------------------------------------------------------------

(
    q_preview_uncontrolled,
    qdot_preview_uncontrolled,
    qddot_preview_uncontrolled

) = newmark_beta_response(

    Q_uncontrolled_preview,

    modal_mass,

    modal_damping,

    modal_stiffness,

    dt
)


root_moment_preview_uncontrolled = (
    bending_moment[0]

    + modal_root_moment_per_unit_q
    * q_preview_uncontrolled
    * root_moment_response_scale
)


tip_preview_uncontrolled = (
    tip_deflection_mass_reduced

    + q_preview_uncontrolled
    * tip_response_scale
)


root_stress_preview_uncontrolled = (
    root_moment_preview_uncontrolled
    / (
        A_cap_mass_reduced[0]
        * box_height[0]
    )
)


peak_root_preview_uncontrolled = np.max(
    root_moment_preview_uncontrolled
)

peak_tip_preview_uncontrolled = np.max(
    tip_preview_uncontrolled
)

peak_stress_preview_uncontrolled = np.max(
    root_stress_preview_uncontrolled
)


# ------------------------------------------------------------
# 7. Sweep available preview time
# ------------------------------------------------------------

for preview_time in preview_time_values:

    # --------------------------------------------------------
    # Ideal command based on gust intensity
    # --------------------------------------------------------

    normal_command = (
        best_gust_required_deflection
        * gust_scale_preview
    )

    normal_command = np.clip(
        normal_command,
        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Forward preview
    #
    # Command at current time uses gust information from
    # preview_time seconds ahead.
    # --------------------------------------------------------

    preview_steps = int(
        round(
            preview_time / dt
        )
    )


    preview_command = np.zeros_like(
        normal_command
    )


    if preview_steps > 0:

        preview_command[
            :-preview_steps
        ] = normal_command[
            preview_steps:
        ]

    else:

        preview_command[:] = (
            normal_command
        )


    # --------------------------------------------------------
    # Existing sensor / processing delay
    # --------------------------------------------------------

    delay_steps = int(
        round(
            preview_control_delay / dt
        )
    )


    delayed_preview_command = np.zeros_like(
        preview_command
    )


    if delay_steps > 0:

        delayed_preview_command[
            delay_steps:
        ] = preview_command[
            :-delay_steps
        ]

    else:

        delayed_preview_command[:] = (
            preview_command
        )


    # --------------------------------------------------------
    # Actuator response
    # --------------------------------------------------------

    actuator_preview = np.zeros_like(
        time_preview
    )


    for k in range(
        1,
        len(time_preview)
    ):

        desired_rate = (
            delayed_preview_command[k]
            - actuator_preview[k-1]
        ) / preview_actuator_tau


        limited_rate = np.clip(
            desired_rate,
            -preview_rate_limit,
            preview_rate_limit
        )


        actuator_preview[k] = (
            actuator_preview[k-1]
            + limited_rate * dt
        )


        actuator_preview[k] = np.clip(
            actuator_preview[k],
            -max_deflection_deg,
            max_deflection_deg
        )


    # --------------------------------------------------------
    # Actual aerodynamic control authority
    # --------------------------------------------------------

    control_scale_preview = (
        actuator_preview
        / best_gust_required_deflection
    )


    # --------------------------------------------------------
    # Controlled generalized force
    # --------------------------------------------------------

    Q_controlled_preview = (
        Q_uncontrolled_preview

        + control_scale_preview
        * Q_control_full_preview
    )


    # --------------------------------------------------------
    # Structural dynamic response
    # --------------------------------------------------------

    (
        q_preview_controlled,
        qdot_preview_controlled,
        qddot_preview_controlled

    ) = newmark_beta_response(

        Q_controlled_preview,

        modal_mass,

        modal_damping,

        modal_stiffness,

        dt
    )


    # --------------------------------------------------------
    # Root bending moment
    # --------------------------------------------------------

    root_moment_preview_controlled = (
        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_preview_controlled
        * root_moment_response_scale
    )


    # --------------------------------------------------------
    # Tip deflection
    # --------------------------------------------------------

    tip_preview_controlled = (
        tip_deflection_mass_reduced

        + q_preview_controlled
        * tip_response_scale
    )


    # --------------------------------------------------------
    # Root stress
    # --------------------------------------------------------

    root_stress_preview_controlled = (
        root_moment_preview_controlled

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Peak structural responses
    # --------------------------------------------------------

    peak_root_controlled = np.max(
        root_moment_preview_controlled
    )

    peak_tip_controlled = np.max(
        tip_preview_controlled
    )

    peak_stress_controlled = np.max(
        root_stress_preview_controlled
    )


    # --------------------------------------------------------
    # Performance improvement
    # --------------------------------------------------------

    root_reduction_preview = (
        (
            peak_root_preview_uncontrolled
            - peak_root_controlled
        )

        / peak_root_preview_uncontrolled

    ) * 100


    tip_reduction_preview = (
        (
            peak_tip_preview_uncontrolled
            - peak_tip_controlled
        )

        / peak_tip_preview_uncontrolled

    ) * 100


    stress_reduction_preview = (
        (
            peak_stress_preview_uncontrolled
            - peak_stress_controlled
        )

        / peak_stress_preview_uncontrolled

    ) * 100


    # --------------------------------------------------------
    # Equivalent physical preview distance
    # --------------------------------------------------------

    preview_distance = (
        V_cruise
        * preview_time
    )


    # --------------------------------------------------------
    # Effective lead relative to system delay
    # --------------------------------------------------------

    effective_lead_time = (
        preview_time
        - preview_control_delay
    )


    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    preview_results.append({

        "Preview_Time_s":
            preview_time,

        "Preview_Distance_m":
            preview_distance,

        "Effective_Lead_s":
            effective_lead_time,

        "Peak_Actuator_Deflection_deg":
            np.max(
                np.abs(
                    actuator_preview
                )
            ),

        "Peak_Root_Moment_MNm":
            peak_root_controlled / 1e6,

        "Root_Moment_Reduction_%":
            root_reduction_preview,

        "Peak_Root_Stress_MPa":
            peak_stress_controlled / 1e6,

        "Stress_Reduction_%":
            stress_reduction_preview,

        "Peak_Tip_Deflection_m":
            peak_tip_controlled,

        "Tip_Deflection_Reduction_%":
            tip_reduction_preview,

        "Meets_10pct_Target":
            root_reduction_preview >= 10.0
    })


# ------------------------------------------------------------
# 8. DataFrame
# ------------------------------------------------------------

preview_df = pd.DataFrame(
    preview_results
)


print()
print(
    "HART-120 GUST PREVIEW / FEEDFORWARD STUDY"
)

print(
    "-----------------------------------------"
)

print(
    preview_df
    .round(3)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 9. Find optimum preview time
# ------------------------------------------------------------

best_preview_index = (
    preview_df[
        "Root_Moment_Reduction_%"
    ].idxmax()
)

best_preview_case = (
    preview_df.loc[
        best_preview_index
    ]
)


# ------------------------------------------------------------
# 10. Minimum preview meeting 10% target
# ------------------------------------------------------------

preview_target_df = (
    preview_df[
        preview_df[
            "Meets_10pct_Target"
        ]
    ]
)


print()
print(
    "BEST GUST PREVIEW CASE"
)

print(
    "----------------------"
)

print(
    f"Preview time: "
    f"{best_preview_case['Preview_Time_s']:.3f} s"
)

print(
    f"Equivalent preview distance: "
    f"{best_preview_case['Preview_Distance_m']:.2f} m"
)

print(
    f"Effective lead relative to delay: "
    f"{best_preview_case['Effective_Lead_s']:.3f} s"
)

print(
    f"Peak root moment: "
    f"{best_preview_case['Peak_Root_Moment_MNm']:.3f} MN·m"
)

print(
    f"Root moment reduction: "
    f"{best_preview_case['Root_Moment_Reduction_%']:.2f} %"
)

print(
    f"Peak root stress: "
    f"{best_preview_case['Peak_Root_Stress_MPa']:.2f} MPa"
)

print(
    f"Stress reduction: "
    f"{best_preview_case['Stress_Reduction_%']:.2f} %"
)

print(
    f"Peak tip deflection: "
    f"{best_preview_case['Peak_Tip_Deflection_m']:.4f} m"
)

print(
    f"Tip deflection reduction: "
    f"{best_preview_case['Tip_Deflection_Reduction_%']:.2f} %"
)

print(
    f"Peak actuator deflection: "
    f"{best_preview_case['Peak_Actuator_Deflection_deg']:.2f} deg"
)


# ------------------------------------------------------------
# 11. Minimum preview needed for project target
# ------------------------------------------------------------

if len(preview_target_df) > 0:

    minimum_preview_index = (
        preview_target_df[
            "Preview_Time_s"
        ].idxmin()
    )

    minimum_preview_case = (
        preview_df.loc[
            minimum_preview_index
        ]
    )


    print()
    print(
        "MINIMUM PREVIEW MEETING 10% TARGET"
    )

    print(
        "----------------------------------"
    )

    print(
        f"Required preview time: "
        f"{minimum_preview_case['Preview_Time_s']:.3f} s"
    )

    print(
        f"Required preview distance: "
        f"{minimum_preview_case['Preview_Distance_m']:.2f} m"
    )

    print(
        f"Root moment reduction: "
        f"{minimum_preview_case['Root_Moment_Reduction_%']:.2f} %"
    )


else:

    print()
    print(
        "No tested preview time achieved "
        "the 10% project target."
    )


# ------------------------------------------------------------
# 12. Plot — preview time vs root bending-moment reduction
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_df[
        "Preview_Time_s"
    ],
    preview_df[
        "Root_Moment_Reduction_%"
    ],
    marker="o"
)

plt.axhline(
    10.0,
    linestyle="--",
    label="Project target"
)

plt.axvline(
    preview_control_delay,
    linestyle="--",
    label="Existing control delay"
)

plt.xlabel(
    "Available Gust Preview Time (s)"
)

plt.ylabel(
    "Critical-Gust Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — Benefit of Gust Preview"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 13. Plot — preview distance vs structural response
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_df[
        "Preview_Distance_m"
    ],
    preview_df[
        "Peak_Root_Moment_MNm"
    ],
    marker="o"
)

plt.xlabel(
    "Equivalent Forward Gust Preview Distance (m)"
)

plt.ylabel(
    "Peak Root Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — Preview Sensor Range vs Wing Root Load"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 14. Plot — stress benefit
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_df[
        "Preview_Time_s"
    ],
    preview_df[
        "Peak_Root_Stress_MPa"
    ],
    marker="o"
)

plt.xlabel(
    "Available Gust Preview Time (s)"
)

plt.ylabel(
    "Peak Root Spar-Cap Stress (MPa)"
)

plt.title(
    "HART-120 — Gust Preview vs Dynamic Root Stress"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 15. Plot — tip-deflection benefit
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_df[
        "Preview_Time_s"
    ],
    preview_df[
        "Peak_Tip_Deflection_m"
    ],
    marker="o"
)

plt.xlabel(
    "Available Gust Preview Time (s)"
)

plt.ylabel(
    "Peak Wing-Tip Deflection (m)"
)

plt.title(
    "HART-120 — Gust Preview vs Dynamic Wing Deflection"
)

plt.grid(True)
plt.show()

# %% [notebook cell 86]
# ============================================================
# HART-120 — PHYSICALLY CORRECTED GUST PREVIEW CONTROL
#
# Improvement:
# The simulation begins BEFORE the gust reaches the wing,
# allowing a forward-looking sensor to command the actuator
# before t = 0.
#
# t = 0 -> gust first reaches the wing
# t < 0 -> preview / pre-actuation period
# ============================================================


# ------------------------------------------------------------
# 1. Critical gust
# ------------------------------------------------------------

critical_H = 40.0

critical_gust_duration = (
    2 * critical_H / V_cruise
)

post_gust_time = 2.0

max_preview_time = 0.15


# Start simulation before gust arrival
time_ff = np.arange(
    -max_preview_time,
    critical_gust_duration
    + post_gust_time
    + dt,
    dt
)


# ------------------------------------------------------------
# 2. Function for gust intensity at the WING
# ------------------------------------------------------------

def gust_scale_at_time(t_array, H):

    scale = np.zeros_like(t_array)

    active = (
        (t_array >= 0.0)
        &
        (
            t_array
            <= 2 * H / V_cruise
        )
    )

    distance = (
        V_cruise
        * t_array[active]
    )

    scale[active] = (
        0.5
        * (
            1
            - np.cos(
                np.pi
                * distance
                / H
            )
        )
    )

    return scale


# Actual gust seen by wing
gust_scale_wing = gust_scale_at_time(
    time_ff,
    critical_H
)


gust_velocity_wing = (
    gust_peak_velocity
    * gust_scale_wing
)


# ------------------------------------------------------------
# 3. Generalized aerodynamic loads
# ------------------------------------------------------------

Q_gust_peak_ff = np.trapezoid(
    delta_lift_per_span_gust
    * phi,
    y
)

Q_control_full_ff = np.trapezoid(
    delta_lift_gla_full
    * phi,
    y
)


Q_uncontrolled_ff = (
    gust_scale_wing
    * Q_gust_peak_ff
)


# ------------------------------------------------------------
# 4. Preview-time sweep
# ------------------------------------------------------------

preview_time_values_corrected = np.arange(
    0.0,
    0.151,
    0.01
)


preview_corrected_results = []


# ------------------------------------------------------------
# 5. Solve uncontrolled response once
# ------------------------------------------------------------

(
    q_ff_uncontrolled,
    qdot_ff_uncontrolled,
    qddot_ff_uncontrolled

) = newmark_beta_response(

    Q_uncontrolled_ff,

    modal_mass,

    modal_damping,

    modal_stiffness,

    dt
)


root_moment_ff_uncontrolled = (
    bending_moment[0]
    + modal_root_moment_per_unit_q
    * q_ff_uncontrolled
    * root_moment_response_scale
)


tip_ff_uncontrolled = (
    tip_deflection_mass_reduced
    + q_ff_uncontrolled
    * tip_response_scale
)


stress_ff_uncontrolled = (
    root_moment_ff_uncontrolled
    / (
        A_cap_mass_reduced[0]
        * box_height[0]
    )
)


peak_root_ff_uncontrolled = np.max(
    root_moment_ff_uncontrolled
)

peak_tip_ff_uncontrolled = np.max(
    tip_ff_uncontrolled
)

peak_stress_ff_uncontrolled = np.max(
    stress_ff_uncontrolled
)


# ------------------------------------------------------------
# 6. Preview-control sweep
# ------------------------------------------------------------

for preview_time in preview_time_values_corrected:

    # --------------------------------------------------------
    # Forward sensor measurement
    #
    # At time t, sensor estimates gust that will arrive at:
    # t + preview_time
    # --------------------------------------------------------

    sensed_gust_scale = gust_scale_at_time(
        time_ff + preview_time,
        critical_H
    )


    command_raw = (
        best_gust_required_deflection
        * sensed_gust_scale
    )


    command_raw = np.clip(
        command_raw,
        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Processing / sensor delay
    # --------------------------------------------------------

    effective_command_time = (
        time_ff
        - preview_control_delay
    )


    delayed_command = np.interp(
        effective_command_time,
        time_ff,
        command_raw,
        left=0.0,
        right=0.0
    )


    # --------------------------------------------------------
    # Actuator model
    # --------------------------------------------------------

    actuator_ff = np.zeros_like(
        time_ff
    )


    for k in range(
        1,
        len(time_ff)
    ):

        desired_rate = (
            delayed_command[k]
            - actuator_ff[k-1]
        ) / preview_actuator_tau


        limited_rate = np.clip(
            desired_rate,
            -preview_rate_limit,
            preview_rate_limit
        )


        actuator_ff[k] = (
            actuator_ff[k-1]
            + limited_rate * dt
        )


        actuator_ff[k] = np.clip(
            actuator_ff[k],
            -max_deflection_deg,
            max_deflection_deg
        )


    # --------------------------------------------------------
    # Actual aerodynamic control authority
    # --------------------------------------------------------

    control_scale_ff = (
        actuator_ff
        / best_gust_required_deflection
    )


    Q_controlled_ff = (
        Q_uncontrolled_ff
        + control_scale_ff
        * Q_control_full_ff
    )


    # --------------------------------------------------------
    # Flexible-wing response
    # --------------------------------------------------------

    (
        q_ff_controlled,
        qdot_ff_controlled,
        qddot_ff_controlled

    ) = newmark_beta_response(

        Q_controlled_ff,

        modal_mass,

        modal_damping,

        modal_stiffness,

        dt
    )


    # --------------------------------------------------------
    # Root bending moment
    # --------------------------------------------------------

    root_moment_ff_controlled = (
        bending_moment[0]
        + modal_root_moment_per_unit_q
        * q_ff_controlled
        * root_moment_response_scale
    )


    # --------------------------------------------------------
    # Tip deflection
    # --------------------------------------------------------

    tip_ff_controlled = (
        tip_deflection_mass_reduced
        + q_ff_controlled
        * tip_response_scale
    )


    # --------------------------------------------------------
    # Root stress
    # --------------------------------------------------------

    stress_ff_controlled = (
        root_moment_ff_controlled
        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Peak response
    # --------------------------------------------------------

    peak_root_ff_controlled = np.max(
        root_moment_ff_controlled
    )

    minimum_root_ff_controlled = np.min(
        root_moment_ff_controlled
    )

    peak_tip_ff_controlled = np.max(
        tip_ff_controlled
    )

    minimum_tip_ff_controlled = np.min(
        tip_ff_controlled
    )

    peak_stress_ff_controlled = np.max(
        stress_ff_controlled
    )


    # --------------------------------------------------------
    # Performance
    # --------------------------------------------------------

    root_reduction_ff = (
        (
            peak_root_ff_uncontrolled
            - peak_root_ff_controlled
        )
        / peak_root_ff_uncontrolled
    ) * 100


    tip_reduction_ff = (
        (
            peak_tip_ff_uncontrolled
            - peak_tip_ff_controlled
        )
        / peak_tip_ff_uncontrolled
    ) * 100


    stress_reduction_ff = (
        (
            peak_stress_ff_uncontrolled
            - peak_stress_ff_controlled
        )
        / peak_stress_ff_uncontrolled
    ) * 100


    # --------------------------------------------------------
    # Preview geometry
    # --------------------------------------------------------

    preview_distance = (
        V_cruise
        * preview_time
    )


    effective_preview = (
        preview_time
        - preview_control_delay
    )


    # --------------------------------------------------------
    # Actuator state at gust arrival
    # --------------------------------------------------------

    gust_arrival_index = np.argmin(
        np.abs(time_ff)
    )

    deflection_at_gust_arrival = (
        actuator_ff[
            gust_arrival_index
        ]
    )


    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    preview_corrected_results.append({

        "Preview_Time_s":
            preview_time,

        "Preview_Distance_m":
            preview_distance,

        "Effective_Preview_s":
            effective_preview,

        "Deflection_at_Gust_Arrival_deg":
            deflection_at_gust_arrival,

        "Peak_Actuator_Deflection_deg":
            np.max(
                np.abs(
                    actuator_ff
                )
            ),

        "Peak_Root_Moment_MNm":
            peak_root_ff_controlled / 1e6,

        "Minimum_Root_Moment_MNm":
            minimum_root_ff_controlled / 1e6,

        "Root_Moment_Reduction_%":
            root_reduction_ff,

        "Peak_Root_Stress_MPa":
            peak_stress_ff_controlled / 1e6,

        "Stress_Reduction_%":
            stress_reduction_ff,

        "Peak_Tip_Deflection_m":
            peak_tip_ff_controlled,

        "Minimum_Tip_Deflection_m":
            minimum_tip_ff_controlled,

        "Tip_Deflection_Reduction_%":
            tip_reduction_ff,

        "Meets_10pct_Target":
            root_reduction_ff >= 10.0
    })


# ------------------------------------------------------------
# 7. Results table
# ------------------------------------------------------------

preview_corrected_df = pd.DataFrame(
    preview_corrected_results
)


print()
print(
    "HART-120 CORRECTED PREVIEW / FEEDFORWARD STUDY"
)

print(
    "----------------------------------------------"
)

print(
    preview_corrected_df
    .round(3)
    .to_string(index=False)
)


# ------------------------------------------------------------
# 8. Best preview case
# ------------------------------------------------------------

best_corrected_preview_index = (
    preview_corrected_df[
        "Root_Moment_Reduction_%"
    ].idxmax()
)


best_corrected_preview = (
    preview_corrected_df.loc[
        best_corrected_preview_index
    ]
)


print()
print(
    "BEST PHYSICALLY CORRECTED PREVIEW CASE"
)

print(
    "--------------------------------------"
)

print(
    f"Preview time: "
    f"{best_corrected_preview['Preview_Time_s']:.3f} s"
)

print(
    f"Forward sensor distance: "
    f"{best_corrected_preview['Preview_Distance_m']:.2f} m"
)

print(
    f"Effective preview after delay: "
    f"{best_corrected_preview['Effective_Preview_s']:.3f} s"
)

print(
    f"Surface deflection at gust arrival: "
    f"{best_corrected_preview['Deflection_at_Gust_Arrival_deg']:.2f} deg"
)

print(
    f"Peak actuator deflection: "
    f"{best_corrected_preview['Peak_Actuator_Deflection_deg']:.2f} deg"
)

print()

print(
    f"Uncontrolled peak root moment: "
    f"{peak_root_ff_uncontrolled/1e6:.3f} MN·m"
)

print(
    f"Controlled peak root moment: "
    f"{best_corrected_preview['Peak_Root_Moment_MNm']:.3f} MN·m"
)

print(
    f"Root moment reduction: "
    f"{best_corrected_preview['Root_Moment_Reduction_%']:.2f} %"
)

print()

print(
    f"Controlled peak stress: "
    f"{best_corrected_preview['Peak_Root_Stress_MPa']:.2f} MPa"
)

print(
    f"Stress reduction: "
    f"{best_corrected_preview['Stress_Reduction_%']:.2f} %"
)

print()

print(
    f"Controlled peak tip deflection: "
    f"{best_corrected_preview['Peak_Tip_Deflection_m']:.4f} m"
)

print(
    f"Tip deflection reduction: "
    f"{best_corrected_preview['Tip_Deflection_Reduction_%']:.2f} %"
)


# ------------------------------------------------------------
# 9. Minimum preview satisfying 10% target
# ------------------------------------------------------------

corrected_target_cases = (
    preview_corrected_df[
        preview_corrected_df[
            "Meets_10pct_Target"
        ]
    ]
)


if len(corrected_target_cases) > 0:

    minimum_corrected_preview_index = (
        corrected_target_cases[
            "Preview_Time_s"
        ].idxmin()
    )

    minimum_corrected_preview = (
        preview_corrected_df.loc[
            minimum_corrected_preview_index
        ]
    )


    print()
    print(
        "MINIMUM CORRECTED PREVIEW MEETING TARGET"
    )

    print(
        "----------------------------------------"
    )

    print(
        f"Preview time: "
        f"{minimum_corrected_preview['Preview_Time_s']:.3f} s"
    )

    print(
        f"Forward sensing distance: "
        f"{minimum_corrected_preview['Preview_Distance_m']:.2f} m"
    )

    print(
        f"Root moment reduction: "
        f"{minimum_corrected_preview['Root_Moment_Reduction_%']:.2f} %"
    )


# ------------------------------------------------------------
# 10. Plot — corrected preview performance
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_corrected_df[
        "Preview_Time_s"
    ],
    preview_corrected_df[
        "Root_Moment_Reduction_%"
    ],
    marker="o"
)

plt.axhline(
    10.0,
    linestyle="--",
    label="Project target"
)

plt.axvline(
    preview_control_delay,
    linestyle="--",
    label="Control delay"
)

plt.xlabel(
    "Gust Preview Time (s)"
)

plt.ylabel(
    "Peak Root Moment Reduction (%)"
)

plt.title(
    "HART-120 — Corrected Preview-Control Performance"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 11. Plot — pre-actuation at gust arrival
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_corrected_df[
        "Preview_Time_s"
    ],
    preview_corrected_df[
        "Deflection_at_Gust_Arrival_deg"
    ],
    marker="o"
)

plt.xlabel(
    "Gust Preview Time (s)"
)

plt.ylabel(
    "Control-Surface Deflection at Gust Arrival (deg)"
)

plt.title(
    "HART-120 — Feedforward Pre-Actuation"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 12. Plot — peak root load vs sensor range
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_corrected_df[
        "Preview_Distance_m"
    ],
    preview_corrected_df[
        "Peak_Root_Moment_MNm"
    ],
    marker="o"
)

plt.xlabel(
    "Forward Gust-Sensing Distance (m)"
)

plt.ylabel(
    "Peak Root Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — Preview Sensor Range vs Dynamic Wing Load"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 13. Plot — positive and minimum root loads
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    preview_corrected_df[
        "Preview_Time_s"
    ],
    preview_corrected_df[
        "Peak_Root_Moment_MNm"
    ],
    marker="o",
    label="Maximum root moment"
)

plt.plot(
    preview_corrected_df[
        "Preview_Time_s"
    ],
    preview_corrected_df[
        "Minimum_Root_Moment_MNm"
    ],
    marker="o",
    label="Minimum root moment"
)

plt.xlabel(
    "Gust Preview Time (s)"
)

plt.ylabel(
    "Root Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — Preview Timing and Load Reversal"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 87]
# ============================================================
# HART-120 — STATIC AEROELASTIC TWIST + LOAD REDISTRIBUTION
#
# Industrial problem:
# A flexible high-aspect-ratio wing twists under aerodynamic
# loading. That twist changes local angle of attack, which
# redistributes lift and therefore changes structural loads.
#
# Reduced-order bending-torsion aeroelastic model.
# ============================================================


# ------------------------------------------------------------
# 1. Aerodynamic / torsional structural assumptions
# ------------------------------------------------------------

nu_eq = 0.30

G_eq = (
    E_eq
    / (2 * (1 + nu_eq))
)

q_cruise = (
    0.5
    * rho_cruise
    * V_cruise**2
)


# Elastic axis and aerodynamic centre
elastic_axis_fraction = 0.40
aerodynamic_center_fraction = 0.25

aero_moment_arm = (
    (
        elastic_axis_fraction
        - aerodynamic_center_fraction
    )
    * chord
)


# ------------------------------------------------------------
# 2. Simplified closed wingbox torsional stiffness
# ------------------------------------------------------------

box_width_fraction = 0.45

box_width = (
    box_width_fraction
    * chord
)

torsion_skin_thickness = 4.0e-3   # m


box_enclosed_area = (
    box_width
    * box_height
)

box_perimeter = (
    2
    * (
        box_width
        + box_height
    )
)


# Thin-walled closed rectangular section
J_torsion = (
    4
    * box_enclosed_area**2
    * torsion_skin_thickness
    / box_perimeter
)


GJ = (
    G_eq
    * J_torsion
)


# ------------------------------------------------------------
# 3. Finite-wing corrected lift-curve slope
# ------------------------------------------------------------

a0 = lift_curve_slope

aeroelastic_lift_curve_slope = (
    a0
    /
    (
        1
        + a0
        / (
            np.pi
            * oswald_e
            * AR_baseline
        )
    )
)


# Force aerodynamic perturbation to approach zero at wing tip
finite_wing_weight = np.sqrt(
    np.maximum(
        0.0,
        1.0 - eta**2
    )
)


aero_sensitivity = (
    q_cruise
    * chord
    * aeroelastic_lift_curve_slope
    * finite_wing_weight
)


# ------------------------------------------------------------
# 4. Aeroelastic iterative solution
# ------------------------------------------------------------

lift_aeroelastic = (
    lift_per_span.copy()
)

relaxation_factor = 0.40
convergence_tolerance = 1.0e-7
max_iterations = 500


for iteration in range(max_iterations):

    # --------------------------------------------------------
    # Distributed aerodynamic torsional moment
    #
    # Negative sign represents passive nose-down / washout
    # twisting for the selected AC-EA arrangement.
    # --------------------------------------------------------

    torsional_moment_per_span = (
        -lift_aeroelastic
        * aero_moment_arm
    )


    # --------------------------------------------------------
    # Internal torque distribution
    # --------------------------------------------------------

    internal_torque = np.zeros_like(
        y
    )

    for i in range(len(y)):

        internal_torque[i] = np.trapezoid(
            torsional_moment_per_span[i:],
            y[i:]
        )


    # --------------------------------------------------------
    # Twist gradient
    #
    # d(theta)/dy = T / GJ
    # --------------------------------------------------------

    twist_rate = (
        internal_torque
        / GJ
    )


    # --------------------------------------------------------
    # Spanwise twist
    # Root is fixed
    # --------------------------------------------------------

    twist = np.zeros_like(
        y
    )

    for i in range(
        1,
        len(y)
    ):

        twist[i] = np.trapezoid(
            twist_rate[:i+1],
            y[:i+1]
        )


    # --------------------------------------------------------
    # Aircraft trim correction
    #
    # Adjust global incidence so total half-wing lift remains
    # equal to the required 1-g lift.
    # --------------------------------------------------------

    trim_angle_rad = (
        -np.trapezoid(
            aero_sensitivity
            * twist,
            y
        )
        /
        np.trapezoid(
            aero_sensitivity,
            y
        )
    )


    # --------------------------------------------------------
    # New aeroelastic lift distribution
    # --------------------------------------------------------

    lift_target = (
        lift_per_span
        + aero_sensitivity
        * (
            twist
            + trim_angle_rad
        )
    )


    # --------------------------------------------------------
    # Convergence check
    # --------------------------------------------------------

    convergence_error = (
        np.max(
            np.abs(
                lift_target
                - lift_aeroelastic
            )
        )
        /
        np.max(
            np.abs(
                lift_per_span
            )
        )
    )


    # --------------------------------------------------------
    # Under-relaxation
    # --------------------------------------------------------

    lift_aeroelastic = (
        (
            1
            - relaxation_factor
        )
        * lift_aeroelastic
        +
        relaxation_factor
        * lift_target
    )


    if convergence_error < convergence_tolerance:
        break


# ------------------------------------------------------------
# 5. Final aeroelastic load solution
# ------------------------------------------------------------

torsional_moment_per_span = (
    -lift_aeroelastic
    * aero_moment_arm
)


internal_torque = np.zeros_like(
    y
)

for i in range(len(y)):

    internal_torque[i] = np.trapezoid(
        torsional_moment_per_span[i:],
        y[i:]
    )


twist_rate = (
    internal_torque
    / GJ
)


twist = np.zeros_like(
    y
)

for i in range(
    1,
    len(y)
):

    twist[i] = np.trapezoid(
        twist_rate[:i+1],
        y[:i+1]
    )


trim_angle_rad = (
    -np.trapezoid(
        aero_sensitivity
        * twist,
        y
    )
    /
    np.trapezoid(
        aero_sensitivity,
        y
    )
)


lift_aeroelastic = (
    lift_per_span
    + aero_sensitivity
    * (
        twist
        + trim_angle_rad
    )
)


# ------------------------------------------------------------
# 6. Verify total lift conservation
# ------------------------------------------------------------

L_half_aeroelastic = np.trapezoid(
    lift_aeroelastic,
    y
)


lift_error_percent = (
    (
        L_half_aeroelastic
        - L_half
    )
    / L_half
) * 100


# ------------------------------------------------------------
# 7. Aeroelastic shear force
# ------------------------------------------------------------

shear_aeroelastic = np.zeros_like(
    y
)

for i in range(len(y)):

    shear_aeroelastic[i] = np.trapezoid(
        lift_aeroelastic[i:],
        y[i:]
    )


# ------------------------------------------------------------
# 8. Aeroelastic bending moment
# ------------------------------------------------------------

moment_aeroelastic = np.zeros_like(
    y
)

for i in range(len(y)):

    moment_aeroelastic[i] = np.trapezoid(
        shear_aeroelastic[i:],
        y[i:]
    )


# ------------------------------------------------------------
# 9. Spar-cap stress
# ------------------------------------------------------------

stress_aeroelastic = (
    moment_aeroelastic
    /
    (
        A_cap_mass_reduced
        * box_height
    )
)


max_stress_aeroelastic = np.max(
    stress_aeroelastic
)


# ------------------------------------------------------------
# 10. Aeroelastic bending deflection
# ------------------------------------------------------------

curvature_aeroelastic = (
    moment_aeroelastic
    / EI_mass_reduced
)


slope_aeroelastic = np.zeros_like(
    y
)

for i in range(
    1,
    len(y)
):

    slope_aeroelastic[i] = np.trapezoid(
        curvature_aeroelastic[:i+1],
        y[:i+1]
    )


deflection_aeroelastic = np.zeros_like(
    y
)

for i in range(
    1,
    len(y)
):

    deflection_aeroelastic[i] = np.trapezoid(
        slope_aeroelastic[:i+1],
        y[:i+1]
    )


tip_deflection_aeroelastic = (
    deflection_aeroelastic[-1]
)


# ------------------------------------------------------------
# 11. Aerodynamic load centroid
# ------------------------------------------------------------

load_centroid_baseline = (
    np.trapezoid(
        lift_per_span
        * y,
        y
    )
    / L_half
)


load_centroid_aeroelastic = (
    np.trapezoid(
        lift_aeroelastic
        * y,
        y
    )
    / L_half_aeroelastic
)


centroid_shift = (
    load_centroid_aeroelastic
    - load_centroid_baseline
)


# ------------------------------------------------------------
# 12. Structural-load reductions
# ------------------------------------------------------------

aeroelastic_root_moment_reduction = (
    (
        bending_moment[0]
        - moment_aeroelastic[0]
    )
    / bending_moment[0]
) * 100


aeroelastic_stress_reduction = (
    (
        np.max(
            sigma_mass_reduced
        )
        - max_stress_aeroelastic
    )
    /
    np.max(
        sigma_mass_reduced
    )
) * 100


aeroelastic_deflection_reduction = (
    (
        tip_deflection_mass_reduced
        - tip_deflection_aeroelastic
    )
    / tip_deflection_mass_reduced
) * 100


# ------------------------------------------------------------
# 13. Output
# ------------------------------------------------------------

print()
print(
    "HART-120 STATIC AEROELASTIC TWIST ANALYSIS"
)

print(
    "------------------------------------------"
)

print(
    f"Iterations to convergence: "
    f"{iteration + 1}"
)

print(
    f"Convergence error: "
    f"{convergence_error:.3e}"
)

print()

print(
    f"Equivalent shear modulus: "
    f"{G_eq/1e9:.2f} GPa"
)

print(
    f"Root torsional stiffness GJ: "
    f"{GJ[0]/1e6:.2f} MN·m²"
)

print(
    f"Tip torsional stiffness GJ: "
    f"{GJ[-1]/1e6:.2f} MN·m²"
)

print()

print(
    f"Root twist: "
    f"{np.degrees(twist[0]):.3f} deg"
)

print(
    f"Tip aeroelastic twist: "
    f"{np.degrees(twist[-1]):.3f} deg"
)

print(
    f"Maximum absolute twist: "
    f"{np.max(np.abs(np.degrees(twist))):.3f} deg"
)

print(
    f"Required trim-angle correction: "
    f"{np.degrees(trim_angle_rad):.3f} deg"
)

print()

print(
    f"Required 1-g half-wing lift: "
    f"{L_half/1000:.2f} kN"
)

print(
    f"Aeroelastic half-wing lift: "
    f"{L_half_aeroelastic/1000:.2f} kN"
)

print(
    f"Lift conservation error: "
    f"{lift_error_percent:.6f} %"
)

print()

print(
    f"Baseline load centroid: "
    f"{load_centroid_baseline:.3f} m"
)

print(
    f"Aeroelastic load centroid: "
    f"{load_centroid_aeroelastic:.3f} m"
)

print(
    f"Spanwise load-centroid shift: "
    f"{centroid_shift:.3f} m"
)

print()

print(
    f"Rigid-load root moment: "
    f"{bending_moment[0]/1e6:.3f} MN·m"
)

print(
    f"Aeroelastic root moment: "
    f"{moment_aeroelastic[0]/1e6:.3f} MN·m"
)

print(
    f"Root-moment change: "
    f"{aeroelastic_root_moment_reduction:.2f} % reduction"
)

print()

print(
    f"Rigid-load maximum stress: "
    f"{np.max(sigma_mass_reduced)/1e6:.2f} MPa"
)

print(
    f"Aeroelastic maximum stress: "
    f"{max_stress_aeroelastic/1e6:.2f} MPa"
)

print(
    f"Stress reduction: "
    f"{aeroelastic_stress_reduction:.2f} %"
)

print()

print(
    f"Rigid-load tip deflection: "
    f"{tip_deflection_mass_reduced:.4f} m"
)

print(
    f"Aeroelastic tip deflection: "
    f"{tip_deflection_aeroelastic:.4f} m"
)

print(
    f"Tip-deflection reduction: "
    f"{aeroelastic_deflection_reduction:.2f} %"
)


# ------------------------------------------------------------
# 14. Plot — aeroelastic twist
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    eta,
    np.degrees(
        twist
    )
)

plt.axhline(
    0.0,
    linestyle="--"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Aeroelastic Twist (deg)"
)

plt.title(
    "HART-120 — Static Aeroelastic Wing Twist"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 15. Plot — lift redistribution
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    eta,
    lift_per_span / 1000,
    label="Rigid-Wing Reference"
)

plt.plot(
    eta,
    lift_aeroelastic / 1000,
    label="Flexible Aeroelastic Wing"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Lift per Unit Span (kN/m)"
)

plt.title(
    "HART-120 — Aeroelastic Lift Redistribution"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 16. Plot — bending moment
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    eta,
    bending_moment / 1e6,
    label="Rigid Load"
)

plt.plot(
    eta,
    moment_aeroelastic / 1e6,
    label="Aeroelastic Load"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — Aeroelastic Bending Load Redistribution"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 17. Plot — bending deflection
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    eta,
    deflection_mass_reduced
    if 'deflection_mass_reduced' in globals()
    else (
        deflection
    ),
    label="Rigid-Load Response"
)

plt.plot(
    eta,
    deflection_aeroelastic,
    label="Aeroelastic Response"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Vertical Deflection (m)"
)

plt.title(
    "HART-120 — Effect of Aeroelastic Load Redistribution"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 88]
# ============================================================
# HART-120 — SPAR-CAP COMPRESSION BUCKLING CHECK
#
# Industrial problem:
# A lightweight wing structure can satisfy material-strength
# limits but fail earlier because the compression cap buckles.
#
# Preliminary equivalent-panel buckling model.
#
# IMPORTANT:
# This is a reduced-order conceptual sizing calculation.
# It is NOT a detailed composite laminate buckling analysis.
# ============================================================


# ------------------------------------------------------------
# 1. Equivalent compression-panel assumptions
# ------------------------------------------------------------

nu_panel = 0.30

# Simply-supported long plate approximation
buckling_coefficient = 4.0

# Effective unsupported compression-cap panel width
# Conceptual baseline assumption
cap_panel_width_fraction = 0.18

cap_panel_width = (
    cap_panel_width_fraction
    * chord
)


# ------------------------------------------------------------
# 2. Convert current spar-cap area into an equivalent
# compression-panel thickness
#
# A = b * t
# ------------------------------------------------------------

cap_thickness_current = (
    A_cap_mass_reduced
    / cap_panel_width
)


# ------------------------------------------------------------
# 3. Elastic plate buckling stress
#
# sigma_cr =
#
# k*pi²*E
# ------------------- * (t/b)²
# 12*(1-nu²)
# ------------------------------------------------------------

sigma_buckling_cr = (

    (
        buckling_coefficient
        * np.pi**2
        * E_eq
    )

    /

    (
        12
        * (
            1
            - nu_panel**2
        )
    )

    *

    (
        cap_thickness_current
        / cap_panel_width
    )**2
)


# ------------------------------------------------------------
# 4. Applied compression-stress load cases
#
# Use absolute stress because upper/lower cap identity
# depends on bending direction.
# ------------------------------------------------------------

sigma_cruise_check = np.abs(
    sigma_mass_reduced
)

sigma_gust_check = np.abs(
    sigma_gust
)

sigma_maneuver_check = np.abs(
    sigma_maneuver
)

sigma_aeroelastic_check = np.abs(
    stress_aeroelastic
)


# ------------------------------------------------------------
# 5. Build structural stress envelope
# ------------------------------------------------------------

sigma_buckling_envelope = np.maximum.reduce([

    sigma_cruise_check,

    sigma_gust_check,

    sigma_maneuver_check,

    sigma_aeroelastic_check
])


# ------------------------------------------------------------
# 6. Governing load case at every span station
# ------------------------------------------------------------

stress_case_stack = np.vstack([

    sigma_cruise_check,

    sigma_gust_check,

    sigma_maneuver_check,

    sigma_aeroelastic_check
])


governing_case_index = np.argmax(
    stress_case_stack,
    axis=0
)


case_names = np.array([

    "1-g Cruise",

    "10 m/s Gust",

    "2.5-g Maneuver",

    "1-g Aeroelastic"
])


governing_buckling_case = (

    case_names[
        governing_case_index
    ]
)


# ------------------------------------------------------------
# 7. Buckling utilization
#
# Utilization <= 1 : PASS
# Utilization >  1 : FAIL
# ------------------------------------------------------------

buckling_utilization = (

    sigma_buckling_envelope

    / sigma_buckling_cr
)


critical_buckling_index = np.argmax(
    buckling_utilization
)


critical_buckling_utilization = (

    buckling_utilization[
        critical_buckling_index
    ]
)


critical_buckling_case = (

    governing_buckling_case[
        critical_buckling_index
    ]
)


# ------------------------------------------------------------
# 8. Required thickness from buckling constraint
#
# Rearranged plate-buckling equation:
#
# t_req =
#
# b * sqrt[
#     sigma * 12*(1-nu²)
#     --------------------
#        k*pi²*E
# ]
# ------------------------------------------------------------

cap_thickness_buckling_required = (

    cap_panel_width

    * np.sqrt(

        (

            sigma_buckling_envelope
            * 12
            * (
                1
                - nu_panel**2
            )

        )

        /

        (

            buckling_coefficient
            * np.pi**2
            * E_eq

        )
    )
)


# ------------------------------------------------------------
# 9. Final cap thickness
#
# Must satisfy BOTH:
#
# current structural area requirement
# AND
# buckling requirement
# ------------------------------------------------------------

cap_thickness_final = np.maximum(

    cap_thickness_current,

    cap_thickness_buckling_required
)


# ------------------------------------------------------------
# 10. New spar-cap area
# ------------------------------------------------------------

A_cap_buckling_sized = (

    cap_panel_width

    * cap_thickness_final
)


# ------------------------------------------------------------
# 11. Cap mass after buckling sizing
# ------------------------------------------------------------

cap_mass_per_span_buckling = (

    2
    * A_cap_buckling_sized
    * rho_eq
)


m_caps_half_buckling = np.trapezoid(

    cap_mass_per_span_buckling,

    y
)


m_caps_total_buckling = (

    2
    * m_caps_half_buckling
)


# ------------------------------------------------------------
# 12. Current cap mass
# ------------------------------------------------------------

m_caps_half_current = np.trapezoid(

    cap_mass_per_span_mass_reduced,

    y
)


m_caps_total_current = (

    2
    * m_caps_half_current
)


# ------------------------------------------------------------
# 13. Buckling mass penalty
# ------------------------------------------------------------

buckling_mass_penalty = (

    m_caps_total_buckling

    - m_caps_total_current
)


buckling_mass_penalty_percent = (

    buckling_mass_penalty

    / m_caps_total_current

) * 100


# ------------------------------------------------------------
# 14. Updated simplified wingbox mass
#
# Use controlled-envelope web mass from previous sizing
# ------------------------------------------------------------

wingbox_mass_buckling_sized = (

    m_caps_total_buckling

    + m_web_total_controlled
)


# ------------------------------------------------------------
# 15. Spanwise buckling margin
#
# Margin = allowable/applied - 1
# ------------------------------------------------------------

buckling_margin = (

    sigma_buckling_cr

    / np.maximum(
        sigma_buckling_envelope,
        1.0
    )

    - 1.0
)


# ------------------------------------------------------------
# 16. Results
# ------------------------------------------------------------

print()
print(
    "HART-120 SPAR-CAP COMPRESSION BUCKLING CHECK"
)

print(
    "--------------------------------------------"
)

print(
    f"Equivalent panel-width fraction: "
    f"{cap_panel_width_fraction:.3f}"
)

print()

print(
    f"Root panel width: "
    f"{cap_panel_width[0]:.3f} m"
)

print(
    f"Root equivalent cap thickness: "
    f"{cap_thickness_current[0]*1000:.2f} mm"
)

print(
    f"Tip equivalent cap thickness: "
    f"{cap_thickness_current[-1]*1000:.2f} mm"
)

print()

print(
    f"Root elastic buckling stress: "
    f"{sigma_buckling_cr[0]/1e6:.2f} MPa"
)

print(
    f"Minimum elastic buckling stress: "
    f"{np.min(sigma_buckling_cr)/1e6:.2f} MPa"
)

print()

print(
    f"Maximum buckling utilization: "
    f"{critical_buckling_utilization:.3f}"
)

print(
    f"Critical span location: "
    f"{y[critical_buckling_index]:.2f} m"
)

print(
    f"Critical normalized span: "
    f"{eta[critical_buckling_index]:.3f}"
)

print(
    f"Governing load case: "
    f"{critical_buckling_case}"
)

print()

print(
    f"Applied stress at critical location: "
    f"{sigma_buckling_envelope[critical_buckling_index]/1e6:.2f} MPa"
)

print(
    f"Critical buckling stress: "
    f"{sigma_buckling_cr[critical_buckling_index]/1e6:.2f} MPa"
)

print(
    f"Buckling margin at critical location: "
    f"{buckling_margin[critical_buckling_index]:.3f}"
)

print()

print(
    f"Current total cap mass: "
    f"{m_caps_total_current:.2f} kg"
)

print(
    f"Buckling-sized total cap mass: "
    f"{m_caps_total_buckling:.2f} kg"
)

print(
    f"Buckling mass penalty: "
    f"{buckling_mass_penalty:.2f} kg"
)

print(
    f"Buckling mass penalty: "
    f"{buckling_mass_penalty_percent:.2f} %"
)

print()

print(
    f"Final simplified wingbox mass: "
    f"{wingbox_mass_buckling_sized:.2f} kg"
)


# ------------------------------------------------------------
# 17. PASS / FAIL
# ------------------------------------------------------------

if critical_buckling_utilization <= 1.0:

    print()
    print(
        "BUCKLING CHECK: PASS"
    )

else:

    print()
    print(
        "BUCKLING CHECK: FAIL"
    )

    print(
        "Additional cap thickness / reduced stiffener spacing required."
    )


# ------------------------------------------------------------
# 18. Plot — applied stress vs buckling stress
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    sigma_buckling_envelope / 1e6,
    label="Applied Compression Stress Envelope"
)

plt.plot(
    eta,
    sigma_buckling_cr / 1e6,
    label="Elastic Buckling Stress"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Stress (MPa)"
)

plt.title(
    "HART-120 — Spar-Cap Compression Buckling"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 19. Plot — buckling utilization
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    buckling_utilization
)

plt.axhline(
    1.0,
    linestyle="--",
    label="Buckling Limit"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Buckling Utilization"
)

plt.title(
    "HART-120 — Spanwise Buckling Utilization"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 20. Plot — current vs required cap thickness
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    cap_thickness_current * 1000,
    label="Current Equivalent Thickness"
)

plt.plot(
    eta,
    cap_thickness_buckling_required * 1000,
    label="Buckling Required Thickness"
)

plt.plot(
    eta,
    cap_thickness_final * 1000,
    label="Final Sized Thickness"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Equivalent Spar-Cap Thickness (mm)"
)

plt.title(
    "HART-120 — Buckling-Driven Cap Sizing"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 89]
# ============================================================
# HART-120 — COMPRESSION-PANEL BUCKLING DESIGN REQUIREMENT
#
# Instead of pretending the entire spar-cap area is one thick
# plate, determine the maximum allowable unsupported width-to-
# thickness ratio (b/t) required to prevent local buckling.
#
# This gives a useful preliminary requirement for:
# - stringer spacing
# - rib spacing
# - cap-panel subdivision
# ============================================================


# ------------------------------------------------------------
# 1. Material / plate assumptions
# ------------------------------------------------------------

nu_panel = 0.30
buckling_coefficient = 4.0


# ------------------------------------------------------------
# 2. Structural compression-stress envelope
# ------------------------------------------------------------

sigma_panel_envelope = np.maximum.reduce([

    np.abs(sigma_mass_reduced),

    np.abs(sigma_gust),

    np.abs(sigma_maneuver),

    np.abs(stress_aeroelastic)

])


# ------------------------------------------------------------
# 3. Maximum allowable b/t ratio
#
# Classical plate buckling:
#
# sigma_cr =
#
# k*pi²*E
# ------------------ * (t/b)²
# 12*(1-nu²)
#
# therefore:
#
# b/t =
#
# sqrt[
# k*pi²*E
# ---------------------
# 12*(1-nu²)*sigma
# ]
# ------------------------------------------------------------

bt_allowable = np.sqrt(

    (
        buckling_coefficient
        * np.pi**2
        * E_eq
    )

    /

    (
        12
        * (
            1
            - nu_panel**2
        )
        * np.maximum(
            sigma_panel_envelope,
            1.0
        )
    )
)


# ------------------------------------------------------------
# 4. Critical location
# ------------------------------------------------------------

critical_bt_index = np.argmin(
    bt_allowable
)

critical_bt_ratio = (
    bt_allowable[
        critical_bt_index
    ]
)


# ------------------------------------------------------------
# 5. Governing load case
# ------------------------------------------------------------

stress_case_stack = np.vstack([

    np.abs(sigma_mass_reduced),

    np.abs(sigma_gust),

    np.abs(sigma_maneuver),

    np.abs(stress_aeroelastic)

])


governing_case_index = np.argmax(
    stress_case_stack,
    axis=0
)


case_names = np.array([

    "1-g Cruise",

    "10 m/s Gust",

    "2.5-g Maneuver",

    "1-g Aeroelastic"
])


critical_panel_case = (

    case_names[
        governing_case_index[
            critical_bt_index
        ]
    ]
)


# ------------------------------------------------------------
# 6. Convert b/t requirement into example support-spacing
# requirements for several panel thicknesses
#
# These are NOT chosen design thicknesses.
# They show what spacing would be allowable IF a given
# effective panel thickness were selected.
# ------------------------------------------------------------

candidate_panel_thickness_mm = np.array([
    2.0,
    3.0,
    4.0,
    5.0,
    6.0,
    8.0
])


candidate_panel_thickness_m = (
    candidate_panel_thickness_mm
    / 1000
)


allowable_support_spacing_root = (

    critical_bt_ratio
    * candidate_panel_thickness_m
)


# ------------------------------------------------------------
# 7. Results
# ------------------------------------------------------------

print()
print(
    "HART-120 COMPRESSION-PANEL BUCKLING REQUIREMENT"
)

print(
    "------------------------------------------------"
)

print(
    f"Critical span location: "
    f"{y[critical_bt_index]:.2f} m"
)

print(
    f"Critical normalized span: "
    f"{eta[critical_bt_index]:.3f}"
)

print(
    f"Governing load case: "
    f"{critical_panel_case}"
)

print(
    f"Critical compression stress: "
    f"{sigma_panel_envelope[critical_bt_index]/1e6:.2f} MPa"
)

print()

print(
    f"Maximum allowable b/t ratio at critical location: "
    f"{critical_bt_ratio:.2f}"
)

print()


# ------------------------------------------------------------
# 8. Example design interpretation
# ------------------------------------------------------------

print(
    "EXAMPLE MAXIMUM UNSUPPORTED PANEL WIDTHS"
)

print(
    "----------------------------------------"
)

for thickness_mm, spacing_m in zip(
    candidate_panel_thickness_mm,
    allowable_support_spacing_root
):

    print(
        f"For t = {thickness_mm:.1f} mm  ->  "
        f"b_max = {spacing_m*1000:.1f} mm"
    )


# ------------------------------------------------------------
# 9. Spanwise b/t requirement
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    bt_allowable
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Maximum Allowable b/t"
)

plt.title(
    "HART-120 — Compression-Panel Buckling Requirement"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 10. Applied compression stress envelope
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    sigma_panel_envelope / 1e6
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Compression Stress Envelope (MPa)"
)

plt.title(
    "HART-120 — Compression Stress Design Envelope"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 11. Example support-spacing requirements
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

for thickness_mm in [
    3.0,
    4.0,
    5.0,
    6.0
]:

    thickness_m = (
        thickness_mm
        / 1000
    )

    allowable_spacing = (
        bt_allowable
        * thickness_m
    )

    plt.plot(
        eta,
        allowable_spacing * 1000,
        label=f"t = {thickness_mm:.0f} mm"
    )


plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Maximum Unsupported Width (mm)"
)

plt.title(
    "HART-120 — Preliminary Panel Support-Spacing Requirement"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 90]
# ============================================================
# HART-120 — CLEAN BUCKLING VISUALIZATION
#
# Remove very-low-stress stations from b/t and support-spacing
# plots because b/t -> infinity as compression stress -> 0.
#
# This affects visualization ONLY.
# Original calculations remain unchanged.
# ============================================================


# ------------------------------------------------------------
# 1. Minimum stress for meaningful local buckling sizing
#
# Stations below this are effectively unloaded for this
# preliminary panel-buckling study.
# ------------------------------------------------------------

buckling_plot_stress_threshold = 5.0e6    # 5 MPa


buckling_active_region = (
    sigma_panel_envelope
    >= buckling_plot_stress_threshold
)


# ------------------------------------------------------------
# 2. Mask low-load stations
# ------------------------------------------------------------

bt_allowable_plot = np.where(
    buckling_active_region,
    bt_allowable,
    np.nan
)


# ------------------------------------------------------------
# 3. Print extent of meaningful buckling region
# ------------------------------------------------------------

active_indices = np.where(
    buckling_active_region
)[0]


last_active_index = active_indices[-1]


print()
print(
    "HART-120 BUCKLING DESIGN REGION"
)

print(
    "-------------------------------"
)

print(
    f"Stress threshold used for plotting: "
    f"{buckling_plot_stress_threshold/1e6:.1f} MPa"
)

print(
    f"Buckling sizing remains relevant to approximately "
    f"η = {eta[last_active_index]:.3f}"
)

print(
    f"Corresponding span location: "
    f"{y[last_active_index]:.2f} m"
)

print()

print(
    f"Critical root b/t requirement: "
    f"{critical_bt_ratio:.2f}"
)


# ------------------------------------------------------------
# 4. CLEAN PLOT — compression stress envelope
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    sigma_panel_envelope / 1e6
)

plt.axhline(
    buckling_plot_stress_threshold / 1e6,
    linestyle="--",
    label="Plotting relevance threshold"
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Compression Stress Envelope (MPa)"
)

plt.title(
    "HART-120 — Compression Stress Design Envelope"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 5. CLEAN PLOT — allowable b/t
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    eta,
    bt_allowable_plot
)

plt.scatter(
    eta[critical_bt_index],
    critical_bt_ratio,
    label=(
        f"Critical requirement: "
        f"b/t = {critical_bt_ratio:.2f}"
    )
)

plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Maximum Allowable b/t"
)

plt.title(
    "HART-120 — Compression-Panel Buckling Requirement"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 6. CLEAN PLOT — example support spacing
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

for thickness_mm in [
    3.0,
    4.0,
    5.0,
    6.0
]:

    thickness_m = (
        thickness_mm
        / 1000
    )

    allowable_spacing_plot = (
        bt_allowable_plot
        * thickness_m
    )

    plt.plot(
        eta,
        allowable_spacing_plot * 1000,
        label=f"t = {thickness_mm:.0f} mm"
    )


plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Maximum Unsupported Panel Width (mm)"
)

plt.title(
    "HART-120 — Preliminary Compression-Panel Support Requirement"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 7. Root design table
# ------------------------------------------------------------

root_spacing_results = pd.DataFrame({

    "Effective_Panel_Thickness_mm":
        candidate_panel_thickness_mm,

    "Maximum_Unsupported_Width_mm":
        allowable_support_spacing_root
        * 1000
})


print()
print(
    "HART-120 ROOT COMPRESSION-PANEL DESIGN GUIDANCE"
)

print(
    "------------------------------------------------"
)

print(
    root_spacing_results
    .round(1)
    .to_string(index=False)
)

# %% [notebook cell 91]
# ============================================================
# HART-120 — ASPECT-RATIO AERO-STRUCTURAL TRADE STUDY
#
# Industrial problem:
# Higher aspect ratio reduces induced drag but increases:
# - wing span
# - root bending moment
# - structural stiffness requirement
# - wingbox mass
#
# Objective:
# Quantify the aerodynamic benefit versus structural penalty.
#
# IMPORTANT:
# Wing area, design lift, taper ratio, cruise condition and
# conceptual material model are held constant.
#
# This is a reduced-order conceptual trade study.
# ============================================================


# ------------------------------------------------------------
# 1. Aspect-ratio design space
# ------------------------------------------------------------

AR_values = np.arange(
    10.0,
    18.5,
    0.5
)


# ------------------------------------------------------------
# 2. Constants for structural trade
# ------------------------------------------------------------

n_AR_stations = 51

deflection_ratio_AR = 0.05

tau_allow_AR = 40e6

web_min_gauge_AR = 2.5e-3

thickness_ratio_AR = 0.12

box_height_fraction_AR = 0.80


# ------------------------------------------------------------
# 3. Storage
# ------------------------------------------------------------

AR_trade_results = []


# ------------------------------------------------------------
# 4. Sweep aspect ratio
# ------------------------------------------------------------

for AR_test in AR_values:

    # ========================================================
    # GEOMETRY
    # ========================================================

    span_test = np.sqrt(
        AR_test
        * S_wing
    )

    half_span_test = (
        span_test / 2
    )


    root_chord_test = (
        2
        * S_wing
        /
        (
            span_test
            * (
                1
                + taper_ratio
            )
        )
    )


    tip_chord_test = (
        taper_ratio
        * root_chord_test
    )


    y_test = np.linspace(
        0.0,
        half_span_test,
        n_AR_stations
    )


    eta_test = (
        y_test
        / half_span_test
    )


    chord_test = (
        root_chord_test
        -
        (
            root_chord_test
            - tip_chord_test
        )
        * eta_test
    )


    # ========================================================
    # AERODYNAMIC LOADING
    # ========================================================

    elliptical_shape_test = np.sqrt(
        np.maximum(
            0.0,
            1.0
            - eta_test**2
        )
    )


    shape_integral_test = np.trapezoid(
        elliptical_shape_test,
        y_test
    )


    lift_scale_test = (
        L_half
        / shape_integral_test
    )


    lift_per_span_test = (
        lift_scale_test
        * elliptical_shape_test
    )


    # ========================================================
    # SHEAR FORCE
    # ========================================================

    shear_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        shear_test[i] = np.trapezoid(
            lift_per_span_test[i:],
            y_test[i:]
        )


    # ========================================================
    # BENDING MOMENT
    # ========================================================

    moment_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        moment_test[i] = np.trapezoid(
            shear_test[i:],
            y_test[i:]
        )


    # ========================================================
    # STRUCTURAL STIFFNESS DISTRIBUTION
    #
    # Same reduced-order stiffness-shape model used earlier.
    # ========================================================

    stiffness_shape_test = (
        chord_test
        / root_chord_test
    )**3


    # --------------------------------------------------------
    # Trial root stiffness
    # --------------------------------------------------------

    EI_root_trial_test = 1.0e9


    EI_trial_test = (
        EI_root_trial_test
        * stiffness_shape_test
    )


    curvature_trial_test = (
        moment_test
        / EI_trial_test
    )


    slope_trial_test = np.zeros_like(
        y_test
    )


    for i in range(
        1,
        len(y_test)
    ):

        slope_trial_test[i] = np.trapezoid(
            curvature_trial_test[:i+1],
            y_test[:i+1]
        )


    deflection_trial_test = np.zeros_like(
        y_test
    )


    for i in range(
        1,
        len(y_test)
    ):

        deflection_trial_test[i] = np.trapezoid(
            slope_trial_test[:i+1],
            y_test[:i+1]
        )


    # --------------------------------------------------------
    # Same 5%-half-span flexibility target
    # --------------------------------------------------------

    deflection_target_test = (
        deflection_ratio_AR
        * half_span_test
    )


    EI_root_required_test = (

        EI_root_trial_test

        * (
            deflection_trial_test[-1]
            / deflection_target_test
        )
    )


    EI_test = (
        EI_root_required_test
        * stiffness_shape_test
    )


    # ========================================================
    # WINGBOX GEOMETRY
    # ========================================================

    airfoil_thickness_test = (
        thickness_ratio_AR
        * chord_test
    )


    box_height_test = (
        box_height_fraction_AR
        * airfoil_thickness_test
    )


    # ========================================================
    # SPAR-CAP SIZING FROM REQUIRED EI
    # ========================================================

    I_required_test = (
        EI_test
        / E_eq
    )


    A_cap_test = (

        2
        * I_required_test

        / (
            box_height_test**2
        )
    )


    # --------------------------------------------------------
    # Spar-cap mass
    # --------------------------------------------------------

    cap_mass_per_span_test = (

        2
        * A_cap_test
        * rho_eq
    )


    cap_mass_half_test = np.trapezoid(
        cap_mass_per_span_test,
        y_test
    )


    cap_mass_total_test = (
        2
        * cap_mass_half_test
    )


    # ========================================================
    # WEB SIZING
    #
    # Use 2.5-g maneuver shear envelope.
    # ========================================================

    shear_design_test = (
        2.5
        * shear_test
    )


    web_thickness_required_test = (

        shear_design_test

        /
        (
            2
            * tau_allow_AR
            * box_height_test
        )
    )


    web_thickness_test = np.maximum(

        web_thickness_required_test,

        web_min_gauge_AR
    )


    web_mass_per_span_test = (

        2
        * web_thickness_test
        * box_height_test
        * rho_eq
    )


    web_mass_half_test = np.trapezoid(
        web_mass_per_span_test,
        y_test
    )


    web_mass_total_test = (
        2
        * web_mass_half_test
    )


    # ========================================================
    # TOTAL SIMPLIFIED WINGBOX MASS
    # ========================================================

    wingbox_mass_test = (

        cap_mass_total_test
        + web_mass_total_test
    )


    # ========================================================
    # 2.5-g STRUCTURAL STRESS CHECK
    # ========================================================

    moment_maneuver_test = (
        2.5
        * moment_test
    )


    stress_maneuver_test = (

        moment_maneuver_test

        /
        (
            A_cap_test
            * box_height_test
        )
    )


    max_stress_maneuver_test = np.max(
        stress_maneuver_test
    )


    # ========================================================
    # AERODYNAMIC EFFICIENCY
    #
    # Induced drag:
    #
    # CDi = CL² / (pi*e*AR)
    # ========================================================

    CDi_test = (

        CL_cruise**2

        /
        (
            np.pi
            * oswald_e
            * AR_test
        )
    )


    induced_drag_test = (

        0.5
        * rho_cruise
        * V_cruise**2
        * S_wing
        * CDi_test
    )


    induced_power_test = (

        induced_drag_test
        * V_cruise
    )


    # ========================================================
    # STORE RESULT
    # ========================================================

    AR_trade_results.append({

        "Aspect_Ratio":
            AR_test,

        "Span_m":
            span_test,

        "Root_Chord_m":
            root_chord_test,

        "Root_Bending_Moment_MNm":
            moment_test[0] / 1e6,

        "Required_Root_EI_GNm2":
            EI_root_required_test / 1e9,

        "Cap_Mass_kg":
            cap_mass_total_test,

        "Web_Mass_kg":
            web_mass_total_test,

        "Wingbox_Mass_kg":
            wingbox_mass_test,

        "Maneuver_Max_Stress_MPa":
            max_stress_maneuver_test / 1e6,

        "Induced_CD":
            CDi_test,

        "Induced_Drag_kN":
            induced_drag_test / 1000,

        "Induced_Power_MW":
            induced_power_test / 1e6
    })


# ------------------------------------------------------------
# 5. DataFrame
# ------------------------------------------------------------

AR_trade_df = pd.DataFrame(
    AR_trade_results
)


# ------------------------------------------------------------
# 6. Locate HART-120 baseline AR = 13.5
# ------------------------------------------------------------

baseline_AR_index = (

    np.abs(
        AR_trade_df[
            "Aspect_Ratio"
        ]
        - AR_baseline
    )

).idxmin()


baseline_AR_case = (
    AR_trade_df.loc[
        baseline_AR_index
    ]
)


baseline_AR_mass = (
    baseline_AR_case[
        "Wingbox_Mass_kg"
    ]
)


baseline_AR_drag = (
    baseline_AR_case[
        "Induced_Drag_kN"
    ]
)


baseline_AR_moment = (
    baseline_AR_case[
        "Root_Bending_Moment_MNm"
    ]
)


# ------------------------------------------------------------
# 7. Relative aerodynamic and structural changes
# ------------------------------------------------------------

AR_trade_df[
    "Wingbox_Mass_Change_%"
] = (

    (
        AR_trade_df[
            "Wingbox_Mass_kg"
        ]
        - baseline_AR_mass
    )

    / baseline_AR_mass

) * 100


AR_trade_df[
    "Induced_Drag_Change_%"
] = (

    (
        AR_trade_df[
            "Induced_Drag_kN"
        ]
        - baseline_AR_drag
    )

    / baseline_AR_drag

) * 100


AR_trade_df[
    "Induced_Drag_Reduction_%"
] = (

    (
        baseline_AR_drag
        - AR_trade_df[
            "Induced_Drag_kN"
        ]
    )

    / baseline_AR_drag

) * 100


AR_trade_df[
    "Root_Moment_Change_%"
] = (

    (
        AR_trade_df[
            "Root_Bending_Moment_MNm"
        ]
        - baseline_AR_moment
    )

    / baseline_AR_moment

) * 100


# ------------------------------------------------------------
# 8. Structural mass cost per induced-drag benefit
#
# Only meaningful for AR > baseline.
# ------------------------------------------------------------

AR_trade_df[
    "kg_Mass_Increase_per_1pct_Drag_Reduction"
] = np.nan


higher_AR_mask = (
    AR_trade_df[
        "Aspect_Ratio"
    ]
    > AR_baseline
)


AR_trade_df.loc[
    higher_AR_mask,
    "kg_Mass_Increase_per_1pct_Drag_Reduction"
] = (

    (
        AR_trade_df.loc[
            higher_AR_mask,
            "Wingbox_Mass_kg"
        ]
        - baseline_AR_mass
    )

    /
    AR_trade_df.loc[
        higher_AR_mask,
        "Induced_Drag_Reduction_%"
    ]
)


# ------------------------------------------------------------
# 9. Print trade table
# ------------------------------------------------------------

print()
print(
    "HART-120 ASPECT-RATIO AERO-STRUCTURAL TRADE"
)

print(
    "-------------------------------------------"
)

print(

    AR_trade_df[
        [
            "Aspect_Ratio",
            "Span_m",
            "Root_Bending_Moment_MNm",
            "Required_Root_EI_GNm2",
            "Wingbox_Mass_kg",
            "Wingbox_Mass_Change_%",
            "Induced_Drag_kN",
            "Induced_Drag_Reduction_%",
            "Maneuver_Max_Stress_MPa"
        ]
    ]
    .round(3)
    .to_string(index=False)

)


# ------------------------------------------------------------
# 10. Baseline summary
# ------------------------------------------------------------

print()
print(
    "HART-120 BASELINE ASPECT-RATIO CASE"
)

print(
    "-----------------------------------"
)

print(
    f"Baseline aspect ratio: "
    f"{baseline_AR_case['Aspect_Ratio']:.1f}"
)

print(
    f"Wing span: "
    f"{baseline_AR_case['Span_m']:.2f} m"
)

print(
    f"Root bending moment: "
    f"{baseline_AR_case['Root_Bending_Moment_MNm']:.3f} MN·m"
)

print(
    f"Required root EI: "
    f"{baseline_AR_case['Required_Root_EI_GNm2']:.3f} GN·m²"
)

print(
    f"Simplified wingbox mass: "
    f"{baseline_AR_case['Wingbox_Mass_kg']:.2f} kg"
)

print(
    f"Induced drag: "
    f"{baseline_AR_case['Induced_Drag_kN']:.2f} kN"
)


# ------------------------------------------------------------
# 11. Highest-AR comparison
# ------------------------------------------------------------

highest_AR_case = (
    AR_trade_df.iloc[-1]
)


print()
print(
    "HIGHEST ASPECT-RATIO CASE"
)

print(
    "-------------------------"
)

print(
    f"Aspect ratio: "
    f"{highest_AR_case['Aspect_Ratio']:.1f}"
)

print(
    f"Wing span: "
    f"{highest_AR_case['Span_m']:.2f} m"
)

print(
    f"Induced-drag reduction vs baseline: "
    f"{highest_AR_case['Induced_Drag_Reduction_%']:.2f} %"
)

print(
    f"Wingbox mass change vs baseline: "
    f"{highest_AR_case['Wingbox_Mass_Change_%']:.2f} %"
)

print(
    f"Root-moment change vs baseline: "
    f"{highest_AR_case['Root_Moment_Change_%']:.2f} %"
)

print(
    f"2.5-g maximum stress: "
    f"{highest_AR_case['Maneuver_Max_Stress_MPa']:.2f} MPa"
)


# ------------------------------------------------------------
# 12. Plot — induced drag vs aspect ratio
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_trade_df[
        "Aspect_Ratio"
    ],
    AR_trade_df[
        "Induced_Drag_kN"
    ],
    marker="o"
)

plt.axvline(
    AR_baseline,
    linestyle="--",
    label="HART-120 baseline"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Cruise Induced Drag (kN)"
)

plt.title(
    "HART-120 — Aerodynamic Benefit of Higher Aspect Ratio"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 13. Plot — wingbox mass vs aspect ratio
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_trade_df[
        "Aspect_Ratio"
    ],
    AR_trade_df[
        "Wingbox_Mass_kg"
    ],
    marker="o"
)

plt.axvline(
    AR_baseline,
    linestyle="--",
    label="HART-120 baseline"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Simplified Wingbox Mass (kg)"
)

plt.title(
    "HART-120 — Structural Mass Penalty of Higher Aspect Ratio"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 14. Plot — root bending moment vs aspect ratio
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_trade_df[
        "Aspect_Ratio"
    ],
    AR_trade_df[
        "Root_Bending_Moment_MNm"
    ],
    marker="o"
)

plt.axvline(
    AR_baseline,
    linestyle="--",
    label="HART-120 baseline"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "1-g Root Bending Moment (MN·m)"
)

plt.title(
    "HART-120 — Structural Load Growth with Aspect Ratio"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 15. Plot — direct aero-structural trade
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_trade_df[
        "Induced_Drag_kN"
    ],
    AR_trade_df[
        "Wingbox_Mass_kg"
    ],
    marker="o"
)


for _, row in AR_trade_df.iterrows():

    plt.annotate(
        f"AR {row['Aspect_Ratio']:.1f}",
        (
            row[
                "Induced_Drag_kN"
            ],
            row[
                "Wingbox_Mass_kg"
            ]
        ),
        fontsize=8
    )


plt.xlabel(
    "Cruise Induced Drag (kN)"
)

plt.ylabel(
    "Simplified Wingbox Mass (kg)"
)

plt.title(
    "HART-120 — Aero-Structural Aspect-Ratio Trade"
)

plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 16. Plot — normalized penalty / benefit
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_trade_df[
        "Aspect_Ratio"
    ],
    AR_trade_df[
        "Wingbox_Mass_Change_%"
    ],
    marker="o",
    label="Wingbox mass change"
)

plt.plot(
    AR_trade_df[
        "Aspect_Ratio"
    ],
    -AR_trade_df[
        "Induced_Drag_Change_%"
    ],
    marker="o",
    label="Induced drag reduction"
)

plt.axvline(
    AR_baseline,
    linestyle="--",
    label="HART-120 baseline"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Change Relative to AR 13.5 (%)"
)

plt.title(
    "HART-120 — Aerodynamic Benefit vs Structural Penalty"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 92]
# ============================================================
# HART-120 — LOAD-ALLEVIATED HIGH-ASPECT-RATIO WING STUDY
#
# INDUSTRIAL QUESTION
# -------------------
# Can passive aeroelastic load redistribution + active
# maneuver load alleviation reduce the structural penalty
# associated with increasing wing aspect ratio?
#
# Conventional wing:
#   - rigid aerodynamic loading
#   - 5% half-span deflection requirement
#   - uncontrolled 2.5-g maneuver sizing
#
# Technology-enabled wing:
#   - passive aeroelastic washout
#   - stiffness resizing after passive load alleviation
#   - active maneuver load redistribution
#   - same deflection and strength requirements
#
# Reduced-order conceptual design study.
# ============================================================


# ------------------------------------------------------------
# 1. Design space
# ------------------------------------------------------------

AR_tech_values = np.arange(
    13.5,
    18.5,
    0.5
)


# ------------------------------------------------------------
# 2. Conceptual structural design limits
# ------------------------------------------------------------

sigma_allow_trade = 250e6       # Pa
tau_allow_trade = 40e6          # Pa

web_min_gauge_trade = 2.5e-3    # m

deflection_ratio_trade = 0.05

thickness_ratio_trade = 0.12
box_height_fraction_trade = 0.80


# ------------------------------------------------------------
# 3. Passive aeroelastic assumptions
# ------------------------------------------------------------

nu_trade = 0.30

G_trade = (
    E_eq
    / (
        2
        * (
            1
            + nu_trade
        )
    )
)


elastic_axis_fraction_trade = 0.40
aerodynamic_center_fraction_trade = 0.25

box_width_fraction_trade = 0.45

torsion_skin_thickness_trade = 4.0e-3


# ------------------------------------------------------------
# 4. Active maneuver-load-alleviation assumption
#
# Based on the earlier HART-120 control-authority study:
# the selected actuator/control-surface configuration achieved
# approximately 12.53% maneuver root-bending-moment reduction.
#
# IMPORTANT:
# We target ROOT-MOMENT REDUCTION directly in the AR sweep,
# rather than hard-coding the old 14.75% load-shift fraction.
# ------------------------------------------------------------

mla_target_root_moment_reduction = 0.1253


# ------------------------------------------------------------
# 5. Storage
# ------------------------------------------------------------

AR_technology_results = []


# ------------------------------------------------------------
# 6. Sweep aspect ratio
# ------------------------------------------------------------

for AR_test in AR_tech_values:

    # ========================================================
    # GEOMETRY
    # ========================================================

    span_test = np.sqrt(
        AR_test
        * S_wing
    )

    half_span_test = (
        span_test
        / 2
    )


    root_chord_test = (
        2
        * S_wing
        /
        (
            span_test
            * (
                1
                + taper_ratio
            )
        )
    )


    tip_chord_test = (
        taper_ratio
        * root_chord_test
    )


    y_test = np.linspace(
        0.0,
        half_span_test,
        51
    )


    eta_test = (
        y_test
        / half_span_test
    )


    chord_test = (
        root_chord_test
        -
        (
            root_chord_test
            - tip_chord_test
        )
        * eta_test
    )


    # ========================================================
    # RIGID 1-g AERODYNAMIC LOAD
    # ========================================================

    ellipse_test = np.sqrt(
        np.maximum(
            0.0,
            1.0
            - eta_test**2
        )
    )


    ellipse_integral_test = np.trapezoid(
        ellipse_test,
        y_test
    )


    lift_rigid_test = (
        L_half
        / ellipse_integral_test
        * ellipse_test
    )


    # ========================================================
    # RIGID-WING SHEAR
    # ========================================================

    shear_rigid_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        shear_rigid_test[i] = np.trapezoid(
            lift_rigid_test[i:],
            y_test[i:]
        )


    # ========================================================
    # RIGID-WING BENDING MOMENT
    # ========================================================

    moment_rigid_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        moment_rigid_test[i] = np.trapezoid(
            shear_rigid_test[i:],
            y_test[i:]
        )


    # ========================================================
    # BASELINE STIFFNESS SIZING
    # ========================================================

    stiffness_shape_test = (
        chord_test
        / root_chord_test
    )**3


    EI_trial_root_test = 1.0e9


    EI_trial_test = (
        EI_trial_root_test
        * stiffness_shape_test
    )


    curvature_trial_test = (
        moment_rigid_test
        / EI_trial_test
    )


    slope_trial_test = np.zeros_like(
        y_test
    )


    for i in range(
        1,
        len(y_test)
    ):

        slope_trial_test[i] = np.trapezoid(
            curvature_trial_test[:i+1],
            y_test[:i+1]
        )


    deflection_trial_test = np.zeros_like(
        y_test
    )


    for i in range(
        1,
        len(y_test)
    ):

        deflection_trial_test[i] = np.trapezoid(
            slope_trial_test[:i+1],
            y_test[:i+1]
        )


    deflection_target_test = (
        deflection_ratio_trade
        * half_span_test
    )


    EI_root_rigid_test = (

        EI_trial_root_test

        * (
            deflection_trial_test[-1]
            / deflection_target_test
        )
    )


    EI_rigid_test = (
        EI_root_rigid_test
        * stiffness_shape_test
    )


    # ========================================================
    # STRUCTURAL BOX GEOMETRY
    # ========================================================

    airfoil_thickness_test = (
        thickness_ratio_trade
        * chord_test
    )


    box_height_test = (
        box_height_fraction_trade
        * airfoil_thickness_test
    )


    box_width_test = (
        box_width_fraction_trade
        * chord_test
    )


    # ========================================================
    # CONVENTIONAL WING:
    # STIFFNESS-DRIVEN CAP AREA
    # ========================================================

    I_stiff_rigid_test = (
        EI_rigid_test
        / E_eq
    )


    A_cap_stiff_rigid_test = (

        2
        * I_stiff_rigid_test

        / (
            box_height_test**2
        )
    )


    # ========================================================
    # CONVENTIONAL 2.5-g MANEUVER
    # ========================================================

    lift_maneuver_uncontrolled_test = (
        2.5
        * lift_rigid_test
    )


    shear_maneuver_uncontrolled_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        shear_maneuver_uncontrolled_test[i] = np.trapezoid(
            lift_maneuver_uncontrolled_test[i:],
            y_test[i:]
        )


    moment_maneuver_uncontrolled_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        moment_maneuver_uncontrolled_test[i] = np.trapezoid(
            shear_maneuver_uncontrolled_test[i:],
            y_test[i:]
        )


    # ========================================================
    # CONVENTIONAL STRENGTH REQUIREMENT
    #
    # sigma = M / (A*h)
    #
    # therefore:
    #
    # A_required = M / (sigma_allow*h)
    # ========================================================

    A_cap_strength_uncontrolled_test = (

        moment_maneuver_uncontrolled_test

        /
        (
            sigma_allow_trade
            * box_height_test
        )
    )


    # ========================================================
    # FINAL CONVENTIONAL CAP AREA
    #
    # Must satisfy BOTH stiffness and strength.
    # ========================================================

    A_cap_conventional_test = np.maximum(

        A_cap_stiff_rigid_test,

        A_cap_strength_uncontrolled_test
    )


    # ========================================================
    # CONVENTIONAL CAP MASS
    # ========================================================

    cap_mass_per_span_conventional_test = (

        2
        * A_cap_conventional_test
        * rho_eq
    )


    cap_mass_total_conventional_test = (

        2
        * np.trapezoid(
            cap_mass_per_span_conventional_test,
            y_test
        )
    )


    # ========================================================
    # CONVENTIONAL WEB SIZING
    # ========================================================

    web_t_conventional_test = (

        shear_maneuver_uncontrolled_test

        /
        (
            2
            * tau_allow_trade
            * box_height_test
        )
    )


    web_t_conventional_test = np.maximum(

        web_t_conventional_test,

        web_min_gauge_trade
    )


    web_mass_per_span_conventional_test = (

        2
        * web_t_conventional_test
        * box_height_test
        * rho_eq
    )


    web_mass_total_conventional_test = (

        2
        * np.trapezoid(
            web_mass_per_span_conventional_test,
            y_test
        )
    )


    wingbox_mass_conventional_test = (

        cap_mass_total_conventional_test

        + web_mass_total_conventional_test
    )


    # ========================================================
    # PASSIVE AEROELASTIC TAILORING
    # ========================================================

    enclosed_area_test = (
        box_width_test
        * box_height_test
    )


    box_perimeter_test = (

        2
        * (
            box_width_test
            + box_height_test
        )
    )


    J_test = (

        4
        * enclosed_area_test**2
        * torsion_skin_thickness_trade

        / box_perimeter_test
    )


    GJ_test = (
        G_trade
        * J_test
    )


    moment_arm_test = (

        (
            elastic_axis_fraction_trade
            - aerodynamic_center_fraction_trade
        )

        * chord_test
    )


    finite_wing_lift_slope_test = (

        lift_curve_slope

        /
        (
            1
            + lift_curve_slope
            /
            (
                np.pi
                * oswald_e
                * AR_test
            )
        )
    )


    finite_wing_weight_test = np.sqrt(

        np.maximum(
            0.0,
            1.0
            - eta_test**2
        )
    )


    aero_sensitivity_test = (

        0.5
        * rho_cruise
        * V_cruise**2
        * chord_test
        * finite_wing_lift_slope_test
        * finite_wing_weight_test
    )


    # --------------------------------------------------------
    # Iterative static aeroelastic solution
    # --------------------------------------------------------

    lift_aero_test = (
        lift_rigid_test.copy()
    )


    relaxation_test = 0.40


    for aero_iteration in range(300):

        torsional_load_test = (

            -lift_aero_test
            * moment_arm_test
        )


        internal_torque_test = np.zeros_like(
            y_test
        )


        for i in range(
            len(y_test)
        ):

            internal_torque_test[i] = np.trapezoid(
                torsional_load_test[i:],
                y_test[i:]
            )


        twist_rate_test = (

            internal_torque_test
            / GJ_test
        )


        twist_test = np.zeros_like(
            y_test
        )


        for i in range(
            1,
            len(y_test)
        ):

            twist_test[i] = np.trapezoid(
                twist_rate_test[:i+1],
                y_test[:i+1]
            )


        trim_test = (

            -np.trapezoid(
                aero_sensitivity_test
                * twist_test,
                y_test
            )

            /
            np.trapezoid(
                aero_sensitivity_test,
                y_test
            )
        )


        lift_aero_target_test = (

            lift_rigid_test

            + aero_sensitivity_test
            * (
                twist_test
                + trim_test
            )
        )


        aero_error_test = (

            np.max(
                np.abs(
                    lift_aero_target_test
                    - lift_aero_test
                )
            )

            /
            np.max(
                lift_rigid_test
            )
        )


        lift_aero_test = (

            (
                1
                - relaxation_test
            )
            * lift_aero_test

            +
            relaxation_test
            * lift_aero_target_test
        )


        if aero_error_test < 1.0e-7:
            break


    # ========================================================
    # PASSIVE-AEROELASTIC BENDING MOMENT
    # ========================================================

    shear_aero_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        shear_aero_test[i] = np.trapezoid(
            lift_aero_test[i:],
            y_test[i:]
        )


    moment_aero_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        moment_aero_test[i] = np.trapezoid(
            shear_aero_test[i:],
            y_test[i:]
        )


    # ========================================================
    # DEFLECTION UNDER PASSIVE AEROELASTIC LOAD
    # using conventional stiffness
    # ========================================================

    curvature_aero_test = (

        moment_aero_test
        / EI_rigid_test
    )


    slope_aero_test = np.zeros_like(
        y_test
    )


    for i in range(
        1,
        len(y_test)
    ):

        slope_aero_test[i] = np.trapezoid(
            curvature_aero_test[:i+1],
            y_test[:i+1]
        )


    deflection_aero_test = np.zeros_like(
        y_test
    )


    for i in range(
        1,
        len(y_test)
    ):

        deflection_aero_test[i] = np.trapezoid(
            slope_aero_test[:i+1],
            y_test[:i+1]
        )


    tip_deflection_aero_test = (
        deflection_aero_test[-1]
    )


    # ========================================================
    # STIFFNESS REDUCTION ENABLED BY PASSIVE LOAD ALLEVIATION
    #
    # delta proportional to 1/EI
    # ========================================================

    passive_EI_scale_test = (

        tip_deflection_aero_test

        / deflection_target_test
    )


    passive_EI_scale_test = min(

        1.0,

        passive_EI_scale_test
    )


    EI_passive_test = (

        passive_EI_scale_test
        * EI_rigid_test
    )


    I_passive_test = (

        EI_passive_test
        / E_eq
    )


    A_cap_stiff_passive_test = (

        2
        * I_passive_test

        /
        (
            box_height_test**2
        )
    )


    # ========================================================
    # ACTIVE MANEUVER LOAD ALLEVIATION
    # ========================================================

    inboard_shape_test = np.zeros_like(
        eta_test
    )


    inboard_mask_test = (
        eta_test
        <= 0.40
    )


    inboard_shape_test[
        inboard_mask_test
    ] = (

        0.5
        * (
            1
            + np.cos(

                np.pi

                * eta_test[
                    inboard_mask_test
                ]

                / 0.40
            )
        )
    )


    outboard_shape_test = np.zeros_like(
        eta_test
    )


    outboard_mask_test = (

        (
            eta_test
            >= 0.65
        )

        &

        (
            eta_test
            <= 0.95
        )
    )


    outboard_shape_test[
        outboard_mask_test
    ] = np.sin(

        np.pi

        * (
            eta_test[
                outboard_mask_test
            ]
            - 0.65
        )

        / 0.30
    )


    # --------------------------------------------------------
    # Normalize control influence shapes
    # --------------------------------------------------------

    inboard_integral_test = np.trapezoid(
        inboard_shape_test,
        y_test
    )


    outboard_integral_test = np.trapezoid(
        outboard_shape_test,
        y_test
    )


    inboard_unit_test = (

        inboard_shape_test
        / inboard_integral_test
    )


    outboard_unit_test = (

        outboard_shape_test
        / outboard_integral_test
    )


    # ========================================================
    # ACTUATOR-LIMITED MANEUVER LOAD REDISTRIBUTION
    #
    # Calibrated to the previously established HART-120
    # maneuver-load-alleviation capability:
    #
    # Root bending-moment reduction ≈ 12.53 %
    # ========================================================


    # --------------------------------------------------------
    # Net redistribution shape
    #
    # Positive inboard, negative outboard.
    # The integral is approximately zero because both control
    # influence shapes were normalized to unit integral.
    # --------------------------------------------------------

    load_transfer_unit_test = (
        inboard_unit_test
        - outboard_unit_test
    )


    transfer_integral_test = np.trapezoid(
        load_transfer_unit_test,
        y_test
    )


    # --------------------------------------------------------
    # Root-moment change produced by one unit of transferred
    # half-wing lift
    # --------------------------------------------------------

    shear_transfer_unit_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        shear_transfer_unit_test[i] = np.trapezoid(
            load_transfer_unit_test[i:],
            y_test[i:]
        )


    moment_transfer_unit_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        moment_transfer_unit_test[i] = np.trapezoid(
            shear_transfer_unit_test[i:],
            y_test[i:]
        )


    # Adding lift inboard and removing it outboard produces
    # a negative root-moment increment. Convert that to a
    # positive reduction effectiveness per newton shifted.

    root_moment_reduction_per_N_test = (
        -moment_transfer_unit_test[0]
    )


    # --------------------------------------------------------
    # Desired root-bending-moment reduction
    # --------------------------------------------------------

    target_root_moment_reduction_test = (
        mla_target_root_moment_reduction
        * moment_maneuver_uncontrolled_test[0]
    )


    # --------------------------------------------------------
    # Required load transfer to achieve that moment reduction
    # --------------------------------------------------------

    requested_shift_test = (
        target_root_moment_reduction_test
        / root_moment_reduction_per_N_test
    )


    # --------------------------------------------------------
    # Prevent negative local aerodynamic loading
    # --------------------------------------------------------

    removal_mask_test = (
        outboard_unit_test
        > 1.0e-12
    )


    maximum_shift_local_test = np.min(
        lift_maneuver_uncontrolled_test[
            removal_mask_test
        ]
        /
        outboard_unit_test[
            removal_mask_test
        ]
    )


    actual_shift_test = min(
        requested_shift_test,
        0.98
        * maximum_shift_local_test
    )


    # --------------------------------------------------------
    # Controlled maneuver load distribution
    # --------------------------------------------------------

    lift_maneuver_controlled_test = (
        lift_maneuver_uncontrolled_test
        + actual_shift_test
        * load_transfer_unit_test
    )


    # --------------------------------------------------------
    # Diagnostics
    # --------------------------------------------------------

    maneuver_half_lift_test = np.trapezoid(
        lift_maneuver_uncontrolled_test,
        y_test
    )


    controlled_half_lift_test = np.trapezoid(
        lift_maneuver_controlled_test,
        y_test
    )


    maneuver_lift_conservation_error_test = (
        controlled_half_lift_test
        - maneuver_half_lift_test
    )


    achieved_shift_fraction_test = (
        actual_shift_test
        / maneuver_half_lift_test
    )


    # ========================================================
    # CONTROLLED MANEUVER SHEAR
    # ========================================================

    shear_maneuver_controlled_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        shear_maneuver_controlled_test[i] = np.trapezoid(

            lift_maneuver_controlled_test[i:],

            y_test[i:]
        )


    # ========================================================
    # CONTROLLED MANEUVER MOMENT
    # ========================================================

    moment_maneuver_controlled_test = np.zeros_like(
        y_test
    )


    for i in range(
        len(y_test)
    ):

        moment_maneuver_controlled_test[i] = np.trapezoid(

            shear_maneuver_controlled_test[i:],

            y_test[i:]
        )


    maneuver_moment_reduction_test = (

        (
            moment_maneuver_uncontrolled_test[0]

            - moment_maneuver_controlled_test[0]
        )

        /
        moment_maneuver_uncontrolled_test[0]

    ) * 100


    # ========================================================
    # STRENGTH AREA AFTER ACTIVE LOAD ALLEVIATION
    # ========================================================

    A_cap_strength_controlled_test = (

        moment_maneuver_controlled_test

        /
        (
            sigma_allow_trade
            * box_height_test
        )
    )


    # ========================================================
    # FINAL TECHNOLOGY-ENABLED CAP AREA
    #
    # Must satisfy:
    # passive-aeroelastic stiffness requirement
    # AND
    # controlled maneuver strength requirement
    # ========================================================

    A_cap_technology_test = np.maximum(

        A_cap_stiff_passive_test,

        A_cap_strength_controlled_test
    )


    # ========================================================
    # TECHNOLOGY-ENABLED CAP MASS
    # ========================================================

    cap_mass_per_span_technology_test = (

        2
        * A_cap_technology_test
        * rho_eq
    )


    cap_mass_total_technology_test = (

        2
        * np.trapezoid(
            cap_mass_per_span_technology_test,
            y_test
        )
    )


    # ========================================================
    # TECHNOLOGY-ENABLED WEB MASS
    # ========================================================

    web_t_technology_test = (

        shear_maneuver_controlled_test

        /
        (
            2
            * tau_allow_trade
            * box_height_test
        )
    )


    web_t_technology_test = np.maximum(

        web_t_technology_test,

        web_min_gauge_trade
    )


    web_mass_per_span_technology_test = (

        2
        * web_t_technology_test
        * box_height_test
        * rho_eq
    )


    web_mass_total_technology_test = (

        2
        * np.trapezoid(
            web_mass_per_span_technology_test,
            y_test
        )
    )


    wingbox_mass_technology_test = (

        cap_mass_total_technology_test

        + web_mass_total_technology_test
    )


    # ========================================================
    # AERODYNAMIC BENEFIT
    # ========================================================

    CDi_test = (

        CL_cruise**2

        /
        (
            np.pi
            * oswald_e
            * AR_test
        )
    )


    induced_drag_test = (

        0.5
        * rho_cruise
        * V_cruise**2
        * S_wing
        * CDi_test
    )


    # ========================================================
    # GOVERNING CAP CONSTRAINT
    # ========================================================

    stiffness_governing_fraction_test = (

        np.mean(

            A_cap_stiff_passive_test

            >= A_cap_strength_controlled_test

        ) * 100
    )


    # ========================================================
    # STORE RESULTS
    # ========================================================

    AR_technology_results.append({

        "Aspect_Ratio":
            AR_test,

        "Span_m":
            span_test,

        "Induced_Drag_kN":
            induced_drag_test / 1000,

        "Conventional_Wingbox_Mass_kg":
            wingbox_mass_conventional_test,

        "Technology_Wingbox_Mass_kg":
            wingbox_mass_technology_test,

        "Passive_EI_Reduction_%":
            (
                1
                - passive_EI_scale_test
            ) * 100,

        "Achieved_MLA_Shift_%":
            achieved_shift_fraction_test * 100,

        "Maneuver_Root_Moment_Reduction_%":
            maneuver_moment_reduction_test,

        "Conventional_Maneuver_Moment_MNm":
            moment_maneuver_uncontrolled_test[0] / 1e6,

        "Controlled_Maneuver_Moment_MNm":
            moment_maneuver_controlled_test[0] / 1e6,

        "Conventional_Cap_Mass_kg":
            cap_mass_total_conventional_test,

        "Technology_Cap_Mass_kg":
            cap_mass_total_technology_test,

        "Conventional_Web_Mass_kg":
            web_mass_total_conventional_test,

        "Technology_Web_Mass_kg":
            web_mass_total_technology_test,

        "Stiffness_Governing_Span_%":
            stiffness_governing_fraction_test,

        "Tip_Aeroelastic_Twist_deg":
            np.degrees(
                twist_test[-1]
            )
    })


# ------------------------------------------------------------
# 7. DataFrame
# ------------------------------------------------------------

AR_technology_df = pd.DataFrame(
    AR_technology_results
)


# ------------------------------------------------------------
# 8. Baseline reference = conventional AR 13.5
# ------------------------------------------------------------

base_index = (

    np.abs(

        AR_technology_df[
            "Aspect_Ratio"
        ]

        - 13.5

    )
).idxmin()


base_conventional_mass = (

    AR_technology_df.loc[
        base_index,
        "Conventional_Wingbox_Mass_kg"
    ]
)


base_drag = (

    AR_technology_df.loc[
        base_index,
        "Induced_Drag_kN"
    ]
)


# ------------------------------------------------------------
# 9. Relative metrics
# ------------------------------------------------------------

AR_technology_df[
    "Drag_Reduction_vs_AR13.5_%"
] = (

    (
        base_drag

        - AR_technology_df[
            "Induced_Drag_kN"
        ]
    )

    / base_drag

) * 100


AR_technology_df[
    "Conventional_Mass_Penalty_%"
] = (

    (
        AR_technology_df[
            "Conventional_Wingbox_Mass_kg"
        ]

        - base_conventional_mass
    )

    / base_conventional_mass

) * 100


AR_technology_df[
    "Technology_Mass_Penalty_%"
] = (

    (
        AR_technology_df[
            "Technology_Wingbox_Mass_kg"
        ]

        - base_conventional_mass
    )

    / base_conventional_mass

) * 100


AR_technology_df[
    "Technology_Mass_Saving_at_Same_AR_%"
] = (

    (
        AR_technology_df[
            "Conventional_Wingbox_Mass_kg"
        ]

        - AR_technology_df[
            "Technology_Wingbox_Mass_kg"
        ]
    )

    /
    AR_technology_df[
        "Conventional_Wingbox_Mass_kg"
    ]

) * 100


# ------------------------------------------------------------
# 10. Structural-penalty recovery
#
# For AR > 13.5:
#
# How much of the extra mass caused by higher AR was recovered
# by passive + active load alleviation?
# ------------------------------------------------------------

AR_technology_df[
    "Structural_Penalty_Recovered_%"
] = np.nan


higher_AR_mask = (

    AR_technology_df[
        "Aspect_Ratio"
    ]

    > 13.5
)


mass_penalty_conventional = (

    AR_technology_df.loc[
        higher_AR_mask,
        "Conventional_Wingbox_Mass_kg"
    ]

    - base_conventional_mass
)


AR_technology_df.loc[
    higher_AR_mask,
    "Structural_Penalty_Recovered_%"
] = (

    (
        AR_technology_df.loc[
            higher_AR_mask,
            "Conventional_Wingbox_Mass_kg"
        ]

        - AR_technology_df.loc[
            higher_AR_mask,
            "Technology_Wingbox_Mass_kg"
        ]
    )

    /
    mass_penalty_conventional

) * 100


# ------------------------------------------------------------
# 11. Print main table
# ------------------------------------------------------------

print()
print(
    "HART-120 LOAD-ALLEVIATED HIGH-ASPECT-RATIO STUDY"
)

print(
    "------------------------------------------------"
)

print(

    AR_technology_df[
        [
            "Aspect_Ratio",
            "Span_m",
            "Drag_Reduction_vs_AR13.5_%",
            "Conventional_Wingbox_Mass_kg",
            "Technology_Wingbox_Mass_kg",
            "Technology_Mass_Saving_at_Same_AR_%",
            "Conventional_Mass_Penalty_%",
            "Technology_Mass_Penalty_%",
            "Passive_EI_Reduction_%",
            "Maneuver_Root_Moment_Reduction_%",
            "Stiffness_Governing_Span_%"
        ]
    ]
    .round(2)
    .to_string(
        index=False
    )

)


# ------------------------------------------------------------
# 12. AR 13.5 baseline check
# ------------------------------------------------------------

base_case = (

    AR_technology_df.loc[
        base_index
    ]
)


print()
print(
    "AR 13.5 TECHNOLOGY EFFECT"
)

print(
    "-------------------------"
)

print(
    f"Conventional wingbox mass: "
    f"{base_case['Conventional_Wingbox_Mass_kg']:.2f} kg"
)

print(
    f"Technology-enabled wingbox mass: "
    f"{base_case['Technology_Wingbox_Mass_kg']:.2f} kg"
)

print(
    f"Mass saving: "
    f"{base_case['Technology_Mass_Saving_at_Same_AR_%']:.2f} %"
)

print(
    f"Passive stiffness reduction: "
    f"{base_case['Passive_EI_Reduction_%']:.2f} %"
)

print(
    f"Active maneuver root-moment reduction: "
    f"{base_case['Maneuver_Root_Moment_Reduction_%']:.2f} %"
)

print(
    f"Tip aeroelastic twist: "
    f"{base_case['Tip_Aeroelastic_Twist_deg']:.3f} deg"
)


# ------------------------------------------------------------
# 13. AR 18 case
# ------------------------------------------------------------

AR18_case = (

    AR_technology_df.iloc[-1]
)


print()
print(
    "AR 18 TECHNOLOGY EFFECT"
)

print(
    "-----------------------"
)

print(
    f"Induced-drag reduction: "
    f"{AR18_case['Drag_Reduction_vs_AR13.5_%']:.2f} %"
)

print(
    f"Conventional mass penalty: "
    f"{AR18_case['Conventional_Mass_Penalty_%']:.2f} %"
)

print(
    f"Technology-enabled mass penalty: "
    f"{AR18_case['Technology_Mass_Penalty_%']:.2f} %"
)

print(
    f"Mass saving at AR 18: "
    f"{AR18_case['Technology_Mass_Saving_at_Same_AR_%']:.2f} %"
)

print(
    f"Structural penalty recovered: "
    f"{AR18_case['Structural_Penalty_Recovered_%']:.2f} %"
)

print(
    f"Passive EI reduction: "
    f"{AR18_case['Passive_EI_Reduction_%']:.2f} %"
)

print(
    f"Active maneuver moment reduction: "
    f"{AR18_case['Maneuver_Root_Moment_Reduction_%']:.2f} %"
)


# ------------------------------------------------------------
# 14. Project mass-budget test
#
# Question:
# If we permit only +30% simplified wingbox mass relative
# to conventional AR 13.5, how much AR can we achieve?
# ------------------------------------------------------------

mass_budget_percent = 30.0


mass_budget = (

    base_conventional_mass

    * (
        1
        + mass_budget_percent / 100
    )
)


conventional_feasible = (

    AR_technology_df[
        "Conventional_Wingbox_Mass_kg"
    ]

    <= mass_budget
)


technology_feasible = (

    AR_technology_df[
        "Technology_Wingbox_Mass_kg"
    ]

    <= mass_budget
)


max_AR_conventional_budget = (

    AR_technology_df.loc[
        conventional_feasible,
        "Aspect_Ratio"
    ].max()
)


max_AR_technology_budget = (

    AR_technology_df.loc[
        technology_feasible,
        "Aspect_Ratio"
    ].max()
)


print()
print(
    "HIGH-ASPECT-RATIO MASS-BUDGET TEST"
)

print(
    "----------------------------------"
)

print(
    f"Allowed wingbox mass increase: "
    f"{mass_budget_percent:.1f} %"
)

print(
    f"Mass budget: "
    f"{mass_budget:.2f} kg"
)

print()

print(
    f"Highest conventional AR within budget: "
    f"{max_AR_conventional_budget:.1f}"
)

print(
    f"Highest technology-enabled AR within budget: "
    f"{max_AR_technology_budget:.1f}"
)


# ------------------------------------------------------------
# 15. Plot — conventional vs technology-enabled mass
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Conventional_Wingbox_Mass_kg"
    ],
    marker="o",
    label="Conventional"
)

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Technology_Wingbox_Mass_kg"
    ],
    marker="o",
    label="Passive + Active Load Alleviation"
)

plt.axhline(
    mass_budget,
    linestyle="--",
    label="+30% mass budget"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Simplified Wingbox Mass (kg)"
)

plt.title(
    "HART-120 — Load Alleviation for Higher Aspect Ratio"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 16. Plot — structural mass penalty
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Conventional_Mass_Penalty_%"
    ],
    marker="o",
    label="Conventional"
)

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Technology_Mass_Penalty_%"
    ],
    marker="o",
    label="Load-Alleviated"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Wingbox Mass Penalty vs Conventional AR 13.5 (%)"
)

plt.title(
    "HART-120 — Recovery of High-AR Structural Penalty"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 17. Plot — drag benefit vs structural penalty
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Drag_Reduction_vs_AR13.5_%"
    ],
    marker="o",
    label="Induced Drag Reduction"
)

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Conventional_Mass_Penalty_%"
    ],
    marker="o",
    label="Conventional Mass Penalty"
)

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Technology_Mass_Penalty_%"
    ],
    marker="o",
    label="Load-Alleviated Mass Penalty"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Change Relative to Conventional AR 13.5 (%)"
)

plt.title(
    "HART-120 — Aerodynamic Benefit vs Load-Alleviated Structural Cost"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 18. Plot — passive vs active contribution
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Passive_EI_Reduction_%"
    ],
    marker="o",
    label="Passive Aeroelastic EI Reduction"
)

plt.plot(
    AR_technology_df[
        "Aspect_Ratio"
    ],
    AR_technology_df[
        "Maneuver_Root_Moment_Reduction_%"
    ],
    marker="o",
    label="Active Maneuver Moment Reduction"
)

plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Benefit (%)"
)

plt.title(
    "HART-120 — Passive and Active Load-Alleviation Contributions"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 93]
# ============================================================
# HART-120 — FINAL HIGH-ASPECT-RATIO DESIGN DECISION
#
# Purpose:
# Convert the AR sweep into an engineering trade-space decision.
#
# Compare:
#   AR 13.5 = original reference
#   AR 15.0 = highest conventional design inside +30% mass budget
#   AR 15.5 = highest technology-enabled design inside budget
#   AR 18.0 = extreme aerodynamic-efficiency case
# ============================================================


# ------------------------------------------------------------
# Reference design
# ------------------------------------------------------------

baseline_row = AR_technology_df[
    np.isclose(
        AR_technology_df["Aspect_Ratio"],
        13.5
    )
].iloc[0]


baseline_mass = baseline_row[
    "Conventional_Wingbox_Mass_kg"
]


mass_budget_fraction = 0.30

mass_budget = (
    baseline_mass
    * (1 + mass_budget_fraction)
)


# ------------------------------------------------------------
# Candidate AR values
# ------------------------------------------------------------

candidate_AR_values = [
    13.5,
    15.0,
    15.5,
    18.0
]


candidate_rows = (
    AR_technology_df[
        AR_technology_df["Aspect_Ratio"].isin(
            candidate_AR_values
        )
    ]
    .copy()
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# Added structural mass relative to original AR 13.5 aircraft
# ------------------------------------------------------------

candidate_rows[
    "Conventional_Added_Mass_kg"
] = (
    candidate_rows[
        "Conventional_Wingbox_Mass_kg"
    ]
    - baseline_mass
)


candidate_rows[
    "Technology_Added_Mass_kg"
] = (
    candidate_rows[
        "Technology_Wingbox_Mass_kg"
    ]
    - baseline_mass
)


# ------------------------------------------------------------
# Technology mass saving at the SAME aspect ratio
# ------------------------------------------------------------

candidate_rows[
    "Technology_Mass_Saving_kg"
] = (
    candidate_rows[
        "Conventional_Wingbox_Mass_kg"
    ]
    -
    candidate_rows[
        "Technology_Wingbox_Mass_kg"
    ]
)


# ------------------------------------------------------------
# Structural-budget feasibility
# ------------------------------------------------------------

candidate_rows[
    "Conventional_Within_30pct_Budget"
] = (
    candidate_rows[
        "Conventional_Wingbox_Mass_kg"
    ]
    <= mass_budget
)


candidate_rows[
    "Technology_Within_30pct_Budget"
] = (
    candidate_rows[
        "Technology_Wingbox_Mass_kg"
    ]
    <= mass_budget
)


# ------------------------------------------------------------
# Aero-structural efficiency metric
#
# Drag reduction obtained per 1% structural mass penalty.
#
# Only meaningful for configurations above baseline AR.
# ------------------------------------------------------------

candidate_rows[
    "Technology_Drag_Benefit_per_Mass_Penalty"
] = np.where(

    candidate_rows[
        "Technology_Mass_Penalty_%"
    ] > 0,

    candidate_rows[
        "Drag_Reduction_vs_AR13.5_%"
    ]
    /
    candidate_rows[
        "Technology_Mass_Penalty_%"
    ],

    np.nan
)


candidate_rows[
    "Conventional_Drag_Benefit_per_Mass_Penalty"
] = np.where(

    candidate_rows[
        "Conventional_Mass_Penalty_%"
    ] > 0,

    candidate_rows[
        "Drag_Reduction_vs_AR13.5_%"
    ]
    /
    candidate_rows[
        "Conventional_Mass_Penalty_%"
    ],

    np.nan
)


# ------------------------------------------------------------
# Display design-decision table
# ------------------------------------------------------------

decision_columns = [

    "Aspect_Ratio",
    "Span_m",

    "Drag_Reduction_vs_AR13.5_%",

    "Conventional_Wingbox_Mass_kg",
    "Technology_Wingbox_Mass_kg",

    "Technology_Mass_Saving_kg",

    "Conventional_Mass_Penalty_%",
    "Technology_Mass_Penalty_%",

    "Passive_EI_Reduction_%",
    "Maneuver_Root_Moment_Reduction_%",

    "Conventional_Within_30pct_Budget",
    "Technology_Within_30pct_Budget"
]


print(
    "HART-120 FINAL HIGH-ASPECT-RATIO DESIGN TRADE"
)

print(
    "--------------------------------------------"
)

print(
    candidate_rows[
        decision_columns
    ]
    .round(2)
    .to_string(index=False)
)


# ============================================================
# Automatically identify best feasible designs
# ============================================================


conventional_feasible = (
    AR_technology_df[
        AR_technology_df[
            "Conventional_Wingbox_Mass_kg"
        ]
        <= mass_budget
    ]
)


technology_feasible = (
    AR_technology_df[
        AR_technology_df[
            "Technology_Wingbox_Mass_kg"
        ]
        <= mass_budget
    ]
)


best_conventional = (
    conventional_feasible
    .sort_values(
        "Aspect_Ratio"
    )
    .iloc[-1]
)


best_technology = (
    technology_feasible
    .sort_values(
        "Aspect_Ratio"
    )
    .iloc[-1]
)


# ------------------------------------------------------------
# Quantify what the technology actually enabled
# ------------------------------------------------------------

AR_gain = (
    best_technology["Aspect_Ratio"]
    -
    best_conventional["Aspect_Ratio"]
)


drag_gain = (
    best_technology[
        "Drag_Reduction_vs_AR13.5_%"
    ]
    -
    best_conventional[
        "Drag_Reduction_vs_AR13.5_%"
    ]
)


technology_mass_saved_selected_AR = (

    best_technology[
        "Conventional_Wingbox_Mass_kg"
    ]

    -

    best_technology[
        "Technology_Wingbox_Mass_kg"
    ]
)


technology_mass_saved_selected_AR_percent = (

    technology_mass_saved_selected_AR

    /

    best_technology[
        "Conventional_Wingbox_Mass_kg"
    ]

) * 100


print()

print(
    "HART-120 DESIGN DECISION"
)

print(
    "------------------------"
)

print(
    f"Structural mass budget: "
    f"{mass_budget:.2f} kg"
)

print()

print(
    "Highest conventional configuration:"
)

print(
    f"  AR = "
    f"{best_conventional['Aspect_Ratio']:.1f}"
)

print(
    f"  Span = "
    f"{best_conventional['Span_m']:.2f} m"
)

print(
    f"  Induced-drag reduction = "
    f"{best_conventional['Drag_Reduction_vs_AR13.5_%']:.2f} %"
)

print(
    f"  Wingbox mass = "
    f"{best_conventional['Conventional_Wingbox_Mass_kg']:.2f} kg"
)


print()

print(
    "Highest technology-enabled configuration:"
)

print(
    f"  AR = "
    f"{best_technology['Aspect_Ratio']:.1f}"
)

print(
    f"  Span = "
    f"{best_technology['Span_m']:.2f} m"
)

print(
    f"  Induced-drag reduction = "
    f"{best_technology['Drag_Reduction_vs_AR13.5_%']:.2f} %"
)

print(
    f"  Wingbox mass = "
    f"{best_technology['Technology_Wingbox_Mass_kg']:.2f} kg"
)


print()

print(
    "TECHNOLOGY VALUE"
)

print(
    "----------------"
)

print(
    f"Additional achievable aspect ratio: "
    f"{AR_gain:.1f}"
)

print(
    f"Additional induced-drag reduction "
    f"within same structural budget: "
    f"{drag_gain:.2f} percentage points"
)

print(
    f"Mass saved at selected technology AR: "
    f"{technology_mass_saved_selected_AR:.2f} kg"
)

print(
    f"Mass saving at selected technology AR: "
    f"{technology_mass_saved_selected_AR_percent:.2f} %"
)


# ============================================================
# PARETO-STYLE TRADE PLOT
# ============================================================

plt.figure(
    figsize=(9, 6)
)


plt.plot(

    AR_technology_df[
        "Drag_Reduction_vs_AR13.5_%"
    ],

    AR_technology_df[
        "Conventional_Mass_Penalty_%"
    ],

    marker="o",

    label="Conventional"
)


plt.plot(

    AR_technology_df[
        "Drag_Reduction_vs_AR13.5_%"
    ],

    AR_technology_df[
        "Technology_Mass_Penalty_%"
    ],

    marker="o",

    label="Passive + Active Load Alleviation"
)


plt.axhline(
    30,
    linestyle="--",
    label="+30% structural mass budget"
)


plt.scatter(

    best_conventional[
        "Drag_Reduction_vs_AR13.5_%"
    ],

    best_conventional[
        "Conventional_Mass_Penalty_%"
    ],

    s=100
)


plt.scatter(

    best_technology[
        "Drag_Reduction_vs_AR13.5_%"
    ],

    best_technology[
        "Technology_Mass_Penalty_%"
    ],

    s=100
)


plt.annotate(

    f"Conventional AR "
    f"{best_conventional['Aspect_Ratio']:.1f}",

    (
        best_conventional[
            "Drag_Reduction_vs_AR13.5_%"
        ],

        best_conventional[
            "Conventional_Mass_Penalty_%"
        ]
    ),

    xytext=(10, -20),

    textcoords="offset points"
)


plt.annotate(

    f"Technology AR "
    f"{best_technology['Aspect_Ratio']:.1f}",

    (
        best_technology[
            "Drag_Reduction_vs_AR13.5_%"
        ],

        best_technology[
            "Technology_Mass_Penalty_%"
        ]
    ),

    xytext=(10, 10),

    textcoords="offset points"
)


plt.xlabel(
    "Induced Drag Reduction vs AR 13.5 (%)"
)

plt.ylabel(
    "Simplified Wingbox Mass Penalty vs AR 13.5 (%)"
)

plt.title(
    "HART-120 — Aero-Structural Design Trade"
)

plt.grid(True)

plt.legend()

plt.show()

# %% [notebook cell 94]
# ============================================================
# HART-120 — AR 15.5 DEGRADED / FAILED LOAD-ALLEVIATION STUDY
#
# Industrial question:
#
# If the active maneuver-load-alleviation system becomes
# partially degraded or completely unavailable, does the
# technology-enabled AR 15.5 wing remain structurally safe?
#
# We evaluate:
#
#   100% MLA available
#    75%
#    50%
#    25%
#     0% = complete active-control loss
#
# Passive aeroelastic tailoring remains available because
# it is a structural/aeroelastic property of the wing.
# ============================================================


selected_AR = 15.5


# ------------------------------------------------------------
# Extract selected design information from previous AR study
# ------------------------------------------------------------

selected_row = (
    AR_technology_df[
        np.isclose(
            AR_technology_df["Aspect_Ratio"],
            selected_AR
        )
    ]
    .iloc[0]
)


passive_EI_scale_selected = (
    1.0
    -
    selected_row[
        "Passive_EI_Reduction_%"
    ] / 100
)


full_MLA_reduction_selected = (
    selected_row[
        "Maneuver_Root_Moment_Reduction_%"
    ] / 100
)


# ============================================================
# GEOMETRY
# ============================================================

span_selected = np.sqrt(
    selected_AR
    * S_wing
)


half_span_selected = (
    span_selected
    / 2
)


root_chord_selected = (
    2
    * S_wing
    /
    (
        span_selected
        * (
            1
            + taper_ratio
        )
    )
)


tip_chord_selected = (
    taper_ratio
    * root_chord_selected
)


y_selected = np.linspace(
    0.0,
    half_span_selected,
    51
)


eta_selected = (
    y_selected
    / half_span_selected
)


chord_selected = (
    root_chord_selected
    -
    (
        root_chord_selected
        - tip_chord_selected
    )
    * eta_selected
)


# ============================================================
# RIGID 1-g REFERENCE LOAD
# ============================================================

ellipse_selected = np.sqrt(
    np.maximum(
        0.0,
        1.0
        - eta_selected**2
    )
)


ellipse_integral_selected = np.trapezoid(
    ellipse_selected,
    y_selected
)


lift_1g_selected = (
    L_half
    / ellipse_integral_selected
    * ellipse_selected
)


shear_1g_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    shear_1g_selected[i] = np.trapezoid(
        lift_1g_selected[i:],
        y_selected[i:]
    )


moment_1g_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    moment_1g_selected[i] = np.trapezoid(
        shear_1g_selected[i:],
        y_selected[i:]
    )


# ============================================================
# RIGID-WING STIFFNESS REQUIREMENT
# ============================================================

stiffness_shape_selected = (
    chord_selected
    / root_chord_selected
)**3


EI_trial_root_selected = 1.0e9


EI_trial_selected = (
    EI_trial_root_selected
    * stiffness_shape_selected
)


curvature_trial_selected = (
    moment_1g_selected
    / EI_trial_selected
)


slope_trial_selected = np.zeros_like(
    y_selected
)


for i in range(
    1,
    len(y_selected)
):

    slope_trial_selected[i] = np.trapezoid(
        curvature_trial_selected[:i+1],
        y_selected[:i+1]
    )


deflection_trial_selected = np.zeros_like(
    y_selected
)


for i in range(
    1,
    len(y_selected)
):

    deflection_trial_selected[i] = np.trapezoid(
        slope_trial_selected[:i+1],
        y_selected[:i+1]
    )


deflection_target_selected = (
    deflection_ratio_trade
    * half_span_selected
)


EI_root_rigid_selected = (
    EI_trial_root_selected
    * (
        deflection_trial_selected[-1]
        / deflection_target_selected
    )
)


EI_rigid_selected = (
    EI_root_rigid_selected
    * stiffness_shape_selected
)


# ============================================================
# STRUCTURAL BOX GEOMETRY
# ============================================================

airfoil_thickness_selected = (
    thickness_ratio_trade
    * chord_selected
)


box_height_selected = (
    box_height_fraction_trade
    * airfoil_thickness_selected
)


# ============================================================
# PASSIVE-AEROELASTIC STIFFNESS DESIGN
# ============================================================

EI_passive_selected = (
    passive_EI_scale_selected
    * EI_rigid_selected
)


I_passive_selected = (
    EI_passive_selected
    / E_eq
)


A_cap_stiff_selected = (
    2
    * I_passive_selected
    /
    (
        box_height_selected**2
    )
)


# ============================================================
# UNCONTROLLED 2.5-g MANEUVER
# ============================================================

lift_maneuver_uncontrolled_selected = (
    2.5
    * lift_1g_selected
)


shear_maneuver_uncontrolled_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    shear_maneuver_uncontrolled_selected[i] = np.trapezoid(
        lift_maneuver_uncontrolled_selected[i:],
        y_selected[i:]
    )


moment_maneuver_uncontrolled_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    moment_maneuver_uncontrolled_selected[i] = np.trapezoid(
        shear_maneuver_uncontrolled_selected[i:],
        y_selected[i:]
    )


# ============================================================
# CONTROL-INFLUENCE SHAPES
# ============================================================

inboard_shape_selected = np.zeros_like(
    eta_selected
)


inboard_mask_selected = (
    eta_selected
    <= 0.40
)


inboard_shape_selected[
    inboard_mask_selected
] = (
    0.5
    * (
        1
        + np.cos(
            np.pi
            * eta_selected[
                inboard_mask_selected
            ]
            / 0.40
        )
    )
)


outboard_shape_selected = np.zeros_like(
    eta_selected
)


outboard_mask_selected = (
    (
        eta_selected
        >= 0.65
    )
    &
    (
        eta_selected
        <= 0.95
    )
)


outboard_shape_selected[
    outboard_mask_selected
] = np.sin(
    np.pi
    * (
        eta_selected[
            outboard_mask_selected
        ]
        - 0.65
    )
    / 0.30
)


inboard_unit_selected = (
    inboard_shape_selected
    /
    np.trapezoid(
        inboard_shape_selected,
        y_selected
    )
)


outboard_unit_selected = (
    outboard_shape_selected
    /
    np.trapezoid(
        outboard_shape_selected,
        y_selected
    )
)


load_transfer_unit_selected = (
    inboard_unit_selected
    - outboard_unit_selected
)


# ============================================================
# MOMENT EFFECTIVENESS OF LOAD TRANSFER
# ============================================================

shear_transfer_unit_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    shear_transfer_unit_selected[i] = np.trapezoid(
        load_transfer_unit_selected[i:],
        y_selected[i:]
    )


moment_transfer_unit_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    moment_transfer_unit_selected[i] = np.trapezoid(
        shear_transfer_unit_selected[i:],
        y_selected[i:]
    )


root_moment_reduction_per_N_selected = (
    -moment_transfer_unit_selected[0]
)


target_root_moment_reduction_selected = (
    full_MLA_reduction_selected
    * moment_maneuver_uncontrolled_selected[0]
)


full_shift_selected = (
    target_root_moment_reduction_selected
    /
    root_moment_reduction_per_N_selected
)


# ============================================================
# FULL-CONTROL DESIGN LOAD
# ============================================================

lift_maneuver_full_control_selected = (
    lift_maneuver_uncontrolled_selected
    +
    full_shift_selected
    * load_transfer_unit_selected
)


shear_maneuver_full_control_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    shear_maneuver_full_control_selected[i] = np.trapezoid(
        lift_maneuver_full_control_selected[i:],
        y_selected[i:]
    )


moment_maneuver_full_control_selected = np.zeros_like(
    y_selected
)


for i in range(
    len(y_selected)
):

    moment_maneuver_full_control_selected[i] = np.trapezoid(
        shear_maneuver_full_control_selected[i:],
        y_selected[i:]
    )


# ============================================================
# TECHNOLOGY CAP DESIGN
#
# Sized for:
#
# 1. passive-aeroelastic stiffness
# 2. fully functioning MLA strength load
# ============================================================

A_cap_strength_full_control_selected = (
    moment_maneuver_full_control_selected
    /
    (
        sigma_allow_trade
        * box_height_selected
    )
)


A_cap_design_selected = np.maximum(
    A_cap_stiff_selected,
    A_cap_strength_full_control_selected
)


# ============================================================
# TECHNOLOGY WEB DESIGN
#
# Current design assumes full active MLA availability.
# ============================================================

web_t_full_control_selected = (
    shear_maneuver_full_control_selected
    /
    (
        2
        * tau_allow_trade
        * box_height_selected
    )
)


web_t_full_control_selected = np.maximum(
    web_t_full_control_selected,
    web_min_gauge_trade
)


# ============================================================
# DEGRADED MLA CASES
# ============================================================

control_availability_values = np.array([
    1.00,
    0.75,
    0.50,
    0.25,
    0.00
])


degraded_results = []


for control_availability in control_availability_values:


    # --------------------------------------------------------
    # Available load transfer
    # --------------------------------------------------------

    degraded_shift = (
        control_availability
        * full_shift_selected
    )


    lift_degraded = (
        lift_maneuver_uncontrolled_selected
        +
        degraded_shift
        * load_transfer_unit_selected
    )


    # --------------------------------------------------------
    # Shear
    # --------------------------------------------------------

    shear_degraded = np.zeros_like(
        y_selected
    )


    for i in range(
        len(y_selected)
    ):

        shear_degraded[i] = np.trapezoid(
            lift_degraded[i:],
            y_selected[i:]
        )


    # --------------------------------------------------------
    # Bending moment
    # --------------------------------------------------------

    moment_degraded = np.zeros_like(
        y_selected
    )


    for i in range(
        len(y_selected)
    ):

        moment_degraded[i] = np.trapezoid(
            shear_degraded[i:],
            y_selected[i:]
        )


    # --------------------------------------------------------
    # Cap stress using FULL-CONTROL-SIZED structure
    # --------------------------------------------------------

    sigma_cap_degraded = (
        moment_degraded
        /
        (
            A_cap_design_selected
            * box_height_selected
        )
    )


    max_cap_stress = np.max(
        sigma_cap_degraded
    )


    max_cap_stress_index = np.argmax(
        sigma_cap_degraded
    )


    cap_utilization = (
        max_cap_stress
        / sigma_allow_trade
    )


    # --------------------------------------------------------
    # Web shear stress using FULL-CONTROL-SIZED web
    # --------------------------------------------------------

    tau_web_degraded = (
        shear_degraded
        /
        (
            2
            * web_t_full_control_selected
            * box_height_selected
        )
    )


    max_web_shear = np.max(
        tau_web_degraded
    )


    max_web_shear_index = np.argmax(
        tau_web_degraded
    )


    web_utilization = (
        max_web_shear
        / tau_allow_trade
    )


    # --------------------------------------------------------
    # Maneuver deflection
    # --------------------------------------------------------

    curvature_degraded = (
        moment_degraded
        / EI_passive_selected
    )


    slope_degraded = np.zeros_like(
        y_selected
    )


    for i in range(
        1,
        len(y_selected)
    ):

        slope_degraded[i] = np.trapezoid(
            curvature_degraded[:i+1],
            y_selected[:i+1]
        )


    deflection_degraded = np.zeros_like(
        y_selected
    )


    for i in range(
        1,
        len(y_selected)
    ):

        deflection_degraded[i] = np.trapezoid(
            slope_degraded[:i+1],
            y_selected[:i+1]
        )


    tip_deflection_degraded = (
        deflection_degraded[-1]
    )


    # --------------------------------------------------------
    # Achieved root-moment reduction
    # --------------------------------------------------------

    achieved_reduction = (
        (
            moment_maneuver_uncontrolled_selected[0]
            - moment_degraded[0]
        )
        /
        moment_maneuver_uncontrolled_selected[0]
    ) * 100


    cap_safe = (
        cap_utilization
        <= 1.0
    )


    web_safe = (
        web_utilization
        <= 1.0
    )


    overall_safe = (
        cap_safe
        and web_safe
    )


    degraded_results.append({

        "MLA_Availability_%":
            control_availability * 100,

        "Root_Moment_MNm":
            moment_degraded[0] / 1e6,

        "Root_Moment_Reduction_%":
            achieved_reduction,

        "Max_Cap_Stress_MPa":
            max_cap_stress / 1e6,

        "Cap_Utilization":
            cap_utilization,

        "Cap_Critical_Eta":
            eta_selected[
                max_cap_stress_index
            ],

        "Max_Web_Shear_MPa":
            max_web_shear / 1e6,

        "Web_Utilization":
            web_utilization,

        "Web_Critical_Eta":
            eta_selected[
                max_web_shear_index
            ],

        "Tip_Deflection_m":
            tip_deflection_degraded,

        "Tip_Deflection_HalfSpan_%":
            (
                tip_deflection_degraded
                / half_span_selected
            ) * 100,

        "Cap_Safe":
            cap_safe,

        "Web_Safe":
            web_safe,

        "Overall_Safe":
            overall_safe
    })


degraded_df = pd.DataFrame(
    degraded_results
)


# ============================================================
# OUTPUT
# ============================================================

print(
    "HART-120 AR 15.5 — DEGRADED MANEUVER LOAD ALLEVIATION"
)

print(
    "-----------------------------------------------------"
)

print(
    degraded_df
    .round(3)
    .to_string(index=False)
)


# ============================================================
# FAIL-SAFE WEB REDESIGN
#
# Size the web so that complete loss of active MLA does NOT
# exceed the conceptual web shear limit.
# ============================================================

web_t_fail_safe_selected = (
    shear_maneuver_uncontrolled_selected
    /
    (
        2
        * tau_allow_trade
        * box_height_selected
    )
)


web_t_fail_safe_selected = np.maximum(
    web_t_fail_safe_selected,
    web_min_gauge_trade
)


# ------------------------------------------------------------
# Web masses
# ------------------------------------------------------------

web_mass_per_span_full_control = (
    2
    * web_t_full_control_selected
    * box_height_selected
    * rho_eq
)


web_mass_total_full_control = (
    2
    * np.trapezoid(
        web_mass_per_span_full_control,
        y_selected
    )
)


web_mass_per_span_fail_safe = (
    2
    * web_t_fail_safe_selected
    * box_height_selected
    * rho_eq
)


web_mass_total_fail_safe = (
    2
    * np.trapezoid(
        web_mass_per_span_fail_safe,
        y_selected
    )
)


# ------------------------------------------------------------
# Cap mass
# ------------------------------------------------------------

cap_mass_per_span_selected = (
    2
    * A_cap_design_selected
    * rho_eq
)


cap_mass_total_selected = (
    2
    * np.trapezoid(
        cap_mass_per_span_selected,
        y_selected
    )
)


# ------------------------------------------------------------
# Wingbox masses
# ------------------------------------------------------------

wingbox_mass_full_control = (
    cap_mass_total_selected
    + web_mass_total_full_control
)


wingbox_mass_fail_safe = (
    cap_mass_total_selected
    + web_mass_total_fail_safe
)


fail_safe_mass_penalty = (
    wingbox_mass_fail_safe
    - wingbox_mass_full_control
)


fail_safe_mass_penalty_percent = (
    fail_safe_mass_penalty
    / wingbox_mass_full_control
) * 100


fail_safe_mass_penalty_vs_baseline = (
    (
        wingbox_mass_fail_safe
        - base_conventional_mass
    )
    /
    base_conventional_mass
) * 100


fail_safe_within_budget = (
    wingbox_mass_fail_safe
    <= mass_budget
)


print()

print(
    "HART-120 AR 15.5 — FAIL-SAFE WEB REDESIGN"
)

print(
    "-----------------------------------------"
)

print(
    f"Full-control technology web mass: "
    f"{web_mass_total_full_control:.2f} kg"
)

print(
    f"Fail-safe web mass: "
    f"{web_mass_total_fail_safe:.2f} kg"
)

print(
    f"Additional fail-safe web mass: "
    f"{fail_safe_mass_penalty:.2f} kg"
)

print(
    f"Fail-safe mass penalty relative to "
    f"technology wingbox: "
    f"{fail_safe_mass_penalty_percent:.2f} %"
)

print()

print(
    f"Original technology wingbox mass: "
    f"{wingbox_mass_full_control:.2f} kg"
)

print(
    f"Fail-safe technology wingbox mass: "
    f"{wingbox_mass_fail_safe:.2f} kg"
)

print(
    f"Fail-safe wingbox penalty vs "
    f"AR 13.5 baseline: "
    f"{fail_safe_mass_penalty_vs_baseline:.2f} %"
)

print(
    f"+30% structural mass budget: "
    f"{mass_budget:.2f} kg"
)

print(
    f"Fail-safe AR 15.5 remains within budget: "
    f"{fail_safe_within_budget}"
)


# ============================================================
# PLOT 1 — FAILURE SENSITIVITY
# ============================================================

plt.figure(
    figsize=(9, 6)
)


plt.plot(
    degraded_df[
        "MLA_Availability_%"
    ],
    degraded_df[
        "Cap_Utilization"
    ],
    marker="o",
    label="Spar-cap stress utilization"
)


plt.plot(
    degraded_df[
        "MLA_Availability_%"
    ],
    degraded_df[
        "Web_Utilization"
    ],
    marker="o",
    label="Web shear utilization"
)


plt.axhline(
    1.0,
    linestyle="--",
    label="Allowable limit"
)


plt.xlabel(
    "Available Maneuver Load-Alleviation Capability (%)"
)

plt.ylabel(
    "Structural Utilization"
)

plt.title(
    "HART-120 AR 15.5 — Structural Sensitivity to MLA Degradation"
)

plt.grid(True)

plt.legend()

plt.show()


# ============================================================
# PLOT 2 — FAIL-SAFE WEB THICKNESS
# ============================================================

plt.figure(
    figsize=(9, 6)
)


plt.plot(
    eta_selected,
    web_t_full_control_selected * 1000,
    label="Full-control-sized web"
)


plt.plot(
    eta_selected,
    web_t_fail_safe_selected * 1000,
    label="Fail-safe web"
)


plt.axhline(
    web_min_gauge_trade * 1000,
    linestyle="--",
    label="Minimum web gauge"
)


plt.xlabel(
    "Normalized Half-Span, η"
)

plt.ylabel(
    "Web Thickness (mm)"
)

plt.title(
    "HART-120 AR 15.5 — Web Sizing for Active-Control Failure"
)

plt.grid(True)

plt.legend()

plt.show()

# %% [notebook cell 95]
# ============================================================
# HART-120 — LOAD-ALLEVIATION SYSTEM MASS BREAK-EVEN STUDY
# ============================================================

fail_safe_wingbox_mass = 6143.69       # kg
structural_mass_budget = 6242.85       # kg

available_system_mass = (
    structural_mass_budget - fail_safe_wingbox_mass
)

print("HART-120 AR 15.5 — CONTROL-SYSTEM MASS ALLOWANCE")
print("------------------------------------------------")
print(f"Structural mass budget: {structural_mass_budget:.2f} kg")
print(f"Fail-safe wingbox mass: {fail_safe_wingbox_mass:.2f} kg")
print(f"Remaining mass allowance: {available_system_mass:.2f} kg")


# Candidate total MLA-system masses
system_mass_cases = np.arange(0, 225, 25)

total_technology_mass = (
    fail_safe_wingbox_mass + system_mass_cases
)

within_budget = total_technology_mass <= structural_mass_budget

mass_margin = (
    structural_mass_budget - total_technology_mass
)


system_mass_df = pd.DataFrame({
    "MLA_System_Mass_kg": system_mass_cases,
    "Total_Technology_Mass_kg": total_technology_mass,
    "Mass_Margin_kg": mass_margin,
    "Within_30pct_Budget": within_budget
})

print()
print("SYSTEM-MASS SENSITIVITY")
print("-----------------------")
print(
    system_mass_df
    .round(2)
    .to_string(index=False)
)


# Maximum tested feasible system mass
feasible_system_masses = system_mass_cases[within_budget]

if len(feasible_system_masses) > 0:
    max_tested_feasible_system_mass = np.max(feasible_system_masses)
else:
    max_tested_feasible_system_mass = 0.0


print()
print("BREAK-EVEN RESULT")
print("-----------------")
print(
    f"Exact remaining mass allowance: "
    f"{available_system_mass:.2f} kg"
)
print(
    f"Maximum tested feasible MLA-system mass: "
    f"{max_tested_feasible_system_mass:.1f} kg"
)


# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    system_mass_cases,
    total_technology_mass,
    marker="o",
    label="Fail-safe wingbox + MLA system"
)

plt.axhline(
    structural_mass_budget,
    linestyle="--",
    label="+30% structural mass budget"
)

plt.axvline(
    available_system_mass,
    linestyle=":",
    label=f"Break-even = {available_system_mass:.1f} kg"
)

plt.xlabel("Total MLA System Mass (kg)")
plt.ylabel("Technology-Enabled Structural + System Mass (kg)")
plt.title(
    "HART-120 AR 15.5 — Load-Alleviation System Mass Break-Even"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 96]
# ============================================================
# HART-120 — WEIGHT-COUPLED AERODYNAMIC BENEFIT
# Does the high-AR wing still reduce drag after its mass penalty?
# ============================================================

# ------------------------------------------------------------
# VERIFIED DESIGN RESULTS FROM PREVIOUS STUDIES
# ------------------------------------------------------------

AR_reference = 13.5
AR_technology = 15.5

baseline_wingbox_mass = 4802.19       # kg
fail_safe_wingbox_mass = 6143.69      # kg

# Use a realistic study point inside our current mass allowance.
# 75 kg was the highest FEASIBLE point in the coarse system-mass sweep.
MLA_system_mass = 75.0                # kg

# Project-level zero-lift drag coefficient assumption.
# This is NOT claimed as a HART-120 validated value.
CD0_reference = 0.020


# ------------------------------------------------------------
# AIRCRAFT MASS ACCOUNTING
# ------------------------------------------------------------

technology_package_mass = (
    fail_safe_wingbox_mass + MLA_system_mass
)

added_aircraft_mass = (
    technology_package_mass - baseline_wingbox_mass
)

mass_technology_aircraft = (
    mass_design + added_aircraft_mass
)


# ------------------------------------------------------------
# CRUISE DYNAMIC PRESSURE
# ------------------------------------------------------------

q_cruise = 0.5 * rho_cruise * V_cruise**2


# ------------------------------------------------------------
# REQUIRED CRUISE LIFT COEFFICIENT
# ------------------------------------------------------------

CL_reference_weight_coupled = (
    mass_design * g
) / (
    q_cruise * S_wing
)

CL_technology_weight_coupled = (
    mass_technology_aircraft * g
) / (
    q_cruise * S_wing
)


# ------------------------------------------------------------
# INDUCED DRAG COEFFICIENT
#
# CDi = CL² / (pi * e * AR)
# ------------------------------------------------------------

CDi_reference = (
    CL_reference_weight_coupled**2
    / (np.pi * oswald_e * AR_reference)
)

CDi_technology = (
    CL_technology_weight_coupled**2
    / (np.pi * oswald_e * AR_technology)
)


# ------------------------------------------------------------
# INDUCED DRAG FORCE
# ------------------------------------------------------------

induced_drag_reference = (
    q_cruise * S_wing * CDi_reference
)

induced_drag_technology = (
    q_cruise * S_wing * CDi_technology
)

weight_coupled_induced_drag_reduction = (
    1
    - induced_drag_technology
    / induced_drag_reference
) * 100


# ------------------------------------------------------------
# PARASITE DRAG
#
# For this first-order study we keep CD0 and wing area constant.
# ------------------------------------------------------------

parasite_drag_reference = (
    q_cruise * S_wing * CD0_reference
)

parasite_drag_technology = parasite_drag_reference


# ------------------------------------------------------------
# TOTAL CRUISE DRAG
# ------------------------------------------------------------

total_drag_reference = (
    parasite_drag_reference
    + induced_drag_reference
)

total_drag_technology = (
    parasite_drag_technology
    + induced_drag_technology
)

total_drag_reduction = (
    1
    - total_drag_technology
    / total_drag_reference
) * 100


# ------------------------------------------------------------
# LIFT-TO-DRAG RATIO
# ------------------------------------------------------------

lift_reference = mass_design * g
lift_technology = mass_technology_aircraft * g

LD_reference = (
    lift_reference
    / total_drag_reference
)

LD_technology = (
    lift_technology
    / total_drag_technology
)

LD_change = (
    LD_technology / LD_reference - 1
) * 100


# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

print("HART-120 AR 15.5 — WEIGHT-COUPLED AERODYNAMIC TRADE")
print("----------------------------------------------------")

print(f"Baseline aircraft mass: {mass_design:.2f} kg")
print(
    f"Fail-safe AR 15.5 wingbox + MLA system: "
    f"{technology_package_mass:.2f} kg"
)
print(
    f"Added aircraft mass vs baseline wingbox: "
    f"{added_aircraft_mass:.2f} kg"
)
print(
    f"Technology aircraft mass: "
    f"{mass_technology_aircraft:.2f} kg"
)

print()
print("CRUISE LIFT REQUIREMENT")
print("-----------------------")

print(
    f"Baseline cruise CL: "
    f"{CL_reference_weight_coupled:.4f}"
)

print(
    f"Technology cruise CL: "
    f"{CL_technology_weight_coupled:.4f}"
)

print()
print("INDUCED DRAG")
print("------------")

print(
    f"Baseline induced drag: "
    f"{induced_drag_reference/1000:.3f} kN"
)

print(
    f"Technology induced drag: "
    f"{induced_drag_technology/1000:.3f} kN"
)

print(
    f"Weight-coupled induced-drag reduction: "
    f"{weight_coupled_induced_drag_reduction:.2f} %"
)

print(
    "Previous constant-weight AR-only reduction: "
    "12.90 %"
)

print()
print("TOTAL CRUISE DRAG")
print("-----------------")

print(
    f"Assumed CD0: "
    f"{CD0_reference:.4f}"
)

print(
    f"Baseline parasite drag: "
    f"{parasite_drag_reference/1000:.3f} kN"
)

print(
    f"Baseline total drag: "
    f"{total_drag_reference/1000:.3f} kN"
)

print(
    f"Technology total drag: "
    f"{total_drag_technology/1000:.3f} kN"
)

print(
    f"Total cruise drag reduction: "
    f"{total_drag_reduction:.2f} %"
)

print()
print("AERODYNAMIC EFFICIENCY")
print("----------------------")

print(
    f"Baseline L/D: "
    f"{LD_reference:.2f}"
)

print(
    f"Technology L/D: "
    f"{LD_technology:.2f}"
)

print(
    f"L/D change: "
    f"{LD_change:.2f} %"
)


# ============================================================
# SYSTEM-MASS SENSITIVITY
# ============================================================

system_mass_sweep = np.linspace(
    0,
    99.16,
    21
)

coupled_induced_drag_reduction_results = []
total_drag_reduction_results = []

for system_mass in system_mass_sweep:

    package_mass = (
        fail_safe_wingbox_mass
        + system_mass
    )

    aircraft_mass = (
        mass_design
        + package_mass
        - baseline_wingbox_mass
    )

    CL_temp = (
        aircraft_mass * g
        / (q_cruise * S_wing)
    )

    CDi_temp = (
        CL_temp**2
        / (np.pi * oswald_e * AR_technology)
    )

    induced_drag_temp = (
        q_cruise
        * S_wing
        * CDi_temp
    )

    total_drag_temp = (
        parasite_drag_reference
        + induced_drag_temp
    )

    coupled_induced_drag_reduction_results.append(
        (
            1
            - induced_drag_temp
            / induced_drag_reference
        ) * 100
    )

    total_drag_reduction_results.append(
        (
            1
            - total_drag_temp
            / total_drag_reference
        ) * 100
    )


coupled_induced_drag_reduction_results = np.array(
    coupled_induced_drag_reduction_results
)

total_drag_reduction_results = np.array(
    total_drag_reduction_results
)


# ------------------------------------------------------------
# Plot 1 — system mass vs surviving aerodynamic benefit
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    system_mass_sweep,
    coupled_induced_drag_reduction_results,
    marker="o",
    label="Induced-drag reduction"
)

plt.plot(
    system_mass_sweep,
    total_drag_reduction_results,
    marker="o",
    label="Total cruise-drag reduction"
)

plt.axvline(
    99.16,
    linestyle="--",
    label="Current mass-budget break-even"
)

plt.xlabel("MLA System Mass (kg)")
plt.ylabel("Drag Reduction vs AR 13.5 Baseline (%)")

plt.title(
    "HART-120 AR 15.5 — "
    "Aerodynamic Benefit After Technology Mass"
)

plt.grid(True)
plt.legend()
plt.show()


# ============================================================
# CD0 UNCERTAINTY STUDY
# ============================================================

CD0_cases = np.array([
    0.015,
    0.020,
    0.025
])

CD0_total_drag_reductions = []

for CD0_case in CD0_cases:

    parasite_drag_case = (
        q_cruise
        * S_wing
        * CD0_case
    )

    reference_total_drag_case = (
        parasite_drag_case
        + induced_drag_reference
    )

    technology_total_drag_case = (
        parasite_drag_case
        + induced_drag_technology
    )

    reduction_case = (
        1
        - technology_total_drag_case
        / reference_total_drag_case
    ) * 100

    CD0_total_drag_reductions.append(
        reduction_case
    )


CD0_sensitivity_df = pd.DataFrame({
    "Assumed_CD0": CD0_cases,
    "Total_Drag_Reduction_%":
        CD0_total_drag_reductions
})


print()
print("HART-120 CD0 SENSITIVITY")
print("------------------------")

print(
    CD0_sensitivity_df
    .round(3)
    .to_string(index=False)
)

# %% [notebook cell 97]
# ============================================================
# HART-120 — MISSION-LEVEL FUEL-BURN BENEFIT
# Does AR 15.5 still save fuel after carrying its added mass?
# ============================================================

# ------------------------------------------------------------
# DESIGN MISSION ASSUMPTIONS
# ------------------------------------------------------------

mission_range_km = 3000.0
mission_range_m = mission_range_km * 1000

# Effective cruise TSFC.
# Project-level assumption, not an engine-specific validated value.
tsfc = 1.70e-4       # 1/s

# Previously calculated aircraft states
mass_baseline = mass_design
mass_technology = mass_technology_aircraft

LD_baseline = LD_reference
LD_technology = LD_technology


# ------------------------------------------------------------
# BREGUET CRUISE RELATION
#
# R = (V/c) * (L/D) * ln(W_initial / W_final)
#
# Rearranged:
#
# W_final / W_initial =
# exp[-R*c / (V*(L/D))]
# ------------------------------------------------------------

baseline_mass_fraction_remaining = np.exp(
    -mission_range_m
    * tsfc
    / (
        V_cruise
        * LD_baseline
    )
)

technology_mass_fraction_remaining = np.exp(
    -mission_range_m
    * tsfc
    / (
        V_cruise
        * LD_technology
    )
)


# ------------------------------------------------------------
# CRUISE FUEL FRACTIONS
# ------------------------------------------------------------

baseline_cruise_fuel_fraction = (
    1
    - baseline_mass_fraction_remaining
)

technology_cruise_fuel_fraction = (
    1
    - technology_mass_fraction_remaining
)


# ------------------------------------------------------------
# CRUISE FUEL MASS
# ------------------------------------------------------------

baseline_cruise_fuel_mass = (
    mass_baseline
    * baseline_cruise_fuel_fraction
)

technology_cruise_fuel_mass = (
    mass_technology
    * technology_cruise_fuel_fraction
)


# ------------------------------------------------------------
# NET FUEL BENEFIT
# ------------------------------------------------------------

cruise_fuel_saving_kg = (
    baseline_cruise_fuel_mass
    - technology_cruise_fuel_mass
)

cruise_fuel_saving_percent = (
    cruise_fuel_saving_kg
    / baseline_cruise_fuel_mass
) * 100


# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

print("HART-120 AR 15.5 — MISSION-LEVEL CRUISE FUEL TRADE")
print("---------------------------------------------------")

print(f"Study cruise range: {mission_range_km:.0f} km")
print(f"Assumed effective TSFC: {tsfc:.2e} 1/s")
print(f"Cruise speed: {V_cruise:.2f} m/s")

print()
print("AIRCRAFT CONFIGURATIONS")
print("-----------------------")

print(
    f"Baseline aircraft mass: "
    f"{mass_baseline:.2f} kg"
)

print(
    f"Technology aircraft mass: "
    f"{mass_technology:.2f} kg"
)

print(
    f"Aircraft mass increase: "
    f"{mass_technology - mass_baseline:.2f} kg"
)

print()

print(
    f"Baseline L/D: "
    f"{LD_baseline:.2f}"
)

print(
    f"Technology L/D: "
    f"{LD_technology:.2f}"
)

print(
    f"L/D improvement: "
    f"{(LD_technology/LD_baseline - 1)*100:.2f} %"
)

print()
print("CRUISE FUEL RESULT")
print("------------------")

print(
    f"Baseline cruise fuel fraction: "
    f"{baseline_cruise_fuel_fraction*100:.2f} %"
)

print(
    f"Technology cruise fuel fraction: "
    f"{technology_cruise_fuel_fraction*100:.2f} %"
)

print(
    f"Baseline cruise fuel mass: "
    f"{baseline_cruise_fuel_mass:.2f} kg"
)

print(
    f"Technology cruise fuel mass: "
    f"{technology_cruise_fuel_mass:.2f} kg"
)

print(
    f"Net cruise fuel saving: "
    f"{cruise_fuel_saving_kg:.2f} kg"
)

print(
    f"Net cruise fuel saving: "
    f"{cruise_fuel_saving_percent:.2f} %"
)


# ============================================================
# RANGE SENSITIVITY
# ============================================================

range_sweep_km = np.arange(
    500,
    6500,
    500
)

baseline_fuel_results = []
technology_fuel_results = []
fuel_saving_results = []

for range_km in range_sweep_km:

    range_m = range_km * 1000

    baseline_fraction_remaining = np.exp(
        -range_m
        * tsfc
        / (
            V_cruise
            * LD_baseline
        )
    )

    technology_fraction_remaining = np.exp(
        -range_m
        * tsfc
        / (
            V_cruise
            * LD_technology
        )
    )

    baseline_fuel = (
        mass_baseline
        * (
            1
            - baseline_fraction_remaining
        )
    )

    technology_fuel = (
        mass_technology
        * (
            1
            - technology_fraction_remaining
        )
    )

    fuel_saving_percent = (
        (
            baseline_fuel
            - technology_fuel
        )
        / baseline_fuel
    ) * 100

    baseline_fuel_results.append(
        baseline_fuel
    )

    technology_fuel_results.append(
        technology_fuel
    )

    fuel_saving_results.append(
        fuel_saving_percent
    )


baseline_fuel_results = np.array(
    baseline_fuel_results
)

technology_fuel_results = np.array(
    technology_fuel_results
)

fuel_saving_results = np.array(
    fuel_saving_results
)


# ------------------------------------------------------------
# Find mission break-even
# ------------------------------------------------------------

positive_fuel_benefit = (
    fuel_saving_results > 0
)

if np.any(positive_fuel_benefit):

    first_positive_index = np.where(
        positive_fuel_benefit
    )[0][0]

    break_even_range_km = (
        range_sweep_km[
            first_positive_index
        ]
    )

else:

    break_even_range_km = np.nan


# ------------------------------------------------------------
# Results table
# ------------------------------------------------------------

mission_trade_df = pd.DataFrame({
    "Range_km":
        range_sweep_km,

    "Baseline_Cruise_Fuel_kg":
        baseline_fuel_results,

    "Technology_Cruise_Fuel_kg":
        technology_fuel_results,

    "Fuel_Saving_%":
        fuel_saving_results
})


print()
print("HART-120 RANGE SENSITIVITY")
print("--------------------------")

print(
    mission_trade_df
    .round(2)
    .to_string(index=False)
)

print()

if np.isfinite(break_even_range_km):

    print(
        "First tested range with positive "
        f"fuel benefit: {break_even_range_km:.0f} km"
    )

else:

    print(
        "No positive fuel benefit found "
        "within tested range."
    )


# ------------------------------------------------------------
# Plot — fuel saving vs mission range
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    range_sweep_km,
    fuel_saving_results,
    marker="o"
)

plt.axhline(
    0,
    linestyle="--",
    label="Fuel break-even"
)

plt.xlabel(
    "Cruise Range (km)"
)

plt.ylabel(
    "Technology Fuel Saving (%)"
)

plt.title(
    "HART-120 AR 15.5 — "
    "Mission Fuel Benefit vs Cruise Range"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# Plot — absolute cruise fuel
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    range_sweep_km,
    baseline_fuel_results,
    marker="o",
    label="AR 13.5 baseline"
)

plt.plot(
    range_sweep_km,
    technology_fuel_results,
    marker="o",
    label="AR 15.5 technology"
)

plt.xlabel(
    "Cruise Range (km)"
)

plt.ylabel(
    "Estimated Cruise Fuel (kg)"
)

plt.title(
    "HART-120 — "
    "Weight-Coupled Cruise Fuel Comparison"
)

plt.grid(True)
plt.legend()
plt.show()

# %% [notebook cell 98]
# ============================================================
# HART-120 — PHYSICS-GENERATED ML SURROGATE
# Mission-Level Aero-Structural Design Exploration
#
# PURPOSE:
# 1. Use the existing HART-120 physics results as the source of truth
# 2. Generate thousands of multidisciplinary design cases
# 3. Train ML surrogate models
# 4. Validate predictions on unseen cases
# 5. Use ML for rapid constrained design exploration
#
# IMPORTANT:
# ML does NOT replace the engineering model.
# It learns a surrogate of the physics-based design space.
# ============================================================


# ------------------------------------------------------------
# 1. Imports
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    accuracy_score,
    confusion_matrix
)


# ------------------------------------------------------------
# 2. Verified HART-120 reference quantities
# ------------------------------------------------------------

aircraft_mass_baseline = 55000.0       # kg

g_ml = 9.81                            # m/s^2
rho_ml = 0.364                         # kg/m^3
V_ml = 224.20                          # m/s
S_ml = 113.42                          # m^2

oswald_ml = 0.85
baseline_AR_ml = 13.5

TSFC_ml = 1.70e-4                      # 1/s

structural_mass_budget_fraction = 0.30


# ------------------------------------------------------------
# 3. Extract physics-generated AR / wingbox data
#
# These values come from the previous aero-structural
# HART-120 study. We are NOT inventing a new mass equation here.
# ------------------------------------------------------------

physics_AR = (
    AR_technology_df[
        "Aspect_Ratio"
    ]
    .to_numpy()
)

physics_wingbox_mass = (
    AR_technology_df[
        "Technology_Wingbox_Mass_kg"
    ]
    .to_numpy()
)

physics_sort_index = np.argsort(
    physics_AR
)

physics_AR = physics_AR[
    physics_sort_index
]

physics_wingbox_mass = physics_wingbox_mass[
    physics_sort_index
]


# Baseline conventional AR 13.5 wingbox mass

baseline_row_index = np.argmin(
    np.abs(
        AR_technology_df[
            "Aspect_Ratio"
        ].to_numpy()
        - baseline_AR_ml
    )
)

baseline_wingbox_mass_ml = (
    AR_technology_df.iloc[
        baseline_row_index
    ][
        "Conventional_Wingbox_Mass_kg"
    ]
)


# ------------------------------------------------------------
# 4. Preliminary fail-safe correction
#
# From our AR 15.5 failure/degradation study:
#
# Original technology wingbox = 6084.03 kg
# Fail-safe wingbox           = 6143.69 kg
#
# This ~0.98% factor is used ONLY as a preliminary
# cross-design approximation.
#
# Later, we should replace this with explicit fail-safe
# web sizing for every AR.
# ------------------------------------------------------------

reference_nominal_AR155_mass = 6084.03
reference_failsafe_AR155_mass = 6143.69

fail_safe_mass_factor = (
    reference_failsafe_AR155_mass
    / reference_nominal_AR155_mass
)


# ------------------------------------------------------------
# 5. Structural mass budget
# ------------------------------------------------------------

structural_mass_budget_ml = (
    baseline_wingbox_mass_ml
    * (
        1
        + structural_mass_budget_fraction
    )
)


# ------------------------------------------------------------
# 6. Mission physics evaluator
#
# INPUTS
# ------
# aspect_ratio
# mla_system_mass
# CD0
# cruise_range_km
#
# OUTPUTS
# -------
# wingbox mass
# technology package mass
# aircraft mass
# CL
# induced drag
# total drag
# L/D
# cruise fuel
# fuel saving
# structural-budget feasibility
# ------------------------------------------------------------

def evaluate_hart120_mission(
    aspect_ratio,
    mla_system_mass,
    CD0,
    cruise_range_km
):

    # --------------------------------------------------------
    # Wingbox mass interpolation
    #
    # Interpolates between the physics-generated AR cases.
    # --------------------------------------------------------

    nominal_wingbox_mass = np.interp(
        aspect_ratio,
        physics_AR,
        physics_wingbox_mass
    )


    # --------------------------------------------------------
    # Preliminary fail-safe correction
    # --------------------------------------------------------

    fail_safe_wingbox_mass = (
        nominal_wingbox_mass
        * fail_safe_mass_factor
    )


    # --------------------------------------------------------
    # Complete wing technology package
    # --------------------------------------------------------

    technology_package_mass = (
        fail_safe_wingbox_mass
        + mla_system_mass
    )


    # --------------------------------------------------------
    # Aircraft mass
    #
    # Replace the original AR 13.5 conventional wingbox
    # with the new wingbox + load-alleviation system.
    # --------------------------------------------------------

    aircraft_mass = (

        aircraft_mass_baseline

        - baseline_wingbox_mass_ml

        + technology_package_mass

    )


    # --------------------------------------------------------
    # Dynamic pressure
    # --------------------------------------------------------

    q = (
        0.5
        * rho_ml
        * V_ml**2
    )


    # --------------------------------------------------------
    # Technology-aircraft cruise lift coefficient
    # --------------------------------------------------------

    technology_CL = (

        aircraft_mass
        * g_ml

        / (
            q
            * S_ml
        )

    )


    # --------------------------------------------------------
    # Technology induced drag coefficient
    # --------------------------------------------------------

    technology_CDi = (

        technology_CL**2

        / (
            np.pi
            * oswald_ml
            * aspect_ratio
        )

    )


    # --------------------------------------------------------
    # Technology induced drag
    # --------------------------------------------------------

    technology_induced_drag = (

        q
        * S_ml
        * technology_CDi

    )


    # --------------------------------------------------------
    # Technology total cruise drag
    # --------------------------------------------------------

    technology_CD = (
        CD0
        + technology_CDi
    )


    technology_total_drag = (

        q
        * S_ml
        * technology_CD

    )


    # --------------------------------------------------------
    # Technology L/D
    # --------------------------------------------------------

    technology_LD = (

        aircraft_mass
        * g_ml

        / technology_total_drag

    )


    # --------------------------------------------------------
    # Baseline aircraft at SAME CD0 and SAME range
    #
    # This makes the comparison fair.
    # --------------------------------------------------------

    baseline_CL = (

        aircraft_mass_baseline
        * g_ml

        / (
            q
            * S_ml
        )

    )


    baseline_CDi = (

        baseline_CL**2

        / (
            np.pi
            * oswald_ml
            * baseline_AR_ml
        )

    )


    baseline_induced_drag = (

        q
        * S_ml
        * baseline_CDi

    )


    baseline_CD = (
        CD0
        + baseline_CDi
    )


    baseline_total_drag = (

        q
        * S_ml
        * baseline_CD

    )


    baseline_LD = (

        aircraft_mass_baseline
        * g_ml

        / baseline_total_drag

    )


    # --------------------------------------------------------
    # Breguet-type cruise-fuel estimate
    # --------------------------------------------------------

    cruise_range_m = (
        cruise_range_km
        * 1000
    )


    baseline_fuel_fraction = (

        1

        - np.exp(

            -cruise_range_m
            * TSFC_ml

            / (
                V_ml
                * baseline_LD
            )

        )

    )


    technology_fuel_fraction = (

        1

        - np.exp(

            -cruise_range_m
            * TSFC_ml

            / (
                V_ml
                * technology_LD
            )

        )

    )


    baseline_fuel_mass = (

        aircraft_mass_baseline
        * baseline_fuel_fraction

    )


    technology_fuel_mass = (

        aircraft_mass
        * technology_fuel_fraction

    )


    # --------------------------------------------------------
    # Fuel benefit
    # --------------------------------------------------------

    fuel_saving_percent = (

        (
            baseline_fuel_mass
            - technology_fuel_mass
        )

        / baseline_fuel_mass

        * 100

    )


    # --------------------------------------------------------
    # Drag reductions
    # --------------------------------------------------------

    induced_drag_reduction_percent = (

        (
            baseline_induced_drag
            - technology_induced_drag
        )

        / baseline_induced_drag

        * 100

    )


    total_drag_reduction_percent = (

        (
            baseline_total_drag
            - technology_total_drag
        )

        / baseline_total_drag

        * 100

    )


    # --------------------------------------------------------
    # Structural mass-budget constraint
    # --------------------------------------------------------

    mass_margin = (

        structural_mass_budget_ml
        - technology_package_mass

    )


    structurally_feasible = (
        technology_package_mass
        <= structural_mass_budget_ml
    )


    # --------------------------------------------------------
    # Return engineering results
    # --------------------------------------------------------

    return {

        "Aspect_Ratio":
            aspect_ratio,

        "MLA_System_Mass_kg":
            mla_system_mass,

        "CD0":
            CD0,

        "Cruise_Range_km":
            cruise_range_km,

        "Nominal_Wingbox_Mass_kg":
            nominal_wingbox_mass,

        "FailSafe_Wingbox_Mass_kg":
            fail_safe_wingbox_mass,

        "Technology_Package_Mass_kg":
            technology_package_mass,

        "Aircraft_Mass_kg":
            aircraft_mass,

        "Cruise_CL":
            technology_CL,

        "Induced_Drag_kN":
            technology_induced_drag / 1000,

        "Total_Cruise_Drag_kN":
            technology_total_drag / 1000,

        "L_over_D":
            technology_LD,

        "Cruise_Fuel_kg":
            technology_fuel_mass,

        "Baseline_Cruise_Fuel_kg":
            baseline_fuel_mass,

        "Fuel_Saving_%":
            fuel_saving_percent,

        "Induced_Drag_Reduction_%":
            induced_drag_reduction_percent,

        "Total_Drag_Reduction_%":
            total_drag_reduction_percent,

        "Structural_Mass_Margin_kg":
            mass_margin,

        "Structurally_Feasible":
            structurally_feasible
    }


# ============================================================
# 7. GENERATE PHYSICS-BASED ML DATASET
# ============================================================

rng = np.random.default_rng(
    42
)

n_ml_cases = 6000


AR_samples = rng.uniform(
    13.5,
    18.0,
    n_ml_cases
)


system_mass_samples = rng.uniform(
    0.0,
    150.0,
    n_ml_cases
)


CD0_samples = rng.uniform(
    0.015,
    0.025,
    n_ml_cases
)


range_samples = rng.uniform(
    500.0,
    6000.0,
    n_ml_cases
)


ml_results = []


for i in range(
    n_ml_cases
):

    case_result = evaluate_hart120_mission(

        aspect_ratio=
            AR_samples[i],

        mla_system_mass=
            system_mass_samples[i],

        CD0=
            CD0_samples[i],

        cruise_range_km=
            range_samples[i]

    )

    ml_results.append(
        case_result
    )


hart120_ml_df = pd.DataFrame(
    ml_results
)


print()
print(
    "HART-120 PHYSICS-GENERATED ML DATASET"
)

print(
    "-------------------------------------"
)

print(
    f"Total design cases: "
    f"{len(hart120_ml_df)}"
)

print(
    f"Feasible cases: "
    f"{hart120_ml_df['Structurally_Feasible'].sum()}"
)

print(
    f"Infeasible cases: "
    f"{(~hart120_ml_df['Structurally_Feasible']).sum()}"
)

print()

display(
    hart120_ml_df.head()
)


# ============================================================
# 8. ML INPUTS AND OUTPUTS
# ============================================================

feature_columns = [

    "Aspect_Ratio",
    "MLA_System_Mass_kg",
    "CD0",
    "Cruise_Range_km"

]


regression_targets = [

    "FailSafe_Wingbox_Mass_kg",
    "Total_Cruise_Drag_kN",
    "L_over_D",
    "Cruise_Fuel_kg",
    "Fuel_Saving_%"

]


X = hart120_ml_df[
    feature_columns
]


Y = hart120_ml_df[
    regression_targets
]


# ------------------------------------------------------------
# Train/test split
# ------------------------------------------------------------

X_train, X_test, Y_train, Y_test = train_test_split(

    X,
    Y,

    test_size=0.20,

    random_state=42

)


# ============================================================
# 9. RANDOM-FOREST MULTI-OUTPUT SURROGATE
# ============================================================

rf_regressor = RandomForestRegressor(

    n_estimators=300,

    min_samples_leaf=2,

    random_state=42,

    n_jobs=-1

)


rf_regressor.fit(
    X_train,
    Y_train
)


Y_prediction = rf_regressor.predict(
    X_test
)


Y_prediction_df = pd.DataFrame(

    Y_prediction,

    columns=
        regression_targets,

    index=
        Y_test.index

)


# ============================================================
# 10. VALIDATION METRICS
# ============================================================

validation_results = []


for target in regression_targets:

    r2 = r2_score(

        Y_test[target],

        Y_prediction_df[target]

    )


    mae = mean_absolute_error(

        Y_test[target],

        Y_prediction_df[target]

    )


    validation_results.append({

        "Target":
            target,

        "R2":
            r2,

        "MAE":
            mae

    })


validation_df = pd.DataFrame(
    validation_results
)


print()
print(
    "HART-120 ML SURROGATE VALIDATION"
)

print(
    "--------------------------------"
)

print(

    validation_df
    .round(5)
    .to_string(
        index=False
    )

)


# ============================================================
# 11. STRUCTURAL-FEASIBILITY CLASSIFIER
# ============================================================

y_feasible = (

    hart120_ml_df[
        "Structurally_Feasible"
    ]

    .astype(int)

)


X_train_class, X_test_class, y_train_class, y_test_class = (
    train_test_split(

        X,
        y_feasible,

        test_size=0.20,

        random_state=42,

        stratify=y_feasible

    )
)


rf_classifier = RandomForestClassifier(

    n_estimators=300,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1

)


rf_classifier.fit(

    X_train_class,
    y_train_class

)


feasibility_prediction = (

    rf_classifier.predict(
        X_test_class
    )

)


classifier_accuracy = accuracy_score(

    y_test_class,

    feasibility_prediction

)


print()
print(
    "STRUCTURAL FEASIBILITY CLASSIFIER"
)

print(
    "---------------------------------"
)

print(
    f"Classification accuracy: "
    f"{classifier_accuracy * 100:.2f} %"
)

print()

print(
    "Confusion matrix:"
)

print(

    confusion_matrix(

        y_test_class,

        feasibility_prediction

    )

)


# ============================================================
# 12. PREDICTED VS PHYSICS — FUEL SAVING
# ============================================================

plt.figure(
    figsize=(7, 6)
)

plt.scatter(

    Y_test[
        "Fuel_Saving_%"
    ],

    Y_prediction_df[
        "Fuel_Saving_%"
    ],

    alpha=0.45

)


fuel_min = min(

    Y_test[
        "Fuel_Saving_%"
    ].min(),

    Y_prediction_df[
        "Fuel_Saving_%"
    ].min()

)


fuel_max = max(

    Y_test[
        "Fuel_Saving_%"
    ].max(),

    Y_prediction_df[
        "Fuel_Saving_%"
    ].max()

)


plt.plot(

    [
        fuel_min,
        fuel_max
    ],

    [
        fuel_min,
        fuel_max
    ],

    linestyle="--"

)


plt.xlabel(
    "Physics-Model Fuel Saving (%)"
)

plt.ylabel(
    "ML-Predicted Fuel Saving (%)"
)

plt.title(
    "HART-120 — ML Surrogate Validation"
)

plt.grid(
    True
)

plt.show()


# ============================================================
# 13. FEATURE IMPORTANCE
# ============================================================

feature_importance_df = pd.DataFrame({

    "Feature":
        feature_columns,

    "Importance":
        rf_regressor.feature_importances_

})


feature_importance_df = (

    feature_importance_df

    .sort_values(

        "Importance",

        ascending=False

    )

)


print()
print(
    "HART-120 ML FEATURE IMPORTANCE"
)

print(
    "------------------------------"
)

print(

    feature_importance_df
    .round(4)
    .to_string(
        index=False
    )

)


plt.figure(
    figsize=(7, 5)
)

plt.bar(

    feature_importance_df[
        "Feature"
    ],

    feature_importance_df[
        "Importance"
    ]

)

plt.ylabel(
    "Random-Forest Feature Importance"
)

plt.title(
    "HART-120 — ML Design Variable Importance"
)

plt.xticks(
    rotation=20
)

plt.grid(
    True,
    axis="y"
)

plt.tight_layout()

plt.show()


# ============================================================
# 14. ML-ASSISTED DESIGN SEARCH
#
# Engineering question:
#
# At:
#   CD0 = 0.020
#   cruise range = 3000 km
#   MLA system mass = 75 kg
#
# What AR gives the largest predicted fuel benefit
# while staying within the +30% structural budget?
# ============================================================

AR_candidate_grid = np.linspace(

    13.5,

    18.0,

    451

)


candidate_df = pd.DataFrame({

    "Aspect_Ratio":
        AR_candidate_grid,

    "MLA_System_Mass_kg":
        np.full(
            len(AR_candidate_grid),
            75.0
        ),

    "CD0":
        np.full(
            len(AR_candidate_grid),
            0.020
        ),

    "Cruise_Range_km":
        np.full(
            len(AR_candidate_grid),
            3000.0
        )

})


candidate_predictions = (

    rf_regressor.predict(
        candidate_df[
            feature_columns
        ]
    )

)


candidate_prediction_df = pd.DataFrame(

    candidate_predictions,

    columns=
        regression_targets

)


candidate_prediction_df[
    "Aspect_Ratio"
] = AR_candidate_grid


candidate_prediction_df[
    "Predicted_Feasible"
] = (

    rf_classifier.predict(

        candidate_df[
            feature_columns
        ]

    )

    .astype(bool)

)


feasible_candidate_predictions = (

    candidate_prediction_df[

        candidate_prediction_df[
            "Predicted_Feasible"
        ]

    ]

)


best_ml_index = (

    feasible_candidate_predictions[
        "Fuel_Saving_%"
    ]

    .idxmax()

)


best_ml_design = (

    feasible_candidate_predictions
    .loc[
        best_ml_index
    ]

)


print()
print(
    "HART-120 ML-ASSISTED DESIGN SEARCH"
)

print(
    "----------------------------------"
)

print(
    f"Predicted best feasible AR: "
    f"{best_ml_design['Aspect_Ratio']:.3f}"
)

print(
    f"Predicted fuel saving: "
    f"{best_ml_design['Fuel_Saving_%']:.3f} %"
)

print(
    f"Predicted L/D: "
    f"{best_ml_design['L_over_D']:.3f}"
)

print(
    f"Predicted cruise drag: "
    f"{best_ml_design['Total_Cruise_Drag_kN']:.3f} kN"
)

print(
    f"Predicted wingbox mass: "
    f"{best_ml_design['FailSafe_Wingbox_Mass_kg']:.2f} kg"
)


# ============================================================
# 15. PHYSICS VERIFICATION OF ML-SUGGESTED DESIGN
#
# Critical engineering rule:
#
# NEVER accept the ML optimum without checking it
# against the physics model.
# ============================================================

best_AR_ml = (
    best_ml_design[
        "Aspect_Ratio"
    ]
)


verified_best_design = (

    evaluate_hart120_mission(

        aspect_ratio=
            best_AR_ml,

        mla_system_mass=
            75.0,

        CD0=
            0.020,

        cruise_range_km=
            3000.0

    )

)


print()
print(
    "PHYSICS VERIFICATION OF ML DESIGN"
)

print(
    "---------------------------------"
)

print(
    f"Verified AR: "
    f"{verified_best_design['Aspect_Ratio']:.3f}"
)

print(
    f"Verified technology package mass: "
    f"{verified_best_design['Technology_Package_Mass_kg']:.2f} kg"
)

print(
    f"Structural mass budget: "
    f"{structural_mass_budget_ml:.2f} kg"
)

print(
    f"Structural mass margin: "
    f"{verified_best_design['Structural_Mass_Margin_kg']:.2f} kg"
)

print(
    f"Verified L/D: "
    f"{verified_best_design['L_over_D']:.3f}"
)

print(
    f"Verified total cruise drag: "
    f"{verified_best_design['Total_Cruise_Drag_kN']:.3f} kN"
)

print(
    f"Verified cruise fuel: "
    f"{verified_best_design['Cruise_Fuel_kg']:.2f} kg"
)

print(
    f"Verified fuel saving: "
    f"{verified_best_design['Fuel_Saving_%']:.3f} %"
)

print(
    f"Structurally feasible: "
    f"{verified_best_design['Structurally_Feasible']}"
)


# ============================================================
# 16. ML DESIGN-SPACE PLOT
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(

    candidate_prediction_df[
        "Aspect_Ratio"
    ],

    candidate_prediction_df[
        "Fuel_Saving_%"
    ],

    label="ML-Predicted Fuel Saving"

)


plt.axvline(

    best_AR_ml,

    linestyle="--",

    label=(
        f"Best Feasible AR = "
        f"{best_AR_ml:.2f}"
    )

)


plt.xlabel(
    "Aspect Ratio"
)

plt.ylabel(
    "Predicted Cruise Fuel Saving (%)"
)

plt.title(
    "HART-120 — ML-Assisted Aspect-Ratio Design Search"
)

plt.grid(
    True
)

plt.legend()

plt.show()

# %% [notebook cell 99]
# ============================================================
# HART-120 — PHYSICS-GENERATED DYNAMIC GLA ML DATABASE
#
# Purpose:
# Generate a multidisciplinary control / gust database from the
# existing first-mode flexible-wing dynamic model.
#
# ML inputs:
#   - Gust gradient H
#   - Actuator time constant
#   - Sensor/control delay
#   - Actuator rate limit
#   - Gust preview time
#
# Physics outputs:
#   - Peak root bending moment
#   - Root-moment reduction
#   - Peak root stress
#   - Peak wing-tip deflection
#   - Peak actuator demand
# ============================================================

from scipy.stats import qmc


# ------------------------------------------------------------
# 1. Helper — 1-cosine gust scale
# ------------------------------------------------------------

def ml_gust_scale(t_array, H):

    scale = np.zeros_like(t_array)

    active = (
        (t_array >= 0.0)
        &
        (t_array <= 2.0 * H / V_cruise)
    )

    distance = (
        V_cruise
        * t_array[active]
    )

    scale[active] = (
        0.5
        * (
            1.0
            - np.cos(
                np.pi
                * distance
                / H
            )
        )
    )

    return scale


# ------------------------------------------------------------
# 2. Generalized aerodynamic loads
#
# These come directly from the previously validated
# HART-120 reduced-order aerodynamic model.
# ------------------------------------------------------------

Q_gust_peak_ml = np.trapezoid(
    delta_lift_per_span_gust
    * phi,
    y
)

Q_control_full_ml = np.trapezoid(
    delta_lift_gla_full
    * phi,
    y
)


# ------------------------------------------------------------
# 3. Dynamic gust simulation function
# ------------------------------------------------------------

def run_dynamic_gla_case(
    H,
    actuator_tau,
    sensor_delay,
    rate_limit,
    preview_time
):

    # --------------------------------------------------------
    # Gust duration
    # --------------------------------------------------------

    gust_duration = (
        2.0 * H
        / V_cruise
    )

    post_gust_time = 2.0

    # Start simulation before gust arrival so preview
    # control can physically pre-actuate the surface.
    pre_gust_time = 0.15

    time_ml = np.arange(
        -pre_gust_time,
        gust_duration
        + post_gust_time
        + dt,
        dt
    )


    # --------------------------------------------------------
    # Actual gust arriving at wing
    # --------------------------------------------------------

    gust_scale_wing_ml = ml_gust_scale(
        time_ml,
        H
    )


    Q_uncontrolled_ml = (
        gust_scale_wing_ml
        * Q_gust_peak_ml
    )


    # --------------------------------------------------------
    # Forward gust measurement
    #
    # Sensor sees the gust preview_time seconds before
    # the gust reaches the wing.
    # --------------------------------------------------------

    sensed_gust_scale_ml = ml_gust_scale(
        time_ml + preview_time,
        H
    )


    command_ml = (
        best_gust_required_deflection
        * sensed_gust_scale_ml
    )

    command_ml = np.clip(
        command_ml,
        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Sensor / control delay
    # --------------------------------------------------------

    delayed_command_time = (
        time_ml
        - sensor_delay
    )

    delayed_command_ml = np.interp(
        delayed_command_time,
        time_ml,
        command_ml,
        left=0.0,
        right=0.0
    )


    # --------------------------------------------------------
    # Actuator response
    # --------------------------------------------------------

    actuator_ml = np.zeros_like(
        time_ml
    )


    for k in range(
        1,
        len(time_ml)
    ):

        desired_rate_ml = (
            delayed_command_ml[k]
            - actuator_ml[k-1]
        ) / actuator_tau


        actual_rate_ml = np.clip(
            desired_rate_ml,
            -rate_limit,
            rate_limit
        )


        actuator_ml[k] = (
            actuator_ml[k-1]
            + actual_rate_ml * dt
        )


        actuator_ml[k] = np.clip(
            actuator_ml[k],
            -max_deflection_deg,
            max_deflection_deg
        )


    # --------------------------------------------------------
    # Achieved aerodynamic control authority
    # --------------------------------------------------------

    control_scale_ml = (
        actuator_ml
        / best_gust_required_deflection
    )


    Q_controlled_ml = (
        Q_uncontrolled_ml

        + control_scale_ml
        * Q_control_full_ml
    )


    # --------------------------------------------------------
    # Flexible-wing modal response
    # --------------------------------------------------------

    (
        q_uncontrolled_ml,
        _,
        _
    ) = newmark_beta_response(

        Q_uncontrolled_ml,
        modal_mass,
        modal_damping,
        modal_stiffness,
        dt
    )


    (
        q_controlled_ml,
        _,
        _
    ) = newmark_beta_response(

        Q_controlled_ml,
        modal_mass,
        modal_damping,
        modal_stiffness,
        dt
    )


    # --------------------------------------------------------
    # Root bending moment
    # --------------------------------------------------------

    root_moment_uncontrolled_ml = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_uncontrolled_ml
        * root_moment_response_scale
    )


    root_moment_controlled_ml = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_controlled_ml
        * root_moment_response_scale
    )


    # --------------------------------------------------------
    # Wing-tip deflection
    # --------------------------------------------------------

    tip_uncontrolled_ml = (

        tip_deflection_mass_reduced

        + q_uncontrolled_ml
        * tip_response_scale
    )


    tip_controlled_ml = (

        tip_deflection_mass_reduced

        + q_controlled_ml
        * tip_response_scale
    )


    # --------------------------------------------------------
    # Root stress
    # --------------------------------------------------------

    root_stress_controlled_ml = (

        root_moment_controlled_ml

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Peak responses
    # --------------------------------------------------------

    peak_root_u_ml = np.max(
        root_moment_uncontrolled_ml
    )

    peak_root_c_ml = np.max(
        root_moment_controlled_ml
    )

    minimum_root_c_ml = np.min(
        root_moment_controlled_ml
    )

    peak_tip_u_ml = np.max(
        tip_uncontrolled_ml
    )

    peak_tip_c_ml = np.max(
        tip_controlled_ml
    )

    peak_stress_c_ml = np.max(
        np.abs(
            root_stress_controlled_ml
        )
    )

    peak_actuator_ml = np.max(
        np.abs(
            actuator_ml
        )
    )


    # --------------------------------------------------------
    # Load-alleviation performance
    # --------------------------------------------------------

    root_moment_reduction_ml = (

        (
            peak_root_u_ml
            - peak_root_c_ml
        )

        / peak_root_u_ml

    ) * 100.0


    tip_reduction_ml = (

        (
            peak_tip_u_ml
            - peak_tip_c_ml
        )

        / peak_tip_u_ml

    ) * 100.0


    gust_characteristic_frequency_ml = (
        1.0 / gust_duration
    )

    frequency_ratio_ml = (
        gust_characteristic_frequency_ml
        / frequency_hz
    )


    # --------------------------------------------------------
    # Return one engineering design case
    # --------------------------------------------------------

    return {

        "Gust_H_m":
            H,

        "Gust_Duration_s":
            gust_duration,

        "Frequency_Ratio":
            frequency_ratio_ml,

        "Actuator_Time_Constant_s":
            actuator_tau,

        "Sensor_Delay_s":
            sensor_delay,

        "Rate_Limit_deg_s":
            rate_limit,

        "Preview_Time_s":
            preview_time,

        "Effective_Lead_s":
            preview_time - sensor_delay,

        "Peak_Root_Moment_Uncontrolled_MNm":
            peak_root_u_ml / 1e6,

        "Peak_Root_Moment_Controlled_MNm":
            peak_root_c_ml / 1e6,

        "Minimum_Root_Moment_Controlled_MNm":
            minimum_root_c_ml / 1e6,

        "Root_Moment_Reduction_%":
            root_moment_reduction_ml,

        "Peak_Root_Stress_MPa":
            peak_stress_c_ml / 1e6,

        "Peak_Tip_Deflection_Uncontrolled_m":
            peak_tip_u_ml,

        "Peak_Tip_Deflection_Controlled_m":
            peak_tip_c_ml,

        "Tip_Deflection_Reduction_%":
            tip_reduction_ml,

        "Peak_Actuator_Deflection_deg":
            peak_actuator_ml,

        "Meets_10pct_GLA_Target":
            root_moment_reduction_ml >= 10.0
    }


# ------------------------------------------------------------
# 4. Generate design space
#
# Latin Hypercube Sampling gives better multidimensional
# coverage than simple random sampling.
# ------------------------------------------------------------

n_dynamic_ml_cases = 3000

sampler = qmc.LatinHypercube(
    d=5,
    seed=42
)

unit_samples = sampler.random(
    n=n_dynamic_ml_cases
)


lower_bounds = np.array([
    10.0,     # H [m]
    0.04,     # actuator tau [s]
    0.00,     # control delay [s]
    40.0,     # rate limit [deg/s]
    0.00      # preview [s]
])


upper_bounds = np.array([
    200.0,    # H [m]
    0.20,     # actuator tau [s]
    0.08,     # control delay [s]
    160.0,    # rate limit [deg/s]
    0.12      # preview [s]
])


dynamic_design_samples = qmc.scale(
    unit_samples,
    lower_bounds,
    upper_bounds
)


# ------------------------------------------------------------
# 5. Run physics model
# ------------------------------------------------------------

dynamic_ml_results = []


print(
    "Generating HART-120 dynamic GLA ML database..."
)


for i, sample in enumerate(
    dynamic_design_samples
):

    H_sample = sample[0]

    tau_sample = sample[1]

    delay_sample = sample[2]

    rate_sample = sample[3]

    preview_sample = sample[4]


    result = run_dynamic_gla_case(

        H_sample,
        tau_sample,
        delay_sample,
        rate_sample,
        preview_sample
    )


    dynamic_ml_results.append(
        result
    )


    if (
        (i + 1) % 500 == 0
        or (i + 1) == n_dynamic_ml_cases
    ):

        print(
            f"Completed "
            f"{i + 1} / "
            f"{n_dynamic_ml_cases}"
        )


# ------------------------------------------------------------
# 6. DataFrame
# ------------------------------------------------------------

dynamic_gla_ml_df = pd.DataFrame(
    dynamic_ml_results
)


# ------------------------------------------------------------
# 7. Dataset diagnostics
# ------------------------------------------------------------

n_meeting_target = (

    dynamic_gla_ml_df[
        "Meets_10pct_GLA_Target"
    ]
    .sum()
)


print()
print(
    "HART-120 DYNAMIC GLA ML DATABASE"
)

print(
    "--------------------------------"
)

print(
    f"Total physics simulations: "
    f"{len(dynamic_gla_ml_df)}"
)

print(
    f"Cases meeting 10% GLA target: "
    f"{n_meeting_target}"
)

print(
    f"Cases below target: "
    f"{len(dynamic_gla_ml_df) - n_meeting_target}"
)


print()
print(
    "ROOT-MOMENT REDUCTION RANGE"
)

print(
    "---------------------------"
)

print(
    f"Minimum: "
    f"{dynamic_gla_ml_df['Root_Moment_Reduction_%'].min():.2f} %"
)

print(
    f"Maximum: "
    f"{dynamic_gla_ml_df['Root_Moment_Reduction_%'].max():.2f} %"
)

print(
    f"Mean: "
    f"{dynamic_gla_ml_df['Root_Moment_Reduction_%'].mean():.2f} %"
)


print()
print(
    dynamic_gla_ml_df
    .head()
    .round(4)
    .to_string(index=False)
)

# %% [notebook cell 100]
# ============================================================
# HART-120 — DYNAMIC GLA ML SURROGATE
#
# Objective:
# Replace thousands of transient aeroelastic simulations with
# fast ML predictions while retaining the physics-generated
# design database.
# ============================================================

from sklearn.model_selection import train_test_split
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    classification_report,
    confusion_matrix,
    balanced_accuracy_score
)
from sklearn.inspection import permutation_importance


# ------------------------------------------------------------
# 1. ML input variables
# ------------------------------------------------------------

dynamic_features = [

    "Gust_H_m",

    "Actuator_Time_Constant_s",

    "Sensor_Delay_s",

    "Rate_Limit_deg_s",

    "Preview_Time_s"
]


# ------------------------------------------------------------
# 2. Regression targets
#
# These are engineering quantities that later matter during
# actuator/control-system design.
# ------------------------------------------------------------

dynamic_targets = [

    "Peak_Root_Moment_Controlled_MNm",

    "Root_Moment_Reduction_%",

    "Peak_Root_Stress_MPa",

    "Peak_Tip_Deflection_Controlled_m",

    "Peak_Actuator_Deflection_deg"
]


X_dynamic = dynamic_gla_ml_df[
    dynamic_features
]


Y_dynamic = dynamic_gla_ml_df[
    dynamic_targets
]


# ------------------------------------------------------------
# 3. Train / test split
# ------------------------------------------------------------

(
    X_train_dyn,
    X_test_dyn,
    Y_train_dyn,
    Y_test_dyn
) = train_test_split(

    X_dynamic,
    Y_dynamic,

    test_size=0.20,
    random_state=42
)


# ------------------------------------------------------------
# 4. Train one random-forest surrogate for each response
# ------------------------------------------------------------

dynamic_regression_models = {}

dynamic_validation_results = []


for target in dynamic_targets:

    model = RandomForestRegressor(

        n_estimators=350,

        max_depth=None,

        min_samples_leaf=2,

        max_features=1.0,

        random_state=42,

        n_jobs=-1
    )


    model.fit(

        X_train_dyn,

        Y_train_dyn[target]
    )


    prediction = model.predict(
        X_test_dyn
    )


    r2 = r2_score(

        Y_test_dyn[target],

        prediction
    )


    mae = mean_absolute_error(

        Y_test_dyn[target],

        prediction
    )


    dynamic_regression_models[
        target
    ] = model


    dynamic_validation_results.append({

        "Target":
            target,

        "R2":
            r2,

        "MAE":
            mae
    })


dynamic_validation_df = pd.DataFrame(
    dynamic_validation_results
)


print()
print(
    "HART-120 DYNAMIC GLA ML SURROGATE VALIDATION"
)

print(
    "--------------------------------------------"
)

print(
    dynamic_validation_df
    .round(5)
    .to_string(index=False)
)


# ============================================================
# 5. STRUCTURAL / GLA FEASIBILITY CLASSIFIER
# ============================================================

classification_target = (

    dynamic_gla_ml_df[
        "Meets_10pct_GLA_Target"
    ]
    .astype(int)
)


(
    X_train_class,
    X_test_class,
    y_train_class,
    y_test_class
) = train_test_split(

    X_dynamic,
    classification_target,

    test_size=0.20,

    random_state=42,

    stratify=classification_target
)


gla_classifier = RandomForestClassifier(

    n_estimators=400,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1
)


gla_classifier.fit(

    X_train_class,

    y_train_class
)


class_prediction = gla_classifier.predict(
    X_test_class
)


class_probability = gla_classifier.predict_proba(
    X_test_class
)[:, 1]


balanced_accuracy = balanced_accuracy_score(

    y_test_class,

    class_prediction
)


print()
print(
    "HART-120 10% GLA FEASIBILITY CLASSIFIER"
)

print(
    "---------------------------------------"
)

print(
    f"Balanced accuracy: "
    f"{balanced_accuracy*100:.2f} %"
)


print()
print(
    "Confusion matrix:"
)

print(
    confusion_matrix(
        y_test_class,
        class_prediction
    )
)


print()
print(
    classification_report(

        y_test_class,

        class_prediction,

        target_names=[
            "Below target",
            "Meets target"
        ],

        digits=4
    )
)


# ============================================================
# 6. ROOT-MOMENT SURROGATE VALIDATION PLOT
# ============================================================

root_reduction_model = (
    dynamic_regression_models[
        "Root_Moment_Reduction_%"
    ]
)


root_reduction_prediction = (
    root_reduction_model.predict(
        X_test_dyn
    )
)


root_reduction_actual = (

    Y_test_dyn[
        "Root_Moment_Reduction_%"
    ]
    .to_numpy()
)


plot_min = min(

    np.min(root_reduction_actual),

    np.min(root_reduction_prediction)
)


plot_max = max(

    np.max(root_reduction_actual),

    np.max(root_reduction_prediction)
)


plt.figure(
    figsize=(8, 7)
)


plt.scatter(

    root_reduction_actual,

    root_reduction_prediction,

    alpha=0.45
)


plt.plot(

    [plot_min, plot_max],

    [plot_min, plot_max],

    "--"
)


plt.xlabel(
    "Physics-Simulated Root-Moment Reduction (%)"
)


plt.ylabel(
    "ML-Predicted Root-Moment Reduction (%)"
)


plt.title(
    "HART-120 — Dynamic GLA ML Surrogate Validation"
)


plt.grid(True)

plt.show()


# ============================================================
# 7. PERMUTATION FEATURE IMPORTANCE
#
# More useful than raw RF impurity importance because it
# measures how prediction quality deteriorates when each
# engineering variable is disturbed.
# ============================================================

importance_result = permutation_importance(

    root_reduction_model,

    X_test_dyn,

    root_reduction_actual,

    n_repeats=15,

    random_state=42,

    n_jobs=-1
)


importance_df = pd.DataFrame({

    "Feature":
        dynamic_features,

    "Importance":
        importance_result.importances_mean,

    "Std":
        importance_result.importances_std
})


importance_df = importance_df.sort_values(

    "Importance",

    ascending=False
)


print()
print(
    "HART-120 DYNAMIC GLA FEATURE IMPORTANCE"
)

print(
    "---------------------------------------"
)

print(

    importance_df
    .round(5)
    .to_string(index=False)
)


plt.figure(
    figsize=(9, 6)
)


plt.bar(

    importance_df["Feature"],

    importance_df["Importance"]
)


plt.ylabel(
    "Permutation Importance"
)


plt.title(
    "HART-120 — Drivers of Dynamic Gust Load Alleviation"
)


plt.xticks(
    rotation=25,
    ha="right"
)


plt.grid(
    True,
    axis="y"
)


plt.tight_layout()

plt.show()

# %% [notebook cell 101]
# ============================================================
# HART-120 — ML-ASSISTED DYNAMIC GLA ARCHITECTURE SEARCH
#
# Goal:
# Search a large controller / actuator design space using the
# trained ML surrogate.
#
# ML is used ONLY for screening.
# Final configurations must later be verified using the
# transient physics model.
# ============================================================

rng = np.random.default_rng(42)

n_search_cases = 100_000


# ------------------------------------------------------------
# 1. Generate candidate architectures
# ------------------------------------------------------------

search_df = pd.DataFrame({

    "Gust_H_m":
        rng.uniform(
            10.0,
            200.0,
            n_search_cases
        ),

    "Actuator_Time_Constant_s":
        rng.uniform(
            0.04,
            0.20,
            n_search_cases
        ),

    "Sensor_Delay_s":
        rng.uniform(
            0.00,
            0.08,
            n_search_cases
        ),

    "Rate_Limit_deg_s":
        rng.uniform(
            40.0,
            160.0,
            n_search_cases
        ),

    "Preview_Time_s":
        rng.uniform(
            0.00,
            0.15,
            n_search_cases
        )
})


# ------------------------------------------------------------
# 2. ML predictions
# ------------------------------------------------------------

search_df[
    "Predicted_Root_Moment_Reduction_%"
] = dynamic_regression_models[
    "Root_Moment_Reduction_%"
].predict(
    search_df[dynamic_features]
)


search_df[
    "Predicted_Peak_Root_Moment_MNm"
] = dynamic_regression_models[
    "Peak_Root_Moment_Controlled_MNm"
].predict(
    search_df[dynamic_features]
)


search_df[
    "Predicted_Root_Stress_MPa"
] = dynamic_regression_models[
    "Peak_Root_Stress_MPa"
].predict(
    search_df[dynamic_features]
)


search_df[
    "Predicted_Tip_Deflection_m"
] = dynamic_regression_models[
    "Peak_Tip_Deflection_Controlled_m"
].predict(
    search_df[dynamic_features]
)


search_df[
    "Predicted_Peak_Actuator_Deflection_deg"
] = dynamic_regression_models[
    "Peak_Actuator_Deflection_deg"
].predict(
    search_df[dynamic_features]
)


search_df[
    "Probability_Meets_10pct_Target"
] = gla_classifier.predict_proba(
    search_df[dynamic_features]
)[:, 1]


# ------------------------------------------------------------
# 3. Conservative ML screening
#
# Physical requirement = 10%
#
# ML screening requirement is deliberately higher because
# surrogate error and classifier false positives exist.
# ------------------------------------------------------------

ml_screening_target = 12.0

minimum_success_probability = 0.98

maximum_surface_deflection = 15.0


search_df[
    "ML_Robustly_Feasible"
] = (

    (
        search_df[
            "Predicted_Root_Moment_Reduction_%"
        ]
        >= ml_screening_target
    )

    &

    (
        search_df[
            "Probability_Meets_10pct_Target"
        ]
        >= minimum_success_probability
    )

    &

    (
        search_df[
            "Predicted_Peak_Actuator_Deflection_deg"
        ]
        <= maximum_surface_deflection
    )
)


robust_candidates = search_df[
    search_df["ML_Robustly_Feasible"]
].copy()


print(
    "HART-120 ML DYNAMIC GLA DESIGN SEARCH"
)

print(
    "-------------------------------------"
)

print(
    f"Designs searched: "
    f"{len(search_df):,}"
)

print(
    f"Robust ML-feasible designs: "
    f"{len(robust_candidates):,}"
)

print(
    f"Fraction feasible: "
    f"{100*len(robust_candidates)/len(search_df):.2f} %"
)


# ============================================================
# 4. Architecture burden metric
#
# We do NOT simply maximize load reduction.
#
# Lower score means a less demanding control architecture:
#
# - slower actuator is preferred
# - lower rate capability is preferred
# - less gust preview is preferred
# - larger tolerable sensor delay is preferred
#
# while still meeting the load requirement.
# ============================================================

if len(robust_candidates) > 0:

    tau_min = search_df[
        "Actuator_Time_Constant_s"
    ].min()

    tau_max = search_df[
        "Actuator_Time_Constant_s"
    ].max()


    rate_min = search_df[
        "Rate_Limit_deg_s"
    ].min()

    rate_max = search_df[
        "Rate_Limit_deg_s"
    ].max()


    preview_min = search_df[
        "Preview_Time_s"
    ].min()

    preview_max = search_df[
        "Preview_Time_s"
    ].max()


    delay_min = search_df[
        "Sensor_Delay_s"
    ].min()

    delay_max = search_df[
        "Sensor_Delay_s"
    ].max()


    # Faster actuator = greater burden
    actuator_speed_burden = (
        tau_max
        - robust_candidates[
            "Actuator_Time_Constant_s"
        ]
    ) / (
        tau_max - tau_min
    )


    # Higher rate capability = greater burden
    actuator_rate_burden = (
        robust_candidates[
            "Rate_Limit_deg_s"
        ]
        - rate_min
    ) / (
        rate_max - rate_min
    )


    # More preview = more demanding sensing requirement
    preview_burden = (
        robust_candidates[
            "Preview_Time_s"
        ]
        - preview_min
    ) / (
        preview_max - preview_min
    )


    # Smaller allowed delay = more demanding electronics /
    # sensing / processing requirement
    delay_burden = (
        delay_max
        - robust_candidates[
            "Sensor_Delay_s"
        ]
    ) / (
        delay_max - delay_min
    )


    # Equal preliminary weighting.
    #
    # These are project-level architecture weights,
    # not industrial procurement costs.
    robust_candidates[
        "Architecture_Burden"
    ] = (

        0.30 * actuator_speed_burden

        + 0.20 * actuator_rate_burden

        + 0.30 * preview_burden

        + 0.20 * delay_burden
    )


    robust_candidates = robust_candidates.sort_values(
        "Architecture_Burden"
    )


    best_architecture = (
        robust_candidates.iloc[0]
    )


    print()
    print(
        "LOWEST-BURDEN ROBUST ML ARCHITECTURE"
    )

    print(
        "------------------------------------"
    )

    print(
        f"Gust gradient: "
        f"{best_architecture['Gust_H_m']:.2f} m"
    )

    print(
        f"Actuator time constant: "
        f"{best_architecture['Actuator_Time_Constant_s']:.4f} s"
    )

    print(
        f"Sensor/control delay: "
        f"{best_architecture['Sensor_Delay_s']:.4f} s"
    )

    print(
        f"Rate capability: "
        f"{best_architecture['Rate_Limit_deg_s']:.2f} deg/s"
    )

    print(
        f"Preview time: "
        f"{best_architecture['Preview_Time_s']:.4f} s"
    )

    print(
        f"Predicted root-moment reduction: "
        f"{best_architecture['Predicted_Root_Moment_Reduction_%']:.2f} %"
    )

    print(
        f"Predicted peak root moment: "
        f"{best_architecture['Predicted_Peak_Root_Moment_MNm']:.3f} MN·m"
    )

    print(
        f"Predicted peak root stress: "
        f"{best_architecture['Predicted_Root_Stress_MPa']:.2f} MPa"
    )

    print(
        f"Predicted peak tip deflection: "
        f"{best_architecture['Predicted_Tip_Deflection_m']:.3f} m"
    )

    print(
        f"Predicted actuator deflection: "
        f"{best_architecture['Predicted_Peak_Actuator_Deflection_deg']:.2f} deg"
    )

    print(
        f"Classifier success probability: "
        f"{100*best_architecture['Probability_Meets_10pct_Target']:.2f} %"
    )

    print(
        f"Architecture burden index: "
        f"{best_architecture['Architecture_Burden']:.4f}"
    )


# ============================================================
# 5. Show top candidate architectures
# ============================================================

candidate_columns = [

    "Gust_H_m",

    "Actuator_Time_Constant_s",

    "Sensor_Delay_s",

    "Rate_Limit_deg_s",

    "Preview_Time_s",

    "Predicted_Root_Moment_Reduction_%",

    "Predicted_Peak_Actuator_Deflection_deg",

    "Probability_Meets_10pct_Target",

    "Architecture_Burden"
]


top_architectures = (

    robust_candidates[
        candidate_columns
    ]
    .head(15)
    .copy()
)


print()
print(
    "TOP 15 ML-SCREENED GLA ARCHITECTURES"
)

print(
    "------------------------------------"
)

print(
    top_architectures
    .round(4)
    .to_string(index=False)
)

# %% [notebook cell 102]
# ============================================================
# HART-120 — ROBUST MULTI-GUST ML CONTROL-ARCHITECTURE SEARCH
#
# IMPORTANT:
# Gust gradient H is now an ENVIRONMENTAL CONDITION,
# not a controller design variable.
#
# One controller architecture is tested across the complete
# gust-gradient envelope.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Gust design envelope
# ------------------------------------------------------------

gust_design_grid = np.arange(
    10.0,
    201.0,
    10.0
)

n_gust_cases = len(gust_design_grid)


# ------------------------------------------------------------
# 2. Generate controller architectures
# ------------------------------------------------------------

rng = np.random.default_rng(84)

n_architectures = 10000


architecture_df = pd.DataFrame({

    "Architecture_ID":
        np.arange(n_architectures),

    "Actuator_Time_Constant_s":
        rng.uniform(
            0.04,
            0.20,
            n_architectures
        ),

    "Sensor_Delay_s":
        rng.uniform(
            0.00,
            0.08,
            n_architectures
        ),

    "Rate_Limit_deg_s":
        rng.uniform(
            40.0,
            160.0,
            n_architectures
        ),

    "Preview_Time_s":
        rng.uniform(
            0.00,
            0.15,
            n_architectures
        )
})


# ------------------------------------------------------------
# 3. Expand each architecture across every gust gradient
# ------------------------------------------------------------

robust_search_df = pd.DataFrame({

    "Architecture_ID":
        np.repeat(
            architecture_df["Architecture_ID"].values,
            n_gust_cases
        ),

    "Gust_H_m":
        np.tile(
            gust_design_grid,
            n_architectures
        ),

    "Actuator_Time_Constant_s":
        np.repeat(
            architecture_df[
                "Actuator_Time_Constant_s"
            ].values,
            n_gust_cases
        ),

    "Sensor_Delay_s":
        np.repeat(
            architecture_df[
                "Sensor_Delay_s"
            ].values,
            n_gust_cases
        ),

    "Rate_Limit_deg_s":
        np.repeat(
            architecture_df[
                "Rate_Limit_deg_s"
            ].values,
            n_gust_cases
        ),

    "Preview_Time_s":
        np.repeat(
            architecture_df[
                "Preview_Time_s"
            ].values,
            n_gust_cases
        )
})


print(
    f"Controller architectures: "
    f"{n_architectures:,}"
)

print(
    f"Gust gradients per architecture: "
    f"{n_gust_cases}"
)

print(
    f"Total ML evaluations: "
    f"{len(robust_search_df):,}"
)


# ------------------------------------------------------------
# 4. ML surrogate evaluation
# ------------------------------------------------------------

robust_search_df[
    "Predicted_Controlled_Root_Moment_MNm"
] = dynamic_regression_models[
    "Peak_Root_Moment_Controlled_MNm"
].predict(
    robust_search_df[
        dynamic_features
    ]
)


robust_search_df[
    "Predicted_Root_Moment_Reduction_%"
] = dynamic_regression_models[
    "Root_Moment_Reduction_%"
].predict(
    robust_search_df[
        dynamic_features
    ]
)


robust_search_df[
    "Predicted_Root_Stress_MPa"
] = dynamic_regression_models[
    "Peak_Root_Stress_MPa"
].predict(
    robust_search_df[
        dynamic_features
    ]
)


robust_search_df[
    "Predicted_Tip_Deflection_m"
] = dynamic_regression_models[
    "Peak_Tip_Deflection_Controlled_m"
].predict(
    robust_search_df[
        dynamic_features
    ]
)


robust_search_df[
    "Predicted_Actuator_Deflection_deg"
] = dynamic_regression_models[
    "Peak_Actuator_Deflection_deg"
].predict(
    robust_search_df[
        dynamic_features
    ]
)


# ------------------------------------------------------------
# 5. Collapse complete gust envelope into one result
#    per controller architecture
# ------------------------------------------------------------

grouped = robust_search_df.groupby(
    "Architecture_ID"
)


robust_results = architecture_df.copy()


robust_results[
    "Worst_Controlled_Root_Moment_MNm"
] = grouped[
    "Predicted_Controlled_Root_Moment_MNm"
].max().values


robust_results[
    "Maximum_Root_Stress_MPa"
] = grouped[
    "Predicted_Root_Stress_MPa"
].max().values


robust_results[
    "Maximum_Tip_Deflection_m"
] = grouped[
    "Predicted_Tip_Deflection_m"
].max().values


robust_results[
    "Maximum_Actuator_Deflection_deg"
] = grouped[
    "Predicted_Actuator_Deflection_deg"
].max().values


robust_results[
    "Minimum_Root_Moment_Reduction_%"
] = grouped[
    "Predicted_Root_Moment_Reduction_%"
].min().values


# ------------------------------------------------------------
# 6. Gust gradient producing worst controlled load
# ------------------------------------------------------------

worst_indices = grouped[
    "Predicted_Controlled_Root_Moment_MNm"
].idxmax()


robust_results[
    "Worst_Case_Gust_H_m"
] = robust_search_df.loc[
    worst_indices.values,
    "Gust_H_m"
].values


# ------------------------------------------------------------
# 7. Robust design requirement
#
# Physics target:
#     10% reduction of uncontrolled envelope peak
#
# ML screening target:
#     12% reduction
#
# Extra margin protects against surrogate error.
# ------------------------------------------------------------

uncontrolled_envelope_peak_MNm = 4.143

physical_target_reduction = 0.10

ml_screening_reduction = 0.12


physical_controlled_limit_MNm = (
    uncontrolled_envelope_peak_MNm
    *
    (
        1.0
        - physical_target_reduction
    )
)


ml_screening_limit_MNm = (
    uncontrolled_envelope_peak_MNm
    *
    (
        1.0
        - ml_screening_reduction
    )
)


maximum_surface_deflection_deg = 15.0


robust_results[
    "Robustly_Feasible"
] = (

    (
        robust_results[
            "Worst_Controlled_Root_Moment_MNm"
        ]
        <= ml_screening_limit_MNm
    )

    &

    (
        robust_results[
            "Maximum_Actuator_Deflection_deg"
        ]
        <= maximum_surface_deflection_deg
    )
)


robust_feasible = robust_results[
    robust_results[
        "Robustly_Feasible"
    ]
].copy()


print()
print(
    "HART-120 ROBUST GUST-ENVELOPE SCREENING"
)

print(
    "---------------------------------------"
)

print(
    f"Uncontrolled envelope peak: "
    f"{uncontrolled_envelope_peak_MNm:.3f} MN·m"
)

print(
    f"Physical 10% controlled-load limit: "
    f"{physical_controlled_limit_MNm:.3f} MN·m"
)

print(
    f"Conservative ML screening limit: "
    f"{ml_screening_limit_MNm:.3f} MN·m"
)

print(
    f"Robust feasible architectures: "
    f"{len(robust_feasible):,} / "
    f"{n_architectures:,}"
)


# ============================================================
# 8. Architecture burden
#
# Lower value = easier / less demanding implementation.
#
# Slow actuator preferred.
# Lower rate capability preferred.
# Less preview preferred.
# Greater allowable delay preferred.
# ============================================================

if len(robust_feasible) > 0:

    tau_min = 0.04
    tau_max = 0.20

    rate_min = 40.0
    rate_max = 160.0

    preview_min = 0.00
    preview_max = 0.15

    delay_min = 0.00
    delay_max = 0.08


    actuator_speed_burden = (

        tau_max

        - robust_feasible[
            "Actuator_Time_Constant_s"
        ]

    ) / (

        tau_max - tau_min

    )


    actuator_rate_burden = (

        robust_feasible[
            "Rate_Limit_deg_s"
        ]

        - rate_min

    ) / (

        rate_max - rate_min

    )


    preview_burden = (

        robust_feasible[
            "Preview_Time_s"
        ]

        - preview_min

    ) / (

        preview_max - preview_min

    )


    delay_burden = (

        delay_max

        - robust_feasible[
            "Sensor_Delay_s"
        ]

    ) / (

        delay_max - delay_min

    )


    robust_feasible[
        "Architecture_Burden"
    ] = (

        0.30 * actuator_speed_burden

        + 0.20 * actuator_rate_burden

        + 0.30 * preview_burden

        + 0.20 * delay_burden
    )


    robust_feasible = robust_feasible.sort_values(
        "Architecture_Burden"
    )


    best_robust_architecture = (
        robust_feasible.iloc[0]
    )


    print()
    print(
        "LOWEST-BURDEN ROBUST CONTROLLER"
    )

    print(
        "-------------------------------"
    )

    print(
        f"Actuator time constant: "
        f"{best_robust_architecture['Actuator_Time_Constant_s']:.4f} s"
    )

    print(
        f"Sensor delay: "
        f"{best_robust_architecture['Sensor_Delay_s']:.4f} s"
    )

    print(
        f"Rate capability: "
        f"{best_robust_architecture['Rate_Limit_deg_s']:.2f} deg/s"
    )

    print(
        f"Preview time: "
        f"{best_robust_architecture['Preview_Time_s']:.4f} s"
    )

    print(
        f"Worst predicted controlled root moment: "
        f"{best_robust_architecture['Worst_Controlled_Root_Moment_MNm']:.3f} MN·m"
    )

    print(
        f"Worst-case gust gradient: "
        f"{best_robust_architecture['Worst_Case_Gust_H_m']:.1f} m"
    )

    print(
        f"Maximum predicted root stress: "
        f"{best_robust_architecture['Maximum_Root_Stress_MPa']:.2f} MPa"
    )

    print(
        f"Maximum predicted tip deflection: "
        f"{best_robust_architecture['Maximum_Tip_Deflection_m']:.3f} m"
    )

    print(
        f"Maximum actuator deflection: "
        f"{best_robust_architecture['Maximum_Actuator_Deflection_deg']:.2f} deg"
    )

    print(
        f"Architecture burden: "
        f"{best_robust_architecture['Architecture_Burden']:.4f}"
    )


# ============================================================
# 9. Top robust designs
# ============================================================

display_columns = [

    "Actuator_Time_Constant_s",

    "Sensor_Delay_s",

    "Rate_Limit_deg_s",

    "Preview_Time_s",

    "Worst_Case_Gust_H_m",

    "Worst_Controlled_Root_Moment_MNm",

    "Maximum_Root_Stress_MPa",

    "Maximum_Tip_Deflection_m",

    "Maximum_Actuator_Deflection_deg",

    "Architecture_Burden"
]


print()
print(
    "TOP 15 ROBUST ML-SCREENED ARCHITECTURES"
)

print(
    "---------------------------------------"
)

print(
    robust_feasible[
        display_columns
    ]
    .head(15)
    .round(4)
    .to_string(index=False)
)


# ============================================================
# 10. Plot the complete gust envelope for selected controller
# ============================================================

if len(robust_feasible) > 0:

    best_id = int(
        best_robust_architecture[
            "Architecture_ID"
        ]
    )


    best_envelope = robust_search_df[
        robust_search_df[
            "Architecture_ID"
        ]
        == best_id
    ].copy()


    plt.figure(
        figsize=(9, 5.5)
    )


    plt.plot(

        best_envelope[
            "Gust_H_m"
        ],

        best_envelope[
            "Predicted_Controlled_Root_Moment_MNm"
        ],

        marker="o",

        label="ML-predicted controlled envelope"
    )


    plt.axhline(

        physical_controlled_limit_MNm,

        linestyle="--",

        label="Physical 10% target"
    )


    plt.axhline(

        ml_screening_limit_MNm,

        linestyle=":",

        label="Conservative ML screening limit"
    )


    plt.xlabel(
        "Gust Gradient H (m)"
    )

    plt.ylabel(
        "Peak Controlled Root Bending Moment (MN·m)"
    )

    plt.title(
        "HART-120 — Robust ML-Screened Gust-Load Envelope"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.show()

# %% [notebook cell 103]
# ============================================================
# HART-120 — FULL-PHYSICS VERIFICATION OF ML-SCREENED
# ROBUST GLA ARCHITECTURES
#
# Purpose:
# ML has screened thousands of architectures.
# We now return the top candidates to the original
# transient aero-structural model for verification.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Verification settings
# ------------------------------------------------------------

physics_gust_grid = np.arange(
    10.0,
    201.0,
    10.0
)

physical_controlled_limit_MNm = (
    4.143 * 0.90
)

maximum_surface_deflection_deg = 15.0

pre_gust_time = 0.15
post_gust_time = 2.0


# ------------------------------------------------------------
# 2. Generalized-force constants
# ------------------------------------------------------------

Q_gust_peak_verify = np.trapezoid(
    delta_lift_per_span_gust * phi,
    y
)

Q_control_full_verify = np.trapezoid(
    delta_lift_gla_full * phi,
    y
)


# ------------------------------------------------------------
# 3. Exact transient physics function
# ------------------------------------------------------------

def verify_controller_physics(
    H,
    actuator_tau,
    sensor_delay,
    rate_limit,
    preview_time
):

    # --------------------------------------------------------
    # Gust duration and simulation time
    # --------------------------------------------------------

    gust_duration = (
        2.0 * H / V_cruise
    )

    time_verify = np.arange(
        -pre_gust_time,
        gust_duration
        + post_gust_time
        + dt,
        dt
    )


    # --------------------------------------------------------
    # Actual gust at aircraft
    # --------------------------------------------------------

    gust_scale_verify = gust_scale_at_time(
        time_verify,
        H
    )

    Q_uncontrolled_verify = (
        gust_scale_verify
        * Q_gust_peak_verify
    )


    # --------------------------------------------------------
    # Uncontrolled structural response
    # --------------------------------------------------------

    (
        q_u,
        qdot_u,
        qddot_u

    ) = newmark_beta_response(

        Q_uncontrolled_verify,

        modal_mass,
        modal_damping,
        modal_stiffness,
        dt
    )


    root_moment_u = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_u
        * root_moment_response_scale
    )


    tip_u = (

        tip_deflection_mass_reduced

        + q_u
        * tip_response_scale
    )


    peak_root_u = np.max(
        root_moment_u
    )

    peak_tip_u = np.max(
        tip_u
    )


    # --------------------------------------------------------
    # Forward gust sensing
    #
    # Sensor at time t estimates gust arriving at:
    #
    #       t + preview_time
    # --------------------------------------------------------

    sensed_gust_scale = gust_scale_at_time(
        time_verify + preview_time,
        H
    )


    command_raw = (

        best_gust_required_deflection

        * sensed_gust_scale
    )


    command_raw = np.clip(

        command_raw,

        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Sensor / processing delay
    # --------------------------------------------------------

    command_query_time = (

        time_verify

        - sensor_delay
    )


    delayed_command = np.interp(

        command_query_time,

        time_verify,

        command_raw,

        left=0.0,
        right=0.0
    )


    # --------------------------------------------------------
    # Actuator dynamics
    # --------------------------------------------------------

    actuator = np.zeros_like(
        time_verify
    )


    for k in range(
        1,
        len(time_verify)
    ):

        desired_rate = (

            delayed_command[k]

            - actuator[k - 1]

        ) / actuator_tau


        actual_rate = np.clip(

            desired_rate,

            -rate_limit,
            rate_limit
        )


        actuator[k] = (

            actuator[k - 1]

            + actual_rate * dt
        )


        actuator[k] = np.clip(

            actuator[k],

            -max_deflection_deg,
            max_deflection_deg
        )


    # --------------------------------------------------------
    # Aerodynamic control authority
    # --------------------------------------------------------

    control_scale = (

        actuator

        / best_gust_required_deflection
    )


    Q_controlled_verify = (

        Q_uncontrolled_verify

        + control_scale
        * Q_control_full_verify
    )


    # --------------------------------------------------------
    # Controlled structural dynamics
    # --------------------------------------------------------

    (
        q_c,
        qdot_c,
        qddot_c

    ) = newmark_beta_response(

        Q_controlled_verify,

        modal_mass,
        modal_damping,
        modal_stiffness,
        dt
    )


    # --------------------------------------------------------
    # Controlled root bending moment
    # --------------------------------------------------------

    root_moment_c = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_c
        * root_moment_response_scale
    )


    # --------------------------------------------------------
    # Controlled tip response
    # --------------------------------------------------------

    tip_c = (

        tip_deflection_mass_reduced

        + q_c
        * tip_response_scale
    )


    # --------------------------------------------------------
    # Root spar-cap stress
    # --------------------------------------------------------

    root_stress_c = (

        root_moment_c

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Peak / minimum quantities
    # --------------------------------------------------------

    peak_root_c = np.max(
        root_moment_c
    )

    minimum_root_c = np.min(
        root_moment_c
    )

    peak_tip_c = np.max(
        tip_c
    )

    peak_stress_c = np.max(
        root_stress_c
    )

    peak_actuator = np.max(
        np.abs(actuator)
    )


    # --------------------------------------------------------
    # Performance
    # --------------------------------------------------------

    root_reduction = (

        (
            peak_root_u
            - peak_root_c
        )

        / peak_root_u

    ) * 100.0


    tip_reduction = (

        (
            peak_tip_u
            - peak_tip_c
        )

        / peak_tip_u

    ) * 100.0


    return {

        "Gust_H_m":
            H,

        "Gust_Duration_s":
            gust_duration,

        "Peak_Root_Moment_Uncontrolled_MNm":
            peak_root_u / 1e6,

        "Peak_Root_Moment_Controlled_MNm":
            peak_root_c / 1e6,

        "Minimum_Root_Moment_Controlled_MNm":
            minimum_root_c / 1e6,

        "Root_Moment_Reduction_%":
            root_reduction,

        "Peak_Root_Stress_MPa":
            peak_stress_c / 1e6,

        "Peak_Tip_Uncontrolled_m":
            peak_tip_u,

        "Peak_Tip_Controlled_m":
            peak_tip_c,

        "Tip_Deflection_Reduction_%":
            tip_reduction,

        "Peak_Actuator_Deflection_deg":
            peak_actuator
    }


# ============================================================
# 4. Verify TOP 15 ML-screened architectures
# ============================================================

candidate_architectures = (

    robust_feasible

    .head(15)

    .copy()
)


physics_candidate_results = []

physics_envelopes = {}


for candidate_number, (
    candidate_index,
    candidate
) in enumerate(
    candidate_architectures.iterrows(),
    start=1
):

    tau_candidate = float(
        candidate[
            "Actuator_Time_Constant_s"
        ]
    )

    delay_candidate = float(
        candidate[
            "Sensor_Delay_s"
        ]
    )

    rate_candidate = float(
        candidate[
            "Rate_Limit_deg_s"
        ]
    )

    preview_candidate = float(
        candidate[
            "Preview_Time_s"
        ]
    )


    envelope_rows = []


    for H in physics_gust_grid:

        result = verify_controller_physics(

            H=H,

            actuator_tau=tau_candidate,

            sensor_delay=delay_candidate,

            rate_limit=rate_candidate,

            preview_time=preview_candidate
        )

        envelope_rows.append(
            result
        )


    envelope_df = pd.DataFrame(
        envelope_rows
    )


    physics_envelopes[
        candidate_number
    ] = envelope_df


    # --------------------------------------------------------
    # Governing physical gust
    # --------------------------------------------------------

    worst_index = envelope_df[
        "Peak_Root_Moment_Controlled_MNm"
    ].idxmax()


    worst_case = envelope_df.loc[
        worst_index
    ]


    worst_controlled_moment = float(
        worst_case[
            "Peak_Root_Moment_Controlled_MNm"
        ]
    )


    maximum_actuator = float(
        envelope_df[
            "Peak_Actuator_Deflection_deg"
        ].max()
    )


    maximum_stress = float(
        envelope_df[
            "Peak_Root_Stress_MPa"
        ].max()
    )


    maximum_tip = float(
        envelope_df[
            "Peak_Tip_Controlled_m"
        ].max()
    )


    minimum_root_moment = float(
        envelope_df[
            "Minimum_Root_Moment_Controlled_MNm"
        ].min()
    )


    physical_pass = (

        (
            worst_controlled_moment
            <= physical_controlled_limit_MNm
        )

        and

        (
            maximum_actuator
            <= maximum_surface_deflection_deg
        )
    )


    physics_candidate_results.append({

        "Candidate":
            candidate_number,

        "Actuator_Time_Constant_s":
            tau_candidate,

        "Sensor_Delay_s":
            delay_candidate,

        "Rate_Limit_deg_s":
            rate_candidate,

        "Preview_Time_s":
            preview_candidate,

        "Effective_Lead_s":
            preview_candidate
            - delay_candidate,

        "ML_Architecture_Burden":
            candidate[
                "Architecture_Burden"
            ],

        "Physics_Worst_Gust_H_m":
            worst_case[
                "Gust_H_m"
            ],

        "Physics_Worst_Controlled_Moment_MNm":
            worst_controlled_moment,

        "Physics_Root_Moment_Reduction_at_Worst_%":
            worst_case[
                "Root_Moment_Reduction_%"
            ],

        "Physics_Max_Root_Stress_MPa":
            maximum_stress,

        "Physics_Max_Tip_Deflection_m":
            maximum_tip,

        "Physics_Max_Actuator_Deflection_deg":
            maximum_actuator,

        "Physics_Minimum_Root_Moment_MNm":
            minimum_root_moment,

        "Passes_Physics_Target":
            physical_pass
    })


physics_verification_df = pd.DataFrame(
    physics_candidate_results
)


# ============================================================
# 5. Results
# ============================================================

print()
print(
    "HART-120 — FULL-PHYSICS VERIFICATION OF ML FINALISTS"
)

print(
    "-----------------------------------------------------"
)

print(
    f"Candidates physics-verified: "
    f"{len(physics_verification_df)}"
)

print(
    f"Physical controlled-load limit: "
    f"{physical_controlled_limit_MNm:.3f} MN·m"
)

print(
    f"Surface-deflection limit: "
    f"{maximum_surface_deflection_deg:.1f} deg"
)


print()
print(
    physics_verification_df
    .round(4)
    .to_string(index=False)
)


# ============================================================
# 6. Find lowest-burden candidate that survives physics
# ============================================================

physics_feasible_df = (

    physics_verification_df[

        physics_verification_df[
            "Passes_Physics_Target"
        ]

    ]

    .sort_values(
        "ML_Architecture_Burden"
    )
)


print()
print(
    "PHYSICS-VERIFIED ROBUST CONTROLLERS"
)

print(
    "-----------------------------------"
)


if len(
    physics_feasible_df
) == 0:

    print(
        "No ML finalist passed the full transient physics check."
    )

else:

    print(
        f"Physics-feasible finalists: "
        f"{len(physics_feasible_df)} / "
        f"{len(physics_verification_df)}"
    )


    final_controller = (
        physics_feasible_df.iloc[0]
    )


    print()
    print(
        "FINAL LOWEST-BURDEN PHYSICS-VERIFIED CONTROLLER"
    )

    print(
        "-----------------------------------------------"
    )


    print(
        f"Actuator time constant: "
        f"{final_controller['Actuator_Time_Constant_s']:.4f} s"
    )

    print(
        f"Sensor/control delay: "
        f"{final_controller['Sensor_Delay_s']:.4f} s"
    )

    print(
        f"Rate capability: "
        f"{final_controller['Rate_Limit_deg_s']:.2f} deg/s"
    )

    print(
        f"Preview time: "
        f"{final_controller['Preview_Time_s']:.4f} s"
    )

    print(
        f"Effective lead: "
        f"{final_controller['Effective_Lead_s']:.4f} s"
    )

    print(
        f"Critical physics gust: "
        f"{final_controller['Physics_Worst_Gust_H_m']:.1f} m"
    )

    print(
        f"Worst controlled root moment: "
        f"{final_controller['Physics_Worst_Controlled_Moment_MNm']:.3f} MN·m"
    )

    print(
        f"Moment reduction at critical gust: "
        f"{final_controller['Physics_Root_Moment_Reduction_at_Worst_%']:.2f} %"
    )

    print(
        f"Maximum root stress: "
        f"{final_controller['Physics_Max_Root_Stress_MPa']:.2f} MPa"
    )

    print(
        f"Maximum tip deflection: "
        f"{final_controller['Physics_Max_Tip_Deflection_m']:.3f} m"
    )

    print(
        f"Maximum actuator deflection: "
        f"{final_controller['Physics_Max_Actuator_Deflection_deg']:.2f} deg"
    )

    print(
        f"Minimum root moment: "
        f"{final_controller['Physics_Minimum_Root_Moment_MNm']:.3f} MN·m"
    )


# ============================================================
# 7. Plot final physics-verified envelope
# ============================================================

if len(
    physics_feasible_df
) > 0:

    final_candidate_number = int(
        final_controller[
            "Candidate"
        ]
    )


    final_physics_envelope = (

        physics_envelopes[
            final_candidate_number
        ]
    )


    plt.figure(
        figsize=(9, 5.5)
    )


    plt.plot(

        final_physics_envelope[
            "Gust_H_m"
        ],

        final_physics_envelope[
            "Peak_Root_Moment_Uncontrolled_MNm"
        ],

        marker="o",

        label="Uncontrolled physics"
    )


    plt.plot(

        final_physics_envelope[
            "Gust_H_m"
        ],

        final_physics_envelope[
            "Peak_Root_Moment_Controlled_MNm"
        ],

        marker="o",

        label="Controlled physics"
    )


    plt.axhline(

        physical_controlled_limit_MNm,

        linestyle="--",

        label="10% envelope target"
    )


    plt.xlabel(
        "Gust Gradient H (m)"
    )

    plt.ylabel(
        "Peak Root Bending Moment (MN·m)"
    )

    plt.title(
        "HART-120 — Physics-Verified Robust GLA Envelope"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.show()


# ============================================================
# 8. ML vs physics comparison for selected controller
# ============================================================

if len(
    physics_feasible_df
) > 0:

    selected_candidate_original_index = (
        candidate_architectures.index[
            final_candidate_number - 1
        ]
    )


    selected_architecture_id = int(

        candidate_architectures.loc[
            selected_candidate_original_index,
            "Architecture_ID"
        ]
    )


    selected_ml_envelope = (

        robust_search_df[

            robust_search_df[
                "Architecture_ID"
            ]

            == selected_architecture_id

        ][
            [
                "Gust_H_m",
                "Predicted_Controlled_Root_Moment_MNm"
            ]
        ]

        .copy()
    )


    comparison_df = pd.merge(

        final_physics_envelope[
            [
                "Gust_H_m",
                "Peak_Root_Moment_Controlled_MNm"
            ]
        ],

        selected_ml_envelope,

        on="Gust_H_m",

        how="left"
    )


    comparison_df[
        "ML_Error_MNm"
    ] = (

        comparison_df[
            "Predicted_Controlled_Root_Moment_MNm"
        ]

        - comparison_df[
            "Peak_Root_Moment_Controlled_MNm"
        ]
    )


    comparison_df[
        "Absolute_ML_Error_MNm"
    ] = np.abs(

        comparison_df[
            "ML_Error_MNm"
        ]
    )


    print()
    print(
        "FINAL CONTROLLER — ML VS PHYSICS"
    )

    print(
        "--------------------------------"
    )

    print(
        comparison_df
        .round(4)
        .to_string(index=False)
    )


    print()
    print(
        f"Envelope MAE: "
        f"{comparison_df['Absolute_ML_Error_MNm'].mean():.4f} MN·m"
    )


    plt.figure(
        figsize=(9, 5.5)
    )


    plt.plot(

        comparison_df[
            "Gust_H_m"
        ],

        comparison_df[
            "Peak_Root_Moment_Controlled_MNm"
        ],

        marker="o",

        label="Full transient physics"
    )


    plt.plot(

        comparison_df[
            "Gust_H_m"
        ],

        comparison_df[
            "Predicted_Controlled_Root_Moment_MNm"
        ],

        marker="s",

        linestyle="--",

        label="ML surrogate"
    )


    plt.xlabel(
        "Gust Gradient H (m)"
    )

    plt.ylabel(
        "Peak Controlled Root Moment (MN·m)"
    )

    plt.title(
        "HART-120 — ML Screening vs Full-Physics Verification"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.show()

# %% [notebook cell 104]
# ============================================================
# HART-120 — ROBUSTNESS / UNCERTAINTY ANALYSIS
#
# Industrial question:
# Does the selected physics-verified GLA controller remain
# acceptable when the aeroelastic model, gust and actuator
# properties differ from their nominal assumptions?
#
# Reduced-order conceptual uncertainty study.
# NOT a certification-level probabilistic analysis.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Selected physics-verified controller
# ------------------------------------------------------------

selected_tau = 0.1923          # s
selected_delay = 0.0717        # s
selected_rate = 44.4053        # deg/s
selected_preview = 0.0601      # s


# ------------------------------------------------------------
# 2. Nominal uncontrolled envelope and design target
# ------------------------------------------------------------

nominal_uncontrolled_envelope = (
    gust_gradient_df[
        "Peak_Root_Moment_Uncontrolled_MNm"
    ].max()
)

physical_target_MNm = (
    0.90
    * nominal_uncontrolled_envelope
)

physical_target_Nm = (
    physical_target_MNm
    * 1e6
)


# ------------------------------------------------------------
# 3. Gust-gradient envelope
# ------------------------------------------------------------

H_robust_values = np.arange(
    10.0,
    201.0,
    10.0
)


# ------------------------------------------------------------
# 4. Project-level uncertainty assumptions
#
# These are conceptual uncertainty bounds,
# not certification tolerances.
# ------------------------------------------------------------

n_uncertainty_cases = 300

rng = np.random.default_rng(
    120
)


# Structural damping:
# nominal = 3%, ±20%
damping_samples = rng.uniform(
    0.024,
    0.036,
    n_uncertainty_cases
)


# First bending natural frequency:
# ±5% around nominal
frequency_scale_samples = rng.uniform(
    0.95,
    1.05,
    n_uncertainty_cases
)


# Gust amplitude:
# ±10%
gust_amplitude_scale_samples = rng.uniform(
    0.90,
    1.10,
    n_uncertainty_cases
)


# Aerodynamic control effectiveness:
# ±10%
control_effectiveness_scale_samples = rng.uniform(
    0.90,
    1.10,
    n_uncertainty_cases
)


# Actuator time constant:
# ±10%
tau_scale_samples = rng.uniform(
    0.90,
    1.10,
    n_uncertainty_cases
)


# Sensor / processing timing uncertainty:
# ±5 ms
delay_error_samples = rng.uniform(
    -0.005,
    0.005,
    n_uncertainty_cases
)


# Actuator rate capability:
# ±10%
rate_scale_samples = rng.uniform(
    0.90,
    1.10,
    n_uncertainty_cases
)


# Preview timing / gust-estimation error:
# ±10 ms
preview_error_samples = rng.uniform(
    -0.010,
    0.010,
    n_uncertainty_cases
)


# ------------------------------------------------------------
# 5. Nominal generalized aerodynamic forces
# ------------------------------------------------------------

Q_gust_peak_robust = np.trapezoid(
    delta_lift_per_span_gust
    * phi,
    y
)

Q_control_full_robust = np.trapezoid(
    delta_lift_gla_full
    * phi,
    y
)


# ------------------------------------------------------------
# 6. Local gust function
# ------------------------------------------------------------

def robust_gust_scale(
    time_array,
    H
):

    scale = np.zeros_like(
        time_array
    )

    active = (
        (time_array >= 0.0)
        &
        (
            time_array
            <= 2 * H / V_cruise
        )
    )

    distance = (
        V_cruise
        * time_array[active]
    )

    scale[active] = (
        0.5
        * (
            1.0
            - np.cos(
                np.pi
                * distance
                / H
            )
        )
    )

    return scale


# ------------------------------------------------------------
# 7. Run one uncertain controller / gust case
# ------------------------------------------------------------

def simulate_uncertain_gust_case(
    H,
    damping_ratio_sample,
    frequency_scale,
    gust_amplitude_scale,
    control_effectiveness_scale,
    tau_sample,
    delay_sample,
    rate_sample,
    preview_sample
):

    gust_duration = (
        2 * H
        / V_cruise
    )

    # Begin before gust arrival so preview control
    # can pre-actuate the surface.
    time_case = np.arange(
        -0.20,
        gust_duration
        + 2.0
        + dt,
        dt
    )


    # --------------------------------------------------------
    # Actual gust at wing
    # --------------------------------------------------------

    gust_shape = robust_gust_scale(
        time_case,
        H
    )

    actual_gust_scale = (
        gust_amplitude_scale
        * gust_shape
    )


    # --------------------------------------------------------
    # Forward-looking gust measurement
    # --------------------------------------------------------

    sensed_shape = robust_gust_scale(
        time_case
        + preview_sample,
        H
    )

    sensed_gust_scale = (
        gust_amplitude_scale
        * sensed_shape
    )


    # --------------------------------------------------------
    # Controller command
    # --------------------------------------------------------

    command_raw = (
        best_gust_required_deflection
        * sensed_gust_scale
    )

    command_raw = np.clip(
        command_raw,
        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Sensor / processing delay
    # --------------------------------------------------------

    delayed_command = np.interp(
        time_case
        - delay_sample,
        time_case,
        command_raw,
        left=0.0,
        right=0.0
    )


    # --------------------------------------------------------
    # Actuator dynamics
    # --------------------------------------------------------

    actuator = np.zeros_like(
        time_case
    )

    for k in range(
        1,
        len(time_case)
    ):

        desired_rate = (
            delayed_command[k]
            - actuator[k-1]
        ) / tau_sample

        limited_rate = np.clip(
            desired_rate,
            -rate_sample,
            rate_sample
        )

        actuator[k] = (
            actuator[k-1]
            + limited_rate * dt
        )

        actuator[k] = np.clip(
            actuator[k],
            -max_deflection_deg,
            max_deflection_deg
        )


    # --------------------------------------------------------
    # Uncertain generalized aerodynamic forcing
    # --------------------------------------------------------

    Q_uncontrolled = (
        actual_gust_scale
        * Q_gust_peak_robust
    )

    control_scale = (
        actuator
        / best_gust_required_deflection
    )

    Q_controlled = (
        Q_uncontrolled

        + control_scale
        * Q_control_full_robust
        * control_effectiveness_scale
    )


    # --------------------------------------------------------
    # Uncertain modal properties
    #
    # If natural frequency changes by factor f:
    # K_new = K_nominal * f²
    # --------------------------------------------------------

    stiffness_sample = (
        modal_stiffness
        * frequency_scale**2
    )

    omega_sample = np.sqrt(
        stiffness_sample
        / modal_mass
    )

    damping_sample = (
        2
        * damping_ratio_sample
        * omega_sample
        * modal_mass
    )


    # --------------------------------------------------------
    # Structural dynamic response
    # --------------------------------------------------------

    (
        q_controlled,
        qdot_controlled,
        qddot_controlled

    ) = newmark_beta_response(

        Q_controlled,

        modal_mass,

        damping_sample,

        stiffness_sample,

        dt
    )


    # --------------------------------------------------------
    # Root bending moment
    # --------------------------------------------------------

    root_moment = (
        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_controlled
        * root_moment_response_scale
    )


    # --------------------------------------------------------
    # Root stress
    # --------------------------------------------------------

    root_stress = (
        root_moment

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Tip response
    # --------------------------------------------------------

    tip_response = (
        tip_deflection_mass_reduced

        + q_controlled
        * tip_response_scale
    )


    return {
        "Peak_Root_Moment_MNm":
            np.max(root_moment) / 1e6,

        "Peak_Root_Stress_MPa":
            np.max(root_stress) / 1e6,

        "Peak_Tip_Deflection_m":
            np.max(tip_response),

        "Peak_Actuator_Deflection_deg":
            np.max(np.abs(actuator))
    }


# ------------------------------------------------------------
# 8. Monte Carlo uncertainty sweep
# ------------------------------------------------------------

robustness_results = []

print(
    "Running HART-120 controller robustness study..."
)


for sample_index in range(
    n_uncertainty_cases
):

    damping_sample = (
        damping_samples[sample_index]
    )

    frequency_scale = (
        frequency_scale_samples[sample_index]
    )

    gust_amplitude_scale = (
        gust_amplitude_scale_samples[sample_index]
    )

    control_effectiveness_scale = (
        control_effectiveness_scale_samples[
            sample_index
        ]
    )

    tau_sample = (
        selected_tau
        * tau_scale_samples[sample_index]
    )

    delay_sample = max(
        0.0,
        selected_delay
        + delay_error_samples[sample_index]
    )

    rate_sample = (
        selected_rate
        * rate_scale_samples[sample_index]
    )

    preview_sample = max(
        0.0,
        selected_preview
        + preview_error_samples[sample_index]
    )


    worst_root_moment = -np.inf
    worst_root_stress = -np.inf
    worst_tip = -np.inf
    worst_actuator = -np.inf
    worst_H = np.nan


    for H_test in H_robust_values:

        result = simulate_uncertain_gust_case(

            H_test,

            damping_sample,

            frequency_scale,

            gust_amplitude_scale,

            control_effectiveness_scale,

            tau_sample,

            delay_sample,

            rate_sample,

            preview_sample
        )


        if (
            result[
                "Peak_Root_Moment_MNm"
            ]
            > worst_root_moment
        ):

            worst_root_moment = (
                result[
                    "Peak_Root_Moment_MNm"
                ]
            )

            worst_H = H_test


        worst_root_stress = max(
            worst_root_stress,
            result[
                "Peak_Root_Stress_MPa"
            ]
        )

        worst_tip = max(
            worst_tip,
            result[
                "Peak_Tip_Deflection_m"
            ]
        )

        worst_actuator = max(
            worst_actuator,
            result[
                "Peak_Actuator_Deflection_deg"
            ]
        )


    passes_target = (
        worst_root_moment
        <= physical_target_MNm
    )


    robustness_results.append({

        "Sample":
            sample_index + 1,

        "Damping_Ratio":
            damping_sample,

        "Frequency_Scale":
            frequency_scale,

        "Gust_Amplitude_Scale":
            gust_amplitude_scale,

        "Control_Effectiveness_Scale":
            control_effectiveness_scale,

        "Actuator_Time_Constant_s":
            tau_sample,

        "Sensor_Delay_s":
            delay_sample,

        "Rate_Limit_deg_s":
            rate_sample,

        "Preview_Time_s":
            preview_sample,

        "Worst_Gust_H_m":
            worst_H,

        "Worst_Root_Moment_MNm":
            worst_root_moment,

        "Maximum_Root_Stress_MPa":
            worst_root_stress,

        "Maximum_Tip_Deflection_m":
            worst_tip,

        "Maximum_Actuator_Deflection_deg":
            worst_actuator,

        "Passes_10pct_Envelope_Target":
            passes_target
    })


    if (
        (sample_index + 1)
        % 50
        == 0
    ):

        print(
            f"Completed "
            f"{sample_index + 1} / "
            f"{n_uncertainty_cases}"
        )


robustness_df = pd.DataFrame(
    robustness_results
)


# ------------------------------------------------------------
# 9. Robustness statistics
# ------------------------------------------------------------

success_rate = (
    robustness_df[
        "Passes_10pct_Envelope_Target"
    ].mean()
    * 100
)

failure_rate = (
    100
    - success_rate
)


moment_mean = (
    robustness_df[
        "Worst_Root_Moment_MNm"
    ].mean()
)

moment_p95 = (
    robustness_df[
        "Worst_Root_Moment_MNm"
    ].quantile(
        0.95
    )
)

moment_p99 = (
    robustness_df[
        "Worst_Root_Moment_MNm"
    ].quantile(
        0.99
    )
)

moment_max = (
    robustness_df[
        "Worst_Root_Moment_MNm"
    ].max()
)

worst_case_index = (
    robustness_df[
        "Worst_Root_Moment_MNm"
    ].idxmax()
)

worst_case = (
    robustness_df.loc[
        worst_case_index
    ]
)


print()
print(
    "HART-120 GLA ROBUSTNESS / UNCERTAINTY STUDY"
)
print(
    "------------------------------------------"
)

print(
    f"Monte Carlo cases: "
    f"{n_uncertainty_cases}"
)

print(
    f"Gust gradients per case: "
    f"{len(H_robust_values)}"
)

print(
    f"Total transient simulations: "
    f"{n_uncertainty_cases * len(H_robust_values):,}"
)

print()

print(
    f"Nominal uncontrolled envelope: "
    f"{nominal_uncontrolled_envelope:.3f} MN·m"
)

print(
    f"10% controlled-envelope target: "
    f"{physical_target_MNm:.3f} MN·m"
)

print()

print(
    f"Robust pass rate: "
    f"{success_rate:.2f} %"
)

print(
    f"Failure rate: "
    f"{failure_rate:.2f} %"
)

print()

print(
    f"Mean worst-case controlled moment: "
    f"{moment_mean:.3f} MN·m"
)

print(
    f"95th-percentile controlled moment: "
    f"{moment_p95:.3f} MN·m"
)

print(
    f"99th-percentile controlled moment: "
    f"{moment_p99:.3f} MN·m"
)

print(
    f"Worst observed controlled moment: "
    f"{moment_max:.3f} MN·m"
)


print()
print(
    "MOST ADVERSE UNCERTAINTY REALIZATION"
)
print(
    "------------------------------------"
)

print(
    f"Critical gust gradient: "
    f"{worst_case['Worst_Gust_H_m']:.1f} m"
)

print(
    f"Damping ratio: "
    f"{worst_case['Damping_Ratio']:.4f}"
)

print(
    f"Natural-frequency scale: "
    f"{worst_case['Frequency_Scale']:.4f}"
)

print(
    f"Gust-amplitude scale: "
    f"{worst_case['Gust_Amplitude_Scale']:.4f}"
)

print(
    f"Control-effectiveness scale: "
    f"{worst_case['Control_Effectiveness_Scale']:.4f}"
)

print(
    f"Actuator time constant: "
    f"{worst_case['Actuator_Time_Constant_s']:.4f} s"
)

print(
    f"Sensor delay: "
    f"{worst_case['Sensor_Delay_s']:.4f} s"
)

print(
    f"Rate capability: "
    f"{worst_case['Rate_Limit_deg_s']:.2f} deg/s"
)

print(
    f"Preview time: "
    f"{worst_case['Preview_Time_s']:.4f} s"
)

print(
    f"Worst root moment: "
    f"{worst_case['Worst_Root_Moment_MNm']:.3f} MN·m"
)


# ------------------------------------------------------------
# 10. Distribution plot
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.hist(
    robustness_df[
        "Worst_Root_Moment_MNm"
    ],
    bins=25,
    alpha=0.8
)

plt.axvline(
    physical_target_MNm,
    linestyle="--",
    linewidth=2,
    label="10% envelope target"
)

plt.axvline(
    3.6952,
    linestyle=":",
    linewidth=2,
    label="Nominal selected controller"
)

plt.xlabel(
    "Worst Controlled Root Bending Moment (MN·m)"
)

plt.ylabel(
    "Monte Carlo Cases"
)

plt.title(
    "HART-120 — Robustness of Selected GLA Controller"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 11. Simple uncertainty-driver ranking
#
# Absolute Spearman correlation with worst root moment.
# ------------------------------------------------------------

uncertainty_features = [
    "Damping_Ratio",
    "Frequency_Scale",
    "Gust_Amplitude_Scale",
    "Control_Effectiveness_Scale",
    "Actuator_Time_Constant_s",
    "Sensor_Delay_s",
    "Rate_Limit_deg_s",
    "Preview_Time_s"
]


sensitivity = (
    robustness_df[
        uncertainty_features
        + [
            "Worst_Root_Moment_MNm"
        ]
    ]
    .corr(
        method="spearman"
    )[
        "Worst_Root_Moment_MNm"
    ]
    .drop(
        "Worst_Root_Moment_MNm"
    )
    .abs()
    .sort_values(
        ascending=False
    )
)


print()
print(
    "ROBUSTNESS SENSITIVITY RANKING"
)
print(
    "------------------------------"
)

print(
    sensitivity
    .round(4)
)


plt.figure(
    figsize=(8, 5)
)

sensitivity.plot(
    kind="bar"
)

plt.ylabel(
    "Absolute Spearman Correlation"
)

plt.title(
    "HART-120 — Drivers of GLA Robustness"
)

plt.grid(
    True,
    axis="y"
)

plt.xticks(
    rotation=35,
    ha="right"
)

plt.tight_layout()
plt.show()

# %% [notebook cell 105]
# ============================================================
# HART-120 — PAIRED ROBUSTNESS ASSESSMENT
#
# Separates two different engineering questions:
#
# 1. ABSOLUTE STRUCTURAL ROBUSTNESS
#    Does controlled root moment stay below the fixed
#    nominal 10% load-envelope target?
#
# 2. RELATIVE GLA ROBUSTNESS
#    Does the controller reduce the uncertain uncontrolled
#    response by at least 10% for the SAME realization?
#
# Reduced-order conceptual uncertainty study.
# ============================================================


# ------------------------------------------------------------
# 1. Paired uncertain simulation
# ------------------------------------------------------------

def simulate_uncertain_gust_pair(
    H,
    damping_ratio_sample,
    frequency_scale,
    gust_amplitude_scale,
    control_effectiveness_scale,
    tau_sample,
    delay_sample,
    rate_sample,
    preview_sample
):

    gust_duration = (
        2 * H
        / V_cruise
    )

    time_case = np.arange(
        -0.20,
        gust_duration
        + 2.0
        + dt,
        dt
    )


    # --------------------------------------------------------
    # Actual gust
    # --------------------------------------------------------

    gust_shape = robust_gust_scale(
        time_case,
        H
    )

    actual_gust_scale = (
        gust_amplitude_scale
        * gust_shape
    )


    # --------------------------------------------------------
    # Preview / sensed gust
    # --------------------------------------------------------

    sensed_shape = robust_gust_scale(
        time_case
        + preview_sample,
        H
    )

    sensed_gust_scale = (
        gust_amplitude_scale
        * sensed_shape
    )


    # --------------------------------------------------------
    # Control command
    # --------------------------------------------------------

    command_raw = (
        best_gust_required_deflection
        * sensed_gust_scale
    )

    command_raw = np.clip(
        command_raw,
        -max_deflection_deg,
        max_deflection_deg
    )


    # --------------------------------------------------------
    # Sensor / processing delay
    # --------------------------------------------------------

    delayed_command = np.interp(
        time_case
        - delay_sample,
        time_case,
        command_raw,
        left=0.0,
        right=0.0
    )


    # --------------------------------------------------------
    # Actuator
    # --------------------------------------------------------

    actuator = np.zeros_like(
        time_case
    )

    for k in range(
        1,
        len(time_case)
    ):

        desired_rate = (
            delayed_command[k]
            - actuator[k-1]
        ) / tau_sample

        limited_rate = np.clip(
            desired_rate,
            -rate_sample,
            rate_sample
        )

        actuator[k] = (
            actuator[k-1]
            + limited_rate * dt
        )

        actuator[k] = np.clip(
            actuator[k],
            -max_deflection_deg,
            max_deflection_deg
        )


    # --------------------------------------------------------
    # Generalized forces
    # --------------------------------------------------------

    Q_uncontrolled = (
        actual_gust_scale
        * Q_gust_peak_robust
    )

    control_scale = (
        actuator
        / best_gust_required_deflection
    )

    Q_controlled = (
        Q_uncontrolled

        + control_scale
        * Q_control_full_robust
        * control_effectiveness_scale
    )


    # --------------------------------------------------------
    # Uncertain structural dynamics
    # --------------------------------------------------------

    stiffness_sample = (
        modal_stiffness
        * frequency_scale**2
    )

    omega_sample = np.sqrt(
        stiffness_sample
        / modal_mass
    )

    damping_sample = (
        2
        * damping_ratio_sample
        * omega_sample
        * modal_mass
    )


    # --------------------------------------------------------
    # Uncontrolled response
    # --------------------------------------------------------

    (
        q_uncontrolled,
        qdot_uncontrolled,
        qddot_uncontrolled

    ) = newmark_beta_response(

        Q_uncontrolled,

        modal_mass,

        damping_sample,

        stiffness_sample,

        dt
    )


    # --------------------------------------------------------
    # Controlled response
    # --------------------------------------------------------

    (
        q_controlled,
        qdot_controlled,
        qddot_controlled

    ) = newmark_beta_response(

        Q_controlled,

        modal_mass,

        damping_sample,

        stiffness_sample,

        dt
    )


    # --------------------------------------------------------
    # Root moments
    # --------------------------------------------------------

    root_moment_uncontrolled = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_uncontrolled
        * root_moment_response_scale
    )


    root_moment_controlled = (

        bending_moment[0]

        + modal_root_moment_per_unit_q
        * q_controlled
        * root_moment_response_scale
    )


    peak_uncontrolled = np.max(
        root_moment_uncontrolled
    )

    peak_controlled = np.max(
        root_moment_controlled
    )


    root_reduction_percent = (

        (
            peak_uncontrolled
            - peak_controlled
        )

        / peak_uncontrolled

        * 100
    )


    # --------------------------------------------------------
    # Stress
    # --------------------------------------------------------

    peak_root_stress = (

        peak_controlled

        / (
            A_cap_mass_reduced[0]
            * box_height[0]
        )
    )


    # --------------------------------------------------------
    # Tip response
    # --------------------------------------------------------

    tip_controlled = (

        tip_deflection_mass_reduced

        + q_controlled
        * tip_response_scale
    )


    return {

        "Peak_Uncontrolled_MNm":
            peak_uncontrolled / 1e6,

        "Peak_Controlled_MNm":
            peak_controlled / 1e6,

        "Root_Moment_Reduction_%":
            root_reduction_percent,

        "Peak_Root_Stress_MPa":
            peak_root_stress / 1e6,

        "Peak_Tip_Deflection_m":
            np.max(tip_controlled),

        "Peak_Actuator_Deflection_deg":
            np.max(np.abs(actuator))
    }



# ------------------------------------------------------------
# 2. Corrected paired Monte Carlo ENVELOPE robustness study
#
# IMPORTANT:
# The primary relative GLA metric is now envelope-to-envelope:
#
#   R_env = 100 * (1 - max_H(M_controlled) / max_H(M_uncontrolled))
#
# This compares the worst controlled gust load with the worst
# uncontrolled gust load for the SAME uncertainty realization.
#
# The old "minimum reduction at every individual gust H" metric
# is retained only as a diagnostic because it answers a much
# stricter and different question.
# ------------------------------------------------------------

paired_results = []

relative_GLA_target_percent = 10.0
robustness_objective_percent = 95.0

print(
    "Running corrected paired HART-120 envelope robustness assessment..."
)


for sample_index in range(
    n_uncertainty_cases
):

    damping_sample = (
        damping_samples[sample_index]
    )

    frequency_scale = (
        frequency_scale_samples[sample_index]
    )

    gust_amplitude_scale = (
        gust_amplitude_scale_samples[sample_index]
    )

    control_effectiveness_scale = (
        control_effectiveness_scale_samples[
            sample_index
        ]
    )

    tau_sample = (
        selected_tau
        * tau_scale_samples[sample_index]
    )

    delay_sample = max(
        0.0,
        selected_delay
        + delay_error_samples[sample_index]
    )

    rate_sample = (
        selected_rate
        * rate_scale_samples[sample_index]
    )

    preview_sample = max(
        0.0,
        selected_preview
        + preview_error_samples[sample_index]
    )


    # --------------------------------------------------------
    # Store the COMPLETE 20-gust envelope for this realization
    # --------------------------------------------------------

    uncontrolled_moment_envelope = []
    controlled_moment_envelope = []
    pointwise_reduction_envelope = []

    root_stress_envelope = []
    tip_deflection_envelope = []
    actuator_deflection_envelope = []


    for H_test in H_robust_values:

        result = simulate_uncertain_gust_pair(

            H_test,

            damping_sample,

            frequency_scale,

            gust_amplitude_scale,

            control_effectiveness_scale,

            tau_sample,

            delay_sample,

            rate_sample,

            preview_sample
        )


        uncontrolled_moment_envelope.append(
            result[
                "Peak_Uncontrolled_MNm"
            ]
        )

        controlled_moment_envelope.append(
            result[
                "Peak_Controlled_MNm"
            ]
        )

        pointwise_reduction_envelope.append(
            result[
                "Root_Moment_Reduction_%"
            ]
        )

        root_stress_envelope.append(
            result[
                "Peak_Root_Stress_MPa"
            ]
        )

        tip_deflection_envelope.append(
            result[
                "Peak_Tip_Deflection_m"
            ]
        )

        actuator_deflection_envelope.append(
            result[
                "Peak_Actuator_Deflection_deg"
            ]
        )


    uncontrolled_moment_envelope = np.asarray(
        uncontrolled_moment_envelope
    )

    controlled_moment_envelope = np.asarray(
        controlled_moment_envelope
    )

    pointwise_reduction_envelope = np.asarray(
        pointwise_reduction_envelope
    )

    root_stress_envelope = np.asarray(
        root_stress_envelope
    )

    tip_deflection_envelope = np.asarray(
        tip_deflection_envelope
    )

    actuator_deflection_envelope = np.asarray(
        actuator_deflection_envelope
    )


    # --------------------------------------------------------
    # Envelope-level quantities
    # --------------------------------------------------------

    uncontrolled_critical_index = np.argmax(
        uncontrolled_moment_envelope
    )

    controlled_critical_index = np.argmax(
        controlled_moment_envelope
    )


    uncontrolled_envelope_peak = (
        uncontrolled_moment_envelope[
            uncontrolled_critical_index
        ]
    )

    controlled_envelope_peak = (
        controlled_moment_envelope[
            controlled_critical_index
        ]
    )


    envelope_reduction_percent = (

        (
            uncontrolled_envelope_peak
            - controlled_envelope_peak
        )

        / uncontrolled_envelope_peak

        * 100.0
    )


    # Old, stricter pointwise metric retained for diagnosis only
    minimum_pointwise_reduction = np.min(
        pointwise_reduction_envelope
    )


    maximum_root_stress = np.max(
        root_stress_envelope
    )

    maximum_tip_deflection = np.max(
        tip_deflection_envelope
    )

    maximum_actuator_deflection = np.max(
        actuator_deflection_envelope
    )


    # --------------------------------------------------------
    # Pass / fail requirements
    # --------------------------------------------------------

    passes_absolute_target = (
        controlled_envelope_peak
        <= physical_target_MNm
    )

    passes_relative_envelope_target = (
        envelope_reduction_percent
        >= relative_GLA_target_percent
    )

    passes_actuator_limit = (
        maximum_actuator_deflection
        <= max_deflection_deg
    )

    passes_joint_requirement = (
        passes_absolute_target
        and passes_relative_envelope_target
        and passes_actuator_limit
    )


    paired_results.append({

        "Sample":
            sample_index + 1,

        "Damping_Ratio":
            damping_sample,

        "Frequency_Scale":
            frequency_scale,

        "Gust_Amplitude_Scale":
            gust_amplitude_scale,

        "Control_Effectiveness_Scale":
            control_effectiveness_scale,

        "Actuator_Time_Constant_s":
            tau_sample,

        "Sensor_Delay_s":
            delay_sample,

        "Rate_Limit_deg_s":
            rate_sample,

        "Preview_Time_s":
            preview_sample,

        "Uncontrolled_Envelope_Peak_MNm":
            uncontrolled_envelope_peak,

        "Uncontrolled_Critical_Gust_H_m":
            H_robust_values[
                uncontrolled_critical_index
            ],

        "Controlled_Envelope_Peak_MNm":
            controlled_envelope_peak,

        "Controlled_Critical_Gust_H_m":
            H_robust_values[
                controlled_critical_index
            ],

        "Envelope_Root_Moment_Reduction_%":
            envelope_reduction_percent,

        "Minimum_Pointwise_GLA_Reduction_%":
            minimum_pointwise_reduction,

        "Maximum_Root_Stress_MPa":
            maximum_root_stress,

        "Maximum_Tip_Deflection_m":
            maximum_tip_deflection,

        "Maximum_Actuator_Deflection_deg":
            maximum_actuator_deflection,

        "Passes_Absolute_Load_Target":
            passes_absolute_target,

        "Passes_10pct_Envelope_GLA_Target":
            passes_relative_envelope_target,

        "Passes_Actuator_Limit":
            passes_actuator_limit,

        "Passes_Joint_Requirement":
            passes_joint_requirement
    })


    if (
        (sample_index + 1)
        % 50
        == 0
    ):

        print(
            f"Completed "
            f"{sample_index + 1} / "
            f"{n_uncertainty_cases}"
        )


paired_robustness_df = pd.DataFrame(
    paired_results
)


# ------------------------------------------------------------
# 3. Corrected robustness / reliability metrics
# ------------------------------------------------------------

absolute_pass_rate = (

    paired_robustness_df[
        "Passes_Absolute_Load_Target"
    ].mean()

    * 100.0
)


relative_envelope_pass_rate = (

    paired_robustness_df[
        "Passes_10pct_Envelope_GLA_Target"
    ].mean()

    * 100.0
)


actuator_pass_rate = (

    paired_robustness_df[
        "Passes_Actuator_Limit"
    ].mean()

    * 100.0
)


joint_pass_rate = (

    paired_robustness_df[
        "Passes_Joint_Requirement"
    ].mean()

    * 100.0
)


# Diagnostic only: old all-gust pointwise requirement
legacy_pointwise_pass_rate = (

    (
        paired_robustness_df[
            "Minimum_Pointwise_GLA_Reduction_%"
        ]
        >= relative_GLA_target_percent
    ).mean()

    * 100.0
)


mean_envelope_reduction = (

    paired_robustness_df[
        "Envelope_Root_Moment_Reduction_%"
    ].mean()
)


p05_envelope_reduction = (

    paired_robustness_df[
        "Envelope_Root_Moment_Reduction_%"
    ].quantile(
        0.05
    )
)


p95_controlled_envelope = (

    paired_robustness_df[
        "Controlled_Envelope_Peak_MNm"
    ].quantile(
        0.95
    )
)


# ------------------------------------------------------------
# 4. Critical Monte Carlo realizations
# ------------------------------------------------------------

worst_absolute_index = (

    paired_robustness_df[
        "Controlled_Envelope_Peak_MNm"
    ].idxmax()
)


worst_relative_index = (

    paired_robustness_df[
        "Envelope_Root_Moment_Reduction_%"
    ].idxmin()
)


worst_absolute_case = (
    paired_robustness_df.loc[
        worst_absolute_index
    ]
)


worst_relative_case = (
    paired_robustness_df.loc[
        worst_relative_index
    ]
)


# ------------------------------------------------------------
# 5. Print engineering results
# ------------------------------------------------------------

print()
print(
    "HART-120 CORRECTED ENVELOPE-LEVEL ROBUSTNESS RESULTS"
)
print(
    "---------------------------------------------------"
)

print(
    f"Monte Carlo realizations: "
    f"{len(paired_robustness_df)}"
)

print(
    f"Gust gradients per realization: "
    f"{len(H_robust_values)}"
)

print(
    f"Total paired transient evaluations: "
    f"{2 * len(paired_robustness_df) * len(H_robust_values):,}"
)

print()

print(
    f"Physical controlled-load limit: "
    f"{physical_target_MNm:.3f} MN·m"
)

print(
    f"Relative envelope GLA target: "
    f"{relative_GLA_target_percent:.1f} %"
)

print(
    f"Surface-deflection limit: "
    f"{max_deflection_deg:.1f} deg"
)

print()

print(
    "ROBUSTNESS PASS RATES"
)
print(
    "---------------------"
)

print(
    f"Absolute load-limit pass rate: "
    f"{absolute_pass_rate:.2f} %"
)

print(
    f"Envelope >=10% GLA pass rate: "
    f"{relative_envelope_pass_rate:.2f} %"
)

print(
    f"Actuator-limit pass rate: "
    f"{actuator_pass_rate:.2f} %"
)

print(
    f"Joint robustness pass rate: "
    f"{joint_pass_rate:.2f} %"
)

print()

print(
    "ENVELOPE STATISTICS"
)
print(
    "-------------------"
)

print(
    f"Mean envelope root-moment reduction: "
    f"{mean_envelope_reduction:.2f} %"
)

print(
    f"5th-percentile envelope reduction: "
    f"{p05_envelope_reduction:.2f} %"
)

print(
    f"95th-percentile controlled envelope peak: "
    f"{p95_controlled_envelope:.3f} MN·m"
)

print()

print(
    "DIAGNOSTIC COMPARISON WITH OLD METRIC"
)
print(
    "-------------------------------------"
)

print(
    f"Legacy all-gust pointwise >=10% pass rate: "
    f"{legacy_pointwise_pass_rate:.2f} %"
)

print(
    "The legacy metric requires at least 10% reduction at "
    "EVERY tested gust gradient; it is retained only as a "
    "diagnostic and is not the primary envelope-level criterion."
)

print()

print(
    "MOST ADVERSE ABSOLUTE-LOAD REALIZATION"
)
print(
    "--------------------------------------"
)

print(
    f"Controlled envelope peak: "
    f"{worst_absolute_case['Controlled_Envelope_Peak_MNm']:.3f} MN·m"
)

print(
    f"Uncontrolled envelope peak: "
    f"{worst_absolute_case['Uncontrolled_Envelope_Peak_MNm']:.3f} MN·m"
)

print(
    f"Envelope reduction: "
    f"{worst_absolute_case['Envelope_Root_Moment_Reduction_%']:.2f} %"
)

print(
    f"Controlled critical gust H: "
    f"{worst_absolute_case['Controlled_Critical_Gust_H_m']:.1f} m"
)

print()

print(
    "WORST RELATIVE-GLA REALIZATION"
)
print(
    "------------------------------"
)

print(
    f"Envelope reduction: "
    f"{worst_relative_case['Envelope_Root_Moment_Reduction_%']:.2f} %"
)

print(
    f"Uncontrolled envelope peak: "
    f"{worst_relative_case['Uncontrolled_Envelope_Peak_MNm']:.3f} MN·m"
)

print(
    f"Controlled envelope peak: "
    f"{worst_relative_case['Controlled_Envelope_Peak_MNm']:.3f} MN·m"
)

print(
    f"Uncontrolled critical gust H: "
    f"{worst_relative_case['Uncontrolled_Critical_Gust_H_m']:.1f} m"
)

print(
    f"Controlled critical gust H: "
    f"{worst_relative_case['Controlled_Critical_Gust_H_m']:.1f} m"
)

print()

print(
    "INTERPRETATION"
)
print(
    "--------------"
)

if relative_envelope_pass_rate >= robustness_objective_percent:

    print(
        "The selected controller robustly preserves the "
        "10% ENVELOPE-level GLA objective over the tested "
        "uncertainty set."
    )

else:

    print(
        "The selected controller does not yet satisfy the "
        "95% project robustness objective for envelope-level "
        "10% gust-load alleviation."
    )


if absolute_pass_rate >= robustness_objective_percent:

    print(
        "The fixed structural controlled-load target is also robust."
    )

else:

    print(
        "The fixed structural load target remains sensitive "
        "to uncertainty even after correcting the relative metric."
    )

# %% [notebook cell 106]
# ============================================================
# HART-120 — CORRECTED ENVELOPE ROBUSTNESS PLOTS
#
# Run AFTER the corrected paired Monte Carlo cell above.
# No transient simulations are repeated here.
# ============================================================


# ------------------------------------------------------------
# 1. Robustness pass-rate summary
# ------------------------------------------------------------

robustness_metric_names = [

    "Absolute\nload target",

    "Envelope\n10% GLA",

    "Actuator\nlimit",

    "Joint\nrequirement"
]


robustness_metric_values = [

    absolute_pass_rate,

    relative_envelope_pass_rate,

    actuator_pass_rate,

    joint_pass_rate
]


plt.figure(
    figsize=(8, 5)
)

plt.bar(
    robustness_metric_names,
    robustness_metric_values
)

plt.axhline(
    robustness_objective_percent,
    linestyle="--",
    linewidth=2,
    label=(
        f"{robustness_objective_percent:.0f}% "
        "project robustness objective"
    )
)

plt.ylabel(
    "Monte Carlo Pass Rate (%)"
)

plt.title(
    "HART-120 — Corrected Controller Robustness Metrics"
)

plt.ylim(
    0,
    105
)

plt.grid(
    True,
    axis="y"
)

plt.legend()
plt.show()


# ------------------------------------------------------------
# 2. Correct envelope-level GLA distribution
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.hist(
    paired_robustness_df[
        "Envelope_Root_Moment_Reduction_%"
    ],
    bins=25,
    alpha=0.8
)

plt.axvline(
    relative_GLA_target_percent,
    linestyle="--",
    linewidth=2,
    label="10% envelope GLA target"
)

plt.axvline(
    p05_envelope_reduction,
    linestyle=":",
    linewidth=2,
    label=(
        f"5th percentile = "
        f"{p05_envelope_reduction:.2f}%"
    )
)

plt.xlabel(
    "Envelope Root-Moment Reduction (%)"
)

plt.ylabel(
    "Monte Carlo Cases"
)

plt.title(
    "HART-120 — Robust Envelope-Level GLA Performance"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 3. Uncontrolled vs controlled envelope peaks
#
# Points below the diagonal 10%-reduction line satisfy the
# relative envelope target. Points below the horizontal line
# satisfy the fixed absolute structural target.
# ------------------------------------------------------------

x_envelope = (

    paired_robustness_df[
        "Uncontrolled_Envelope_Peak_MNm"
    ].to_numpy()
)

y_envelope = (

    paired_robustness_df[
        "Controlled_Envelope_Peak_MNm"
    ].to_numpy()
)


x_reference = np.linspace(
    np.min(x_envelope) * 0.98,
    np.max(x_envelope) * 1.02,
    200
)


plt.figure(
    figsize=(8, 6)
)

plt.scatter(
    x_envelope,
    y_envelope,
    alpha=0.65
)

plt.plot(
    x_reference,
    0.90 * x_reference,
    linestyle="--",
    linewidth=2,
    label="10% envelope-reduction boundary"
)

plt.axhline(
    physical_target_MNm,
    linestyle=":",
    linewidth=2,
    label=(
        f"Absolute load limit = "
        f"{physical_target_MNm:.3f} MN·m"
    )
)

plt.xlabel(
    "Uncontrolled Gust-Envelope Peak (MN·m)"
)

plt.ylabel(
    "Controlled Gust-Envelope Peak (MN·m)"
)

plt.title(
    "HART-120 — Paired Uncontrolled vs Controlled Gust Envelopes"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 4. Controlled-envelope structural load distribution
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.hist(
    paired_robustness_df[
        "Controlled_Envelope_Peak_MNm"
    ],
    bins=25,
    alpha=0.8
)

plt.axvline(
    physical_target_MNm,
    linestyle="--",
    linewidth=2,
    label=(
        f"Absolute load limit = "
        f"{physical_target_MNm:.3f} MN·m"
    )
)

plt.axvline(
    p95_controlled_envelope,
    linestyle=":",
    linewidth=2,
    label=(
        f"95th percentile = "
        f"{p95_controlled_envelope:.3f} MN·m"
    )
)

plt.xlabel(
    "Worst Controlled Root Bending Moment per Realization (MN·m)"
)

plt.ylabel(
    "Monte Carlo Cases"
)

plt.title(
    "HART-120 — Controlled Gust-Envelope Robustness"
)

plt.grid(True)
plt.legend()
plt.show()


# ------------------------------------------------------------
# 5. What drives ENVELOPE-level GLA robustness?
#
# Spearman correlation is used because the relationships can
# be monotonic without being perfectly linear.
# ------------------------------------------------------------

robustness_driver_features = [

    "Gust_Amplitude_Scale",

    "Frequency_Scale",

    "Damping_Ratio",

    "Control_Effectiveness_Scale",

    "Actuator_Time_Constant_s",

    "Sensor_Delay_s",

    "Rate_Limit_deg_s",

    "Preview_Time_s"
]


driver_correlations = (

    paired_robustness_df[
        robustness_driver_features
        +
        [
            "Envelope_Root_Moment_Reduction_%"
        ]
    ]

    .corr(
        method="spearman"
    )[
        "Envelope_Root_Moment_Reduction_%"
    ]

    .drop(
        "Envelope_Root_Moment_Reduction_%"
    )

    .sort_values(
        key=np.abs,
        ascending=False
    )
)


print()
print(
    "HART-120 ENVELOPE-GLA ROBUSTNESS SENSITIVITY"
)
print(
    "--------------------------------------------"
)

print(
    driver_correlations.round(4)
)


plt.figure(
    figsize=(9, 5)
)

plt.bar(
    driver_correlations.index,
    driver_correlations.values
)

plt.axhline(
    0.0,
    linewidth=1
)

plt.ylabel(
    "Spearman Correlation with Envelope GLA Reduction"
)

plt.title(
    "HART-120 — Drivers of Envelope-Level GLA Robustness"
)

plt.xticks(
    rotation=35,
    ha="right"
)

plt.grid(
    True,
    axis="y"
)

plt.tight_layout()
plt.show()

# %% [notebook cell 108]
# ============================================================
# HART-120
# ROBUST CONTROLLER ARCHITECTURE REDESIGN
#
# Objective:
# Find the lowest-burden preview / sensor-delay architecture
# that robustly satisfies:
#
# 1. Controlled gust-envelope peak <= physical_target_MNm
# 2. Envelope-level GLA >= 10 %
# 3. Actuator deflection <= max_deflection_deg
# 4. Joint pass probability >= 95 %
#
# Existing actuator time constant and rate capability are held
# fixed initially. They can be optimized later if necessary.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Robust-design search space
# ------------------------------------------------------------

preview_design_values = np.arange(
    0.06,
    0.121,
    0.01
)

delay_design_values = np.arange(
    0.03,
    0.071,
    0.01
)

robust_design_target_percent = 95.0


# Use a representative subset for preliminary screening.
# Full 300-case verification follows after candidate selection.

n_screen_cases = min(
    60,
    n_uncertainty_cases
)

screen_indices = np.linspace(
    0,
    n_uncertainty_cases - 1,
    n_screen_cases,
    dtype=int
)


print(
    "HART-120 ROBUST CONTROLLER REDESIGN"
)

print(
    "---------------------------------"
)

print(
    f"Preview designs: "
    f"{len(preview_design_values)}"
)

print(
    f"Delay designs: "
    f"{len(delay_design_values)}"
)

print(
    f"Architectures screened: "
    f"{len(preview_design_values) * len(delay_design_values)}"
)

print(
    f"Monte Carlo cases per architecture: "
    f"{n_screen_cases}"
)

print()


# ------------------------------------------------------------
# 2. Architecture screening
# ------------------------------------------------------------

architecture_results = []

architecture_counter = 0

total_architectures = (
    len(preview_design_values)
    *
    len(delay_design_values)
)


for preview_design in preview_design_values:

    for delay_design in delay_design_values:

        architecture_counter += 1

        absolute_passes = 0
        relative_passes = 0
        actuator_passes = 0
        joint_passes = 0

        envelope_reductions = []
        controlled_peaks = []
        actuator_peaks = []


        for sample_index in screen_indices:

            damping_sample = (
                damping_samples[sample_index]
            )

            frequency_scale = (
                frequency_scale_samples[
                    sample_index
                ]
            )

            gust_amplitude_scale = (
                gust_amplitude_scale_samples[
                    sample_index
                ]
            )

            control_effectiveness_scale = (
                control_effectiveness_scale_samples[
                    sample_index
                ]
            )


            # Existing actuator architecture retained
            # during this first robust redesign.

            tau_sample = (
                selected_tau
                *
                tau_scale_samples[
                    sample_index
                ]
            )

            rate_sample = (
                selected_rate
                *
                rate_scale_samples[
                    sample_index
                ]
            )


            # Candidate sensor delay including uncertainty

            delay_sample = max(
                0.0,
                delay_design
                +
                delay_error_samples[
                    sample_index
                ]
            )


            # Candidate preview time including
            # gust-estimation / timing uncertainty

            preview_sample = max(
                0.0,
                preview_design
                +
                preview_error_samples[
                    sample_index
                ]
            )


            controlled_envelope = []
            actuator_envelope = []


            for H_test in H_robust_values:

                result = simulate_uncertain_gust_pair(

                    H_test,

                    damping_sample,

                    frequency_scale,

                    gust_amplitude_scale,

                    control_effectiveness_scale,

                    tau_sample,

                    delay_sample,

                    rate_sample,

                    preview_sample
                )


                controlled_envelope.append(

                    result[
                        "Peak_Controlled_MNm"
                    ]
                )


                actuator_envelope.append(

                    result[
                        "Peak_Actuator_Deflection_deg"
                    ]
                )


            controlled_envelope = np.asarray(
                controlled_envelope
            )

            actuator_envelope = np.asarray(
                actuator_envelope
            )


            controlled_peak = np.max(
                controlled_envelope
            )

            actuator_peak = np.max(
                actuator_envelope
            )


            # Uncontrolled envelope has already been
            # calculated for this same uncertainty realization.

            uncontrolled_peak = (

                paired_robustness_df.iloc[
                    sample_index
                ][
                    "Uncontrolled_Envelope_Peak_MNm"
                ]
            )


            envelope_reduction = (

                (
                    uncontrolled_peak
                    -
                    controlled_peak
                )

                / uncontrolled_peak

                * 100.0
            )


            passes_absolute = (

                controlled_peak
                <= physical_target_MNm
            )


            passes_relative = (

                envelope_reduction
                >= relative_GLA_target_percent
            )


            passes_actuator = (

                actuator_peak
                <= max_deflection_deg
            )


            passes_joint = (

                passes_absolute
                and passes_relative
                and passes_actuator
            )


            absolute_passes += int(
                passes_absolute
            )

            relative_passes += int(
                passes_relative
            )

            actuator_passes += int(
                passes_actuator
            )

            joint_passes += int(
                passes_joint
            )


            envelope_reductions.append(
                envelope_reduction
            )

            controlled_peaks.append(
                controlled_peak
            )

            actuator_peaks.append(
                actuator_peak
            )


        # ----------------------------------------------------
        # Pass probabilities
        # ----------------------------------------------------

        absolute_pass_rate_candidate = (

            absolute_passes
            /
            n_screen_cases
            *
            100.0
        )

        relative_pass_rate_candidate = (

            relative_passes
            /
            n_screen_cases
            *
            100.0
        )

        actuator_pass_rate_candidate = (

            actuator_passes
            /
            n_screen_cases
            *
            100.0
        )

        joint_pass_rate_candidate = (

            joint_passes
            /
            n_screen_cases
            *
            100.0
        )


        envelope_reductions = np.asarray(
            envelope_reductions
        )

        controlled_peaks = np.asarray(
            controlled_peaks
        )


        # ----------------------------------------------------
        # Architecture burden
        #
        # Longer preview distance increases sensor burden.
        # Lower delay increases processing / hardware burden.
        # ----------------------------------------------------

        preview_denominator = max(

            preview_design_values.max()
            -
            selected_preview,

            1e-9
        )

        delay_denominator = max(

            selected_delay
            -
            delay_design_values.min(),

            1e-9
        )


        preview_burden = max(

            0.0,

            (
                preview_design
                -
                selected_preview
            )
            /
            preview_denominator
        )


        delay_burden = max(

            0.0,

            (
                selected_delay
                -
                delay_design
            )
            /
            delay_denominator
        )


        architecture_burden = (

            0.70
            *
            preview_burden

            +

            0.30
            *
            delay_burden
        )


        architecture_results.append({

            "Preview_Time_s":
                preview_design,

            "Preview_Distance_m":
                preview_design
                *
                V_cruise,

            "Sensor_Delay_s":
                delay_design,

            "Absolute_Pass_Rate_%":
                absolute_pass_rate_candidate,

            "Envelope_GLA_Pass_Rate_%":
                relative_pass_rate_candidate,

            "Actuator_Pass_Rate_%":
                actuator_pass_rate_candidate,

            "Joint_Pass_Rate_%":
                joint_pass_rate_candidate,

            "Mean_Envelope_Reduction_%":
                np.mean(
                    envelope_reductions
                ),

            "P05_Envelope_Reduction_%":
                np.quantile(
                    envelope_reductions,
                    0.05
                ),

            "P95_Controlled_Peak_MNm":
                np.quantile(
                    controlled_peaks,
                    0.95
                ),

            "Architecture_Burden":
                architecture_burden
        })


        print(

            f"Architecture "
            f"{architecture_counter:02d} / "
            f"{total_architectures} | "

            f"Preview = "
            f"{preview_design:.3f} s | "

            f"Delay = "
            f"{delay_design:.3f} s | "

            f"Joint = "
            f"{joint_pass_rate_candidate:.1f} %"
        )


robust_design_df = pd.DataFrame(
    architecture_results
)


# ------------------------------------------------------------
# 3. Select robust architecture
# ------------------------------------------------------------

robust_candidates = robust_design_df[

    robust_design_df[
        "Joint_Pass_Rate_%"
    ]
    >= robust_design_target_percent

].copy()


if len(robust_candidates) > 0:

    robust_candidates = (

        robust_candidates

        .sort_values(

            by=[
                "Architecture_Burden",
                "P95_Controlled_Peak_MNm"
            ],

            ascending=[
                True,
                True
            ]
        )
    )

    robust_candidate_found = True

    selected_robust_design = (
        robust_candidates.iloc[0]
    )


else:

    # If the current architecture family cannot
    # achieve 95%, select the best available design.
    # This is an engineering result, not a failure.

    robust_candidate_found = False

    selected_robust_design = (

        robust_design_df

        .sort_values(

            by=[
                "Joint_Pass_Rate_%",
                "P05_Envelope_Reduction_%",
                "Architecture_Burden"
            ],

            ascending=[
                False,
                False,
                True
            ]
        )

        .iloc[0]
    )


print()
print(
    "ROBUST CONTROLLER SCREENING RESULT"
)
print(
    "----------------------------------"
)

print(
    f"95% robust design found: "
    f"{robust_candidate_found}"
)

print(
    f"Selected preview time: "
    f"{selected_robust_design['Preview_Time_s']:.3f} s"
)

print(
    f"Equivalent sensing distance: "
    f"{selected_robust_design['Preview_Distance_m']:.2f} m"
)

print(
    f"Selected sensor delay: "
    f"{selected_robust_design['Sensor_Delay_s']:.3f} s"
)

print(
    f"Screening absolute pass rate: "
    f"{selected_robust_design['Absolute_Pass_Rate_%']:.2f} %"
)

print(
    f"Screening envelope-GLA pass rate: "
    f"{selected_robust_design['Envelope_GLA_Pass_Rate_%']:.2f} %"
)

print(
    f"Screening joint pass rate: "
    f"{selected_robust_design['Joint_Pass_Rate_%']:.2f} %"
)

print(
    f"5th-percentile envelope reduction: "
    f"{selected_robust_design['P05_Envelope_Reduction_%']:.2f} %"
)

print(
    f"95th-percentile controlled load: "
    f"{selected_robust_design['P95_Controlled_Peak_MNm']:.3f} MN·m"
)


# ============================================================
# 4. FULL 300-CASE PHYSICS VERIFICATION
# ============================================================

robust_preview_selected = (
    selected_robust_design[
        "Preview_Time_s"
    ]
)

robust_delay_selected = (
    selected_robust_design[
        "Sensor_Delay_s"
    ]
)


final_robust_results = []


print()
print(
    "Running full physics verification "
    "of redesigned controller..."
)


for sample_index in range(
    n_uncertainty_cases
):

    damping_sample = (
        damping_samples[sample_index]
    )

    frequency_scale = (
        frequency_scale_samples[
            sample_index
        ]
    )

    gust_amplitude_scale = (
        gust_amplitude_scale_samples[
            sample_index
        ]
    )

    control_effectiveness_scale = (
        control_effectiveness_scale_samples[
            sample_index
        ]
    )


    tau_sample = (

        selected_tau
        *
        tau_scale_samples[
            sample_index
        ]
    )


    rate_sample = (

        selected_rate
        *
        rate_scale_samples[
            sample_index
        ]
    )


    delay_sample = max(

        0.0,

        robust_delay_selected
        +
        delay_error_samples[
            sample_index
        ]
    )


    preview_sample = max(

        0.0,

        robust_preview_selected
        +
        preview_error_samples[
            sample_index
        ]
    )


    controlled_envelope = []
    actuator_envelope = []


    for H_test in H_robust_values:

        result = simulate_uncertain_gust_pair(

            H_test,

            damping_sample,

            frequency_scale,

            gust_amplitude_scale,

            control_effectiveness_scale,

            tau_sample,

            delay_sample,

            rate_sample,

            preview_sample
        )


        controlled_envelope.append(

            result[
                "Peak_Controlled_MNm"
            ]
        )


        actuator_envelope.append(

            result[
                "Peak_Actuator_Deflection_deg"
            ]
        )


    controlled_peak = np.max(
        controlled_envelope
    )

    actuator_peak = np.max(
        actuator_envelope
    )


    uncontrolled_peak = (

        paired_robustness_df.iloc[
            sample_index
        ][
            "Uncontrolled_Envelope_Peak_MNm"
        ]
    )


    envelope_reduction = (

        (
            uncontrolled_peak
            -
            controlled_peak
        )

        / uncontrolled_peak

        * 100.0
    )


    passes_absolute = (

        controlled_peak
        <= physical_target_MNm
    )


    passes_relative = (

        envelope_reduction
        >= relative_GLA_target_percent
    )


    passes_actuator = (

        actuator_peak
        <= max_deflection_deg
    )


    passes_joint = (

        passes_absolute
        and passes_relative
        and passes_actuator
    )


    final_robust_results.append({

        "Sample":
            sample_index + 1,

        "Uncontrolled_Envelope_MNm":
            uncontrolled_peak,

        "Controlled_Envelope_MNm":
            controlled_peak,

        "Envelope_Reduction_%":
            envelope_reduction,

        "Peak_Actuator_Deflection_deg":
            actuator_peak,

        "Passes_Absolute_Target":
            passes_absolute,

        "Passes_Envelope_GLA":
            passes_relative,

        "Passes_Actuator":
            passes_actuator,

        "Passes_Joint":
            passes_joint
    })


    if (
        (sample_index + 1)
        % 50
        == 0
    ):

        print(
            f"Verified "
            f"{sample_index + 1} / "
            f"{n_uncertainty_cases}"
        )


final_robust_df = pd.DataFrame(
    final_robust_results
)


new_absolute_pass = (

    final_robust_df[
        "Passes_Absolute_Target"
    ].mean()

    * 100.0
)


new_relative_pass = (

    final_robust_df[
        "Passes_Envelope_GLA"
    ].mean()

    * 100.0
)


new_actuator_pass = (

    final_robust_df[
        "Passes_Actuator"
    ].mean()

    * 100.0
)


new_joint_pass = (

    final_robust_df[
        "Passes_Joint"
    ].mean()

    * 100.0
)


new_p05_reduction = (

    final_robust_df[
        "Envelope_Reduction_%"
    ].quantile(
        0.05
    )
)


new_p95_controlled = (

    final_robust_df[
        "Controlled_Envelope_MNm"
    ].quantile(
        0.95
    )
)


print()
print(
    "HART-120 ROBUST CONTROLLER — FINAL VERIFICATION"
)
print(
    "-----------------------------------------------"
)

print(
    f"Preview time: "
    f"{robust_preview_selected:.3f} s"
)

print(
    f"Equivalent sensing distance: "
    f"{robust_preview_selected * V_cruise:.2f} m"
)

print(
    f"Sensor delay: "
    f"{robust_delay_selected:.3f} s"
)

print()

print(
    f"Absolute load pass rate: "
    f"{new_absolute_pass:.2f} %"
)

print(
    f"Envelope >=10% GLA pass rate: "
    f"{new_relative_pass:.2f} %"
)

print(
    f"Actuator pass rate: "
    f"{new_actuator_pass:.2f} %"
)

print(
    f"Joint robustness pass rate: "
    f"{new_joint_pass:.2f} %"
)

print()

print(
    f"5th-percentile envelope reduction: "
    f"{new_p05_reduction:.2f} %"
)

print(
    f"95th-percentile controlled envelope: "
    f"{new_p95_controlled:.3f} MN·m"
)


# ============================================================
# 5. ROBUST-DESIGN MAP
# ============================================================

robustness_map = (

    robust_design_df

    .pivot(

        index="Sensor_Delay_s",

        columns="Preview_Time_s",

        values="Joint_Pass_Rate_%"
    )
)


plt.figure(
    figsize=(9, 6)
)

image = plt.imshow(

    robustness_map.values,

    origin="lower",

    aspect="auto"
)


plt.colorbar(
    image,
    label="Joint Robustness Pass Rate (%)"
)


plt.xticks(

    np.arange(
        len(
            robustness_map.columns
        )
    ),

    [
        f"{value:.2f}"
        for value
        in robustness_map.columns
    ]
)


plt.yticks(

    np.arange(
        len(
            robustness_map.index
        )
    ),

    [
        f"{value:.2f}"
        for value
        in robustness_map.index
    ]
)


plt.xlabel(
    "Nominal Gust Preview Time (s)"
)

plt.ylabel(
    "Nominal Sensor / Processing Delay (s)"
)

plt.title(
    "HART-120 — Robust GLA Controller Design Map"
)

plt.tight_layout()
plt.show()


# ============================================================
# 6. CURRENT VS REDESIGNED CONTROLLER
# ============================================================

metric_names = [

    "Absolute\nload",

    "Envelope\n10% GLA",

    "Actuator\nlimit",

    "Joint\nrequirement"
]


current_rates = [

    absolute_pass_rate,

    relative_envelope_pass_rate,

    actuator_pass_rate,

    joint_pass_rate
]


redesigned_rates = [

    new_absolute_pass,

    new_relative_pass,

    new_actuator_pass,

    new_joint_pass
]


x = np.arange(
    len(metric_names)
)

bar_width = 0.36


plt.figure(
    figsize=(9, 6)
)


plt.bar(

    x - bar_width/2,

    current_rates,

    bar_width,

    label="Current Selected Controller"
)


plt.bar(

    x + bar_width/2,

    redesigned_rates,

    bar_width,

    label="Robustly Redesigned Controller"
)


plt.axhline(

    robust_design_target_percent,

    linestyle="--",

    linewidth=2,

    label="95% Project Robustness Objective"
)


plt.xticks(
    x,
    metric_names
)

plt.ylabel(
    "Monte Carlo Pass Rate (%)"
)

plt.title(
    "HART-120 — Effect of Robust Controller Redesign"
)

plt.grid(
    True,
    axis="y"
)

plt.legend()

plt.tight_layout()
plt.show()


# ============================================================
# 7. FINAL ENVELOPE-REDUCTION DISTRIBUTION
# ============================================================

plt.figure(
    figsize=(8, 5)
)


plt.hist(

    final_robust_df[
        "Envelope_Reduction_%"
    ],

    bins=25,

    alpha=0.8
)


plt.axvline(

    relative_GLA_target_percent,

    linestyle="--",

    linewidth=2,

    label="10% Envelope GLA Target"
)


plt.axvline(

    new_p05_reduction,

    linestyle=":",

    linewidth=2,

    label=(
        f"5th percentile = "
        f"{new_p05_reduction:.2f}%"
    )
)


plt.xlabel(
    "Envelope Root-Moment Reduction (%)"
)

plt.ylabel(
    "Monte Carlo Cases"
)

plt.title(
    "HART-120 — Robustly Redesigned GLA Performance"
)

plt.legend()
plt.tight_layout()
plt.show()

# %% [notebook cell 109]
# ============================================================
# HART-120 — TECHNOLOGY MASS & SYSTEM-LEVEL DESIGN CLOSURE
#
# INDUSTRIAL QUESTION
# -------------------
# Does the selected AR 15.5 technology wing still provide
# an aircraft-level benefit after accounting for:
#
#   - fail-safe structural sizing
#   - GLA / MLA system mass
#   - aircraft weight increase
#   - weight-coupled cruise aerodynamics
#   - mission fuel burn
#   - robust controller performance
#
# This is a reduced-order conceptual system-closure study.
# ============================================================


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. REFERENCE AIRCRAFT
# ------------------------------------------------------------

baseline_aircraft_mass = 55000.0       # kg
baseline_wingbox_mass = 4802.19        # kg

AR_baseline = 13.5
AR_technology = 15.5

span_baseline = 39.13                  # m
span_technology = 41.93                # m


# ------------------------------------------------------------
# 2. TECHNOLOGY STRUCTURAL MASSES
#
# Values obtained from the previous HART-120 analyses.
# ------------------------------------------------------------

nominal_technology_wingbox_mass = 6084.03   # kg
failsafe_wingbox_mass = 6143.69             # kg

structural_mass_budget = 6242.85             # kg
mass_budget_increase_percent = 30.0


# ------------------------------------------------------------
# 3. CONCEPTUAL GLA / MLA SYSTEM MASS BREAKDOWN
#
# IMPORTANT:
# These are PROJECT-LEVEL conceptual assumptions,
# NOT production-aircraft hardware mass claims.
#
# The previous mission analysis used 75 kg total system mass.
# We now explicitly distribute that mass into subsystems.
# ------------------------------------------------------------

system_mass_breakdown = {

    "Forward gust sensor / mounting":
        12.0,

    "Flight-control computing":
        7.0,

    "Actuator hardware increment":
        26.0,

    "Power electronics":
        8.0,

    "Wiring / communication":
        7.0,

    "Redundancy / integration allowance":
        15.0
}


mla_system_mass = sum(
    system_mass_breakdown.values()
)


# ------------------------------------------------------------
# 4. SYSTEM MASS ALLOWANCE
# ------------------------------------------------------------

maximum_system_mass_allowance = (
    structural_mass_budget
    - failsafe_wingbox_mass
)

system_mass_margin = (
    maximum_system_mass_allowance
    - mla_system_mass
)


realistic_technology_package_mass = (
    failsafe_wingbox_mass
    + mla_system_mass
)


structural_budget_margin = (
    structural_mass_budget
    - realistic_technology_package_mass
)


# ------------------------------------------------------------
# 5. AIRCRAFT MASS COUPLING
#
# Replace baseline wingbox by technology package.
# ------------------------------------------------------------

nominal_technology_aircraft_mass = (

    baseline_aircraft_mass

    - baseline_wingbox_mass

    + nominal_technology_wingbox_mass
)


realistic_technology_aircraft_mass = (

    baseline_aircraft_mass

    - baseline_wingbox_mass

    + realistic_technology_package_mass
)


realistic_aircraft_mass_increase = (

    realistic_technology_aircraft_mass
    - baseline_aircraft_mass
)


realistic_aircraft_mass_increase_percent = (

    realistic_aircraft_mass_increase
    / baseline_aircraft_mass

) * 100


# ------------------------------------------------------------
# 6. CRUISE AERODYNAMIC MODEL
# ------------------------------------------------------------

rho_cruise = 0.364                    # kg/m^3
V_cruise = 224.20                     # m/s
S_wing = 113.42                       # m^2

oswald_e = 0.85

CD0 = 0.020

g = 9.81


dynamic_pressure = (

    0.5
    * rho_cruise
    * V_cruise**2
)


# ------------------------------------------------------------
# 7. FUNCTION — CRUISE PERFORMANCE
# ------------------------------------------------------------

def calculate_cruise_performance(
    aircraft_mass,
    aspect_ratio
):

    weight = (
        aircraft_mass
        * g
    )

    CL = (

        weight

        /
        (
            dynamic_pressure
            * S_wing
        )
    )

    CDi = (

        CL**2

        /
        (
            np.pi
            * oswald_e
            * aspect_ratio
        )
    )

    parasite_drag = (

        dynamic_pressure
        * S_wing
        * CD0
    )

    induced_drag = (

        dynamic_pressure
        * S_wing
        * CDi
    )

    total_drag = (

        parasite_drag
        + induced_drag
    )

    L_over_D = (

        weight
        / total_drag
    )

    return {

        "CL":
            CL,

        "Induced_Drag_N":
            induced_drag,

        "Parasite_Drag_N":
            parasite_drag,

        "Total_Drag_N":
            total_drag,

        "L_over_D":
            L_over_D
    }


# ------------------------------------------------------------
# 8. BASELINE / NOMINAL / REALISTIC AERODYNAMICS
# ------------------------------------------------------------

baseline_aero = calculate_cruise_performance(
    baseline_aircraft_mass,
    AR_baseline
)


nominal_tech_aero = calculate_cruise_performance(
    nominal_technology_aircraft_mass,
    AR_technology
)


realistic_tech_aero = calculate_cruise_performance(
    realistic_technology_aircraft_mass,
    AR_technology
)


# ------------------------------------------------------------
# 9. MISSION FUEL MODEL
#
# Jet Breguet-style cruise fuel model.
# ------------------------------------------------------------

study_range_km = 3000.0

study_range_m = (
    study_range_km
    * 1000
)

effective_TSFC = 1.70e-4               # 1/s


def calculate_cruise_fuel(
    aircraft_mass,
    L_over_D
):

    fuel_fraction = (

        1

        - np.exp(

            -study_range_m
            * effective_TSFC

            /
            (
                V_cruise
                * L_over_D
            )
        )
    )

    fuel_mass = (

        aircraft_mass
        * fuel_fraction
    )

    return (
        fuel_fraction,
        fuel_mass
    )


baseline_fuel_fraction, baseline_fuel_mass = (
    calculate_cruise_fuel(
        baseline_aircraft_mass,
        baseline_aero[
            "L_over_D"
        ]
    )
)


nominal_fuel_fraction, nominal_fuel_mass = (
    calculate_cruise_fuel(
        nominal_technology_aircraft_mass,
        nominal_tech_aero[
            "L_over_D"
        ]
    )
)


realistic_fuel_fraction, realistic_fuel_mass = (
    calculate_cruise_fuel(
        realistic_technology_aircraft_mass,
        realistic_tech_aero[
            "L_over_D"
        ]
    )
)


realistic_fuel_saving = (

    baseline_fuel_mass
    - realistic_fuel_mass
)


realistic_fuel_saving_percent = (

    realistic_fuel_saving
    / baseline_fuel_mass

) * 100


induced_drag_reduction_percent = (

    (
        baseline_aero[
            "Induced_Drag_N"
        ]

        - realistic_tech_aero[
            "Induced_Drag_N"
        ]
    )

    /
    baseline_aero[
        "Induced_Drag_N"
    ]

) * 100


total_drag_reduction_percent = (

    (
        baseline_aero[
            "Total_Drag_N"
        ]

        - realistic_tech_aero[
            "Total_Drag_N"
        ]
    )

    /
    baseline_aero[
        "Total_Drag_N"
    ]

) * 100


LD_improvement_percent = (

    (
        realistic_tech_aero[
            "L_over_D"
        ]

        - baseline_aero[
            "L_over_D"
        ]
    )

    /
    baseline_aero[
        "L_over_D"
    ]

) * 100


# ------------------------------------------------------------
# 10. ROBUST CONTROLLER RESULTS
#
# Latest full-physics verification.
# ------------------------------------------------------------

selected_preview_time = 0.060          # s

equivalent_sensing_distance = 13.45    # m

selected_sensor_delay = 0.040          # s


absolute_load_pass_rate = 93.67        # %

envelope_GLA_pass_rate = 100.00        # %

actuator_pass_rate = 100.00            # %

joint_robustness_pass_rate = 93.67     # %


fifth_percentile_GLA = 12.66           # %

controlled_envelope_95th = 3.735       # MN*m

controlled_load_target = 3.729         # MN*m


project_robustness_objective = 95.0    # %


# ------------------------------------------------------------
# 11. SYSTEM-LEVEL DESIGN GATES
# ------------------------------------------------------------

structural_mass_pass = (

    realistic_technology_package_mass
    <= structural_mass_budget
)


system_mass_pass = (

    mla_system_mass
    <= maximum_system_mass_allowance
)


fuel_benefit_pass = (

    realistic_fuel_saving_percent
    > 0.0
)


relative_GLA_pass = (

    envelope_GLA_pass_rate
    >= project_robustness_objective
)


actuator_pass = (

    actuator_pass_rate
    >= project_robustness_objective
)


joint_robustness_pass = (

    joint_robustness_pass_rate
    >= project_robustness_objective
)


robust_absolute_load_pass = (

    controlled_envelope_95th
    <= controlled_load_target
)


overall_system_closure = all([

    structural_mass_pass,

    system_mass_pass,

    fuel_benefit_pass,

    relative_GLA_pass,

    actuator_pass,

    joint_robustness_pass,

    robust_absolute_load_pass
])


# ------------------------------------------------------------
# 12. CONFIGURATION COMPARISON TABLE
# ------------------------------------------------------------

configuration_table = pd.DataFrame({

    "Configuration": [

        "AR 13.5 Conventional",

        "AR 15.5 Nominal Technology",

        "AR 15.5 Fail-Safe + Control System"
    ],

    "Aspect_Ratio": [

        AR_baseline,

        AR_technology,

        AR_technology
    ],

    "Aircraft_Mass_kg": [

        baseline_aircraft_mass,

        nominal_technology_aircraft_mass,

        realistic_technology_aircraft_mass
    ],

    "Structural_Package_Mass_kg": [

        baseline_wingbox_mass,

        nominal_technology_wingbox_mass,

        realistic_technology_package_mass
    ],

    "Cruise_CL": [

        baseline_aero[
            "CL"
        ],

        nominal_tech_aero[
            "CL"
        ],

        realistic_tech_aero[
            "CL"
        ]
    ],

    "Induced_Drag_kN": [

        baseline_aero[
            "Induced_Drag_N"
        ] / 1000,

        nominal_tech_aero[
            "Induced_Drag_N"
        ] / 1000,

        realistic_tech_aero[
            "Induced_Drag_N"
        ] / 1000
    ],

    "Total_Drag_kN": [

        baseline_aero[
            "Total_Drag_N"
        ] / 1000,

        nominal_tech_aero[
            "Total_Drag_N"
        ] / 1000,

        realistic_tech_aero[
            "Total_Drag_N"
        ] / 1000
    ],

    "L_over_D": [

        baseline_aero[
            "L_over_D"
        ],

        nominal_tech_aero[
            "L_over_D"
        ],

        realistic_tech_aero[
            "L_over_D"
        ]
    ],

    "Cruise_Fuel_kg": [

        baseline_fuel_mass,

        nominal_fuel_mass,

        realistic_fuel_mass
    ]
})


# ------------------------------------------------------------
# 13. DESIGN-GATE TABLE
# ------------------------------------------------------------

design_gate_table = pd.DataFrame({

    "Design_Gate": [

        "Structural mass budget",

        "GLA system mass allowance",

        "Positive mission fuel benefit",

        "Envelope >=10% GLA robustness",

        "Actuator robustness",

        "Joint robustness >=95%",

        "95th-percentile absolute load target"
    ],

    "Pass": [

        structural_mass_pass,

        system_mass_pass,

        fuel_benefit_pass,

        relative_GLA_pass,

        actuator_pass,

        joint_robustness_pass,

        robust_absolute_load_pass
    ]
})


# ------------------------------------------------------------
# 14. PRINT RESULTS
# ------------------------------------------------------------

print()
print(
    "HART-120 — TECHNOLOGY MASS & SYSTEM CLOSURE"
)
print(
    "-------------------------------------------"
)

print()
print(
    "SYSTEM MASS ACCOUNTING"
)
print(
    "----------------------"
)

for subsystem, subsystem_mass in system_mass_breakdown.items():

    print(
        f"{subsystem:<38s}: "
        f"{subsystem_mass:6.2f} kg"
    )


print()
print(
    f"Total conceptual MLA/GLA system mass: "
    f"{mla_system_mass:.2f} kg"
)

print(
    f"Maximum allowable system mass: "
    f"{maximum_system_mass_allowance:.2f} kg"
)

print(
    f"System mass margin: "
    f"{system_mass_margin:.2f} kg"
)


print()
print(
    "STRUCTURAL PACKAGE"
)
print(
    "------------------"
)

print(
    f"Baseline AR 13.5 wingbox: "
    f"{baseline_wingbox_mass:.2f} kg"
)

print(
    f"AR 15.5 nominal technology wingbox: "
    f"{nominal_technology_wingbox_mass:.2f} kg"
)

print(
    f"AR 15.5 fail-safe wingbox: "
    f"{failsafe_wingbox_mass:.2f} kg"
)

print(
    f"Fail-safe wingbox + control system: "
    f"{realistic_technology_package_mass:.2f} kg"
)

print(
    f"Structural mass budget: "
    f"{structural_mass_budget:.2f} kg"
)

print(
    f"Remaining structural mass margin: "
    f"{structural_budget_margin:.2f} kg"
)


print()
print(
    "AIRCRAFT-LEVEL EFFECT"
)
print(
    "---------------------"
)

print(
    f"Baseline aircraft mass: "
    f"{baseline_aircraft_mass:.2f} kg"
)

print(
    f"Technology aircraft mass: "
    f"{realistic_technology_aircraft_mass:.2f} kg"
)

print(
    f"Aircraft mass increase: "
    f"{realistic_aircraft_mass_increase:.2f} kg"
)

print(
    f"Aircraft mass increase: "
    f"{realistic_aircraft_mass_increase_percent:.2f} %"
)


print()
print(
    "AERODYNAMIC CLOSURE"
)
print(
    "-------------------"
)

print(
    f"Induced-drag reduction: "
    f"{induced_drag_reduction_percent:.2f} %"
)

print(
    f"Total cruise-drag reduction: "
    f"{total_drag_reduction_percent:.2f} %"
)

print(
    f"Baseline L/D: "
    f"{baseline_aero['L_over_D']:.2f}"
)

print(
    f"Technology L/D: "
    f"{realistic_tech_aero['L_over_D']:.2f}"
)

print(
    f"L/D improvement: "
    f"{LD_improvement_percent:.2f} %"
)


print()
print(
    "MISSION CLOSURE"
)
print(
    "---------------"
)

print(
    f"Study cruise range: "
    f"{study_range_km:.0f} km"
)

print(
    f"Baseline cruise fuel: "
    f"{baseline_fuel_mass:.2f} kg"
)

print(
    f"Technology cruise fuel: "
    f"{realistic_fuel_mass:.2f} kg"
)

print(
    f"Net cruise fuel saving: "
    f"{realistic_fuel_saving:.2f} kg"
)

print(
    f"Net cruise fuel saving: "
    f"{realistic_fuel_saving_percent:.2f} %"
)


print()
print(
    "ROBUST GLA CLOSURE"
)
print(
    "------------------"
)

print(
    f"Preview time: "
    f"{selected_preview_time:.3f} s"
)

print(
    f"Equivalent sensing distance: "
    f"{equivalent_sensing_distance:.2f} m"
)

print(
    f"Sensor / processing delay: "
    f"{selected_sensor_delay:.3f} s"
)

print(
    f"Envelope >=10% GLA pass rate: "
    f"{envelope_GLA_pass_rate:.2f} %"
)

print(
    f"Joint robustness pass rate: "
    f"{joint_robustness_pass_rate:.2f} %"
)

print(
    f"5th-percentile envelope GLA: "
    f"{fifth_percentile_GLA:.2f} %"
)

print(
    f"95th-percentile controlled load: "
    f"{controlled_envelope_95th:.3f} MN·m"
)

print(
    f"Project controlled-load target: "
    f"{controlled_load_target:.3f} MN·m"
)


print()
print(
    "CONFIGURATION COMPARISON"
)
print(
    "------------------------"
)

print(
    configuration_table
    .round(3)
    .to_string(
        index=False
    )
)


print()
print(
    "SYSTEM DESIGN GATES"
)
print(
    "-------------------"
)

print(
    design_gate_table
    .to_string(
        index=False
    )
)


print()
print(
    "FINAL SYSTEM STATUS"
)
print(
    "-------------------"
)

if overall_system_closure:

    print(
        "PASS — HART-120 AR 15.5 satisfies all current "
        "project-level system closure requirements."
    )

else:

    print(
        "NOT FULLY CLOSED — the AR 15.5 concept retains "
        "an aerodynamic / mission benefit, but at least one "
        "robustness or system constraint remains unresolved."
    )


# ============================================================
# 15. PLOT — SYSTEM MASS BREAKDOWN
# ============================================================

plt.figure(
    figsize=(10, 5)
)

plt.bar(
    list(
        system_mass_breakdown.keys()
    ),
    list(
        system_mass_breakdown.values()
    )
)

plt.ylabel(
    "Conceptual System Mass (kg)"
)

plt.title(
    "HART-120 AR 15.5 — Conceptual GLA / MLA System Mass Breakdown"
)

plt.xticks(
    rotation=30,
    ha="right"
)

plt.grid(
    True,
    axis="y"
)

plt.tight_layout()

plt.show()


# ============================================================
# 16. PLOT — SYSTEM-MASS BREAK-EVEN
# ============================================================

system_mass_sweep = np.linspace(
    0,
    150,
    151
)


package_mass_sweep = (

    failsafe_wingbox_mass
    + system_mass_sweep
)


plt.figure(
    figsize=(9, 5)
)

plt.plot(
    system_mass_sweep,
    package_mass_sweep,
    linewidth=2,
    label="Fail-safe wingbox + control system"
)

plt.axhline(
    structural_mass_budget,
    linestyle="--",
    label="+30% structural mass budget"
)

plt.axvline(
    maximum_system_mass_allowance,
    linestyle=":",
    label=(
        f"Break-even = "
        f"{maximum_system_mass_allowance:.1f} kg"
    )
)

plt.scatter(
    [mla_system_mass],
    [realistic_technology_package_mass],
    s=90,
    label=(
        f"Reference system = "
        f"{mla_system_mass:.0f} kg"
    )
)

plt.xlabel(
    "GLA / MLA System Mass (kg)"
)

plt.ylabel(
    "Technology Structural Package Mass (kg)"
)

plt.title(
    "HART-120 AR 15.5 — Technology System Mass Closure"
)

plt.grid(
    True
)

plt.legend()

plt.tight_layout()

plt.show()


# ============================================================
# 17. PLOT — CONFIGURATION MASS COMPARISON
# ============================================================

plt.figure(
    figsize=(9, 5)
)

plt.bar(

    configuration_table[
        "Configuration"
    ],

    configuration_table[
        "Structural_Package_Mass_kg"
    ]
)

plt.axhline(
    structural_mass_budget,
    linestyle="--",
    label="+30% structural mass budget"
)

plt.ylabel(
    "Structural / Technology Package Mass (kg)"
)

plt.title(
    "HART-120 — Structural Technology Accounting"
)

plt.xticks(
    rotation=15,
    ha="right"
)

plt.legend()

plt.grid(
    True,
    axis="y"
)

plt.tight_layout()

plt.show()


# ============================================================
# 18. PLOT — CRUISE FUEL COMPARISON
# ============================================================

plt.figure(
    figsize=(9, 5)
)

plt.bar(

    configuration_table[
        "Configuration"
    ],

    configuration_table[
        "Cruise_Fuel_kg"
    ]
)

plt.ylabel(
    "Estimated 3000-km Cruise Fuel (kg)"
)

plt.title(
    "HART-120 — Mission Fuel After Technology-System Accounting"
)

plt.xticks(
    rotation=15,
    ha="right"
)

plt.grid(
    True,
    axis="y"
)

plt.tight_layout()

plt.show()

# %% [notebook cell 110]
# ============================================================
# HART-120 — FAST FINAL CONTROLLER MICRO-TUNING
#
# Goal:
# Recover the small remaining robustness margin without
# redesigning the aircraft or running another huge search.
#
# Screening only:
#   4 nearby controllers
#   80 common Monte Carlo cases
#   5 critical gust gradients
#
# The winner will later receive one full 300-case verification.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Candidate controllers
# ------------------------------------------------------------

controller_candidates = pd.DataFrame({

    "Controller": [
        "Current",
        "More preview",
        "Lower delay",
        "Preview + lower delay"
    ],

    "Preview_Time_s": [
        0.060,
        0.070,
        0.060,
        0.070
    ],

    "Sensor_Delay_s": [
        0.040,
        0.040,
        0.030,
        0.030
    ]
})


# ------------------------------------------------------------
# 2. Fast-screening setup
#
# Same uncertainty realizations are used for every controller.
# This is important: differences then come from controller
# design, not different random samples.
# ------------------------------------------------------------

n_screen_cases = 80

H_screen_values = np.array([
    20.0,
    30.0,
    40.0,
    50.0,
    60.0
])

physical_target_MNm = (
    4.143
    * 0.90
)

relative_target_percent = 10.0

surface_limit_deg = 15.0


# ------------------------------------------------------------
# 3. Screen candidates
# ------------------------------------------------------------

screening_results = []


print(
    "Running HART-120 final controller micro-screen..."
)


for candidate_index, candidate in controller_candidates.iterrows():

    preview_nominal = candidate[
        "Preview_Time_s"
    ]

    delay_nominal = candidate[
        "Sensor_Delay_s"
    ]


    absolute_passes = []

    relative_passes = []

    actuator_passes = []

    joint_passes = []

    controlled_peaks = []

    envelope_reductions = []


    for sample_index in range(
        n_screen_cases
    ):

        damping_sample = (
            damping_samples[
                sample_index
            ]
        )

        frequency_scale = (
            frequency_scale_samples[
                sample_index
            ]
        )

        gust_amplitude_scale = (
            gust_amplitude_scale_samples[
                sample_index
            ]
        )

        control_effectiveness_scale = (
            control_effectiveness_scale_samples[
                sample_index
            ]
        )


        tau_sample = (
            selected_tau
            * tau_scale_samples[
                sample_index
            ]
        )


        rate_sample = (
            selected_rate
            * rate_scale_samples[
                sample_index
            ]
        )


        delay_sample = max(

            0.0,

            delay_nominal
            + delay_error_samples[
                sample_index
            ]
        )


        preview_sample = max(

            0.0,

            preview_nominal
            + preview_error_samples[
                sample_index
            ]
        )


        uncontrolled_envelope = []

        controlled_envelope = []

        actuator_envelope = []


        for H_test in H_screen_values:

            result = simulate_uncertain_gust_pair(

                H_test,

                damping_sample,

                frequency_scale,

                gust_amplitude_scale,

                control_effectiveness_scale,

                tau_sample,

                delay_sample,

                rate_sample,

                preview_sample
            )


            uncontrolled_envelope.append(

                result[
                    "Peak_Uncontrolled_MNm"
                ]
            )


            controlled_envelope.append(

                result[
                    "Peak_Controlled_MNm"
                ]
            )


            actuator_envelope.append(

                result[
                    "Peak_Actuator_Deflection_deg"
                ]
            )


        uncontrolled_peak = np.max(
            uncontrolled_envelope
        )

        controlled_peak = np.max(
            controlled_envelope
        )


        envelope_reduction = (

            1.0

            -

            controlled_peak
            / uncontrolled_peak

        ) * 100.0


        absolute_pass = (
            controlled_peak
            <= physical_target_MNm
        )


        relative_pass = (
            envelope_reduction
            >= relative_target_percent
        )


        actuator_pass = (

            np.max(
                np.abs(
                    actuator_envelope
                )
            )

            <= surface_limit_deg
        )


        joint_pass = (

            absolute_pass
            and relative_pass
            and actuator_pass
        )


        absolute_passes.append(
            absolute_pass
        )

        relative_passes.append(
            relative_pass
        )

        actuator_passes.append(
            actuator_pass
        )

        joint_passes.append(
            joint_pass
        )

        controlled_peaks.append(
            controlled_peak
        )

        envelope_reductions.append(
            envelope_reduction
        )


    absolute_pass_rate = (
        np.mean(
            absolute_passes
        )
        * 100
    )


    relative_pass_rate = (
        np.mean(
            relative_passes
        )
        * 100
    )


    actuator_pass_rate = (
        np.mean(
            actuator_passes
        )
        * 100
    )


    joint_pass_rate = (
        np.mean(
            joint_passes
        )
        * 100
    )


    p95_controlled = np.percentile(
        controlled_peaks,
        95
    )


    p05_reduction = np.percentile(
        envelope_reductions,
        5
    )


    screening_results.append({

        "Controller":
            candidate[
                "Controller"
            ],

        "Preview_Time_s":
            preview_nominal,

        "Sensor_Delay_s":
            delay_nominal,

        "Absolute_Pass_%":
            absolute_pass_rate,

        "Envelope_GLA_Pass_%":
            relative_pass_rate,

        "Actuator_Pass_%":
            actuator_pass_rate,

        "Joint_Pass_%":
            joint_pass_rate,

        "P95_Controlled_Moment_MNm":
            p95_controlled,

        "P05_Envelope_Reduction_%":
            p05_reduction
    })


    print(
        f"{candidate['Controller']:<24s}"
        f" | Joint = {joint_pass_rate:6.2f} %"
        f" | P95 load = {p95_controlled:.3f} MN·m"
        f" | P05 GLA = {p05_reduction:.2f} %"
    )


controller_screen_df = pd.DataFrame(
    screening_results
)


# ------------------------------------------------------------
# 4. Selection logic
#
# Require:
#   >=95% joint robustness
#   >=10% fifth-percentile envelope GLA
#   P95 load <= physical target
#
# Among successful candidates choose the smallest modification.
# ------------------------------------------------------------

controller_screen_df[
    "Meets_Final_Target"
] = (

    (
        controller_screen_df[
            "Joint_Pass_%"
        ]
        >= 95.0
    )

    &

    (
        controller_screen_df[
            "P05_Envelope_Reduction_%"
        ]
        >= 10.0
    )

    &

    (
        controller_screen_df[
            "P95_Controlled_Moment_MNm"
        ]
        <= physical_target_MNm
    )
)


# Simple deviation from current controller
controller_screen_df[
    "Design_Change_Index"
] = (

    np.abs(
        controller_screen_df[
            "Preview_Time_s"
        ]
        - 0.060
    ) / 0.010

    +

    np.abs(
        controller_screen_df[
            "Sensor_Delay_s"
        ]
        - 0.040
    ) / 0.010
)


successful_candidates = (
    controller_screen_df[
        controller_screen_df[
            "Meets_Final_Target"
        ]
    ]
)


if len(
    successful_candidates
) > 0:

    best_screened_controller = (

        successful_candidates
        .sort_values(
            [
                "Design_Change_Index",
                "P95_Controlled_Moment_MNm"
            ]
        )
        .iloc[0]
    )

else:

    best_screened_controller = (

        controller_screen_df
        .sort_values(
            [
                "Joint_Pass_%",
                "P95_Controlled_Moment_MNm"
            ],

            ascending=[
                False,
                True
            ]
        )
        .iloc[0]
    )


# ------------------------------------------------------------
# 5. Results
# ------------------------------------------------------------

print()
print(
    "HART-120 FINAL CONTROLLER MICRO-SCREEN"
)
print(
    "--------------------------------------"
)

print(
    controller_screen_df
    .round(3)
    .to_string(
        index=False
    )
)


print()
print(
    "BEST SCREENED CONTROLLER"
)
print(
    "------------------------"
)

print(
    f"Controller: "
    f"{best_screened_controller['Controller']}"
)

print(
    f"Preview time: "
    f"{best_screened_controller['Preview_Time_s']:.3f} s"
)

print(
    f"Equivalent sensing distance: "
    f"{best_screened_controller['Preview_Time_s'] * V_cruise:.2f} m"
)

print(
    f"Sensor delay: "
    f"{best_screened_controller['Sensor_Delay_s']:.3f} s"
)

print(
    f"Joint robustness: "
    f"{best_screened_controller['Joint_Pass_%']:.2f} %"
)

print(
    f"95th-percentile controlled load: "
    f"{best_screened_controller['P95_Controlled_Moment_MNm']:.3f} MN·m"
)

print(
    f"5th-percentile envelope GLA: "
    f"{best_screened_controller['P05_Envelope_Reduction_%']:.2f} %"
)

print(
    f"Meets final screening target: "
    f"{best_screened_controller['Meets_Final_Target']}"
)


# ------------------------------------------------------------
# 6. Plot — robustness comparison
# ------------------------------------------------------------

plt.figure(
    figsize=(9, 5)
)

plt.bar(

    controller_screen_df[
        "Controller"
    ],

    controller_screen_df[
        "Joint_Pass_%"
    ]
)

plt.axhline(
    95.0,
    linestyle="--",
    label="95% project robustness objective"
)

plt.ylabel(
    "Joint Robustness Pass Rate (%)"
)

plt.title(
    "HART-120 — Final Controller Micro-Tuning"
)

plt.xticks(
    rotation=15,
    ha="right"
)

plt.grid(
    True,
    axis="y"
)

plt.legend()

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 7. Plot — absolute load robustness
# ------------------------------------------------------------

plt.figure(
    figsize=(9, 5)
)

plt.bar(

    controller_screen_df[
        "Controller"
    ],

    controller_screen_df[
        "P95_Controlled_Moment_MNm"
    ]
)

plt.axhline(
    physical_target_MNm,
    linestyle="--",
    label=(
        f"Controlled-load target = "
        f"{physical_target_MNm:.3f} MN·m"
    )
)

plt.ylabel(
    "95th-Percentile Controlled Root Moment (MN·m)"
)

plt.title(
    "HART-120 — Absolute Gust-Load Robustness"
)

plt.xticks(
    rotation=15,
    ha="right"
)

plt.grid(
    True,
    axis="y"
)

plt.legend()

plt.tight_layout()

plt.show()

# %% [notebook cell 111]
# ============================================================
# HART-120 — FINAL FULL-PHYSICS ROBUSTNESS VERIFICATION
#
# Final candidate:
#   Preview = 0.070 s
#   Delay   = 0.040 s
#
# Full verification:
#   300 uncertainty realizations
#   full 20-point gust-gradient envelope
#
# This is the FINAL robustness gate.
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Final controller
# ------------------------------------------------------------

final_preview = 0.070
final_delay = 0.040

final_sensing_distance = (
    final_preview
    * V_cruise
)

physical_target_MNm = (
    4.143
    * 0.90
)

relative_GLA_target_percent = 10.0
surface_deflection_limit_deg = 15.0


print(
    "HART-120 FINAL CONTROLLER"
)

print(
    "-------------------------"
)

print(
    f"Preview time: "
    f"{final_preview:.3f} s"
)

print(
    f"Equivalent sensing distance: "
    f"{final_sensing_distance:.2f} m"
)

print(
    f"Sensor / processing delay: "
    f"{final_delay:.3f} s"
)

print(
    f"Effective timing lead: "
    f"{final_preview - final_delay:.3f} s"
)

print(
    f"Controlled-load target: "
    f"{physical_target_MNm:.3f} MN·m"
)


# ------------------------------------------------------------
# 2. Full verification
# ------------------------------------------------------------

n_final_cases = min(
    300,
    len(damping_samples)
)

final_results = []


print()
print(
    "Running FINAL 300-case full-physics verification..."
)


for sample_index in range(
    n_final_cases
):

    damping_sample = (
        damping_samples[
            sample_index
        ]
    )

    frequency_scale = (
        frequency_scale_samples[
            sample_index
        ]
    )

    gust_amplitude_scale = (
        gust_amplitude_scale_samples[
            sample_index
        ]
    )

    control_effectiveness_scale = (
        control_effectiveness_scale_samples[
            sample_index
        ]
    )


    tau_sample = (
        selected_tau
        * tau_scale_samples[
            sample_index
        ]
    )


    rate_sample = (
        selected_rate
        * rate_scale_samples[
            sample_index
        ]
    )


    delay_sample = max(

        0.0,

        final_delay
        + delay_error_samples[
            sample_index
        ]
    )


    preview_sample = max(

        0.0,

        final_preview
        + preview_error_samples[
            sample_index
        ]
    )


    uncontrolled_envelope = []
    controlled_envelope = []
    actuator_envelope = []
    root_stress_envelope = []
    tip_deflection_envelope = []


    for H_test in H_robust_values:

        result = simulate_uncertain_gust_pair(

            H_test,

            damping_sample,

            frequency_scale,

            gust_amplitude_scale,

            control_effectiveness_scale,

            tau_sample,

            delay_sample,

            rate_sample,

            preview_sample
        )


        uncontrolled_envelope.append(

            result[
                "Peak_Uncontrolled_MNm"
            ]
        )


        controlled_envelope.append(

            result[
                "Peak_Controlled_MNm"
            ]
        )


        actuator_envelope.append(

            result[
                "Peak_Actuator_Deflection_deg"
            ]
        )


        root_stress_envelope.append(

            result[
                "Peak_Root_Stress_MPa"
            ]
        )


        tip_deflection_envelope.append(

            result[
                "Peak_Tip_Deflection_m"
            ]
        )


    uncontrolled_envelope = np.array(
        uncontrolled_envelope
    )

    controlled_envelope = np.array(
        controlled_envelope
    )

    actuator_envelope = np.array(
        actuator_envelope
    )


    uncontrolled_peak = np.max(
        uncontrolled_envelope
    )

    controlled_peak = np.max(
        controlled_envelope
    )


    envelope_reduction = (

        1.0

        -

        controlled_peak
        / uncontrolled_peak

    ) * 100.0


    critical_controlled_index = np.argmax(
        controlled_envelope
    )


    critical_uncontrolled_index = np.argmax(
        uncontrolled_envelope
    )


    absolute_pass = (
        controlled_peak
        <= physical_target_MNm
    )


    relative_pass = (
        envelope_reduction
        >= relative_GLA_target_percent
    )


    actuator_peak = np.max(
        np.abs(
            actuator_envelope
        )
    )


    actuator_pass = (
        actuator_peak
        <= surface_deflection_limit_deg
    )


    joint_pass = (

        absolute_pass
        and relative_pass
        and actuator_pass
    )


    final_results.append({

        "Case":
            sample_index + 1,

        "Uncontrolled_Envelope_Peak_MNm":
            uncontrolled_peak,

        "Controlled_Envelope_Peak_MNm":
            controlled_peak,

        "Envelope_GLA_%":
            envelope_reduction,

        "Critical_Uncontrolled_H_m":
            H_robust_values[
                critical_uncontrolled_index
            ],

        "Critical_Controlled_H_m":
            H_robust_values[
                critical_controlled_index
            ],

        "Maximum_Root_Stress_MPa":
            np.max(
                root_stress_envelope
            ),

        "Maximum_Tip_Deflection_m":
            np.max(
                tip_deflection_envelope
            ),

        "Maximum_Actuator_Deflection_deg":
            actuator_peak,

        "Absolute_Load_Pass":
            absolute_pass,

        "Envelope_GLA_Pass":
            relative_pass,

        "Actuator_Pass":
            actuator_pass,

        "Joint_Pass":
            joint_pass
    })


    if (
        (sample_index + 1) % 50
        == 0
    ):

        print(
            f"Verified "
            f"{sample_index + 1} / "
            f"{n_final_cases}"
        )


final_verification_df = pd.DataFrame(
    final_results
)


# ------------------------------------------------------------
# 3. Robustness statistics
# ------------------------------------------------------------

absolute_pass_rate = (

    final_verification_df[
        "Absolute_Load_Pass"
    ]
    .mean()
    * 100
)


relative_pass_rate = (

    final_verification_df[
        "Envelope_GLA_Pass"
    ]
    .mean()
    * 100
)


actuator_pass_rate = (

    final_verification_df[
        "Actuator_Pass"
    ]
    .mean()
    * 100
)


joint_pass_rate = (

    final_verification_df[
        "Joint_Pass"
    ]
    .mean()
    * 100
)


p95_controlled = np.percentile(

    final_verification_df[
        "Controlled_Envelope_Peak_MNm"
    ],

    95
)


p99_controlled = np.percentile(

    final_verification_df[
        "Controlled_Envelope_Peak_MNm"
    ],

    99
)


p05_GLA = np.percentile(

    final_verification_df[
        "Envelope_GLA_%"
    ],

    5
)


mean_GLA = (

    final_verification_df[
        "Envelope_GLA_%"
    ]
    .mean()
)


worst_controlled = (

    final_verification_df[
        "Controlled_Envelope_Peak_MNm"
    ]
    .max()
)


worst_case_index = (

    final_verification_df[
        "Controlled_Envelope_Peak_MNm"
    ]
    .idxmax()
)


worst_case = (

    final_verification_df.loc[
        worst_case_index
    ]
)


# ------------------------------------------------------------
# 4. Final decision
# ------------------------------------------------------------

final_controller_closed = (

    joint_pass_rate
    >= 95.0

    and

    p05_GLA
    >= 10.0

    and

    p95_controlled
    <= physical_target_MNm

    and

    actuator_pass_rate
    >= 95.0
)


print()
print(
    "HART-120 FINAL CONTROLLER — FULL VERIFICATION"
)

print(
    "---------------------------------------------"
)

print(
    f"Monte Carlo cases: "
    f"{n_final_cases}"
)

print(
    f"Gust gradients per case: "
    f"{len(H_robust_values)}"
)

print(
    f"Total gust cases: "
    f"{n_final_cases * len(H_robust_values):,}"
)

print()

print(
    "ROBUSTNESS PASS RATES"
)

print(
    "---------------------"
)

print(
    f"Absolute load pass rate: "
    f"{absolute_pass_rate:.2f} %"
)

print(
    f"Envelope >=10% GLA pass rate: "
    f"{relative_pass_rate:.2f} %"
)

print(
    f"Actuator pass rate: "
    f"{actuator_pass_rate:.2f} %"
)

print(
    f"Joint robustness pass rate: "
    f"{joint_pass_rate:.2f} %"
)

print()

print(
    "STATISTICAL MARGINS"
)

print(
    "-------------------"
)

print(
    f"Mean envelope GLA: "
    f"{mean_GLA:.2f} %"
)

print(
    f"5th-percentile envelope GLA: "
    f"{p05_GLA:.2f} %"
)

print(
    f"95th-percentile controlled load: "
    f"{p95_controlled:.3f} MN·m"
)

print(
    f"99th-percentile controlled load: "
    f"{p99_controlled:.3f} MN·m"
)

print(
    f"Worst observed controlled load: "
    f"{worst_controlled:.3f} MN·m"
)

print()

print(
    "MOST ADVERSE REALIZATION"
)

print(
    "------------------------"
)

print(
    f"Uncontrolled envelope peak: "
    f"{worst_case['Uncontrolled_Envelope_Peak_MNm']:.3f} MN·m"
)

print(
    f"Controlled envelope peak: "
    f"{worst_case['Controlled_Envelope_Peak_MNm']:.3f} MN·m"
)

print(
    f"Envelope GLA: "
    f"{worst_case['Envelope_GLA_%']:.2f} %"
)

print(
    f"Critical controlled gust H: "
    f"{worst_case['Critical_Controlled_H_m']:.1f} m"
)

print(
    f"Maximum root stress: "
    f"{worst_case['Maximum_Root_Stress_MPa']:.2f} MPa"
)

print(
    f"Maximum tip deflection: "
    f"{worst_case['Maximum_Tip_Deflection_m']:.3f} m"
)

print(
    f"Maximum actuator deflection: "
    f"{worst_case['Maximum_Actuator_Deflection_deg']:.2f} deg"
)

print()

print(
    "FINAL HART-120 ROBUSTNESS GATE"
)

print(
    "------------------------------"
)

print(
    f"Final controller closed: "
    f"{final_controller_closed}"
)


if final_controller_closed:

    print()
    print(
        "PASS — robust GLA controller satisfies "
        "the HART-120 project-level design objectives."
    )

else:

    print()
    print(
        "NOT CLOSED — at least one full-physics "
        "robustness objective remains unresolved."
    )


# ------------------------------------------------------------
# 5. Plot — controlled load distribution
# ------------------------------------------------------------

plt.figure(
    figsize=(9, 5)
)

plt.hist(

    final_verification_df[
        "Controlled_Envelope_Peak_MNm"
    ],

    bins=20
)

plt.axvline(

    physical_target_MNm,

    linestyle="--",

    label=(
        f"Project load target = "
        f"{physical_target_MNm:.3f} MN·m"
    )
)

plt.axvline(

    p95_controlled,

    linestyle=":",

    label=(
        f"95th percentile = "
        f"{p95_controlled:.3f} MN·m"
    )
)

plt.xlabel(
    "Controlled Gust-Envelope Peak Root Moment (MN·m)"
)

plt.ylabel(
    "Monte Carlo Cases"
)

plt.title(
    "HART-120 — Final Robust Controlled-Load Distribution"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 6. Plot — envelope GLA distribution
# ------------------------------------------------------------

plt.figure(
    figsize=(9, 5)
)

plt.hist(

    final_verification_df[
        "Envelope_GLA_%"
    ],

    bins=20
)

plt.axvline(

    10.0,

    linestyle="--",

    label="10% envelope GLA target"
)

plt.axvline(

    p05_GLA,

    linestyle=":",

    label=(
        f"5th percentile = "
        f"{p05_GLA:.2f}%"
    )
)

plt.xlabel(
    "Envelope Root-Moment Reduction (%)"
)

plt.ylabel(
    "Monte Carlo Cases"
)

plt.title(
    "HART-120 — Final Robust GLA Performance"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()


# ------------------------------------------------------------
# 7. Plot — final design gates
# ------------------------------------------------------------

final_gate_names = [

    "Absolute\nload",
    "Envelope\n10% GLA",
    "Actuator\nlimit",
    "Joint\nrequirement"
]

final_gate_values = [

    absolute_pass_rate,
    relative_pass_rate,
    actuator_pass_rate,
    joint_pass_rate
]


plt.figure(
    figsize=(8, 5)
)

plt.bar(
    final_gate_names,
    final_gate_values
)

plt.axhline(

    95.0,

    linestyle="--",

    label="95% project robustness objective"
)

plt.ylabel(
    "Monte Carlo Pass Rate (%)"
)

plt.ylim(
    0,
    105
)

plt.title(
    "HART-120 — Final System Robustness Closure"
)

plt.grid(
    True,
    axis="y"
)

plt.legend()

plt.tight_layout()

plt.show()

# %% [notebook cell 112]
# ============================================================
# HART-120 — FINAL PROJECT CLOSURE
#
# Frozen project-level configuration after:
# aerodynamic, structural, aeroelastic, load-alleviation,
# ML-surrogate, fail-safe, mission and robustness studies.
#
# Reduced-order conceptual design study.
# NOT certification-level aircraft analysis.
# ============================================================

import pandas as pd
import numpy as np


# ------------------------------------------------------------
# 1. FINAL CONFIGURATION
# ------------------------------------------------------------

final_config = {
    "Baseline_Aspect_Ratio": 13.5,
    "Final_Aspect_Ratio": 15.5,

    "Baseline_Span_m": 39.13,
    "Final_Span_m": 41.93,

    "Baseline_Aircraft_Mass_kg": 55000.00,
    "Final_Aircraft_Mass_kg": 56416.50,

    "Static_Aeroelastic_Tip_Twist_deg": -1.769,
    "Static_Root_Moment_Reduction_pct": 4.43,

    "Baseline_Wingbox_Mass_kg": 4802.19,
    "Conventional_AR15p5_Wingbox_Mass_kg": 6629.17,

    "Nominal_Technology_Wingbox_Mass_kg": 6084.03,
    "FailSafe_Wingbox_Mass_kg": 6143.69,

    "GLA_MLA_System_Mass_kg": 75.00,
    "Final_Structural_Control_Package_kg": 6218.69,

    "Structural_Mass_Budget_kg": 6242.85,

    "Induced_Drag_Reduction_pct": 8.36,
    "Total_Cruise_Drag_Reduction_pct": 2.28,

    "Baseline_L_over_D": 18.91,
    "Technology_L_over_D": 19.85,

    "Cruise_Range_km": 3000.0,

    "Baseline_Cruise_Fuel_kg": 6234.17,
    "Technology_Cruise_Fuel_kg": 6109.06,

    "Preview_Time_s": 0.070,
    "Sensor_Delay_s": 0.040,

    "Controlled_Load_Target_MNm": 3.729,

    "Mean_Envelope_GLA_pct": 15.79,
    "P05_Envelope_GLA_pct": 13.81,

    "P95_Controlled_Root_Moment_MNm": 3.687,
    "P99_Controlled_Root_Moment_MNm": 3.775,
    "Worst_Controlled_Root_Moment_MNm": 3.807,

    "Absolute_Load_Pass_pct": 98.0,
    "Envelope_GLA_Pass_pct": 100.0,
    "Actuator_Pass_pct": 100.0,
    "Joint_Robustness_pct": 98.0,

    "Maximum_Root_Stress_MPa": 159.87,
    "Maximum_Dynamic_Tip_Deflection_m": 1.679,
    "Maximum_Actuator_Deflection_deg": 13.89
}


# ------------------------------------------------------------
# 2. DERIVED FINAL METRICS
# ------------------------------------------------------------

final_config["Aspect_Ratio_Increase_pct"] = (
    (
        final_config["Final_Aspect_Ratio"]
        / final_config["Baseline_Aspect_Ratio"]
        - 1.0
    )
    * 100.0
)

final_config["Span_Increase_pct"] = (
    (
        final_config["Final_Span_m"]
        / final_config["Baseline_Span_m"]
        - 1.0
    )
    * 100.0
)

final_config["Aircraft_Mass_Increase_kg"] = (
    final_config["Final_Aircraft_Mass_kg"]
    - final_config["Baseline_Aircraft_Mass_kg"]
)

final_config["Aircraft_Mass_Increase_pct"] = (
    final_config["Aircraft_Mass_Increase_kg"]
    / final_config["Baseline_Aircraft_Mass_kg"]
    * 100.0
)

final_config["Structural_Mass_Margin_kg"] = (
    final_config["Structural_Mass_Budget_kg"]
    - final_config["Final_Structural_Control_Package_kg"]
)

final_config["AR15p5_Final_Package_Saving_vs_Conventional_pct"] = (
    (
        final_config["Conventional_AR15p5_Wingbox_Mass_kg"]
        - final_config["Final_Structural_Control_Package_kg"]
    )
    /
    final_config["Conventional_AR15p5_Wingbox_Mass_kg"]
    * 100.0
)

final_config["L_over_D_Improvement_pct"] = (
    (
        final_config["Technology_L_over_D"]
        / final_config["Baseline_L_over_D"]
        - 1.0
    )
    * 100.0
)

final_config["Cruise_Fuel_Saving_kg"] = (
    final_config["Baseline_Cruise_Fuel_kg"]
    - final_config["Technology_Cruise_Fuel_kg"]
)

final_config["Cruise_Fuel_Saving_pct"] = (
    final_config["Cruise_Fuel_Saving_kg"]
    /
    final_config["Baseline_Cruise_Fuel_kg"]
    * 100.0
)

final_config["Effective_Timing_Lead_s"] = (
    final_config["Preview_Time_s"]
    - final_config["Sensor_Delay_s"]
)

final_config["P95_Load_Margin_MNm"] = (
    final_config["Controlled_Load_Target_MNm"]
    - final_config["P95_Controlled_Root_Moment_MNm"]
)

final_config["Actuator_Deflection_Margin_deg"] = (
    15.0
    - final_config["Maximum_Actuator_Deflection_deg"]
)


# ------------------------------------------------------------
# 3. FINAL ENGINEERING DASHBOARD
# ------------------------------------------------------------

final_dashboard = pd.DataFrame({

    "Metric": [
        "Aspect ratio",
        "Wing span",
        "Aircraft mass",
        "Structural + control package",
        "Structural budget margin",
        "Induced-drag reduction",
        "Total cruise-drag reduction",
        "L/D improvement",
        "3000-km cruise fuel saving",
        "Static aeroelastic tip twist",
        "Mean envelope GLA",
        "5th-percentile envelope GLA",
        "95th-percentile controlled root moment",
        "Controlled-load target",
        "Absolute load robustness",
        "Envelope >=10% GLA robustness",
        "Actuator robustness",
        "Joint robustness",
        "Maximum actuator deflection"
    ],

    "Baseline_or_Limit": [
        "13.5",
        "39.13 m",
        "55,000 kg",
        "4,802.19 kg baseline",
        "> 0 kg",
        "0 %",
        "0 %",
        "18.91 L/D",
        "0 kg",
        "0 deg rigid reference",
        ">= 10 %",
        ">= 10 %",
        "< 3.729 MN·m",
        "3.729 MN·m",
        ">= 95 %",
        ">= 95 %",
        ">= 95 %",
        ">= 95 %",
        "<= 15 deg"
    ],

    "Final_Result": [
        "15.5",
        "41.93 m",
        "56,416.50 kg",
        "6,218.69 kg",
        f"{final_config['Structural_Mass_Margin_kg']:.2f} kg",
        "8.36 %",
        "2.28 %",
        f"{final_config['L_over_D_Improvement_pct']:.2f} %",
        f"{final_config['Cruise_Fuel_Saving_kg']:.2f} kg "
        f"({final_config['Cruise_Fuel_Saving_pct']:.2f} %)",
        "-1.769 deg",
        "15.79 %",
        "13.81 %",
        "3.687 MN·m",
        "3.729 MN·m",
        "98.0 %",
        "100.0 %",
        "100.0 %",
        "98.0 %",
        "13.89 deg"
    ],

    "Status": [
        "FINAL",
        "FINAL",
        "FINAL",
        "PASS",
        "PASS",
        "BENEFIT",
        "BENEFIT",
        "BENEFIT",
        "BENEFIT",
        "RESULT",
        "PASS",
        "PASS",
        "PASS",
        "PROJECT TARGET",
        "PASS",
        "PASS",
        "PASS",
        "PASS",
        "PASS"
    ]
})


print()
print("HART-120 — FINAL ENGINEERING DESIGN CLOSURE")
print("-------------------------------------------")
print()

print(
    final_dashboard.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# 4. FINAL PROJECT GATES
# ------------------------------------------------------------

final_gates = pd.DataFrame({

    "Design_Gate": [
        "Structural package within +30% mass budget",
        "Positive induced-drag benefit",
        "Positive total cruise-drag benefit",
        "Positive 3000-km mission fuel benefit",
        "P05 envelope GLA >= 10%",
        "P95 controlled load below project target",
        "Absolute load robustness >= 95%",
        "Envelope GLA robustness >= 95%",
        "Actuator robustness >= 95%",
        "Joint robustness >= 95%"
    ],

    "Pass": [
        final_config["Final_Structural_Control_Package_kg"]
        <= final_config["Structural_Mass_Budget_kg"],

        final_config["Induced_Drag_Reduction_pct"] > 0,

        final_config["Total_Cruise_Drag_Reduction_pct"] > 0,

        final_config["Cruise_Fuel_Saving_kg"] > 0,

        final_config["P05_Envelope_GLA_pct"] >= 10.0,

        final_config["P95_Controlled_Root_Moment_MNm"]
        <= final_config["Controlled_Load_Target_MNm"],

        final_config["Absolute_Load_Pass_pct"] >= 95.0,

        final_config["Envelope_GLA_Pass_pct"] >= 95.0,

        final_config["Actuator_Pass_pct"] >= 95.0,

        final_config["Joint_Robustness_pct"] >= 95.0
    ]
})


print()
print("FINAL DESIGN GATES")
print("------------------")
print(
    final_gates.to_string(
        index=False
    )
)


project_closed = final_gates["Pass"].all()


print()
print("FINAL HART-120 STATUS")
print("---------------------")

if project_closed:

    print(
        "PASS — HART-120 satisfies all defined "
        "project-level conceptual design gates."
    )

else:

    print(
        "OPEN — one or more project-level "
        "design gates remain unresolved."
    )
