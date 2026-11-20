# Review before publishing numerical claims

The notebook is preserved as a record of a 2025 computational assignment; no new results were generated during portfolio preparation.

1. **Azimuthal rate vs gyration rate.** `d(atan2(y,x))/dt` tracks rotation about the jet axis, not automatically the cyclotron motion about the *local magnetic field*. Its direct comparison with $|q|B/(2πγm)$ requires physical justification or a better diagnostic.
2. **Coordinate conventions.** Some explanatory markdown cells use natural units and SI inconsistently, and a few signs/indices are written incorrectly (for example, the invariant should be $U^μU_μ=c²$, and the correct time component has a **plus** sign in $γ=√(1+|u|²/c²)$). The equations in the README state the intended SI conventions.
3. **Field regularization.** $B_φ=B_1/r$ is singular at the axis; the denominator clamp is numerical, not physical. Units of $B_1$ must be treated consistently as field × length.
4. **Radiative model.** $I_ν∝δ³$ plus a hard cone cutoff is illustrative and depends on assumed emissivity/spectral index. No synchrotron emission integral or radiation-reaction energy losses are modeled.
5. **Reproducibility.** Run the notebook in a clean environment with compatible versions of `pymcel`, NumPy, SciPy, Matplotlib and Plotly; report versions and compare plots before removing this warning.
6. **Publishing coursework.** Confirm that course policies permit public distribution. If reusing visual resources or course diagrams, obtain rights/attribution first (original assignment text and images were excluded).
