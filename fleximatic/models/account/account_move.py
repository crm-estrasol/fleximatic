    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximatiAccountMove(models.Model):
    
    _inherit = 'account.move'
    def adenda_walmart(self,actual_inv):
        actual_inv = actual_inv
        #Vars needed
        control=str(0000)
        date_s1 = fields.Datetime.today().strftime("%Y")[-2:]+fields.Datetime.today().strftime("%m")+fields.Datetime.today().strftime("%d")
        hour_s1 = fields.Datetime.today().strftime("%H%S")
        invoiceId_s3 = str(actual_inv.id)
        date_s4 = actual_inv.invoice_date.strftime("%Y")+actual_inv.invoice_date.strftime("%m")+actual_inv.invoice_date.strftime("%d")
        totalLetter_s5 = "PENDIENTE PESOS MX"
        orderBuy_s5 = "Manual"
        orderDate_s6 = "Manual"
        invoiceSerie_s7  = actual_inv.name
        buyEanCode_s9 = "Manual"
        numberSupplier9s_s13 = "Manual"
        if actual_inv.invoice_payment_term_id:
            days = sum([ line.days for line in  actual_inv.invoice_payment_term_id.line_ids]) 
        else:
            days = 0
        creditDays_s16 = days

        segments = [
        """UNB+UNOA:2+MXG1390:ZZ+925485MX00:8+%s:%s+%s'""" % (date_s1,hour_s1,control)  , 
        """UNH+1+INVOIC:D:01B:UN:AMC002'""",
        """BGM+380+%s+9'""" % (invoiceId_s3), 
        """DTM+137:%s:102'""" % (date_s4) ,
        """FTX+ZZZ+++%s+ES'""" % (totalLetter_s5),
        """RFF+ON:%s'""" % (orderBuy_s5), 
        """DTM+171:%s:102'""" % (orderDate_s6), 
        """RFF+BT:%s'""" % (invoiceSerie_s7) ,
        """RFF+ATZ:0'""",
        """NAD+BY+%s::9++NUEVA WAL MART DE MEXICO S DE RL DE:CV+NEXTENGO # 78:COL SANTA CRUZ ACAYUCAN+CIUDAD DE MEXICO+DF+02770'""" % (buyEanCode_s9),
        """RFF+GN:NWM9709244W4'""",
        """NAD+SU+7504023427002::9++FLEXIMATIC SA DE CV+CAMINO REAL DE COLIMA:901 14+SANTA ANITA+JALISCO+45645'""",
        """RFF+GN:FLE980113E95'""",
        """RFF+IA:%s'""" %( numberSupplier9s_s13),
        """NAD+ST+7507003116583::9++WALMART DC+CARRETERA EL SALTO NO 420:LAS ALAMEDAS+TLAJOMULCO DE ZUNIGA+JALISCO+45679'""",
        """CUX+2:MXN:4'""",
        """PAT+1++5:3:D:%s'""" % (creditDays_s16),
        ]
        return "".join(segments)