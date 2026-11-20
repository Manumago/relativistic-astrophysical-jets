"""Independent numerical checks for the 2025 single-electron jet model.

This reproduces the stated initial parameters with physical constants from
scipy.constants, without requiring the course-specific pymcel package.
It tests dynamical conservation and integration stability, not the accuracy
of the assumed radiation or magnetic-field model.
"""
from __future__ import annotations
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants
from scipy.integrate import solve_ivp


q = -constants.e
m = constants.m_e
c = constants.c
B0 = 5.0e-4  # T: 5 Gauss
B1 = 0.3e-4  # T*m: 0.3 Gauss*m (since B_phi = B1/r)
gamma0 = 30.0
R0 = 1.0  # m
r_min = 0.01  # m, denominator regularization

def magnetic_field(x, y):
    r2 = max(x*x + y*y, r_min*r_min)
    return np.array([-B1*y/r2, B1*x/r2, B0], dtype=float)


def rhs(tau, state):
    # X=(t,x,y,z,ux,uy,uz), ux,uy,uz = gamma*velocity [m/s].
    _, x, y, _, ux, uy, uz = state
    u = np.array([ux, uy, uz])
    gamma = np.sqrt(1.0 + np.dot(u, u)/c**2)
    dudtau = (q/m)*np.cross(u, magnetic_field(x, y))
    return np.array([gamma, *u, *dudtau])


tau_end = 5e-6
sample_times = np.linspace(0.0, tau_end, 2000)
v0z = c*np.sqrt(1.0 - 1.0/gamma0**2)
y0 = np.array([0.0, R0, 0.0, 0.0, 0.0, 0.0, gamma0*v0z])

sol = solve_ivp(rhs, (0, tau_end), y0, t_eval=sample_times,
                method='DOP853', rtol=1e-9, atol=1e-12)
if not sol.success or sol.y.shape[1] != len(sample_times):
    raise RuntimeError(f'Integration failed: {sol.message}')
sol_ref = solve_ivp(rhs, (0, tau_end), y0, t_eval=sample_times,
                    method='DOP853', rtol=1e-11, atol=1e-13,
                    max_step=1.0e-8)
if not sol_ref.success:
    raise RuntimeError(f'Reference integration failed: {sol_ref.message}')

coordinate_time, x, y, z, ux, uy, uz = sol.y
u = sol.y[4:7].T
gammas = np.sqrt(1 + np.sum(u**2, axis=1)/c**2)
B = np.array([magnetic_field(xi, yi) for xi, yi in zip(x, y)])
a = (q/m)*np.cross(u, B)

# Dimensionless relative checks: much more meaningful than raw U·A.
relative_gamma_drift = np.max(np.abs(gammas/gamma0 - 1.0))
relative_u2_drift = np.max(np.abs(np.sum(u**2, axis=1)/np.sum(u[0]**2) - 1.0))
gamma_ref = np.sqrt(1.0 + np.sum(sol_ref.y[4:7]**2, axis=0)/c**2)
relative_gamma_drift_ref = np.max(np.abs(gamma_ref/gamma0 - 1.0))

# t(tau) = gamma0*tau as gamma0 is conserved for a purely magnetic field.
relative_time_error = np.max(np.abs(coordinate_time - gamma0*sample_times))/(gamma0*tau_end)
radial_dist = np.hypot(x, y)

# Orthogonality is identically true for the continuous RHS.  Evaluate the
# numerical dot product relative to the norms at each time.
ua_spatial = np.sum(u*a, axis=1)
angle_error = np.max(np.abs(ua_spatial) / (np.linalg.norm(u, axis=1) * np.linalg.norm(a, axis=1)))

# Direct trajectory comparisons between integration tolerances.
r = sol.y[1:4]
r_ref = sol_ref.y[1:4]
position_diff_abs = np.linalg.norm((r-r_ref).T, axis=1)
max_position_difference_m = np.max(position_diff_abs)
max_position_difference_scaled = max_position_difference_m/max(np.ptp(z), 1)

# Test discrete speed gamma relationship and magnetic work rate.
speed_ratio = np.linalg.norm(u/gammas[:,None], axis=1)/c
max_speed_ratio = np.max(speed_ratio)

