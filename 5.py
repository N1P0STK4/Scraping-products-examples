from requests_html import HTMLSession
import os 
from time import sleep, time
from hashlib import sha1
import wget
import csv
from bs4 import BeautifulSoup
import json
import re
import itertools

session = HTMLSession(browser_args=["--no-sandbox", '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'])
url = 'https://www.test.com'

rutaImagenes = r'C:\Users\ufo_51\Desktop\Imagenes'
if not os.path.exists(rutaImagenes):
    os.makedirs(rutaImagenes)

rutaPDFs = r'C:\Users\ufo_51\Desktop\PDFs'
if not os.path.exists(rutaPDFs):
    os.makedirs(rutaPDFs)

contadorImagenes = 0
contadorPDFs = 1384
idProducto = 3312
idCategoria = "316,315,16,3"

r = session.get(url)
r.html.render(sleep=10, keep_page=True)
enlaceProducto = r.html.xpath("//*[@name-class='url']")

listaAtributos = []
listaValores = []
listaImagenProducto = []
listaTest = []
listaCuak = []
listaCuak2 = []
listaPDFsProducto = []
listaPsAttachment = []
listaPsAttachmentLang = []
listaEnlaceProducto = []
listaCSVcombinaciones = [['ID producto','Atributos','Valores','Precio','Cantidad','Por defecto']]
listacsvProductos = [['ID producto','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad', 'Descripcion larga']]

for j in enlaceProducto:
        id_lang = 0
        while True:
            try:
                idProducto += 1
                q = session.get("https://www.test.com")
                q.html.render(sleep=1,keep_page=False)
                
                tituloProducto = q.html.find('.name-class', first=True)
                imagenProducto = q.html.find('.name-class')
                precioProducto = q.html.find('.name-class', first=True)
                descripcionProductoLarga = q.html.find('.name-class', first=True)
                descripcionProductocCorta = q.html.find('.name-class', first=True)

                titulossProducto = q.html.find('.name-class:has(> select)')
                valorProducto = q.html.find('.name-class.name-class.name-class > option')
            
                print("---------------------")
                print(tituloProducto.text)

                precioProductoLimpio = float(precioProducto.full_text.replace(" ","").replace(".","").replace("€","").replace(",","."))
                calcularIVA = "%.6f" % float(precioProductoLimpio/1.21)

                print(precioProductoLimpio)
                print(calcularIVA)
                print(re.sub('<a href=[^<]+</a>', '', descripcionProductoLarga.html))
                print(re.sub('<b[^<]+</b>', '', descripcionProductocCorta.html).replace("<br/>",""))

                for item in imagenProducto:
                    contadorImagenes += 1
                    r = session.get(item.attrs['name-attrs'])

                    with open(rutaImagenes+"\\Octocat.webp", "wb") as fp:
                        fp.write(r.content)

                    os.rename(rutaImagenes+"\\Octocat.webp", rutaImagenes+"\\"+str(contadorImagenes)+".webp")

                    listaImagenProducto.append("/usr/home/barbacoasevilla/www/imagenes/"+str(contadorImagenes)+".jpg")

                kk = ", ".join(map(str, listaImagenProducto))
                print(kk) 
                listaImagenProducto.clear()
                
                testing2 = 0
                indexListaCoche = 0
                index0 = 0
                index1 = 0
                for item3 in titulossProducto:
                    testing2 += 1
                    porDefault = 1
                    listaAtributos = list(filter(None, item3.full_text.split("\n")))
                    soup = BeautifulSoup(item3.html, 'html.parser')
                    options = soup.find_all('option')
                    pp = listaAtributos.pop(0)
                    if (pp.replace(" ","") != "coche:" and pp.replace(" ","") != "Color coche:"):
                        print("Atributo: "+pp.replace(" ","")+"select:"+str(index0))
                        listaTest.append(pp.replace(" ","")+"select:"+str(index0))
                        listaValores.append([nombre + ":" + str(index0) for nombre in listaAtributos])

                        print([nombre + ":" + str(index0) for nombre in listaAtributos])
                        print([option['value'] if option['value'].strip() else '0' for option in options])

                        for (x, y) in zip([nombre + ":" + str(index0) for nombre in listaAtributos], [option['value'] if option['value'].strip() else '0' for option in options]):
                            pppp = x + "|" + y.replace("+","") + "|"
                            listaCuak.append(pppp)
                        listaCuak2.append(list(listaCuak))
                        listaCuak.clear()

                        index0 += 1
                    '''if pp.replace(" ","") == "coche:":
                        #print(pp.replace(" ",""), ', '.join(listaAtributos))
                        print("Atributo: "+pp.replace(" ","")+"select:"+str(index0))
                        for iwi in listaAtributos:
                            listaTest.append(iwi)
                        index0 += 1
                        print("Atributo: "+"Color coche:"+"select:"+str(index0))
                        listaValores.append(listaAtributos)
                        print(listaAtributos)
                        index0 += 1
                    if pp.replace(" ","") == "Color coche:":
                        print("Valor: "+listaTest[indexListaCoche]+":", ', '.join(listaAtributos).replace(",",":"+str(indexListaCoche))+":"+str(indexListaCoche))
                        listaValores.append(listaAtributos)
                        print(listaAtributos)
                        indexListaCoche += 1'''
                permutaciones = list(itertools.product(*listaCuak2))
                for item4 in permutaciones:
                    patron = re.compile(f'{re.escape("|")}(.*?){re.escape("|")}')
                    ads = str(item4).replace("(","").replace(")","").replace("\'", "").replace(",", "").split("|")[:-1]
                    print(idProducto,', '.join(listaTest),patron.sub('', str(item4)).replace("(","").replace(")","").replace("'",""), "%.6f" % float(sum([int(valor) for indice, valor in enumerate(ads) if indice % 2 == 1])/1.21), porDefault)
                    listaCSVcombinaciones.append([idProducto,', '.join(listaTest),patron.sub('', str(item4)).replace("(","").replace(")","").replace("'",""), "%.6f" % float(sum([int(valor) for indice, valor in enumerate(ads) if indice % 2 == 1])/1.21),5, porDefault])
                    index1 += 1
                    porDefault = 0

                listacsvProductos.append([idProducto, tituloProducto.text, calcularIVA, precioProductoLimpio, "1", re.sub('<b[^<]+</b>', '', descripcionProductocCorta.html).replace("<br/>",""), kk, idCategoria, "1",re.sub('<a href=[^<]+</a>', '', descripcionProductoLarga.html)])

                with open('combinaciones_import.csv', 'a', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerows(sorted(listaCSVcombinaciones,key=lambda x: str(x[5]), reverse=True))
                with open('products_import.csv', 'w', newline='') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerows(listacsvProductos) 
                listaCSVcombinaciones.clear()
                listaTest.clear()
                listaCuak2.clear()
            except:
                sleep(10)
                break
            break
