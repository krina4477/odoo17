from odoo import fields, models, _
from odoo.tests.common import Form


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def button_mark_done_new(self):
        action = self.action_serial_mass_produce_wizard()
        wizard = Form(self.env['stock.assign.serial'].with_context(**action['context']))
        # # Let the wizard generate all serial numbers
        # # wizard.next_serial_number = "sn#1"
        # # wizard.next_serial_count = count
        action = wizard.save().generate_serial_numbers_production()
        # # Reload the wizard to apply generated serial numbers
        wizard = Form(self.env['stock.assign.serial'].browse(action['res_id']))
        wizard.save().apply()
        backorder_ids = self.procurement_group_id.mrp_production_ids
        if backorder_ids:
            backorder_ids.filtered(lambda mo1: mo1.state in {'confirmed', 'to_close', 'progress'}).button_mark_done()
        return True