# Distinct observables: azimuth about jet axis vs local gyrofrequency.
angle = np.unwrap(np.arctan2(y, x))
f_azimuth = np.abs(np.gradient(angle, coordinate_time))/(2*np.pi)
f_local_gyro = abs(q)*np.linalg.norm(B, axis=1)/(2*np.pi*m*gammas)

# Test boost E' against analytic formula in one representative simulation point.
k = len(sample_times)//2
v = u[k]/gammas[k]
beta = v/c
g = gammas[k]
Lam = np.eye(4)
Lam[0,0] = g
Lam[0,1:] = -g*beta
Lam[1:,0] = -g*beta
Lam[1:,1:] = np.eye(3) + (g*g/(g+1))*np.outer(beta, beta)
Bx,By,Bz = B[k]
F = np.array([[0,0,0,0], [0,0,-Bz,By], [0,Bz,0,-Bx], [0,-By,Bx,0]])
Fp = Lam @ F @ Lam.T
Ep = -c * Fp[0,1:]
Bp = np.array([-Fp[2,3], Fp[1,3], -Fp[1,2]])
E_target = g*np.cross(v,B[k])
vhat = v/np.linalg.norm(v)
Bpara = np.dot(B[k],vhat)*vhat
B_target = Bpara + g*(B[k]-Bpara)
E_diff = np.linalg.norm(Ep - E_target)/np.linalg.norm(E_target)
B_diff = np.linalg.norm(Bp - B_target)/np.linalg.norm(B_target)

metrics = dict(
    integration_success=bool(sol.success),
    reference_integration_success=bool(sol_ref.success),
    gamma0=gamma0,
    max_relative_gamma_drift=relative_gamma_drift,
    max_relative_gamma_drift_tighter_solver=relative_gamma_drift_ref,
    max_relative_u_squared_drift=relative_u2_drift,
    max_relative_coordinate_time_error=relative_time_error,
    max_relative_spatial_u_dot_du_orthogonality=angle_error,
    max_v_over_c=max_speed_ratio,
    min_radius_m=float(radial_dist.min()),
    cutoff_radius_m=r_min,
    max_position_discrepancy_between_solvers_m=max_position_difference_m,
    max_position_discrepancy_as_fraction_of_z_extent=max_position_difference_scaled,
    mean_azimuthal_axis_frequency_hz=float(np.mean(f_azimuth)),
    mean_local_gyrofrequency_hz=float(np.mean(f_local_gyro)),
    E_boost_relative_difference=E_diff,
    B_boost_relative_difference=B_diff,
    scipy_version=__import__('scipy').__version__,
    numpy_version=np.__version__,
)

path=Path(__file__).resolve().parent
(path/'validation_metrics.json').write_text(json.dumps(metrics, indent=2, ensure_ascii=False)+'\n')
print(json.dumps(metrics, indent=2, ensure_ascii=False))

# Original figure replacement? no. This is an *additional* validation figure.
fig, (ax1, ax2) = plt.subplots(2,1,figsize=(8.3,7),constrained_layout=True)
ax1.plot(coordinate_time, gammas/gamma0-1.0,lw=1,color='tab:blue')
ax1.set(xlabel='Coordinate time t [s]',ylabel=r'$\gamma/\gamma_0-1$',title='Conservation of Lorentz factor (relative drift)')
ax1.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
ax1.grid(alpha=0.25)
ax2.plot(coordinate_time,f_azimuth/1e3,label=r'$|d\varphi/dt|/(2\pi)$: rotation about jet axis',color='tab:orange')
ax2.plot(coordinate_time,f_local_gyro/1e3,label=r'$|q|B/(2\pi\gamma m_e)$: local gyrofrequency',color='tab:purple')
ax2.set(xlabel='Coordinate time t [s]',ylabel='Frequency [kHz]',title='Two distinct angular observables (not equivalent)')
ax2.legend(fontsize=9)
ax2.grid(alpha=0.25)
fig.savefig(path/'independent_numerical_validation.png',dpi=160)
plt.close(fig)
