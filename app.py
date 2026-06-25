import streamlit as st
import numpy as np
from scipy.optimize import linprog

st.title("Optimización de producción de resistencias y condensadores")

st.write("Maximizar la ganancia total de la fábrica")

if st.button("Calcular solución óptima"):

    # Maximizar → se multiplica por -1
    c = [-2, -3, -5, -4, -6, -8]

    # Restricciones del problema (Ax <= b)
    A = [
        [1,1,1,0,0,0],                 # resistencias ≤ 1000
        [0,0,0,1,1,1],                 # condensadores ≤ 800
        [0.5,0.7,0.9,0.8,1.0,1.2],     # tiempo ≤ 2000
        [0.01,0.015,0.02,0.05,0.08,0.1], # material ≤ 50
        [-1,-1,0,1,1,1],              # x5+x6 ≤ x1+x2
    ]

    b = [1000, 800, 2000, 50, 0]

    bounds = [(0, None)] * 6

    res = linprog(
        c=c,
        A_ub=A,
        b_ub=b,
        bounds=bounds,
        method="highs"
    )

    if res.success:
        st.success("Solución encontrada")

        variables = ["x1 (1kΩ)", "x2 (10kΩ)", "x3 (100kΩ)",
                     "x4 (10µF)", "x5 (100µF)", "x6 (1000µF)"]

        for i, val in enumerate(res.x):
            st.write(f"{variables[i]} = {val:.2f}")

        st.write("Ganancia máxima:", -res.fun)

    else:
        st.error("No se encontró solución")
