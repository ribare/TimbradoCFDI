'''
Aplicación que se encarga de realizar el Timbrado CFDI de facturas
de ERP Soluciones.
PAC: Folios Digitales

            ****ERP Soluciones****
'''

# Librerias

import cx_Oracle                # Para conexion a BD
import zeep
from zeep import Client         # Para el consusmo del WS
import sys                      # Para leer parametros externos
import base64                   
import os                       # Funciones del SO
import lxml.etree as ET         # Para lectura de XML
from M2Crypto import RSA        # Para cargar llave
import hashlib                  # Codificar cadena original sha256
import time                     # Para Monitoreo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ruta absoluta
PATH = os.path.abspath(os.path.dirname(__file__))
    
def procesarXML(ruta):
    
    # Certificado a Base64
    cert_file = open(PATH + "/certKey/CertificadoFirmadoPF.cer","rb")
    cert = base64.b64encode(cert_file.read())
    certificado = cert.decode('utf-8')
    #print (certificado)

    # Cadena Original
    xml_file = open(ruta,"r")
    dom = ET.parse(xml_file)
    xslt = ET.parse(PATH + "/xslt/cadenaoriginal_3_3.xslt")
    transform = ET.XSLT(xslt)
    cadena_original = transform(dom)
    #print(str(cadena_original))
    
    # Sello
    key = RSA.load_key(PATH + "/certKey/key.pem")
    digest = hashlib.new('sha256', str(cadena_original).encode('utf-8')).digest()
    sello = base64.b64encode(key.sign(digest,"sha256"))
    sello = sello.decode('utf-8')
    #print(sello)
    
    '''
    
    Agregar atributos a XML - RODRIGO
    
    '''
    
    # Timbrar
    rutaXML = ruta
    timbrarCFDI(rutaXML)


def timbrarCFDI(rutaXML):
    # Autenticacion WS
    usuario = "EPT040421D33"
    password = "contRa$3na"

    # Cliente WS Folios Digitales
    wsdl = "https://app.foliosdigitalespac.com/WSTimbrado33Test/WSCFDI33.svc?WSDL"
    client = Client(wsdl)
    
    # Leer xml y pasarlo a String
    xml_file = open(rutaXML,"rb").read()
    cadena = xml_file.decode('utf-8')

    referencia = "001"

    # Timbrar
    response = client.service.TimbrarCFDI(usuario, password, cadena, referencia)
    print(response)
    res = zeep.helpers.serialize_object(response)
    codRespuesta = res['CodigoRespuesta']
    #msgError = res['MensajeError']
    #mdgErrorDetalle = res['MensajeErrorDetallado']
    uuid = res['Timbre']['UUID']
    
    
    '''
    Extraer atributos
    Agregar atributos de respuesta a XML - RODRIGO
    Mover a carpeta Procesados si es OK
    
    '''
    
    # Llamar funcion para obtener PDF
    if codRespuesta == '0':
        obtenerPDF(uuid, usuario, password, client)


def obtenerPDF(uuid, usuario, password, client):
    # Logo a Base64
    logo_file = open(PATH + "/images/erp_logo.png","rb")
    logo = base64.b64encode(logo_file.read())
    logoB64 = logo.decode('utf-8')
    
    res = client.service.ObtenerPDF(usuario, password, uuid, logoB64)
    pdfRes = zeep.helpers.serialize_object(res)
    pdf = pdfRes['PDFResultado']
    pdfDecode = base64.b64decode(pdf)
    with open(os.path.expanduser(PATH + '/facturas/procesados/test.pdf'), 'wb') as fout: #Cambiar nombre <<<---
        fout.write(pdfDecode)


def monitoreo():
    # Se ejecuta cuando encuentra nuevo archivo
    def on_created(event):
        print(f"{event.src_path} ha sido creado")
        procesarXML(event.src_path)
        
    # Event handler - notifica cuando haya un cambio filesystem
    if __name__ == "__main__":
        # Controlador de eventos
        event_handler = FileSystemEventHandler()
        # Especifica que evento ejecutar
        event_handler.on_created = on_created
        # Observer
        path = "./facturas/no_procesados/"
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        #Start
        observer.start()
        try:
            print("Monitoreando")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()

# Ejecutar
monitoreo()