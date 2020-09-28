import base64
import lxml.etree as ET
import os
from M2Crypto import RSA
import hashlib
import shutil
import xml.etree.ElementTree as ELT
#from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

PATH = os.path.abspath(os.path.dirname(__file__))
# 'B810FDB8-7E57-7E57-7E57-C6E0876DC543'
# ->> Certificado a Base64
'''cert_file = open(PATH + "\\certKey\\CertificadoFirmadoPF.cer","rb")  # r = read, b = binario
cert = base64.b64encode(cert_file.read())
certificado = cert.decode('utf-8')
print (certificado)'''

# ->> Cadena Original
xml_file = open(PATH + "/facturas/no_procesados/XML_Ejemplo_33.xml","r")
dom = ET.parse(xml_file)
xslt = ET.parse(PATH + "/xslt/cadenaoriginal_3_3.xslt")
transform = ET.XSLT(xslt)
cadena_original = transform(dom)
cadena_original = base64.b64encode(cadena_original)
#print(ET.tostring(newxml, pretty_print = True))
#print(str(cadena_original))
#file = open("cadena_original.txt", "w")
#file.write(str(cadena_original))

# ->> Sello
key = RSA.load_key(PATH + "/certKey/key.pem")
digest = hashlib.new('sha256', str(cadena_original).encode('utf-8')).digest()
sello = base64.b64encode(key.sign(digest,"sha256"))
print(sello.decode('utf-8'))
#file = open("sello.txt", "w")
#file.write(sello.decode('utf-8'))




# Para leer xml y pasarlo a String
'''xml_file = open(PATH + "\\XML_Ejemplo_33.xml","rb").read()
#dom = ET.fromstring(xml_file)
print(xml_file.decode('utf-8'))'''

#Parse XML y actualizar valor de atributo
'''tree = ET.parse(PATH + "\\XML_Ejemplo_33.xml")
root = tree.getroot()
#root.attrib['Version'] = "1"
print(root.attrib['Version'])'''

# Obtener Path
#print(os.path.abspath(os.getcwd()))
#print(os.path.abspath(os.path.dirname(__file__)))


'''
xslt_file = open("C:\\Users\\ricar\\OneDrive\\Documentos\\Cursos\\Python\\TimbradoCFDI\\xslt\\cadenaoriginal_3_3.xslt")
xslt_content = xslt_file.read()
xslt = ET.XML(xslt_content)
dom = ET.parse("C:\\Users\\ricar\\OneDrive\\Documentos\\Cursos\\Python\\TimbradoCFDI\\XML_Ejemplo_33.xml")
transform = ET.XSLT(xslt)
newxml = transform(dom)
print(ET.tostring(newxml, pretty_print = True))
print(dom)
'''

