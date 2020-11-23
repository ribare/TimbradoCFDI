'''
Aplicación que se encarga de realizar el Timbrado CFDI de facturas
de ERP Soluciones.
PAC: Folios Digitales

            ****ERP Soluciones****
    Develop by Ricardo B.R. & Rodrigo T.C.
'''

# Librerias

import cx_Oracle                # Para conexion a BD
import zeep
from zeep import Client         # Para el consusmo del WS
import base64                   
import os                       # Funciones del SO
import lxml.etree as ET         # Para lectura de XML
import xml.etree.ElementTree as ELT
import hashlib                  # Codificar cadena original sha256
import time                     # Monitoreo
import shutil                   # Mover archivo
from Crypto.PublicKey import RSA # Obtener sello
from Crypto.Hash import SHA256  # Obtener sello
from Crypto.Signature import PKCS1_v1_5 # Obtener sello
from threading import Timer
from configparser import ConfigParser # Leer archivo de configuración
from datetime import datetime, date

# Ruta absoluta
PATH = os.path.abspath(os.path.dirname(__file__))

# Leer archivo de configuración
config_object = ConfigParser()
config_object.read("conf/config.ini")

def delay(ruta):
    print("Procesando XML...")
    t = Timer(1, procesarXML, [ruta])
    t.start()
    
def procesarXML(ruta):
    # Certificado a Base64
    cert_file = open(PATH + "/certKey/certificado.cer","rb")
    cert = base64.b64encode(cert_file.read())
    string_cert = cert.decode('utf-8')
    #print (certificado)
    
    # Cadena Original
    xml_file = open(ruta,"r")
    dom = ET.parse(xml_file)
    xslt = ET.parse(PATH + "/xslt/cadenaoriginal.xslt")
    transform = ET.XSLT(xslt)
    cadena_original = transform(dom)
    cadena_original = base64.b64encode(cadena_original)
    #print(str(cadena_original))
    
    # Sello
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
    print("Conectando a Folios Digitales...")
    
    # Obtener credenciales y URL del Web Service de config.ini
    userinfo = config_object["WSINFO"]
    
    # Autenticacion WS
    usuario = userinfo["userfd"]
    password = userinfo["passfd"]

    # Cliente WS Folios Digitales
    wsdl = userinfo["urlfd"]
    client = Client(wsdl)
    
    # Leer xml y pasarlo a String
    xml_file = open(rutaXML,"rb").read()
    cadena = xml_file.decode('utf-8')

    referencia = "001"

    # Timbrar
    response = client.service.TimbrarCFDI(usuario, password, cadena, referencia)
    #print(response)
    #Serializar respuesta para obtener atributos
    res = zeep.helpers.serialize_object(response)
    codRespuesta = res['CodigoRespuesta']
    msgError = res['MensajeError']
    msgErrorDetalle = res['MensajeErrorDetallado']
    uuid = res['Timbre']['UUID']
    xmlResultado = res['XMLResultado']

    if codRespuesta == '0':
        print("Factura " + folio + " Timbrada.\n")
        
        # Sobreescribir XML - Respuesta SAT
        file = rutaXML
        with open(file, 'w') as filetowrite:
            filetowrite.write(xmlResultado)
        
        # Copiar a carpeta de Attachment JDE
        shutil.copy(rutaXML, '/u03/htmlupload/')
        
        # Mover a carpeta Procesados
        shutil.move(rutaXML, '/efs/CFDI/procesados/')
        
        # Obtener nombre archivo XML
        filename = rutaXML.split('/')[4].split('.')[0]
        
        # Llamar funcion para obtener PDF
        obtenerPDF(usuario, password, client, uuid, filename)
        
        # Actualizar F554256A
        dbOracle(folio, uuid, codRespuesta, msgError, filename)
    
    elif codRespuesta == '801': 
        # Ya fue Timbrada Anteriormente
        print("Factura " + folio + " NO Timbrada. " + msgError + "\n")
        
    else:
        # Error
        msg = str(msgError) + " " + str(msgErrorDetalle)
        print("Factura " + folio + " NO Timbrada. " + msg + "\n")
        
        # Mover a carpeta No Procesados
        shutil.move(rutaXML, '/efs/CFDI/no_procesados/')
        
        # Actualizar F554256A con Error
        uuid = 'N/A'
        filename = 'N/A'
        dbOracle(folio, uuid, codRespuesta, msg, filename)


