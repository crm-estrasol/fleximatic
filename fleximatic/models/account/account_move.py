# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximatiAccountMove(models.Model):
    
    _inherit = 'account.move'
   
    addenda_verify = fields.Char(related="partner_id.l10n_mx_edi_addenda.name")
    total_letter =  fields.Char('Total en numero')
    num_order = fields.Char('Numero de orden de compra')
    date_order = fields.Date('Fecha orden')
    buyEan_code = fields.Char('Código EAN comprador')
    number_supplier = fields.Char('Numero proveedor 9 digitos',size=9)

    def adenda_walmart(self,actual_inv):
        actual_inv = actual_inv
        #Vars needed
        control = self.env['ir.sequence'].next_by_code('fleximatic.adenda.walmart.sequence')
        date_s1 = fields.Datetime.today().strftime("%Y")[-2:]+fields.Datetime.today().strftime("%m")+fields.Datetime.today().strftime("%d")
        hour_s1 = fields.Datetime.today().strftime("%H%S")
        invoiceId_s3 = str(actual_inv.id)
        date_s4 = actual_inv.invoice_date.strftime("%Y")+actual_inv.invoice_date.strftime("%m")+actual_inv.invoice_date.strftime("%d")
        total = actual_inv.amount_total
        total_untx = actual_inv.amount_untaxed
        amount_tax = actual_inv.amount_tax
        totalLetter_s5 = self.numero_to_letras(total) 
        orderBuy_s6 = actual_inv.num_order
        #PENDIENTE FORMATO
        orderDate_s7 = actual_inv.date_order.strftime("%Y")+actual_inv.date_order.strftime("%m")+actual_inv.date_order.strftime("%d")
        invoiceSerie_s8  = actual_inv.name
        buyEanCode_s10 = actual_inv.buyEan_code
        #Global pendiente
        sellEanCode_s12 ="7504023427002" 
        numberSupplier9s_s14 = actual_inv.number_supplier
        if actual_inv.invoice_payment_term_id:
            days = sum([ line.days for line in  actual_inv.invoice_payment_term_id.line_ids]) 
        else:
            days = 0
        creditDays_s17 = days

        segments = [
        """UNB+UNOA:2+MXG1390:ZZ+925485MX00:8+%s:%s+%s'""" % (date_s1,hour_s1,control)  , 
        """UNH+1+INVOIC:D:01B:UN:AMC002'""",
        """BGM+380+%s+9'""" % (invoiceId_s3), 
        """DTM+137:%s:102'""" % (date_s4) ,
        """FTX+ZZZ+++%s+ES'""" % (totalLetter_s5),
        """RFF+ON:%s'""" % (orderBuy_s6), 
        """DTM+171:%s:102'""" % (orderDate_s7), 
        """RFF+BT:%s'""" % (invoiceSerie_s8) ,
        """RFF+ATZ:0'""",
        """NAD+BY+%s::9++NUEVA WAL MART DE MEXICO S DE RL DE:CV+NEXTENGO # 78:COL SANTA CRUZ ACAYUCAN+CIUDAD DE MEXICO+DF+02770'""" % (buyEanCode_s10),
        """RFF+GN:NWM9709244W4'""",
        """NAD+SU+%s::9++FLEXIMATIC SA DE CV+CAMINO REAL DE COLIMA:901 14+SANTA ANITA+JALISCO+45645'""" % (sellEanCode_s12),
        """RFF+GN:FLE980113E95'""",
        """RFF+IA:%s'""" %( numberSupplier9s_s14),
        """NAD+ST+7507003116583::9++WALMART DC+CARRETERA EL SALTO NO 420:LAS ALAMEDAS+TLAJOMULCO DE ZUNIGA+JALISCO+45679'""",
        """CUX+2:MXN:4'""",
        """PAT+1++5:3:D:%s'""" % (creditDays_s17),
        ]
        total_segments = len(segments)
        segments_elements = [
               "".join( ["""LIN+1++%s:SRV::9'""" % (prod.product_id.barcode),
               """PIA+1+%s:IN'""" % (prod.product_id.default_code),
               """IMD+F++:::%s %s::ES'""" % (prod.product_id.description_sale,self.get_date_adenda(prod.l10n_mx_edi_customs_number) ),
               """QTY+47:%s:EA'""" % (str(prod.tax_base_amount+prod.price_subtotal )),
               """MOA+203:%s'""" % (str(prod.price_subtotal )),
               """PRI+AAA:%s::::EA'""" % ( str(prod.price_unit ) ),
               """TAX+7+VAT+++:::%s+B'""" % ( "".join( [str(x.amount) for x in  prod.tax_ids] )  ),
               """MOA+124:%s'""" % (str(prod.tax_base_amount ))] )
                                                    for prod in actual_inv.invoice_line_ids] 
        segments.append("".join(segments_elements) )
        line_ammount = len(segments_elements)
        total_segments += 7 + (line_ammount * 8) 
        last_segment = [ 
                """UNS+S'""",
                """CNT+2:%s'"""  % ( str(line_ammount) ),
                """MOA+9:%s'"""  % (str(total)),
                """MOA+79:%s'"""  % (str(total_untx)),
                """MOA+125:%s'"""  % (str(	total_untx )),
                """TAX+7+VAT+++:::16.00+B'""",#Pendiente 
                """MOA+124:%s'"""  % (str(amount_tax)),
                """UNT+%s+1'"""  % (str(total_segments)),
                """UNZ+1+%s'""" % ( control ),
        ]
        segments.append("".join(last_segment) )
        return "".join(segments)
    def get_date_adenda(self,adendas):
        if adendas:
            texto = "Fecha Documento Aduanero "
            adendas =  adendas.split(',')
            for adenda in adendas:
                adenda = self.env['stock.landed.cost'].sudo().search( [('l10n_mx_edi_customs_number','=',adenda)] )
                texto+= "%s/%s/%s" % (adenda.date.strftime("%d"),adenda.date.strftime("%m"),adenda.date.strftime("%Y")[-2:] ) +" "
            return texto
        return ""
    def numero_to_letras(self,numero):
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
                en_letras = self.convierte_cifra(a, 1).strip()
            else:
                en_letras = self.convierte_cifra(a, 0).strip()
            
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
        numero_letras = numero_letras + ' CON ' + str(decimal) + '/100'
        return numero_letras

    def convierte_cifra(self,numero, sw):
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
  
