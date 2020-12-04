    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximatiAccountMove(models.Model):
    
    _inherit = 'account.move'
    def adenda_walmart(self,actual_inv):
        actual_inv = actual_inv
        segments = []
        control = "555"
        #Var needed
        date_s1 = actual_inv.invoice_date.strftime("%Y")[-2:]+actual_inv.invoice_date.strftime("%m")+actual_inv.invoice_date.strftime("%d")
        hour_s1 = fields.Datetime.today().strftime("%H%S")
        invoiceId_s3 = str(actual_inv.id)
        date_s4 = actual_inv.invoice_date.strftime("%Y")+actual_inv.invoice_date.strftime("%m")+actual_inv.invoice_date.strftime("%d")
        letterTot_s5 = "Pendiente "
        purchaseOrderId_s6 = "Pendiente"
        invoiceSerie_s7 = "pendiente"
        buyEanCode_s
        creditDays
        #----------Segments
        segments.append("""UNB+UNOA:2+MXG1390:ZZ+925485MX00:8+%s:%s+%s'""" % (date_s1,hour_s1,control))
        #pendiente
        date_s6 = actual_inv.invoice_date.strftime("%Y")+actual_inv.invoice_date.strftime("%m")+actual_inv.invoice_date.strftime("%d")
        #Fixed node 2
        segments.append("""UNH+1+INVOIC:D:01B:UN:AMC002'""")
        #Invoice node 3
        segments.append("""BGM+380+%s+9'""" % (invoiceId_s3))
        #Invopice date node 4
        segments.append("""DTM+137:%s:102'""" % (date_s4))
        #Letter total node 5
        segments.append("""FTX+ZZZ+++%s+ES'""" % (letterTot_s5))
        #Purchase Order id node 5
        segments.append("""RFF+ON:%s'""" % (purchaseOrderId_s6))
        #Purchase date id node 6
        segments.append("""DTM+171:%s:102'""" % (date_s6))
        #Invoice seriie  node 7
        segments.append("""RFF+BT:%s'""" % (invoiceSerie_s7))
        #Invoice seriie  node 8 zero is approve number  
        segments.append("""RFF+ATZ:0'""")
        #Client ean purshase node *   
        segments.append("""NAD+BY+%s::9++NUEVA WAL MART DE MEXICO S DE RL DE:CV+NEXTENGO # 78:COL SANTA CRUZ ACAYUCAN+CIUDAD DE MEXICO+DF+02770'""")
        #RFC buyer number  
        segments.append("""RFF+GN:NWM9709244W4'""")
        #Fleximatic address  
        segments.append("""NAD+SU+7504023427002::9++FLEXIMATIC SA DE CV+CAMINO REAL DE COLIMA:901 14+SANTA ANITA+JALISCO+45645'""")
        #RFC fleximatic  
        segments.append("""RFF+GN:FLE980113E95'""")
        #RFC fleximatic  
        segments.append("""RFF+IA:%s'""")
        return "".join(segments)


        # Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
           
def literal_number(num):
    lista_centana = ["",("CIEN","CIENTO "),"DOSCIENTOS ","TRESCIENTOS","CUATROCIENTOS","QUINIENTOS","SEISCIENTOS","SETECIENTOS","OCHOCIENTOS","NOVECIENTOS"]
    lista_decena = ["",("DIEZ","ONCE",
                        "DOCE","TRECE","CATORCE",
                        "QUINCE","DIECISEIS",
                        "DIECISIETE","DIECIOCHO","DIECINUEVE"), 
                        ("VEINTE","VEINTI"),
                        ("TREINTA","TREINTA Y "),
                        ("CUARENTA" , "CUARENTA Y "), 
                        ("CINCUENTA" , "CINCUENTA Y "),
                        ("SESENTA" , "SESENTA Y "),
                        ("SETENTA" , "SETENTA Y "),
                        ("OCHENTA" , "OCHENTA Y "),
    					("NOVENTA" , "NOVENTA Y ")
    				]
    lista_unidad = ["",("UN" , "UNO"),"DOS","TRES","CUATRO","CINCO","SEIS","SIETE","OCHO","NUEVE"]
    indicador = [("",""),("MIL","MIL"),("MILLON","MILLONES"),("MIL","MIL"),("BILLON","BILLONES")]
    def numero_to_letras(numero):
        arrays = last(numero)
        word = ""
        index = 0
        print(arrays)
        lenarray = len(arrays)
        for x in arrays:
            index+=1
            x = "".join(('00' if len(x) == 1 else '0' if  len(x) == 2 else "", x))
            
            value = indicador[index][0] if x == '001' and index != lenarray else centenas(x) 
            word +=value +" " +(str(indicador[index][1]+"0") if index != lenarray else '')   
        return word    
    def last(a):
        ln = len(a) 
        if ln == 5 :
            return [a[:2]] + last(a[-3:]) 
        if ln == 4:
            return [a[:1]] + last(a[-3:]) 
        if  ln <= 3:
            return [a]
        return [a[-3:]] + last(a[:-3])  
    def centenas(number):
        if len(number) == 3:
            dec = ""
            cent = ""
            if number[1]  == "0" and number[2]  == "0" and number[0] == "1":
                return lista_centana[ int(number[0]) ][0]
            elif number[0] == "1" :
                 cent = lista_centana[ int(number[0]) ][1]            
            else:
                cent = lista_centana[ int(number[0]) ]  
            if  number[1] == "1":
                print(str(int(number[2])))
                cent +=" "+lista_decena[ int(number[1]) ][int(number[2])]
                return cent
            elif number[1] != "0":
                cent +=" "+lista_decena[ int(number[1]) ][ 0 if int(number[2]) == 0 else 1 ]
            if number[1] == "2"  and  number[2] == "1":
                dec = lista_unidad[ int(number[2]) ][0]
            elif number[2] == "1":
                dec = lista_unidad[ int(number[2]) ][1]
            else:
                 dec =(" " if number[1] == "0" else "") +  lista_unidad[ int(number[2]) ]
            
            return cent+dec
    return numero_to_letras(num)
