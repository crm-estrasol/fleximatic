from odoo import api, fields, models
from odoo.addons.website.tools import get_video_embed_code
import logging
_logger = logging.getLogger(__name__)
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ean_code = fields.Char("Código EAN (Walmart)")
   
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            ean_code =  self.env['ir.config_parameter'].sudo().get_param('fleximatic.ean_code'),    
        )
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        ean_code = self.ean_code or False 
        param.set_param('fleximatic.ean_code', ean_code)
       