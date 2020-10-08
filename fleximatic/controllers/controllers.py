# -*- coding: utf-8 -*-
from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv import expression
import base64
import json
from datetime import datetime
from datetime import timedelta
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response
import logging
import copy
_logger = logging.getLogger(__name__)
import pytz
import json
class Flexomatic(http.Controller):
     @http.route('/flexi/items/',  type='http', auth='none')
     def index(self, **kw):
         data = json.loads(kw['json'])
         return str(data)

