
import pandas as pd
import matplotlib.pyplot as plt
import os

# ── CARGA DEL DATASET ──────────────────────────────────────────────────────────
# Usamos la URL raw del gist para descargar directamente desde Google Colab.
# parse_dates convierte la columna sales_date a tipo datetime automáticamente,
# lo que nos permite agrupar por mes sin conversiones adicionales.
URL = "https://gist.githubusercontent.com/khanusama20/ee33c2869dd5cf3cebdf020be1ca43f6/raw/cbcbbb2651dd0b631d7bd194bc51b2fbb105d108/sales_sample_2024.csv"

df = pd.read_csv(URL, parse_dates=["sales_date"])

# Guardamos el dataset en /datos para cumplir con la estructura del repositorio
os.makedirs("datos", exist_ok=True)
df.to_csv("datos/dataset.csv", index=False)
print(f"Dataset cargado: {len(df)} registros")
print(df.head())

# ── INDICADORES ────────────────────────────────────────────────────────────────
# Ventas totales del año: suma de todos los montos del período
total = df["sales_amount"].sum()

# Promedio diario: útil para identificar si un mes estuvo por encima o debajo
promedio_diario = df["sales_amount"].mean()

# Día con mayor y menor venta: permite identificar picos y valles operativos
idx_max = df["sales_amount"].idxmax()
idx_min = df["sales_amount"].idxmin()
dia_max = df.loc[idx_max, "sales_date"].date()
dia_min = df.loc[idx_min, "sales_date"].date()
venta_max = df.loc[idx_max, "sales_amount"]
venta_min = df.loc[idx_min, "sales_amount"]

# Ventas por mes: agrupamos usando dt.to_period("M") para preservar año y mes
# juntos. Esto evita errores si el dataset abarcara más de un año.
df["mes"] = df["sales_date"].dt.to_period("M")
ventas_por_mes = df.groupby("mes")["sales_amount"].sum()
mes_mayor = ventas_por_mes.idxmax()
mes_menor = ventas_por_mes.idxmin()

print("\n── INDICADORES ──────────────────────────────")
print(f"Ventas totales 2024:      ${total:,.2f}")
print(f"Promedio diario de ventas: ${promedio_diario:,.2f}")
print(f"Día con mayor venta:       {dia_max} (${venta_max:,})")
print(f"Día con menor venta:       {dia_min} (${venta_min:,})")
print(f"Mes con mayor facturación: {mes_mayor} (${ventas_por_mes[mes_mayor]:,.2f})")
print(f"Mes con menor facturación: {mes_menor} (${ventas_por_mes[mes_menor]:,.2f})")

# ── GRÁFICO ────────────────────────────────────────────────────────────────────
# Graficamos la evolución mensual con barras para facilitar la comparación
# entre meses. La línea de promedio ayuda a visualizar desvíos respecto a
# la media anual, lo que es más informativo que las barras solas.
fig, ax = plt.subplots(figsize=(12, 5))

meses_str = [str(m) for m in ventas_por_mes.index]
ax.bar(meses_str, ventas_por_mes.values, color="steelblue", edgecolor="white", label="Ventas mensuales")
ax.axhline(ventas_por_mes.mean(), color="tomato", linestyle="--", linewidth=1.5, label=f"Promedio mensual (${ventas_por_mes.mean():,.0f})")

ax.set_title("Evolución de ventas mensuales — 2024", fontsize=14, fontweight="bold")
ax.set_xlabel("Mes")
ax.set_ylabel("Monto total ($)")
ax.tick_params(axis="x", rotation=45)
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Guardamos en /resultados con ruta relativa para garantizar reproducibilidad
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/grafico_ventas.png", dpi=150, bbox_inches="tight")
print("\n✓ Gráfico guardado en resultados/grafico_ventas.png")

# ── RESUMEN EN TEXTO ───────────────────────────────────────────────────────────
resumen = f"""RESUMEN DE ANÁLISIS DE VENTAS — 2024
=====================================
Total de registros:        {len(df)}
Período:                   01/01/2024 al 31/12/2024
Ventas totales:            ${total:,.2f}
Promedio diario de ventas: ${promedio_diario:,.2f}
Día con mayor venta:       {dia_max} (${venta_max:,})
Día con menor venta:       {dia_min} (${venta_min:,})
Mes con mayor facturación: {mes_mayor} (${ventas_por_mes[mes_mayor]:,.2f})
Mes con menor facturación: {mes_menor} (${ventas_por_mes[mes_menor]:,.2f})
=====================================
"""
with open("resultados/resumen_analisis.txt", "w") as f:
    f.write(resumen)
print(resumen)
