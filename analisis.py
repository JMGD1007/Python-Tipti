import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scrapping import obtener_datos
from decorators import log_execution, time_execution

url = "https://sommiercenter.com/almohadas"

@log_execution
@time_execution
def crear_dataframe(datos):
    return pd.DataFrame({
        'PRODUCTO': datos['nombres_productos'],
        'PRECIO': datos['precios'],
        'PRECIO DE PROMOCION': datos['precios_promo'],
        'DISPONIBILIDAD': datos['disponibilidad']
    })

@log_execution
@time_execution
def limpiar_datos(df):
    df.replace('N/A', np.nan, inplace=True)
    df_limpio = df.dropna(subset=['PRECIO', 'PRECIO DE PROMOCION'])
    df_limpio['PRECIO'] = df_limpio['PRECIO'].str.replace('$', '').str.replace(',', '').astype(float)
    df_limpio['PRECIO DE PROMOCION'] = df_limpio['PRECIO DE PROMOCION'].str.replace('$', '').str.replace(',', '').astype(float)
    return df_limpio

@log_execution
@time_execution
def calcular_precio_promedio(df):
    return df[df['DISPONIBILIDAD'] == 'Disponible']['PRECIO'].mean()

@log_execution
@time_execution
def guardar_datos(df, filename):
    df.to_csv(filename, index=False)

@log_execution
@time_execution
def analisis_descriptivo(df):
    print("Resumen Estadístico:")
    print(df.describe())

@log_execution
@time_execution
def calcular_descuentos(df):
    df['DESCUENTO'] = df['PRECIO'] - df['PRECIO DE PROMOCION']
    df['PORCENTAJE DE DESCUENTO'] = (df['DESCUENTO'] / df['PRECIO']) * 100
    descuento_promedio = df['PORCENTAJE DE DESCUENTO'].mean()
    print(f"\nDescuento Promedio: {descuento_promedio:.2f}%")
    return df

@log_execution
@time_execution
def mostrar_producto_extremos(df):
    producto_mayor_descuento = df.loc[df['PORCENTAJE DE DESCUENTO'].idxmax()]
    producto_menor_descuento = df.loc[df['PORCENTAJE DE DESCUENTO'].idxmin()]

    print("\nProducto con Mayor Descuento:")
    print(producto_mayor_descuento[['PRODUCTO', 'PRECIO', 'PRECIO DE PROMOCION', 'PORCENTAJE DE DESCUENTO']])

    print("\nProducto con Menor Descuento:")
    print(producto_menor_descuento[['PRODUCTO', 'PRECIO', 'PRECIO DE PROMOCION', 'PORCENTAJE DE DESCUENTO']])

@log_execution
@time_execution
def graficar_precios(df):
    plt.figure(figsize=(14, 7))
    df.plot(kind='bar', x='PRODUCTO', y=['PRECIO', 'PRECIO DE PROMOCION'], figsize=(14, 7))
    plt.ylabel('Precio')
    plt.title('Comparación de Precios y Precios de Promoción')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Proceso completo
datos = obtener_datos(url)
df = crear_dataframe(datos)
df_limpio = limpiar_datos(df)
precio_promedio = calcular_precio_promedio(df_limpio)
guardar_datos(df_limpio, 'datos_productos_limpios.csv')
analisis_descriptivo(df_limpio)
df_limpio = calcular_descuentos(df_limpio)
mostrar_producto_extremos(df_limpio)
graficar_precios(df_limpio)

# Imprimir el DataFrame con precios numéricos
print(df_limpio)