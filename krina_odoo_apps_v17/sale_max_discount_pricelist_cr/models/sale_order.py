# -*- coding: utf-8 -*-

# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models,api,fields,_


class SaleOrderLineInherit(models.Model):
    
    _inherit = 'sale.order.line'
    
    pricelist_id = fields.Many2one('product.pricelist',string='Pricelist')

   
    def _get_pricelist(self, product,pricelist,type):
        print("*** sale.order.line in _get_pricelist function *** ")

        #code
        attributes_price_extra = [
            ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
                lambda ptav:
                    ptav.price_extra and
                    ptav not in product.product_template_attribute_value_ids
            )
        ]
        if attributes_price_extra:
            print("***  sale.order.line in _get_pricelist function attributes_price_extra ***")
            product = product.with_context(
                attributes_price_extra=tuple(attributes_price_extra)
            )
            print("***  sale.order.line in _get_pricelist function attributes_price_extra if product  ***",product)

        # if pricelist.discount_policy == 'with_discount':
        #     print("_____pricelist.discount_policy_____________",pricelist.discount_policy)
        #     return product.with_context(pricelist=pricelist.id, uom=self.product_uom.id).list_price
        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)
        # print("***sale.order.line in _get_pricelist function in product_context*** ",product_context)

        final_price, rule_id = pricelist.with_context(product_context)._get_product_price_rule(product or self.product_id, self.product_uom_qty or 1.0)
        base_price = 0
        print("---",final_price)
        # base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, pricelist.id)
        # if currency != pricelist.currency_id:
        #     base_price = currency._convert(
        #         base_price, pricelist.currency_id,
        #         self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())

        
        if type == 'min':
            print("******if")
            return min(base_price, final_price)
        else:
            print("********else if type")
            return max(base_price, final_price)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        print("*** sale.order.line _compute_amount**** ")
        for line in self:
            partner_pricelists_ids = line.order_id.partner_id.pricelist_ids
            partner_pricelists_dict = {}

            if line.product_id:
                print("*** sale.order.line _compute_amount line.product_id**** ")
                if partner_pricelists_ids:
                    print("*** sale.order.line _compute_amount line.product_id in partner_pricelists_ids**** ")

                    for pricelist_id in partner_pricelists_ids:
                        product = line.product_id.with_context(
                            partner=line.order_id.partner_id,
                            quantity=line.product_uom_qty,
                            date=line.order_id.date_order,
                            pricelist=pricelist_id.id,
                            uom=line.product_uom.id,
                            from_sale_order=True,
                        )

                        data = self.env['account.tax']._fix_tax_included_price_company(line._get_pricelist(product,pricelist_id,'max'), product.taxes_id, self.tax_id, self.company_id)

                        if data != line.product_id.lst_price:
                            partner_pricelists_dict.update({pricelist_id : data})


                    print("partner_pricelists_dict",partner_pricelists_dict)
                    if partner_pricelists_dict:
                        print("*** sale.order.line _compute_amount partner_pricelists_dict**** ")
                        order_line_list = []
                        temp = max(partner_pricelists_dict.values())
                        res = [key for key in partner_pricelists_dict if partner_pricelists_dict[key] == temp]
                        pricelist = res[0]
                        price_unit = partner_pricelists_dict.get(pricelist)

                        product_id = line.product_id.with_context(
                            partner=line.order_id.partner_id,
                            quantity=line.product_uom_qty,
                            date=line.order_id.date_order,
                            pricelist=pricelist.id,
                            uom=line.product_uom.id,
                            from_sale_order = True,
                        )
                        apply_price_unit = self.env['account.tax']._fix_tax_included_price_company(
                            line._get_pricelist(product,pricelist,'max'), line.product_id.taxes_id, line.tax_id, line.company_id)
                        print("********apply_price_unit",apply_price_unit)
                        if pricelist.discount_policy == 'without_discount' and price_unit:
                            print("*********************1 if")
                            discount = max(0, (apply_price_unit - price_unit) * 100 / apply_price_unit)
                        else:
                            print("*********************1 else")
                            discount = 0
                        order_line_list.append((1, line.id, {'price_unit': apply_price_unit,'pricelist_id' : pricelist.id}))
                        print("**********order_line_list.append",order_line_list.append('discount'))
                        line.order_id.update({'order_line': order_line_list})
                        print("**********line.order_id.update",line.order_id.update)
                    else:
                        print("******3 else else else")
                        line._onchange_product_id_warning()
                        line.pricelist_id = False
                else:
                    print("******4 else else else")
                    line._onchange_product_id_warning()
                    line.pricelist_id = False

        return super(SaleOrderLineInherit,self)._compute_amount()


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    pricelist_ids = fields.Many2many('product.pricelist',compute='compute_pricelist_ids',string='Custom Pricelists')
    print("####sale.order####")
    @api.depends('order_line')
    def compute_pricelist_ids(self):
        print("### sale.order incompute_pricelist_ids ####")
        for order in self:
            order.pricelist_ids = order.order_line.mapped('pricelist_id')
            
            
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        print("### onchange_partner_id ###")
        # super(SaleOrderInherit,self).onchange_partner_id()
        for line in self.order_line:
            line._compute_amount()

        self.compute_pricelist_ids()
    

