import requests
from bs4 import BeautifulSoup

url = "https://sommiercenter.com/almohadas"

respuesta = requests.get(url)
soup = BeautifulSoup(respuesta.text, 'html.parser')

# Extraer nombres de productos
nombres_productos = [item.text.strip() for item in soup.select('.product-item-link')]

# Extraer precios
precios = [item.text.strip() for item in soup.select('.special-price .price')]

# Extraer precios de promoción
precios_promo = [item.text.strip() for item in soup.select('.promo-price .price')]

#Extraer disponibilidad del producto
disponibilidad = []
for item in soup.select('.product-item'):
    if item.select_one('.stock.available'):
        disponibilidad.append('Disponible')
    else:
        disponibilidad.append('No disponible')

# Imprimir los resultados
for i in range(len(nombres_productos)):
    print(f"Nombre del producto: {nombres_productos[i]}")
    print(f"Precio: {precios[i]}")
    print(f"Precio de promoción: {precios_promo[i]}")
    print(f"Disponibilidad: {disponibilidad[i]}")
    print("---")
