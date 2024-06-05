import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scraping import obtener_datos
from decorators import log_execution, time_execution

# URL base de ejemplo
url_base = "https://sommiercenter.com/mega-ofertas"

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
    # Reemplazar valores 'N/A' por NaN
    df.replace('N/A', np.nan, inplace=True)
    
    # Eliminar filas con valores faltantes en las columnas 'PRECIO' y 'PRECIO DE PROMOCION'
    df_limpio = df.dropna(subset=['PRECIO', 'PRECIO DE PROMOCION'])
    
    # Limpiar y convertir precios a formato numérico, eliminando caracteres no deseados
    df_limpio['PRECIO'] = df_limpio['PRECIO'].str.replace(r'[$\.\xa0]', '', regex=True).astype(float)
    df_limpio['PRECIO DE PROMOCION'] = df_limpio['PRECIO DE PROMOCION'].str.replace(r'[$\.\xa0]', '', regex=True).astype(float)
    
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
def leer_datos_csv(filename):
    return pd.read_csv(filename)

@log_execution
@time_execution
def guardar_datos_excel(df, filename):
    df.to_excel(filename, index=False)

@log_execution
@time_execution
def leer_datos_excel(filename):
    return pd.read_excel(filename)

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
datos = obtener_datos(url_base, num_paginas=5)
df = crear_dataframe(datos)
df_limpio = limpiar_datos(df)
precio_promedio = calcular_precio_promedio(df_limpio)
guardar_datos(df_limpio, 'REPORTE.csv')
guardar_datos_excel(df_limpio, 'REPORTE.xlsx')
analisis_descriptivo(df_limpio)
df_limpio = calcular_descuentos(df_limpio)
mostrar_producto_extremos(df_limpio)
graficar_precios(df_limpio)

# Leer datos desde los archivos para verificar
df_csv = leer_datos_csv('REPORTE.csv')
df_excel = leer_datos_excel('REPORTE.xlsx')

# Imprimir los DataFrames leídos
print("Datos leídos desde CSV:")
print(df_csv.head())

print("Datos leídos desde Excel:")
print(df_excel.head())

# Imprimir el DataFrame con precios numéricos
print(df_limpio)
