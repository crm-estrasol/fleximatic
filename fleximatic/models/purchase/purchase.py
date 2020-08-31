from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import logging
_logger = logging.getLogger(__name__)

class purchaseFleximatic(models.Model):
    _inherit = 'purchase.order'

    is_freight = fields.Boolean('Is freight')

    