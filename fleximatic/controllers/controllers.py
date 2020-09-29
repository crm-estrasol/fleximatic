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

class Flexomatic(http.Controller):
     @http.route('/flexi/find_of/', auth='public')
     def index(self, **kw):
         return "Hello, world"