print(literal_number("150321"))
 
def numero_to_letras(numero):
    indicador = [('', ''), ('MIL', 'MIL'), ('MILLON', 'MILLONES'),
                 ('MIL', 'MIL'), ('BILLON', 'BILLONES')]
    entero = int(numero)
    decimal = int(round((numero - entero) * 100))

    # print 'decimal : ',decimal

    contador = 0
    numero_letras = ''
    while entero > 0:
        a = entero % 1000
        if contador == 0:
            en_letras = convierte_cifra(a, 1).strip()
        else:
            en_letras = convierte_cifra(a, 0).strip()
        if a == 0:
            numero_letras = en_letras + ' ' + numero_letras
        elif a == 1:
            if contador in (1, 3):
                numero_letras = indicador[contador][0] + ' ' \
                    + numero_letras
            else:
                numero_letras = en_letras + ' ' \
                    + indicador[contador][0] + ' ' + numero_letras
        else:
            numero_letras = en_letras + ' ' + indicador[contador][1] \
                + ' ' + numero_letras
        numero_letras = numero_letras.strip()
        contador = contador + 1
        entero = int(entero / 1000)
    numero_letras = numero_letras + ' con ' + str(decimal) + '/100'
    print( numero )
    print( numero_letras)


def numero_to_letras(numero):
    indicador = [('', ''), ('MIL', 'MIL'), ('MILLON', 'MILLONES'),
                 ('MIL', 'MIL'), ('BILLON', 'BILLONES')]
    entero = int(numero)
    decimal = int(round((numero - entero) * 100))

    # print 'decimal : ',decimal

    contador = 0
    numero_letras = ''
    while entero > 0:
        a = entero % 1000
        if contador == 0:
            en_letras = convierte_cifra(a, 1).strip()
        else:
            en_letras = convierte_cifra(a, 0).strip()
        
        if a == 0:
            numero_letras = en_letras + ' ' + numero_letras
        elif a == 1:
            if contador in (1, 3):
                numero_letras = indicador[contador][0] + ' ' \
                    + numero_letras
                    
            else:
                numero_letras = en_letras + ' ' \
                    + indicador[contador][0] + ' ' + numero_letras
                
        else:
            numero_letras = en_letras + ' ' + indicador[contador][1] \
                + ' ' + numero_letras
            print(numero_letras)
        numero_letras = numero_letras.strip()
        contador = contador + 1
        entero = int(entero / 1000)
    numero_letras = numero_letras + ' con ' + str(decimal) + '/100'
    print( numero )
    print( numero_letras)


def convierte_cifra(numero, sw):
    lista_centana = [
        '',
        ('CIEN', 'CIENTO'),
        'DOSCIENTOS',
        'TRESCIENTOS',
        'CUATROCIENTOS',
        'QUINIENTOS',
        'SEISCIENTOS',
        'SETECIENTOS',
        'OCHOCIENTOS',
        'NOVECIENTOS',
        ]
    lista_decena = [
        '',
        (
            'DIEZ',
            'ONCE',
            'DOCE',
            'TRECE',
            'CATORCE',
            'QUINCE',
            'DIECISEIS',
            'DIECISIETE',
            'DIECIOCHO',
            'DIECINUEVE',
            ),
        ('VEINTE', 'VEINTI'),
        ('TREINTA', 'TREINTA Y '),
        ('CUARENTA', 'CUARENTA Y '),
        ('CINCUENTA', 'CINCUENTA Y '),
        ('SESENTA', 'SESENTA Y '),
        ('SETENTA', 'SETENTA Y '),
        ('OCHENTA', 'OCHENTA Y '),
        ('NOVENTA', 'NOVENTA Y '),
        ]
    lista_unidad = [
        '',
        ('UN', 'UNO'),
        'DOS',
        'TRES',
        'CUATRO',
        'CINCO',
        'SEIS',
        'SIETE',
        'OCHO',
        'NUEVE',
        ]
    centena = int(numero / 100)
    decena = int((numero - centena * 100) / 10)
    unidad = int(numero - (centena * 100 + decena * 10))

    # print "centena: ",centena, "decena: ",decena,'unidad: ',unidad

    texto_centena = ''
    texto_decena = ''
    texto_unidad = ''

    # Validad las centenas

    texto_centena = lista_centana[centena]
    if centena == 1:
        if decena + unidad != 0:
            texto_centena = texto_centena[1]
        else:
            texto_centena = texto_centena[0]

    # Valida las decenas

    texto_decena = lista_decena[decena]
    if decena == 1:
        texto_decena = texto_decena[unidad]
    elif decena > 1:
        if unidad != 0:
            texto_decena = texto_decena[1]
        else:
            texto_decena = texto_decena[0]

     # Validar las unidades
     # print "texto_unidad: ",texto_unidad

    if decena != 1:
        texto_unidad = lista_unidad[unidad]
    
        if unidad == 1 :
            texto_unidad = texto_unidad[sw]
            return '%s %s%s' % (texto_centena, texto_decena, texto_unidad)
    if decena == 2 :
        return '%s %s%s' % (texto_centena, texto_decena, texto_unidad)
    return '%s %s %s' % (texto_centena, texto_decena, texto_unidad)
print(numero_to_letras(120))