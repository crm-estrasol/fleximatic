
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import timedelta, datetime, date
from odoo import tools
from odoo import api, fields, models
from odoo import fields, models
import sys
import itertools
from operator import itemgetter
import functools 
#Filtrar
from collections import deque
import json
from odoo import http
from odoo.http import request
from odoo.tools import ustr
from odoo.tools.misc import xlwt
#XLS
import xlwt
import base64
from io import BytesIO

from PIL import Image
import os.path

class FleximaticSaleOrder(models.Model):
    _inherit  = "sale.order"

 #WIZARD
    def show_pricelistAvaible(self):
        if self.order_line:   
            view_id = self.env.ref('fleximatic.view_sale_pricelist_wizard').id
            view = {
                'name': ('Descuento'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'tomcat.sale.discount.wizard',
                'views':  [(view_id,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context':{'default_sale':self.id},
                'domain': {'product_id': [('partner_id', 'in', [item.product_id.id for item in self.order_line] )]},
                #'domain': [('product_id', 'in', )]   
                
                }
        return view 