def obtenerPDF(usuario, password, client, uuid, filename):
    # Logo a Base64
    logo_file = open(PATH + "/images/erp_logo.png","rb")
    logo = base64.b64encode(logo_file.read())
    logoB64 = logo.decode('utf-8')
    
    res = client.service.ObtenerPDF(usuario, password, uuid, logoB64)
    pdfRes = zeep.helpers.serialize_object(res)
    pdf = pdfRes['PDFResultado']
    pdfDecode = base64.b64decode(pdf)
    with open(os.path.expanduser('/efs/CFDI/procesados/' + filename +'.pdf'), 'wb') as fout:
        fout.write(pdfDecode)
        
    # Copiar a carpeta de Attachment JDE
    rutaPDF = '/efs/CFDI/procesados/' + filename +'.pdf'
    shutil.copy(rutaPDF, '/u03/htmlupload/')


def dbOracle(folio, uuid, codRespuesta, mensaje, filename):
    # Obtener credenciales de config.ini
    dbinfo = config_object["DBINFO"]
    # Usuario, password y servicename
    user = dbinfo["userdb"]
    password = dbinfo["passdb"]
    servicename = dbinfo["servname"]
    print (folio)
    print (uuid)
    print (codRespuesta)
    print (mensaje)
    print (filename)
    conn = cx_Oracle.connect(user, password, servicename)

    cursor = conn.cursor()
    query = "UPDATE CRPDTA.F554256A SET FEK70ENUM=:uuid, FEAA15=:codR, FEADS1=:msg WHERE FEDOC=:folio"
    cursor.execute(query, [uuid, codRespuesta, mensaje, folio])
    conn.commit()
    
    if codRespuesta == '0':
        # Attachments JDE
        
        select = 'SELECT FEKCOO, FEDOCO, FEDCTO FROM CRPDTA.F554256A WHERE FEDOC=:doc'
        cursor.execute(select, doc = folio)
        for row in cursor:
            ## print (row[0])
            KCOO = row[0]
            DOCO = row[1]
            DCTO = row[2]
            DOCOSTR = str(DOCO)
        
        OBNM = 'GT554256A'
        TXKY = KCOO + '|' + DOCOSTR + '|' + DCTO
        TYPE = 5
        USER = 'JFLORES'
        # Hora actual
        now = datetime.now()
        time = now.strftime("%H%M%S")
        TDAY = time
        # Fecha actual Juliana
        siglo = "1"
        # Año
        now = date.today()
        year = now.strftime("%y")
        # Día
        dt = str(date.today())
        sdtdate = datetime.strptime(dt, "%Y-%m-%d")
        sdtdate = sdtdate.timetuple()
        day = sdtdate.tm_yday
        UPMJ = siglo + str(year) + str(day)
        NAME = filename + '.xml'
        FILENAME = "\\\\ERPDEPE1A\E910\MEDIAOBJ\HTMLUpload" + "\\" + NAME
        NAME2 = filename + '.pdf'
        FILENAME2 = "\\\\ERPDEPE1A\E910\MEDIAOBJ\HTMLUpload" + "\\" + NAME2
        
        insertXML = 'INSERT INTO CRPDTA.F00165 (GDOBNM, GDTXKY, GDMOSEQN, GDGTMOTYPE, GDUSER, GDUPMJ, GDTDAY, GDGTITNM, GDGTFILENM) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)'
        cursor.execute(insertXML, [OBNM, TXKY, 1, TYPE, USER, UPMJ, TDAY, NAME, FILENAME])
        
        insertPDF = 'INSERT INTO CRPDTA.F00165 (GDOBNM, GDTXKY, GDMOSEQN, GDGTMOTYPE, GDUSER, GDUPMJ, GDTDAY, GDGTITNM, GDGTFILENM) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)'
        cursor.execute(insertPDF, [OBNM, TXKY, 2, TYPE, USER, UPMJ, TDAY, NAME2, FILENAME2])
        
    conn.commit()
    conn.close()


def monitoreo():
    watchdir = '/efs/CFDI/TimbradoCFDI/'
    contents = os.listdir(watchdir)
    print("Monitoreando")
    while True:
        newcontents = os.listdir(watchdir)
        added = set(newcontents).difference(contents)
        if added:
            print ("Nuevo archivo añadido: %s" %(" ".join(added)))
            delay(watchdir + "%s" %(" ".join(added)))
            time.sleep(3)
        else:
            for filename in contents:
                if filename.endswith('.xml'):
                    print('Archivo en carpeta')
                    delay(watchdir + filename)
                    time.sleep(3)
                    
        contents = os.listdir(watchdir)
        time.sleep(3)
  
# Ejecutar
monitoreo()
