from odoo import api, models, fields
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from datetime import datetime, date

class PosScrapHistory(models.Model):
    _name = 'pos.scrap.history'
    _description = "POS Scrap History"
    _rec_name = 'pos_session'

    date = fields.Date(string='Date')
    pos_session = fields.Many2one('pos.session', string='Session', required=True)
    user_id = fields.Many2one('res.users', string='Responsible',default=lambda self: self.env.uid)
    partner_id = fields.Many2one('res.partner', string='Customer')
    table_id = fields.Many2one('restaurant.table', string='Table', readonly=True)
    customer_count = fields.Integer(string='Guests', readonly=True)
    pos_config = fields.Char("Point of Sale")
    reason = fields.Text(string="Reason")
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    price_unit = fields.Float(string="Unit Price")
    subtotal = fields.Float(string='Subtotal')
    order_id = fields.Many2one('pos.order', string="POS Order", required=False)

    scrap_location_id = fields.Many2one('stock.location', 'Scrap Location',store=True, required=True)
    scrap_history_line_ids = fields.One2many('pos.scrap.history.line', 'scrap_history_id', string="Scrap History Lines")


class PosScrapHistoryLine(models.Model):
    _name = 'pos.scrap.history.line'
    _description = "POS Scrap History Line"

    scrap_history_id = fields.Many2one('pos.scrap.history', string="Scrap History", required=True)
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    price_unit = fields.Float(string="Unit Price")
    subtotal = fields.Float(string='Subtotal')
    order_id = fields.Many2one('pos.order', string="POS Order", required=False)
