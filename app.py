import streamlit as st
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

st.title("Optimización de Resistencias y Capacitores")

st.write("Maximización de producción usando programación lineal")

st.write("### Variables:")
st.write("x1, x2, x3 = resistencias")
st.write("x4, x5, x6 = capacitores")

if st.button("Calcular solución óptima"):

    # Función objetivo (maximizar → ponemos negativo)
    c = [-2, -3, -5, -4, -6, -8]

    # Restricciones
    A = [
        [1,1,1,0,0,0],        # resistencias ≤ 1000
        [0,0,0,1,1,1],        # capacitores ≤ 800
        [0.5,0.7,0.9,0.8,1.0,1.2],  # tiempo ≤ 2000
        [0.01,0.015,0.02,0.05,0.08,0.1], # material ≤ 50
        [-1,-1,0,0,1,1]       # restricción combinada
    ]

    bu = [1000, 800, 2000, 50, 0]
    bl = [0, 0, 0, 0, 0]

    constraints = LinearConstraint(A, bl, bu)
    bounds = Bounds([0]*6, [np.inf]*6)

    res = milp(
        c=c,
        constraints=constraints,
        bounds=bounds,
        integrality=[0]*6
    )

    if res.success:
        st.success("Solución encontrada")

        for i, val in enumerate(res.x):
            st.write(f"x{i+1} =", val)

        st.write("Valor óptimo:", -res.fun)
    else:
        st.error("No se encontró solución")
