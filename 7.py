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
idProducto = 2793
idCategoria = "275,265"

listaEnlaceProducto = []
listaImagenProducto = []
listacsvProductos = [['ID producto','Resumen','Descripcion','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad', "Activo"]]

r = session.get(url)
r.html.render(sleep=20,keep_page=False)
enlaceProducto = r.html.find('.name-class > .name-class.name-class > .name-class > .name-class.name-class')

for j in enlaceProducto:
    id_lang = 0
    while True:

        idProducto += 1

        q = session.get(str(j.absolute_links).replace("'","").replace("{","").replace("}",""))
        q.html.render(sleep=1,keep_page=False)

        tituloProducto = q.html.find('.name-class > h1', first=True)
        precioProducto = q.html.find('.name-class', first=True)
        imagenProducto = q.html.find('.name-class > img')
        resumenProducto = q.html.find('.name-class > p', first=True)
        descripcionProducto = q.html.find('.name-class.name-class', first=True)

        print("---------------------")
        print(str(j.absolute_links).replace("'","").replace("{","").replace("}",""))
        print(tituloProducto.text)
        print(precioProducto.text.replace(" ","").replace(".","").replace("€","").replace(",","."))
        if resumenProducto == None:
            resumenProductoReturn = ""
        else:
            resumenProductoReturn = resumenProducto.html
            print(resumenProducto.html)
        print(str(descripcionProducto.html).replace("<div class=\"name-class name-class\">","").replace("\n","").rsplit('</div>', 1)[0].replace("​",""))
        
        for item in imagenProducto:
            contadorImagenes += 1
            print(item.attrs['name-attrs'])
            r = session.get(item.attrs['name-attrs'])

            with open(rutaImagenes+"\\Octocat.jpg", "wb") as fp:
                fp.write(r.content)

            os.rename(rutaImagenes+"\\Octocat.jpg", rutaImagenes+"\\"+str(contadorImagenes)+".jpg")

            listaImagenProducto.append("/usr/home/barbacoasevilla/www/imagenes/"+str(contadorImagenes)+".png")

        kk = ", ".join(map(str, listaImagenProducto))
        print(kk) 
        listaImagenProducto.clear()

        precioProductoLimpio = float(precioProducto.text.replace(" ","").replace(".","").replace("€","").replace(",","."))
        calcularIVA = "%.6f" % float(precioProductoLimpio/1.21)

        print(calcularIVA.replace(".",","))

        listacsvProductos.append([idProducto, resumenProductoReturn, str(descripcionProducto.html).replace("<div class=\"name-class name-class\">","").replace("\n","").rsplit('</div>', 1)[0].replace("​","").replace("\u2033","").replace("\u014d",""), tituloProducto.text, calcularIVA.replace(".",","), precioProductoLimpio, "1", "", kk, idCategoria, "200", "1"])
        with open('products_import.csv', 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(listacsvProductos)

        break