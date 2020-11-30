    # -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class fleximatiAccountMove(models.Model):
    
    _inherit = 'account.move'
    def adenda_walmart(self,actual_inv):
        actual_inv = actual_inv
        segments = []
        numero_control = "555"
        fecha_s1 = ""
        hora_s1 = ""
        segments.append("""UNB+UNOA:2+MXG1390:ZZ+925485MX00:8+%s:%s+%s'""" % (fecha_s1,hora_s1,numero_control))
        return "".join(segments)