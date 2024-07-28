from requests_html import HTMLSession
import os 
from time import sleep, time
from hashlib import sha1
import wget
import csv
from bs4 import BeautifulSoup
import json

session = HTMLSession(browser_args=["--no-sandbox", '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'])
url = 'https://www.test.com'

rutaImagenes = r'C:\Users\ufo_51\Desktop\Imagenes'
if not os.path.exists(rutaImagenes):
    os.makedirs(rutaImagenes)

contadorImagenes = 0
idProducto = 1818
idCategoria = "14,206"

listaEnlaceProducto = []
listaImagenProducto = []
listacsvProductos = [['ID producto','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad']]

r = session.get(url)
r.html.render(sleep=10,keep_page=False)
enlaceProducto = r.html.find('.name-class > a')
obtenerEnlaceCategoria = r.html.find(".name-class")

for nombreYenlacesHTML in obtenerEnlaceCategoria:
    nombreCategoria = str(nombreYenlacesHTML.html).split('>')[1].split('<')[0].replace("Gas","/*").split('*')[0].replace("/","Gas")
    if nombreCategoria == "coche":
        listaEnlaceProducto.append(nombreYenlacesHTML.absolute_links)

for j in listaEnlaceProducto:
	id_lang = 0
	while True:
		try:
			idProducto += 1
			
			q = session.get(str(j).replace("'","").replace("{","").replace("}",""))
			q.html.render(sleep=1, keep_page=True)
			soup = BeautifulSoup(q.content, 'html.parser')
			
			tituloProducto = q.html.find('.name-class.name-class > h1', first=True)
			precioProducto = q.html.find('.name-class', first=True)
			imagenProducto = q.html.find('#name-id > ul > li > a')

			print("---------------------")
			print(str(j).replace("'","").replace("{","").replace("}",""))
			print(tituloProducto.text)
			print(str(precioProducto.text).replace(".","").replace(",",".").replace(" €",""))

			for item in imagenProducto:
				contadorImagenes += 1
				sesionObtenidaImagen = wget.download(str(item.absolute_links).replace("'","").replace("{","").replace("}",""), out=rutaImagenes)
				
				os.rename(sesionObtenidaImagen, rutaImagenes+"\\"+str(contadorImagenes)+".jpg")

				listaImagenProducto.append("/usr/home/pierrechimen/www/tienda/imagenes/"+str(contadorImagenes)+".jpg")

			kk = ", ".join(map(str, listaImagenProducto))
			print(kk) 
			listaImagenProducto.clear()

			precioProductoLimpio = float(str(precioProducto.text).replace(".","").replace(",",".").replace(" €",""))
			calcularIVA = "%.6f" % float(precioProductoLimpio/1.21)

			listacsvProductos.append([idProducto, tituloProducto.text, calcularIVA, precioProductoLimpio, "1", "", kk, idCategoria, "1"])

			with open('products_import.csv', 'w', newline='') as f:
				writer = csv.writer(f, delimiter=';')
				writer.writerows(listacsvProductos)   
		except:
			sleep(10)
			continue
		break
		