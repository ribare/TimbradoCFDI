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
import base64                   #
import os                       # Funciones del SO
import lxml.etree as ET         # Para lectura de XML
#from M2Crypto import RSA       # Para cargar llave
import hashlib                  # Codificar cadena original sha256

# ->> Ruta absoluta
PATH = os.path.abspath(os.path.dirname(__file__))

# ->> Certificado a Base64
'''cert_file = open(PATH + "\\certKey\\CertificadoFirmadoPF.cer","rb")  # r = read, b = binario
cert = base64.b64encode(cert_file.read())
certificado = cert.decode('utf-8')
#print (certificado)'''

# Autenticacion WS
usuario = "EPT040421D33"
password = "contRa$3na"

# Cliente WS
wsdl = "https://app.foliosdigitalespac.com/WSTimbrado33Test/WSCFDI33.svc?WSDL"
client = Client(wsdl)

# ->> Web Service Folios Digitales
def timbrarCFDI():

    # Leer xml y pasarlo a String
    xml_file = open(PATH + "\\XML_Ejemplo_33.xml","rb").read()
    cadena = xml_file.decode('utf-8')
    #print(cadena)

    referencia = "001"

    response = client.service.TimbrarCFDI(usuario, password, cadena, referencia)
    #print(client.service.TimbrarCFDI(usuario, password, cadena, referencia))
    res = zeep.helpers.serialize_object(response)
    codRespuesta = res['CodigoRespuesta']
    msgError = res['MensajeError']
    mdgErrorDetalle = res['MensajeErrorDetallado']
    uuid = res['Timbre']['UUID']
    xmlResult = res['XMLResultado']
    
    # Llamar funcion para obtener PDF
    obtenerPDF('B810FDB8-7E57-7E57-7E57-C6E0876DC543')


# Obtener PDF 
def obtenerPDF(uuid):
    #Logo a Base64
    logo_file = open(PATH + "\\images\\erp_logo.png","rb")
    logo = base64.b64encode(logo_file.read())
    logoB64 = logo.decode('utf-8')
    
    res = client.service.ObtenerPDF(usuario, password, uuid, logoB64)
    pdfRes = zeep.helpers.serialize_object(res)
    #print(pdfRes['PDFResultado'])
    pdf = pdfRes['PDFResultado']
    pdfDecode = base64.b64decode(pdf)
    with open(os.path.expanduser('test.pdf'), 'wb') as fout:
        fout.write(pdfDecode)
    
    xmlResult = pdfRes['XMLResultado']
    file = open("xmltest.xml", "w")
    file.write(xmlResult)


def sello():
    # ->> Cadena Original
    xml_file = open(PATH + "/XML_Ejemplo_33.xml","r")
    dom = ET.parse(xml_file)
    xslt = ET.parse(PATH + "/xslt/cadenaoriginal_3_3.xslt")
    transform = ET.XSLT(xslt)
    cadena_original = transform(dom)
    #print(str(cadena_original))
    
    # ->> Sello
    '''key = RSA.load_key(PATH + "/certKey/key.pem")
    digest = hashlib.new('sha256', str(cadena_original).encode('utf-8')).digest()
    sello = base64.b64encode(key.sign(digest,"sha256"))
    sello = sello.decode('utf-8')
    #print(sello.decode('utf-8'))'''
    
    
timbrarCFDI()