from requests_html import HTMLSession
import os 
from time import sleep, time
from hashlib import sha1
import wget
import csv
from bs4 import BeautifulSoup
import json
import gdown

session = HTMLSession(browser_args=["--no-sandbox", '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'])

rutaImagenes = r'C:\Users\ufo_51\Desktop\Imagenes'
if not os.path.exists(rutaImagenes):
    os.makedirs(rutaImagenes)

rutaPDFs = r'C:\Users\ufo_51\Desktop\PDFs'
if not os.path.exists(rutaPDFs):
    os.makedirs(rutaPDFs)

contadorImagenes = 0
contadorPDFs = 1768
idProducto = 1194
idCategoria = "291,4,290"
paginasProductos = 3

listaImagenProducto = []
listaPDFsProducto = []
listaPsAttachment = []
listaPsAttachmentLang = []
listaEnlaceProducto = []
listaNombreArchivo = []
listacsvProductos = [['ID producto','Resumen','Descripcion','Nombre','Precio sin impuestos','Precio con impuestos','ID Impuesto','Especificaciones','Url imagen', 'Categoria', 'Cantidad', "Activo"]]

for x in range(1, paginasProductos):
    url = 'https://test.com/page/'+str(x)
    r = session.get(url)
    r.html.render(sleep=10,keep_page=True)
    listaEnlaceProducto = r.html.find('.name-class.name-class.name-class > a')

    for j in listaEnlaceProducto:
        id_lang = 0
        while True:
            try:
                idProducto += 1

                q = session.get(str(j.absolute_links).replace("'","").replace("{","").replace("}",""))
                q.html.render(sleep=1,keep_page=False)

                tituloProducto = q.html.find('.name-class', first=True)
                resumenProducto = q.html.find('.name-class > .name-class > p > strong', first=True)
                descripcionProducto = q.html.find('p:has(> br)', first=True)
                archivosProducto = q.html.find('a:has(> i)') #.li-producto > a
                imagenProducto = q.html.find('.name-class > a')
            
                print("---------------------")
                print(str(j.absolute_links).replace("'","").replace("{","").replace("}",""))
                print(tituloProducto.text)
                if resumenProducto:
                    print(resumenProducto.html)
                    resumenProductoReturn = resumenProducto.html
                else:
                    resumenProductoReturn = ""
                if descripcionProducto:
                    print(descripcionProducto.html)
                    descripcionProductoReturn = descripcionProducto.html
                else:
                    descripcionProductoReturn = ""

                for item in imagenProducto:
                    contadorImagenes += 1
                    print(str(item.absolute_links).replace("'","").replace("{","").replace("}",""))
                    r = session.get(str(item.absolute_links).replace("'","").replace("{","").replace("}",""))

                    with open(rutaImagenes+"\\Octocat.jpg", "wb") as fp:
                        fp.write(r.content)

                    os.rename(rutaImagenes+"\\Octocat.jpg", rutaImagenes+"\\"+str(contadorImagenes)+".jpg")

                    listaImagenProducto.append("/usr/home/barbacoasevilla/www/imagenes/"+str(contadorImagenes)+".jpg")

                kk = ", ".join(map(str, listaImagenProducto))
                print(kk) 
                listaImagenProducto.clear()
                
                if archivosProducto:
                    for archivo in archivosProducto:
                        try:
                            contadorPDFs += 1   
                            # para que no de errores en la descarga de archivos de google drive |https://github.com/wkentaro/gdown/issues/43#issuecomment-621356443 | -> pip install -U --no-cache-dir gdown --pre
                            print(archivo.text)
                            file_id = str(archivo.absolute_links).replace("{'","").replace("'}","").split('/')[5]
                            url = f'https://drive.google.com/uc?id={file_id}'
                            nombreArchivo = r"\attachment_"+str(contadorPDFs)+".pdf"
                            output = rutaPDFs+nombreArchivo
                            gdown.download(url, output, quiet=False)

                            now = time()
                            sha1Encriptado = sha1((str(now - int(now)) + ' ' + str(int(now))).encode()).hexdigest()
                            os.rename(output, rutaPDFs+"\\"+sha1Encriptado)
                            listaPsAttachment.append(", \'" + str(sha1Encriptado) + "', \'" + str(nombreArchivo) + "\', '" + str(os.path.getsize(rutaPDFs + "\\" + sha1Encriptado)))
                            listaPsAttachmentLang.append(sha1Encriptado)
                            listaNombreArchivo.append(archivo.text)

                            listaPDFsProducto.append("/usr/home/barbacoasevilla/www/archivos/attachment_"+str(contadorPDFs))
                        except:
                            continue

                print(", ".join(map(str, listaPDFsProducto))) 
                listaPDFsProducto.clear()

                listacsvProductos.append([idProducto, resumenProductoReturn, descripcionProductoReturn, tituloProducto.text, "0", "0", "1", "", kk, idCategoria, "200", "0"])
                with open('products_import.csv', 'w', newline='', encoding='utf8') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerows(listacsvProductos)

                for i in listaPsAttachment:
                    attachmentSQL = open("attachment.sql", 'a', encoding='utf8')
                    attachmentSQL.write(r"INSERT INTO `ps_attachment` (`id_attachment`, `file`, `file_name`, `file_size`, `mime`) VALUES (NULL" + str(i) + r"', 'application/pdf');" + '\n')
                    attachmentSQL.close()
                listaPsAttachment.clear()
                for b in zip(listaPsAttachmentLang, listaNombreArchivo):
                    id_lang += 1
                    attachmentSQL = open("attachment.sql", 'a', encoding='utf8')
                    attachmentSQL.write(r"INSERT INTO `ps_attachment_lang` (`id_attachment`, `id_lang`, `name`, `description`) SELECT `ps_attachment`.`id_attachment`,1 , '" + str(b[1]) + "', '' FROM `ps_attachment` WHERE `ps_attachment`.`file` = '" + str(b[0]) + r"' LIMIT 1;" + '\n')
                    attachmentSQL.write(r"INSERT INTO `ps_product_attachment` (`id_product`, `id_attachment`)  SELECT `ps_product`.`id_product`, `ps_attachment`.`id_attachment` FROM `ps_product` JOIN `ps_attachment` ON `ps_product`.`id_product` = '" + str(idProducto) + "' AND `ps_attachment`.`file` = '" + str(b[0]) + "' LIMIT 1;" + '\n' + '\n')
                    attachmentSQL.close()
                listaNombreArchivo.clear()
                listaPsAttachmentLang.clear()

            except:
                sleep(10)
                continue
            break
