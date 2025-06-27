# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from odoo import http



class ComboDeals(models.Model):
    _name = "combo.deals"
    _description = "Combo Deals"

    name = fields.Char(string="Combo Deal",required=True)
    related_product_tmpl_id = fields.Many2one('product.template',string="Related Product",readonly=True,copy=False)
    combo_line_ids = fields.One2many('combo.lines','combo_id',string="Combo Lines",copy=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('approve', 'Approve'),
                              ('expire', 'Expire')], string='Combo Status',store=True, readonly=True, default='draft')
    currency_id = fields.Many2one('res.currency', default=lambda x: x.env.company.currency_id)
    amount_total = fields.Float(string='Amount Total',compute="_compute_total",store=True,copy=False)
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0,copy=False)
    price_total = fields.Float(string='Total',compute="_compute_total",store=True,copy=False)
    combo_count = fields.Integer(string="Combo order count",compute="_get_combo_pos_order",default=0)

    @api.depends('related_product_tmpl_id','related_product_tmpl_id.product_variant_id')
    def _get_combo_pos_order(self):
        for rec in self:
            pos_orders = self.env['pos.order'].search([('lines.product_id.id','=',rec.related_product_tmpl_id.product_variant_id.id)])
            if pos_orders:
                rec.combo_count = len(pos_orders)
            else:
                rec.combo_count = 0

    def action_view_combo_pos(self):
        self.ensure_one()
        tree_view_id = self.env.ref('point_of_sale.view_pos_order_tree').id
        form_view_id = self.env.ref('point_of_sale.view_pos_pos_form').id
        pos_orders = self.env['pos.order'].search([('lines.product_id.id','=',self.related_product_tmpl_id.product_variant_id.id)])
        return {
            "type": "ir.actions.act_window",
            "res_model": "pos.order",
            "views": [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'domain': [('id','in',pos_orders.ids or [])],
            "name": _("Pos Orders"),
        }

    def approve_combo(self):
        return self.write({'state':'approve'})

    def expire_combo(self):
        return self.write({'state':'expire'})

    def reset_to_draft(self):
        return self.write({'state':'draft'})

    @api.depends('combo_line_ids','combo_line_ids.product_uom_qty','combo_line_ids.price_subtotal','discount')
    def _compute_total(self):
        for rec in self:
            line_subtotal = sum(rec.mapped('combo_line_ids').mapped('price_subtotal'))
            rec.amount_total = line_subtotal
            if rec.discount:
                discount_amount = (line_subtotal - (line_subtotal * (rec.discount / 100)))
                rec.price_total = discount_amount
            else:
                rec.price_total = line_subtotal
            rec.related_product_tmpl_id.list_price = rec.price_total

    @api.model
    def create(self,vals):
        res = super(ComboDeals, self).create(vals)
        if vals.get('name'):
            product_val = {
                            'name': vals.get('name'),
                            'type': 'consu',
                            'list_price': 15.00,
                            'categ_id': self.env.ref('product.product_category_all').id, 
                            'sale_line_warn': 'no-message',
                            'tracking': 'none',
                            'taxes_id': [(6,0,[])],
                            'uom_id': self.env.ref('uom.product_uom_unit').id,
                            'uom_po_id': self.env.ref('uom.product_uom_unit').id,
                            'is_combo_deal': True,
                            'available_in_pos': True,
                        }
            combo_product = self.env['product.template'].create(product_val)
            res.related_product_tmpl_id = combo_product.id
            combo_product.combo_deals_id = res.id
            combo_product.list_price = res.price_total
        return res

class CombiLines(models.Model):
    _name = "combo.lines"
    _description = "Combo Deal Lines"

    combo_id = fields.Many2one('combo.deals', string='Combo Reference', index=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product',required=True)
    name = fields.Text(string='Description',required=True)
    product_uom_qty = fields.Float(string='Quantity',default=1.0,required=True)
    price_unit = fields.Float('Unit Price', digits='Product Price',required=True)
    price_subtotal = fields.Float(string='Subtotal',readonly=True)
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.default_code:
                    rec.name = '['+str(rec.product_id.default_code)+'] '+ rec.product_id.name
                else:
                    rec.name = rec.product_id.name
                rec.price_unit = rec.product_id.list_price
                rec.price_subtotal = rec.product_id.list_price

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        for rec in self:
            if rec.product_uom_qty:
                rec.price_subtotal = rec.product_id.list_price * rec.product_uom_qty

class rpc_service(http.Controller):
    @http.route('/rpc_service', type="json", auth="user")
    def fetch_combo_deal(self, **data):
        filter_dict = {}

        ProductObj = http.request.env['product.product']
        vall = data.get('ld')
        if vall is not None:
            for val in vall:
                if val and isinstance(val, dict) and 'product_id' in val:
                    product_id = val.get('product_id')
                    product_rec = ProductObj.browse(product_id)
                    if product_rec and product_rec.is_combo_deal:
                        pass
                    else:
                        qty = float(val.get('qty', 0))
                        if filter_dict.get(product_id):
                            filter_dict[product_id] += qty
                        else:
                            filter_dict[product_id] = qty

            pos_order_line_list = [(val, filter_dict[val]) for val in filter_dict]
            pos_order_line_list.sort()
            all_combo_deal = http.request.env['combo.deals'].sudo().search([])
            for combo in all_combo_deal:
                combo_line = [(line.product_id.id, line.product_uom_qty) for line in combo.combo_line_ids]
                combo_line.sort()
                if pos_order_line_list == combo_line and combo.state == 'approve':
                    return combo.related_product_tmpl_id.product_variant_id.id
                else:
                    combo_line.clear()
            return False
