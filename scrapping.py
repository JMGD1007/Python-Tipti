import requests
from bs4 import BeautifulSoup

#Ajusta la longitud de las listas dadas para que todas tengan la misma longitud. 
#Rellena con 'N/A' los elementos faltantes en cada lista.
def ajustar_longitud_listas(*listas):
    max_length = max(len(lista) for lista in listas)
    for lista in listas:
        lista.extend(['N/A'] * (max_length - len(lista)))
    return listas

# Extraer los datos de los productos e iterar las páginas. 
def obtener_datos(url_base, num_paginas=5):
    nombres_productos = []
    precios = []
    precios_promo = []
    disponibilidad = []

    for pagina in range(1, num_paginas + 1):
        url = f"{url_base}?p={pagina}"
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.text, 'html.parser')

            nombres_productos.extend([item.text.strip() for item in soup.select('.product-item-link')])
            precios.extend([item.text.strip() for item in soup.select('.special-price .price')])
            precios_promo.extend([item.text.strip() for item in soup.select('.promo-price .price')])

            for item in soup.select('.product-item'):
                if item.select_one('.stock.available'):
                    disponibilidad.append('Disponible')
                else:
                    disponibilidad.append('No Disponible')

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener los datos de la página {pagina}: {e}")
            continue

    # Ajustar las listas para que todas tengan la misma longitud
    nombres_productos, precios, precios_promo, disponibilidad = ajustar_longitud_listas(
        nombres_productos, precios, precios_promo, disponibilidad
    )

    return {
        'nombres_productos': nombres_productos,
        'precios': precios,
        'precios_promo': precios_promo,
        'disponibilidad': disponibilidad
}

# Imprimir los resultados
if __name__ == "__main__":
    url_base = "https://sommiercenter.com/mega-ofertas"
    datos = obtener_datos(url_base, num_paginas=5)
    for i in range(len(datos['nombres_productos'])):
        print(f"Nombre del producto: {datos['nombres_productos'][i]}")
        print(f"Precio: {datos['precios'][i]}")
        print(f"Precio de promoción: {datos['precios_promo'][i]}")
        print(f"Disponibilidad: {datos['disponibilidad'][i]}")
        print("---")