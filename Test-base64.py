import base64
import lxml.etree as ET
import os
#from M2Crypto import RSA
import hashlib

PATH = os.path.abspath(os.path.dirname(__file__))

# ->> Certificado a Base64
'''cert_file = open(PATH + "\\certKey\\CertificadoFirmadoPF.cer","rb")  # r = read, b = binario
cert = base64.b64encode(cert_file.read())
certificado = cert.decode('utf-8')
print (certificado)'''

# ->> Cadena Original
'''xml_file = open(PATH + "/XML_Ejemplo_33.xml","r")
dom = ET.parse(xml_file)
xslt = ET.parse(PATH + "/xslt/cadenaoriginal_3_3.xslt")
transform = ET.XSLT(xslt)
cadena_original = transform(dom)'''
#print(ET.tostring(newxml, pretty_print = True))
#print(str(cadena_original))
#file = open("cadena_original.txt", "w")
#file.write(str(cadena_original))

# ->> Sello
'''key = RSA.load_key(PATH + "/certKey/key.pem")
digest = hashlib.new('sha256', str(cadena_original).encode('utf-8')).digest()
sello = base64.b64encode(key.sign(digest,"sha256"))
print(sello.decode('utf-8'))'''
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
