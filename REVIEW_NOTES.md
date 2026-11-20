# Review notes and limitations (updated November 2026)

This is an **idealized one-electron dynamics and synchrotron-characteristic-frequency** study from a 2025 Relativity course at Universidad de Antioquia.

## Independently checked

1. A fresh integration of the stated system succeeded, including a tighter-tolerance second run. Lorentz-factor drift is below $2.3\\times10^{-11}$ in the baseline and $3.0\\times10^{-13}$ in the reference calculation. See `validation/validate_jets.py`.
2. The numerical relation $t=\\gamma_0\\tau$ was verified to high precision, consistent with energy conservation in a purely magnetic field.
3. The Lorentz-transformed $E'$ and $B'$ fields were checked against analytic formulas for a sampled trajectory point.
4. The trajectory in this parameter setup stays at $r\\ge 1$ m, safely outside the artificial cutoff $r_{\\min}=0.01$ m.
5. Notebook documentation now uses SI units with $B_1$ expressed as field times length (T·m), corrects the sign in $dt/d\\tau$, clarifies the gyration-vs-axis-rotation comparison, and uses a common relative-intensity normalization across viewing angles.

## Remaining physical/model limitations

- **Nonuniform helical field:** rotation of the projected position around the jet axis is not the local gyration around the magnetic-field direction. The frequency curves should not be interpreted as a theory/experiment discrepancy.
- **Radiation is not fully simulated:** the code computes characteristic synchrotron frequencies and schematic Doppler-boosted relative light curves, not the total synchrotron spectrum from a particle population, emissivity, or radiative transfer.
- **Radiation losses neglected:** particle dynamics treat the electron as moving in a fixed externally prescribed magnetic field with no synchrotron radiation-reaction force. This is a model assumption, not a demonstration that radiation carries no energy.
- **$B_\\phi=B_1/r$ singularity:** a denominator floor is numerical regularization and is not a resolved jet core model. At the chosen parameters the computed orbit never enters the cutoff region.
- **Geometric beaming gate:** imposing $\\psi\\le 1/\\gamma$ and $I\\propto\\delta^3$ is illustrative; real synchrotron angular emissivity and the appropriate Doppler exponent depend on the source and observable.
- **Coursework/reuse:** check any course rules concerning publication. The instructor-provided assignment text and any personal identification have been omitted. Cite external scientific sources and give credit for contributions.

## Reproducibility

Run `python -m pip install -r requirements.txt` then `python validation/validate_jets.py`. For the full original analysis, open `notebooks/jets_astrophysical.ipynb` and run all cells in the intended Python environment. Both the standalone validation script and all notebook code cells were executed successfully in the preparation environment. Run again in the target environment and compare diagnostic outputs.
