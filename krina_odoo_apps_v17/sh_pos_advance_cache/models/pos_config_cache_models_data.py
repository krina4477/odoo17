# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosConfigCacheModelData(models.Model):
    _name = "pos.config.cache.model.data"

    config_id = fields.Many2one("pos.config", string="Pos Config")
    session_id = fields.Many2one("pos.session", string="Pos Session", domain=[('active', '=', False)])
    model_name = fields.Char("Model Name")
    res_id  = fields.Integer("Res ID")
    json_data = fields.Text("JSON Data")
    product_id = fields.Many2one("product.product")