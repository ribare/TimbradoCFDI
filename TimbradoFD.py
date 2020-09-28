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
import base64                   
import os                       # Funciones del SO
import lxml.etree as ET         # Para lectura de XML
import xml.etree.ElementTree as ELT
#RESPALDO#from M2Crypto import RSA        # Para cargar llave
import hashlib                  # Codificar cadena original sha256
import time                     # Para Monitoreo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

# Ruta absoluta
PATH = os.path.abspath(os.path.dirname(__file__))
    
def procesarXML(ruta):
    
    # Certificado a Base64
    cert_file = open(PATH + "/certKey/CertificadoFirmadoPF.cer","rb")
    cert = base64.b64encode(cert_file.read())
    string_cert = cert.decode('utf-8')
    #print (certificado)

    # Cadena Original
    xml_file = open(ruta,"r")
    dom = ET.parse(xml_file)
    xslt = ET.parse(PATH + "/xslt/cadenaoriginal_3_3.xslt")
    transform = ET.XSLT(xslt)
    cadena_original = transform(dom)
    cadena_original = base64.b64encode(cadena_original)
    #print(str(cadena_original))
    
    # Sello
    '''key = RSA.load_key(PATH + "/certKey/key.pem")
    digest = hashlib.new('sha256', str(cadena_original).encode('utf-8')).digest()
    sello = base64.b64encode(key.sign(digest,"sha256"))
    sello = sello.decode('utf-8')
    #print(sello)'''#Respaldo, v1
    key = open (PATH + "/certKey/key.pem", "rb").read()
    rsakey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(base64.b64decode(cadena_original))
    sign = signer.sign(digest)
    sello =base64.b64encode(sign)
    sello = sello.decode('utf-8')
    
    # INICIO
    #Se hace el llamado del namespace para que el XML este en formato correcto. 
    ELT.register_namespace("cfdi","http://www.sat.gob.mx/cfd/3")
    ELT.register_namespace("xs","http://www.w3.org/2001/XMLSchema")
    ELT.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")
    
    #Se abre el archivo con su respectiva ruta para la modificacion del xml por parte del certificado ----------------------------------------------------------------
    tree = ELT.parse (ruta)
    #Se consigue el root del archivo xml
    root = tree.getroot()
    
    for edit_xml in root.iter('{http://www.sat.gob.mx/cfd/3}Comprobante'):
        folio = edit_xml.get('Folio')
        edit_xml.set('Certificado', string_cert)
        edit_xml.set('Sello', sello)
        tree.write(ruta, encoding='utf-8', xml_declaration=True)
    # FIN
    
    # Timbrar
    rutaXML = ruta
    timbrarCFDI(rutaXML, folio)


def timbrarCFDI(rutaXML, folio):
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
    xmlResultado = res['XMLResultado']
    
    if codRespuesta == '0':
        # Sobreescribir XML - Respuesta SAT
        file = rutaXML
        with open(file, 'w') as filetowrite:
            filetowrite.write(xmlResultado)
        
        # Mover a carpeta Procesados
        shutil.move(rutaXML, './facturas/procesados/')
        
        # Obtener nombre archivo XML
        filename = rutaXML.split('/')[3].split('.')[0]
        
        # Llamar funcion para obtener PDF
        obtenerPDF(usuario, password, client, uuid, filename)


def obtenerPDF(usuario, password, client, uuid, filename):
    # Logo a Base64
    logo_file = open(PATH + "/images/erp_logo.png","rb")
    logo = base64.b64encode(logo_file.read())
    logoB64 = logo.decode('utf-8')
    
    res = client.service.ObtenerPDF(usuario, password, uuid, logoB64)
    pdfRes = zeep.helpers.serialize_object(res)
    pdf = pdfRes['PDFResultado']
    pdfDecode = base64.b64decode(pdf)
    with open(os.path.expanduser(PATH + '/facturas/procesados/' + filename +'.pdf'), 'wb') as fout:
        fout.write(pdfDecode)


def dbOracle():
    user = "CRPDTA"
    password = "CRPDTA"

    conn = cx_Oracle.connect(user, password, "172.31.31.136/DB910")

    cursor = conn.cursor()
    cursor.execute("SELECT ABAN8, ABALPH FROM CRPDTA.F0101 MAXROW=15")

    for ABAN8, ABALPH in cursor:
        print (ABAN8, ABALPH)


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