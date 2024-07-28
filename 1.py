from requests_html import HTMLSession
import os 
from time import sleep, time
from hashlib import sha1
import wget
import csv
from bs4 import BeautifulSoup
import json

session = HTMLSession(browser_args=["--no-sandbox", '--user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'])
url = 'https://www.test.com'

rutaImagenes = r'C:\Users\ufo_51\Desktop\Imagenes'
if not os.path.exists(rutaImagenes):
    os.makedirs(rutaImagenes)

contadorImagenes = 0
idProducto = 1861
idCategoria = "13,213"

listaEnlaceProducto = []
listaImagenProducto = []
listacsvProductos = [['ID producto','Descripcion','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad', "Activo"]]

r = session.get(url)
r.html.render(sleep=10,keep_page=False)
enlaceProducto = r.html.find('.name-class')
obtenerEnlaceCategoria = r.html.find('.name-class')

for nombreYenlacesHTML in obtenerEnlaceCategoria:
    try:
        nombreCategoria = str(nombreYenlacesHTML.text).replace("Coche","*/*").split('*/')[1].replace("*","Coche")
        if nombreCategoria:
            listaEnlaceProducto.append(nombreYenlacesHTML.absolute_links)
    except:
        continue

for j in listaEnlaceProducto:
    id_lang = 0
    while True:
        try:
            idProducto += 1

            q = session.get(str(j).replace("'","").replace("{","").replace("}",""))
            q.html.render(sleep=1,keep_page=False)

            tituloProducto = q.html.find('.name-class', first=True)
            imagenProducto = q.html.find('.name-class > name-class > img')
            descripcionProducto = q.html.find('.name-class > .name-class > .name-class', first=True)

            print("---------------------")
            print(str(j).replace("'","").replace("{","").replace("}",""))
            print(tituloProducto.text)
            print(str(descripcionProducto.html).replace("<div class=\"name-class\">","").replace("\n",""))
            
            for item in imagenProducto:
                contadorImagenes += 1
                print(item.attrs['name-class'])
                r = session.get(item.attrs['name-class'])

                with open(rutaImagenes+"\\Octocat.jpg", "wb") as fp:
                    fp.write(r.content)

                os.rename(rutaImagenes+"\\Octocat.jpg", rutaImagenes+"\\"+str(contadorImagenes)+".jpg")

                listaImagenProducto.append("/usr/home/pierrechimen/www/imagenes/"+str(contadorImagenes)+".jpg")

            kk = ", ".join(map(str, listaImagenProducto))
            print(kk) 
            listaImagenProducto.clear()

            listacsvProductos.append([idProducto, str(descripcionProducto.html).replace("<div class=\"name-class\">","").replace("\n","").replace("‎",""), tituloProducto.text, "0", "0", "1", "", kk, idCategoria, "200", "0"])
            with open('products_import.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(listacsvProductos)
            
        except:
            sleep(10)
            continue
        break
