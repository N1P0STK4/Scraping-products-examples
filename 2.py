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

rutaPDFs = r'C:\Users\ufo_51\Desktop\PDFs'
if not os.path.exists(rutaPDFs):
    os.makedirs(rutaPDFs)

contadorImagenes = 0
contadorPDFs = 1350
idProducto = 1841
idCategoria = "14,206"

r = session.get(url)
r.html.render(sleep=10,keep_page=False)
enlaceProducto = r.html.find('.name-class')
enlaceDirectoProducto = r.html.find('.name-class.name-class')


listaAtributos = []
listaValores = []
listaCSVcombinaciones = []
titulocsvProductos = [['ID producto','Atributos','Valores','Precio','Cantidad','Por defecto']]
listaImagenProducto = []
listacsvProductos = [['ID producto','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad']]
enlacesCategorias = []


with open('combinaciones_import.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(titulocsvProductos)

for j in enlaceDirectoProducto:
	id_lang = 0
	while True:
		try:
			idProducto += 1

			print(str(j.absolute_links).replace("{'","").replace("'}",""))

			q = session.get(str(j.absolute_links).replace("{'","").replace("'}",""))
			q.html.render(sleep=1, keep_page=True)
			soup = BeautifulSoup(q.content, 'html.parser')

			tituloProducto = q.html.find('.name-class.name-class.name-class.name-class', first=True)
			precioProducto = q.html.find('span.name-class.name-class bdi')[1].full_text
			caracteristicasProducto = "".join(map(str, soup.find_all(class_=["name-class", "name-class"]))).replace("</th>",":").replace("<th class=\"name-class\">","").replace("<td class=\"name-class\"><p>","").replace("\n","").replace(",",".").replace("</p></td>",", ")[:-2]
			imagenProducto = q.html.find('.name-class.name-class > img')
			archivosProducto = q.html.find('.name-class > p > a')
			categoriaProducto = q.html.find('.name-class > a')[2].full_text

			print("---------------------")
			print(tituloProducto.text)
			print(precioProducto)
			print(caracteristicasProducto)

			for imagenes in q.html.find('.name-class.name-class.name-class'):
				print(imagenes.attrs['name-attrs'])
				contadorImagenes += 1
				sesionObtenidaImagen = wget.download(imagenes.attrs['name-attrs'])

				os.rename(sesionObtenidaImagen, rutaImagenes+"\\"+str(contadorImagenes)+".jpg")

				listaImagenProducto.append("/usr/home/pierrechimen/www/tienda/imagenes/"+str(contadorImagenes)+".jpg")
			kk = ", ".join(map(str, listaImagenProducto))
			listaImagenProducto.clear()  

			if caracteristicasProducto:
			    caracteristicasProductoMostrarLista = caracteristicasProducto
			else:
			    caracteristicasProductoMostrarLista = ""

			if soup.find("form", class_="name-class") != None:

				variations = json.loads(soup.find("form", class_="name-class").get("name-class"))

				salir = 0

				for i in variations:
				    contadorCarasteristicas = 0
				    for attribute, value in i['attributes'].items():
				        jj = attribute.replace("attribute_", "")
				        caracteristicasAtributos = q.html.xpath("//*[@for='"+jj+"']", first=True)
				        caracteristicasValores = q.html.xpath("//*[@value='"+value+"']", first=True)
				        listaAtributos.append(caracteristicasAtributos.text+":select:"+str(contadorCarasteristicas))
				        listaValores.append(caracteristicasValores.text+":"+str(contadorCarasteristicas))
				        contadorCarasteristicas+=1
				    print(", ".join(map(str, listaAtributos)), ", ".join(map(str, listaValores)), "%.2f" % float((int(i.get("name-class"))-int(precioProducto.replace(".","").replace("€","")))/1.21), "100")

				    if ((int(i.get("name-class"))-int(precioProducto.replace(".","").replace("€","")) == 0) and (salir == 0)):
				        porDefault = 1
				        salir = 1
				    else:
				        porDefault = 0

				    listaCSVcombinaciones.append([idProducto, ", ".join(map(str, listaAtributos)), ", ".join(map(str, listaValores)), "%.2f" % float((int(i.get("name-class"))-int(precioProducto.replace(".","").replace("€","")))/1.21), "10", porDefault])
				    listaAtributos.clear()
				    listaValores.clear()

				with open('combinaciones_import.csv', 'a', newline='') as f:
				    writer = csv.writer(f, delimiter=';')
				    writer.writerows(sorted(listaCSVcombinaciones,key=lambda x: str(x[5]), reverse=True))
				listaCSVcombinaciones.clear()

			precioProductoLimpio = float(precioProducto.replace(" ","").replace(".","").replace("€","").replace(",","."))

			calcularIVA = "%.6f" % float(precioProductoLimpio/1.21)

			listacsvProductos.append([idProducto, tituloProducto.text, calcularIVA, precioProductoLimpio, "1", caracteristicasProductoMostrarLista, kk, idCategoria, "1"])

			with open('products_import.csv', 'w', newline='') as f:
				writer = csv.writer(f, delimiter=';')
				writer.writerows(listacsvProductos)            
		except:
		    sleep(10)
		    break
		break
		