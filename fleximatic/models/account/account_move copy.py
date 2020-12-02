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