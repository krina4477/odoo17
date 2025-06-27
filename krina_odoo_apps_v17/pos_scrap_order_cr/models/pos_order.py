from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    config_id = fields.Many2one('pos.config', related='order_id.config_id', store=True)

    def pos_scrap_button(self):
        if self.env['pos.config'].search([('is_pos_scrap', '=', True)]):
            return {
                'type': 'ir.actions.act_window',
                'name': 'POS Scrap',
                'res_model': 'pos.scrap.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'active_ids': self.ids, 'active_session_id': self.order_id.session_id.id},
            }
        else:
            raise UserError(_("The POS Scrap feature is disabled for this configuration."))

class PosOrder(models.Model):
    _inherit = 'pos.order'

    scrap_history_line_ids = fields.One2many(
        'pos.scrap.history.line', 'order_id',
        string="Scrap History Lines",
    )


class PosConfiguration(models.Model):
    _inherit = 'pos.config'

    is_pos_scrap = fields.Boolean(
        string='Pos Scrap'
    )

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_pos_scrap = fields.Boolean(
        string='Pos Scrap',
        related="pos_config_id.is_pos_scrap",
        readonly=False
    )