# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)


class warningClient(models.TransientModel):
    _name = 'warning.client'

    name = fields.Text(string='Name')