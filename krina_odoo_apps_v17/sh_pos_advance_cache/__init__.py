# Copyright (C) Softhealer Technologies.
# Part of Softhealer Technologies.
from . import models


from odoo import api, SUPERUSER_ID


def create_config_cache_data(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    update_cache_data_model = env['pos.config.cache.data']
    update_cache_data_model.sudo().import_cache_data()
    update_cache_data_model.sudo().import_cache_all_data()
