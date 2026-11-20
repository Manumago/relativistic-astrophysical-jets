# Breve explicación teórica: electrones en un jet astrofísico

Este proyecto modela el movimiento de **un electrón** en un campo magnético helicoidal idealizado; no representa todo el plasma del jet.

**Campo magnético.** Se considera un campo sin componente eléctrica, compuesto por una parte paralela al eje del jet y otra que rodea dicho eje:

$$\mathbf B=B_0\hat{\mathbf e}_z+\frac{B_1}{r}\hat{\mathbf e}_{\phi}. $$

La componente toroidal cambia con la distancia al eje. El código introduce un radio mínimo para evitar una singularidad numérica cerca de $r=0$.

**Dinámica relativista.** Definiendo $\mathbf u=\gamma\mathbf v$ y usando el tiempo propio $\tau$, la fuerza de Lorentz se expresa como

$$\frac{d\mathbf u}{d\tau}=\frac{q}{m_e}(\mathbf u\times\mathbf B),\qquad \frac{dt}{d\tau}=\gamma=\sqrt{1+\frac{|\mathbf u|^2}{c^2}}.$$

La integración se realiza con `solve_ivp` de SciPy. Al ser un campo puramente magnético, la energía de la partícula se conserva en el modelo ideal, y también se puede comprobar $U^\mu A_\mu=0$.

**Emisión sincrotrón.** El campo hace que el electrón cambie de dirección y, por tanto, acelere. Una frecuencia característica de la emisión es

$$f_c=\frac{3|q|B_\perp\gamma^2}{4\pi m_e},$$

donde $B_\perp$ es la componente de $\mathbf B$ perpendicular a la velocidad del electrón. El código calcula también una estimación de la frecuencia del máximo espectral, $f_{\rm peak}\approx0.29f_c$.

**Beaming relativista.** Para un observador en dirección $\hat{\mathbf n}$, el factor Doppler es

$$\delta=\frac{1}{\gamma(1-\boldsymbol\beta\cdot\hat{\mathbf n})},\qquad \boldsymbol\beta=\mathbf v/c.$$

El notebook emplea una aproximación de intensidad relativa $I_\nu\propto\delta^3$ y un cono geométrico idealizado de apertura $\sim1/\gamma$ para explorar cómo cambia la señal con el ángulo de observación. No se calcula transferencia radiativa completa.

**Precaución:** el método original que deriva una «frecuencia de giro experimental» de $\mathrm{atan2}(y,x)$ mide la variación azimutal alrededor del eje del jet, no necesariamente la girofrecuencia local alrededor de $\mathbf B$. Antes de interpretar esa comparación como una validación física hay que revisarla.


## Comprobaciones numéricas independientes (noviembre de 2026)\n\nSe reprodujo la integración con `solve_ivp` en un archivo separado (`validation/validate_jets.py`) y se comprobó que el factor de Lorentz se conserva con una desviación relativa máxima de $2.27\\times10^{-11}$, que disminuye a $2.99\\times10^{-13}$ con tolerancias más exigentes. Esto es una comprobación de consistencia numérica del modelo, no una validación de todos sus supuestos físicos.\n\nSe comprobó también la relación $t\\simeq\\gamma_0\\tau$ y las transformaciones de $\\mathbf E$ y $\\mathbf B$ al sistema instantáneo del electrón. En este modelo $B_1$ tiene dimensiones de campo por longitud (T·m) cuando $B_\\phi=B_1/r$.\n\nLa frecuencia $|d\\varphi/dt|/(2\\pi)$ describe una rotación **alrededor del eje del jet**, mientras que $|q|B/(2\\pi\\gamma m_e)$ es la frecuencia local de giro en un campo aproximadamente uniforme. Ambas cantidades no tienen que coincidir.\n\nPara las curvas de *beaming*, una comparación de amplitudes entre ángulos exige normalizar las curvas con una **referencia común**; normalizar cada una por su máximo impide esa comparación. La versión revisada del notebook usa una sola referencia para todos los ángulos.\n