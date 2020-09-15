'''
Aplicación que se encarga de realizar el Timbrado CFDI de facturas
de ERP Soluciones.
PAC: Folios Digitales

            ****ERP Soluciones****
'''

# Librerias
# Para lectura de XML
# Para conexion a BD
from zeep import Client         # Para el consusmo del WS
import sys          # Para leer parametros externos


'''Consumo del Web Service de Folios Digitales'''

usuario = "EPT040421D33"
password = "contRa$3na"

# Cliente
wsdl = "https://app.foliosdigitalespac.com/WSTimbrado33Test/WSCFDI33.svc?WSDL"
client = Client(wsdl)

cadena = """<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd" Version="3.3" Folio="FOL123456" Fecha="2020-09-13T09:36:11" Sello="Ab0Qf4ZDeokzh+pBEgkFvsXvqm6r7BBIii6aDsZ6Juw1DIT+h2gmqnGmVnxKp+T4jpenm0zJiIOnIWDzH3nrznibG/onVrVx8VBMGqCGA5weHnMn3/ya+URbxUOKSOEq35nnhljvsh+ScjylJnXiEei4GmKidh86GWtoyJUGRXu12YatFg5j3IzhfZcXgrWj2wUtoCJUnIulCXq5O2VJOre+TEk65L/C/ystfRm5WZfjzKHeyFBwys6fWOaaSuFaOZRUvJed7tSX4SEczar77rbdE7cXv1zQXoCGzCbcD3WfpQh3AvrcdqM2SFAUlpg5Sv5gHVEZmGr1Ds98RH99Ug==" FormaPago="01" NoCertificado="20001000000300022823" Certificado="MIIDhDCCAmygAwIBAgIUMjAwMDEwMDAwMDAzMDAwMjI4MjMwDQYJKoZIhvcNAQEFBQAwSzEVMBMGA1UEAwwMQS5DLiBQcnVlYmFzMRAwDgYDVQQKDAdQcnVlYmFzMQswCQYDVQQGEwJNWDETMBEGA1UEBwwKQ3VhdWh0ZW1vYzAeFw0xNzA0MjgxODMwMzZaFw0yMjEwMTkxODMwMzZaMIGQMRswGQYDVQQDDBJQYWJsbyBOZXJ1ZGEgUGVyZXoxGzAZBgNVBCkMElBhYmxvIE5lcnVkYSBQZXJlejEbMBkGA1UECgwSUGFibG8gTmVydWRhIFBlcmV6MSUwIwYDVQQtDBxURVNUMDEwMjAzMDAxIC8gVEVTVDEwMzE3QTQ2MRAwDgYDVQQLDAdDRU5UUkFMMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4S8y29PfV6zBib8HEx/SK2XaUBeAb5YZbL+MHjX4K710kFdskgYhX35N0StfN5wbHLIsnj0eLtIk7gjXmaAjF6PkM9jtRtUrWgS22lcah0K7ws+nqfhNFuPX9rfm8SXzkBFDjUiBmW0U0Lz3cT/fEoJiqMxTwgJyhpuQ3vIcrv85cUaNpnf85eSCWVXGFmXpZD7EgXKLQulD1OOQbqcBPF6sK0wlz27HeQsM0X+2rO+RJvWAsHqIT4z0Sct4FFzj3XjGiF+DK8KxbQOmWpTnOSw0k9oKHmrFG3c1GxxyhvHoz+RurZFWPwuCWAzaUDhwq3uB6dtP7foeEjUUFlRD/wIDAQABoxowGDAJBgNVHRMEAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQUFAAOCAQEAl/4v3mCKfiwvPqmtFOnQ5HomJQq5W351gC5vKwP4vDKSdFDsvKtU5UMET6AnN6zHdI13AIZiOQQ8t1yv8RByMQ8dSHaoWaBkR0thzbK+Uol91Rp/TffNfneESAqvfBWKwXBTxGIxTNkJl5XXG5SyChRIan2sXvrSEGmfqxzzf3X5QFeQstRw80RbUWS21PGSgC9LMGkQVd76wqujP6P/QPjbYes5PD3xV0+6vbm3Q2NGj24s42I4Op2UEX+QjkTMd2o6FY2ek1zzcVjCyN2eNRgb/OKDjfiA/tyJ0HV1JxW3nc7BgIpRuHRI63NLWzIxe8233LgIf+y1oypT2W/o9Q==" CondicionesDePago="CondicionesDePago" SubTotal="1000.00" Descuento="100.00" Moneda="MXN" TipoCambio="1" Total="900.00" TipoDeComprobante="I" MetodoPago="PUE" LugarExpedicion="72000" xmlns:cfdi="http://www.sat.gob.mx/cfd/3">
    <cfdi:Emisor Rfc="TEST010203001" Nombre="Pablo Neruda Perez" RegimenFiscal="612"/>
    <cfdi:Receptor Rfc="TEST010203001" Nombre="RECEPTOR" UsoCFDI="G02"/>
    <cfdi:Conceptos>
        <cfdi:Concepto ClaveUnidad="C81" ClaveProdServ="84111506" NoIdentificacion="1234567890" Cantidad="1" Unidad="ACT" Descripcion="Pago" ValorUnitario="1000" Importe="1000.00" Descuento="100.00">
            <cfdi:Impuestos>
                <cfdi:Traslados>
                    <cfdi:Traslado Base="1000" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="160.00"/>
                </cfdi:Traslados>
                <cfdi:Retenciones>
                    <cfdi:Retencion Base="1000" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="160.00"/>
                </cfdi:Retenciones>
            </cfdi:Impuestos>
        </cfdi:Concepto>
    </cfdi:Conceptos>
    <cfdi:Impuestos TotalImpuestosRetenidos="160.00" TotalImpuestosTrasladados="160.00">
        <cfdi:Retenciones>
            <cfdi:Retencion Impuesto="002" Importe="160.00"/>
        </cfdi:Retenciones>
        <cfdi:Traslados>
            <cfdi:Traslado Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="160.00"/>
        </cfdi:Traslados>
    </cfdi:Impuestos>
</cfdi:Comprobante>"""

referencia = "001"

print(client.service.TimbrarCFDI(usuario, password, cadena, referencia))
