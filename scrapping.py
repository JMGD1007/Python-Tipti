import requests
from bs4 import BeautifulSoup

def obtener_datos(url):
    respuesta = requests.get(url)
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Extraer nombres de productos
    nombres_productos = [item.text.strip() for item in soup.select('.product-item-link')]

    # Extraer precios
    precios = [item.text.strip() for item in soup.select('.special-price .price')]

    # Extraer precios de promoción
    precios_promo = [item.text.strip() for item in soup.select('.promo-price .price')]

    # Extraer disponibilidad del producto
    disponibilidad = []
    for item in soup.select('.product-item'):
        if item.select_one('.stock.available'):
            disponibilidad.append('Disponible')
        else:
            disponibilidad.append('No Disponible')
    
    # Ajustar las listas para que todas tengan la misma longitud
    max_length = max(len(nombres_productos), len(precios), len(precios_promo), len(disponibilidad))
    nombres_productos.extend(['N/A'] * (max_length - len(nombres_productos)))
    precios.extend(['N/A'] * (max_length - len(precios)))
    precios_promo.extend(['N/A'] * (max_length - len(precios_promo)))
    disponibilidad.extend(['N/A'] * (max_length - len(disponibilidad)))

    # Devolver los datos en forma de diccionario
    return {
        'nombres_productos': nombres_productos,
        'precios': precios,
        'precios_promo': precios_promo,
        'disponibilidad': disponibilidad
}

# Imprimir los resultados
if __name__ == "__main__":
    url = "https://sommiercenter.com/almohadas"
    datos = obtener_datos(url)
    for i in range(len(datos['nombres_productos'])):
        print(f"Nombre del producto: {datos['nombres_productos'][i]}")
        print(f"Precio: {datos['precios'][i]}")
        print(f"Precio de promoción: {datos['precios_promo'][i]}")
        print(f"Disponibilidad: {datos['disponibilidad'][i]}")
        print("---")