# Pare crear archivo XML Nota: Sobreescribe XML con la respuesta del SAT
#xml = '<?xml version="1.0" encoding="UTF-8"?><cfdi:Comprobante xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd" Version="3.3" Folio="FOL123456" Fecha="2020-09-13T09:36:11" Sello="Ab0Qf4ZDeokzh+pBEgkFvsXvqm6r7BBIii6aDsZ6Juw1DIT+h2gmqnGmVnxKp+T4jpenm0zJiIOnIWDzH3nrznibG/onVrVx8VBMGqCGA5weHnMn3/ya+URbxUOKSOEq35nnhljvsh+ScjylJnXiEei4GmKidh86GWtoyJUGRXu12YatFg5j3IzhfZcXgrWj2wUtoCJUnIulCXq5O2VJOre+TEk65L/C/ystfRm5WZfjzKHeyFBwys6fWOaaSuFaOZRUvJed7tSX4SEczar77rbdE7cXv1zQXoCGzCbcD3WfpQh3AvrcdqM2SFAUlpg5Sv5gHVEZmGr1Ds98RH99Ug==" FormaPago="01" NoCertificado="20001000000300022823" Certificado="MIIDhDCCAmygAwIBAgIUMjAwMDEwMDAwMDAzMDAwMjI4MjMwDQYJKoZIhvcNAQEFBQAwSzEVMBMGA1UEAwwMQS5DLiBQcnVlYmFzMRAwDgYDVQQKDAdQcnVlYmFzMQswCQYDVQQGEwJNWDETMBEGA1UEBwwKQ3VhdWh0ZW1vYzAeFw0xNzA0MjgxODMwMzZaFw0yMjEwMTkxODMwMzZaMIGQMRswGQYDVQQDDBJQYWJsbyBOZXJ1ZGEgUGVyZXoxGzAZBgNVBCkMElBhYmxvIE5lcnVkYSBQZXJlejEbMBkGA1UECgwSUGFibG8gTmVydWRhIFBlcmV6MSUwIwYDVQQtDBxURVNUMDEwMjAzMDAxIC8gVEVTVDEwMzE3QTQ2MRAwDgYDVQQLDAdDRU5UUkFMMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4S8y29PfV6zBib8HEx/SK2XaUBeAb5YZbL+MHjX4K710kFdskgYhX35N0StfN5wbHLIsnj0eLtIk7gjXmaAjF6PkM9jtRtUrWgS22lcah0K7ws+nqfhNFuPX9rfm8SXzkBFDjUiBmW0U0Lz3cT/fEoJiqMxTwgJyhpuQ3vIcrv85cUaNpnf85eSCWVXGFmXpZD7EgXKLQulD1OOQbqcBPF6sK0wlz27HeQsM0X+2rO+RJvWAsHqIT4z0Sct4FFzj3XjGiF+DK8KxbQOmWpTnOSw0k9oKHmrFG3c1GxxyhvHoz+RurZFWPwuCWAzaUDhwq3uB6dtP7foeEjUUFlRD/wIDAQABoxowGDAJBgNVHRMEAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQUFAAOCAQEAl/4v3mCKfiwvPqmtFOnQ5HomJQq5W351gC5vKwP4vDKSdFDsvKtU5UMET6AnN6zHdI13AIZiOQQ8t1yv8RByMQ8dSHaoWaBkR0thzbK+Uol91Rp/TffNfneESAqvfBWKwXBTxGIxTNkJl5XXG5SyChRIan2sXvrSEGmfqxzzf3X5QFeQstRw80RbUWS21PGSgC9LMGkQVd76wqujP6P/QPjbYes5PD3xV0+6vbm3Q2NGj24s42I4Op2UEX+QjkTMd2o6FY2ek1zzcVjCyN2eNRgb/OKDjfiA/tyJ0HV1JxW3nc7BgIpRuHRI63NLWzIxe8233LgIf+y1oypT2W/o9Q==" CondicionesDePago="CondicionesDePago" SubTotal="1000.00" Descuento="100.00" Moneda="MXN" TipoCambio="1" Total="900.00" TipoDeComprobante="I" MetodoPago="PUE" LugarExpedicion="72000" xmlns:cfdi="http://www.sat.gob.mx/cfd/3"><cfdi:Emisor Rfc="TEST010203001" Nombre="Pablo Neruda Perez" RegimenFiscal="612" /><cfdi:Receptor Rfc="TEST010203001" Nombre="RECEPTOR" UsoCFDI="G02" /><cfdi:Conceptos><cfdi:Concepto ClaveUnidad="C81" ClaveProdServ="84111506" NoIdentificacion="1234567890" Cantidad="1" Unidad="ACT" Descripcion="Pago" ValorUnitario="1000" Importe="1000.00" Descuento="100.00"><cfdi:Impuestos><cfdi:Traslados><cfdi:Traslado Base="1000" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="160.00" /></cfdi:Traslados><cfdi:Retenciones><cfdi:Retencion Base="1000" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="160.00" /></cfdi:Retenciones></cfdi:Impuestos></cfdi:Concepto></cfdi:Conceptos><cfdi:Impuestos TotalImpuestosRetenidos="160.00" TotalImpuestosTrasladados="160.00"><cfdi:Retenciones><cfdi:Retencion Impuesto="002" Importe="160.00" /></cfdi:Retenciones><cfdi:Traslados><cfdi:Traslado Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="160.00" /></cfdi:Traslados></cfdi:Impuestos><cfdi:Complemento><tfd:TimbreFiscalDigital Version="1.1" RfcProvCertif="PAC010101TE0" UUID="B810FDB8-7E57-7E57-7E57-C6E0876DC543" FechaTimbrado="2020-09-14T19:59:02" SelloCFD="Ab0Qf4ZDeokzh+pBEgkFvsXvqm6r7BBIii6aDsZ6Juw1DIT+h2gmqnGmVnxKp+T4jpenm0zJiIOnIWDzH3nrznibG/onVrVx8VBMGqCGA5weHnMn3/ya+URbxUOKSOEq35nnhljvsh+ScjylJnXiEei4GmKidh86GWtoyJUGRXu12YatFg5j3IzhfZcXgrWj2wUtoCJUnIulCXq5O2VJOre+TEk65L/C/ystfRm5WZfjzKHeyFBwys6fWOaaSuFaOZRUvJed7tSX4SEczar77rbdE7cXv1zQXoCGzCbcD3WfpQh3AvrcdqM2SFAUlpg5Sv5gHVEZmGr1Ds98RH99Ug==" NoCertificadoSAT="20001000000300022323" SelloSAT="At1seULwiETA9ZPzU7z7tpx7KqhpvQ79UeYIzDJexE/bv2DxP9CA/KTfhAhVgGdHBitkcChdUv0lNZrhyRxvXza6T6kQ7RYzB/txmgnUGOtn9J4HZMLBBwgmahIKLbWHRZcUFoHR69Ktjf+C4zvokLu/db55e70+ra/EO2/pDcbqUVvbNiZS9WrUbH/0YuM4+54VINLUxJXOtnSWsyiI6/NQfwnmNpkvtJH92CIeAGNOfs/3fQtoGVk/Z+8gQCB+3JQeqyXm/YOZjCiaA42hcXDAZFS46QUL1MzAFVE42ODas0BdpEX2D9+9zBcfYwTBuencFSp80Be1WA3cRxmttQ==" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" xsi:schemaLocation="http://www.sat.gob.mx/TimbreFiscalDigital http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd" /></cfdi:Complemento></cfdi:Comprobante>'
'''xml = ELT.parse('./facturas/procesados/XML_Ejemplo_33.xml')
file= PATH + '/facturas/procesados/test.xml'
with open(file, 'w') as filetowrite:
    filetowrite.write(xml)'''
    
    
# mover archivo - Rodri
#shutil.move('./facturas/no_procesados/XML_Ejemplo_33.xml', './facturas/procesados/')

#RSA.importKey(open("/Users/roo/Downloads/TimbradoCFDI-master/certKey/key.pem", "rb").read())

'''key = open (PATH + "/certKey/key.pem", "rb").read()
rsakey = RSA.importKey(key)
signer = PKCS1_v1_5.new(rsakey)
digest = SHA256.new()
digest.update(base64.b64decode(cadena_original))
sello = signer.sign(digest)
base64sing =base64.b64encode(sello)
print (base64sing.decode('utf-8'))'''