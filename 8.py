from requests_html import HTMLSession
import os 
from time import sleep, time
from hashlib import sha1
import wget
import csv

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
idProducto = 1614
idCategoria = "3,196"

r = session.get(url)
r.html.render(sleep=10, keep_page=True)
enlaceProducto = r.html.find('.name-class')
obtenerEnlaceCategoria = r.html.find(".name-class")

listaImagenProducto = []
listaPDFsProducto = []
listaPsAttachment = []
listaPsAttachmentLang = []
listaEnlaceProducto = []
listacsvProductos = [['ID producto','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad']]

for nombreYenlacesHTML in obtenerEnlaceCategoria:
    nombreCategoria = str(nombreYenlacesHTML.html).split('</div>')[0].split('name-class">')[1]
    if nombreCategoria == "Coche":
        listaEnlaceProducto.append(str(nombreYenlacesHTML.html).split('</h2>')[0].split('href="')[1].split('"')[0])

for j in listaEnlaceProducto:
    id_lang = 0
    idProducto += 1
    while True:
        try:
            q = session.get(j)
            q.html.render(sleep=1, keep_page=True)

            tituloProducto = q.html.find('.name-class', first=True)
            precioProducto = q.html.find('.name-class', first=True)
            caracteristicasProducto = q.html.find('.name-class', first=True)
            imagenProducto = q.html.find('.name-class.name-class > img')
            archivosProducto = q.html.find('.name-class > p > a')

            print("---------------------")
            print(j)
            print(tituloProducto.text)
            print(precioProducto.text.replace(" ","").replace(".","").replace("€","").replace(",","."))
            
            for item in imagenProducto:
                contadorImagenes += 1
                sesionObtenidaImagen = wget.download(str(item).split('content=\'')[1].split('\'')[0], out=rutaImagenes)

                os.rename(sesionObtenidaImagen, rutaImagenes+"\\"+str(contadorImagenes)+".jpg")

                listaImagenProducto.append("/usr/home/pierrechimen/www/tienda/imagenes/"+str(contadorImagenes)+".jpg")

            kk = ", ".join(map(str, listaImagenProducto))
            print(kk) 
            listaImagenProducto.clear()  

            if caracteristicasProducto:
                caracteristicasProductoMostrarLista = caracteristicasProducto.html.replace('\n','').replace('</dt>', ': ').replace('</dd>', ', ').replace('<dd class="name-class">', '').replace('<dt class="name-class">', '').split("\">", 1)[1].replace(', </dl>', '')
                print(caracteristicasProducto.html.replace('\n','').replace('</dt>', ': ').replace('</dd>', ', ').replace('<dd class="name-class">', '').replace('<dt class="name-class">', '').split("\">", 1)[1].replace(', </dl>', ''))
            else:
                caracteristicasProductoMostrarLista = ""

            for archivo in archivosProducto:
                contadorPDFs += 1
                sesionObtenidaArchivo = wget.download(str(archivo.absolute_links).replace("{'","").replace("'}",""), out=rutaPDFs)

                nombreArchivo = "attachment_"+str(contadorPDFs)+"."+sesionObtenidaArchivo.split('.')[1]
                now = time()
                sha1Encriptado = sha1((str(now - int(now)) + ' ' + str(int(now))).encode()).hexdigest()
                os.rename(sesionObtenidaArchivo, rutaPDFs+"\\"+sha1Encriptado)
                listaPsAttachment.append(", \'" + str(sha1Encriptado) + "', \'" + str(nombreArchivo) + "\', '" + str(os.path.getsize(rutaPDFs + "\\" + sha1Encriptado)))
                listaPsAttachmentLang.append(sha1Encriptado)

                listaPDFsProducto.append("/usr/home/pierrechimen/www/tienda/archivos/attachment_"+str(contadorPDFs))

            print(", ".join(map(str, listaPDFsProducto))) 
            listaPDFsProducto.clear()

            precioProductoLimpio = float(precioProducto.text.replace(" ","").replace(".","").replace("€","").replace(",","."))

            calcularIVA = "%.6f" % float(precioProductoLimpio/1.21)
            print(str(precioProductoLimpio/1.21).replace(".",",").replace(",","."))
            listacsvProductos.append([idProducto, tituloProducto.text, calcularIVA, precioProductoLimpio, "1", caracteristicasProductoMostrarLista, kk, idCategoria, "1"])
            with open('products_import.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(listacsvProductos)
            
            for i in listaPsAttachment:
                attachmentSQL = open("attachment.sql", 'a', encoding='utf8')
                attachmentSQL.write(r"INSERT INTO `ps_attachment` (`id_attachment`, `file`, `file_name`, `file_size`, `mime`) VALUES (NULL" + str(i) + r"', 'application/pdf');" + '\n')
                attachmentSQL.close()
            listaPsAttachment.clear()
            for b in listaPsAttachmentLang:
                id_lang += 1
                attachmentSQL = open("attachment.sql", 'a', encoding='utf8')
                attachmentSQL.write(r"INSERT INTO `ps_attachment_lang` (`id_attachment`, `id_lang`, `name`, `description`) SELECT `ps_attachment`.`id_attachment`,1 , 'Archivo " + str(id_lang) + "', '' FROM `ps_attachment` WHERE `ps_attachment`.`file` = '" + str(b) + r"' LIMIT 1;" + '\n')
                attachmentSQL.write(r"INSERT INTO `ps_product_attachment` (`id_product`, `id_attachment`)  SELECT `ps_product`.`id_product`, `ps_attachment`.`id_attachment` FROM `ps_product` JOIN `ps_attachment` ON `ps_product`.`id_product` = '" + str(idProducto) + "' AND `ps_attachment`.`file` = '" + str(b) + "' LIMIT 1;" + '\n' + '\n')
                attachmentSQL.close()
            listaPsAttachmentLang.clear()
            
        except:
            sleep(10)
            continue
        break