# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_orderlines_for_report(self):
        line_dic = {}
        for line in self.order_line:
            if line.product_id.categ_id.name in line_dic:
                line_dic[line.product_id.categ_id.name].append(line)
            else:
                line_dic[line.product_id.categ_id.name] = [line]
        return line_dic

