import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scrapping import obtener_datos

url = "https://sommiercenter.com/almohadas"

# Obtener los datos de "scrapping.py"
datos = obtener_datos(url)

# Crear un DF con los datos extraídos
df = pd.DataFrame({
    'PRODUCTO': datos['nombres_productos'],
    'PRECIO': datos['precios'],
    'PRECIO DE PROMOCION': datos['precios_promo'],
    'DISPONIBILIDAD': datos['disponibilidad']
})

# Limpiar datos
df.replace('N/A', np.nan, inplace=True)
df_limpio = df.dropna(subset=['PRECIO', 'PRECIO DE PROMOCION'])

# Convertir precios a formato numérico
df_limpio['PRECIO'] = df_limpio['PRECIO'].str.replace('$', '').astype(float)
df_limpio['PRECIO DE PROMOCION'] = df_limpio['PRECIO DE PROMOCION'].str.replace('$', '').astype(float)

# Calcular el precio promedio de los productos disponibles
precio_promedio = df_limpio[df_limpio['DISPONIBILIDAD'] == 'Disponible']['PRECIO'].mean()

# Guardar en un archivo CSV
df_limpio.to_csv('datos_productos_limpios.csv', index=False)
print(df_limpio)

# Análisis Descriptivo
print("Resumen Estadístico:")
print(df_limpio.describe())

# Descuento Promedio
df_limpio['DESCUENTO'] = df_limpio['PRECIO'] - df_limpio['PRECIO DE PROMOCION']
df_limpio['PORCENTAJE DE DESCUENTO'] = (df_limpio['DESCUENTO'] / df_limpio['PRECIO']) * 100
descuento_promedio = df_limpio['PORCENTAJE DE DESCUENTO'].mean()
print(f"\nDescuento Promedio: {descuento_promedio:.2f}%")

# Producto con mayor y menor descuento
producto_mayor_descuento = df_limpio.loc[df_limpio['PORCENTAJE DE DESCUENTO'].idxmax()]
producto_menor_descuento = df_limpio.loc[df_limpio['PORCENTAJE DE DESCUENTO'].idxmin()]

print("\nProducto con Mayor Descuento:")
print(producto_mayor_descuento[['PRODUCTO', 'PRECIO', 'PRECIO DE PROMOCION', 'PORCENTAJE DE DESCUENTO']])

print("\nProducto con Menor Descuento:")
print(producto_menor_descuento[['PRODUCTO', 'PRECIO', 'PRECIO DE PROMOCION', 'PORCENTAJE DE DESCUENTO']])

# Gráfica de Barras de Precios
plt.figure(figsize=(14, 7))
df_limpio.plot(kind='bar', x='PRODUCTO', y=['PRECIO', 'PRECIO DE PROMOCION'], figsize=(14, 7))
plt.ylabel('Precio')
plt.title('Comparación de Precios y Precios de Promoción')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()