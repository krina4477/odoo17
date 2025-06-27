from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class POSScrapWizard(models.TransientModel):
    _name = 'pos.scrap.wizard'
    _description = 'POS Scrap Wizard'

    quantity = fields.Float(string="Quantity", required=True)
    reason = fields.Text(string="Reason")

    def apply_scrap(self):
        # import pdb
        # pdb.set_trace()
        active_ids = self.env.context.get('active_ids', [])
        pos_lines = self.env['pos.order.line'].browse(active_ids)

        for line in pos_lines:
            if self.quantity != line.qty:
                raise ValidationError(
                    _("Scrap quantity must be equal to the available quantity. Available quantity: %s") % line.qty
                )

            scrap_vals = {
                'product_id': line.product_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'scrap_qty': self.quantity,
                'company_id': line.company_id.id,
                'date_done': line.order_id.date_order,
                'origin': line.order_id.session_id.name,
            }
            scrap_value = self.env['stock.scrap'].create(scrap_vals)

            scrap_history_vals = {
                'date': fields.Date.today(),
                'pos_session': line.order_id.session_id.id,
                'user_id': self.env.uid,
                'partner_id': line.order_id.partner_id.id,
                'table_id': line.order_id.table_id.id,
                'customer_count': line.order_id.customer_count,
                'pos_config': line.order_id.config_id.name,
                'reason': self.reason,
                'scrap_location_id': scrap_value.scrap_location_id.id,
                'product_id': line.product_id.id,
                'quantity': self.quantity,
                'subtotal': line.price_subtotal,
                'price_unit': line.price_unit
            }
            scrap_history = self.env['pos.scrap.history'].create(scrap_history_vals)

            scrap_history_line_vals = {
                'scrap_history_id': scrap_history.id,
                'product_id': line.product_id.id,
                'quantity': self.quantity,
                'subtotal': line.price_subtotal,
                'price_unit': line.price_unit
            }
            scrap_line = self.env['pos.scrap.history.line'].create(scrap_history_line_vals)

            if line.order_id.session_id.id == self.env.context.get('active_session_id'):
                line.order_id.sudo().write({
                    'scrap_history_line_ids': [(4, scrap_line.id)],
                })

            line.qty -= self.quantity

            # line.qty -= self.quantity
            # if line.qty <= 0:
            #     line.unlink()

            # self.env['bus.bus']._sendone(line.order_id.partner_id, 'discuss.channel/leave')
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'line_delete', {'id': line.id,'order_id': line.order_id.id, 'product_id': line.product_id.id})

            if line.qty <= 0:
                line.unlink()

        return True