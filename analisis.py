import pandas as pd
import numpy as np
from scrapping import obtener_datos

# URL de ejemplo
url = "https://sommiercenter.com/almohadas"

# Obtener los datos usando la función importada
datos = obtener_datos(url)

# Crear un DataFrame con los datos extraídos
df = pd.DataFrame({
    'NOMBRE': datos['nombres_productos'],
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

# Guardar el df limpio en un archivo CSV
df_limpio.to_csv('datos_productos_limpios.csv', index=False)

# Imprimir el DataFrame con precios numéricos
print(df_limpio)