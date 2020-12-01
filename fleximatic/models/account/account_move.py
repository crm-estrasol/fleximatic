    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximatiAccountMove(models.Model):
    
    _inherit = 'account.move'
    def adenda_walmart(self,actual_inv):
        actual_inv = actual_inv
        segments = []
        control = "555"
        date_s1 = actual_inv.invoice_date.strftime("%Y")[-2:]+actual_inv.invoice_date.strftime("%m")+actual_inv.invoice_date.strftime("%d")
        hour_s1 = fields.Datetime.today().strftime("%H%S")
        segments.append("""UNB+UNOA:2+MXG1390:ZZ+925485MX00:8+%s:%s+%s'""" % (date_s1,hour_s1,control))
        return "".join(segments)