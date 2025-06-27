from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    def update_cache_data_and_model(self):
        update_cache_data_model = self.env['pos.config.cache.data']
        update_cache_data_model.sudo().import_cache_data()
        update_cache_data_model.sudo().import_cache_all_data()
