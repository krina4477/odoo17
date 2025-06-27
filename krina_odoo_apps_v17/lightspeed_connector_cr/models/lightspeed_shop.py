# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import datetime, json
import pytz
from dateutil.parser import parse
from odoo import models, api, _, fields
import base64
import requests

import logging

_logger = logging.getLogger(__name__)


def get_as_base64(url):
    try:
        return base64.b64encode(requests.get(url).content)
    except:
        return False


def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


class LightSpeedShop(models.Model):
    _name = 'lightspeed.shop'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Lightspeed Shop'

    name = fields.Char(string='Name')
    api_key = fields.Char(string='API Key')
    api_secret = fields.Char(string='API Secret')
    code = fields.Char(string='Code')
    token = fields.Char(string='Token')
    url = fields.Char(string='URL', compute='_compute_url')
    refresh_token = fields.Char(string='Refresh Token')
    account_id = fields.Char(string='Account ID')
    language = fields.Char(string='Language Code')
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse for DO")
    order_fetch_from = fields.Datetime(string='Orders Fetch from')
    do_complete = fields.Boolean(srting='Create DO?')
    invoice_complete = fields.Boolean(srting='Create Invoice?')
    payment_complete = fields.Boolean(srting='Create Payment?')
    # email_to = fields.Char('Email To', readonly=False, help='Failure jobs will be sent on given email address')
    failure_jobs = fields.One2many(
        'lightspeed.failure.log', 'lightspeed_id', string='Failure Jobs',
        compute='_compute_failure_jobs', store=True)

    def action_view_results(self, res_data, res_ids):
        return {
            'name': res_data[0],
            'view_mode': 'tree,form',
            'domain': [('id', 'in', res_ids)],
            'res_model': res_data[1],
            'type': 'ir.actions.act_window',
            'context': {},
        }

    def _compute_url(self):
        if self.api_key and self.api_secret:
            self.url = 'https://cloud.lightspeedapp.com/oauth/authorize.php?response_type=code&client_id=%s&scope=employee:all' % self.api_key


    def generate_access_token(self):
        url = "https://cloud.merchantos.com/oauth/access_token.php"
        payload = {
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "grant_type": "authorization_code"
        }
        if self.code and not self.refresh_token: payload.update({'code': self.code, "grant_type": "authorization_code"})
        if self.refresh_token: payload.update({'refresh_token': self.refresh_token, "grant_type": "refresh_token"})
        response_req = requests.request("POST", url, data=payload)
        response = response_req.json()
        if response.get('access_token', False): self.token = response.get('access_token')
        if response.get('refresh_token', False): self.refresh_token = response.get('refresh_token')
        if response.get('refresh_token'):
            account_req_url = "https://api.lightspeedapp.com/API/V3/Account.json"
            header = {
                "Authorization": "Bearer " + self.token,
                "Accept": "application/json"
            }
            response = requests.get(account_req_url, headers=header, data=payload)
            if response.json().get('Account', False):
                self.account_id = response.json().get('Account').get('accountID')
                self.refresh_token = self.refresh_token

    def _compute_failure_jobs(self):
        for lightshop in self:
            lightshop.failure_jobs = self.env['lightspeed.failure.log'].search(
                [('is_send', '=', False), ('lightspeed_id', '=', self.id)])

    def lightspeed_update_product_stock(self, product_id):
        self.generate_access_token()
        if product_id and product_id.lightspeed_id:
            url = 'https://api.lightspeedapp.com/API/V3/Account/%s/Item/%s.json' % (
                self.account_id, product_id.lightspeed_id)
            data = json.dumps(
                {"ItemShops":
                    {
                        "ItemShop":
                            {
                                "itemShopID": self._context.get('itemshopid'),
                                "qoh": product_id.qty_available
                            }
                    }
                }
            )
            header = {
                "Authorization": "Bearer " + self.token,
                "Accept": "application/json"
            }
            requests.put(url, data=data, headers=header)

    def _update_lightspeed_price(self, product_id):
        shop_ids = self.search([])

        for shop in shop_ids:
            check = True
            while check:
                if not product_id:
                    lightspeed_product_ids = self.env['product.product'].sudo().search([
                        ('shop_id', '=', shop.id)
                    ], limit=1)
                else:
                    lightspeed_product_ids = product_id
                if lightspeed_product_ids:
                    for product in lightspeed_product_ids:
                        variant_dict = {

                            # 'defaultCost': product.standard_price,
                            # 'customSku': product.default_code,

                            "Prices": {
                                "ItemPrice": [
                                    {
                                        "amount": product.lst_price,
                                        "useTypeID": "1",
                                        "useType": "Default"
                                    }
                                ]
                            }
                        }
                        url = 'https://api.lightspeedapp.com/API/V3/Account/%s/Item/%s.json' % (
                            shop.account_id, product.lightspeed_id)
                        header = {
                            "Authorization": "Bearer " + shop.token,
                            "Accept": "application/json"
                        }
                        responese = requests.put(url, headers=header, data=json.dumps(variant_dict))

                        if responese.status_code == 200:
                            return True

                        else:
                            check = False

    def lightspeed_get_response_by_type(self, type, retrive_key, lightspeed_id=False, params={}):
        if not self.token:
            self.generate_access_token()
        account_id = self.account_id

        header = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/json"
        }
        if not lightspeed_id:
            # Get total records count
            total_count_url = 'https://api.lightspeedapp.com/API/V3/Account/%s/%s.json' % (
                account_id, type)
            if type == 'Item':
                total_count_url += '?load_relations=["ItemShops"]'
            if type == 'Customer':
                total_count_url += '?load_relations=["Contact"]'

            total_count_resp = requests.get(total_count_url, headers=header, data={})

        else:
            url = ''
            if is_int(lightspeed_id):
                url = 'https://api.lightspeedapp.com/API/V3/Account/%s/%s/%s.json' % (
                    account_id, type, int(lightspeed_id))
            elif isinstance(lightspeed_id, bool):
                url = 'https://api.lightspeedapp.com/API/V3/Account/%s/%s/%s.json' % (
                    account_id, type)
            else:
                url = 'https://api.lightspeedapp.com/API/V3/Account/%s/%s/%s.json' % (
                    account_id, type)
            if type == 'Item':
                url += '?load_relations=["ItemShops"]'
            if type == "Customer":
                url += '?load_relations=["Contact"]'
            total_count_resp = requests.get(url, headers=header, data={})

        if isinstance(total_count_resp.json().get(type, False), str):
            total_count = [eval(total_count_resp.json().get(type, False))]

        elif isinstance(total_count_resp.json().get(type, False), dict):
            total_count = [total_count_resp.json().get(type, False)]

        elif isinstance(total_count_resp.json().get(type, False), list):
            total_count = total_count_resp.json().get(type, False)

        else:
            total_count = total_count_resp.json().get(type, False)
        return total_count

    def import_category(self, lightspeed_id=False):
        categ_obj = self.env['product.category'].sudo()
        categ_ids = categ_obj
        self.generate_access_token()
        category_result = self.lightspeed_get_response_by_type('Category', 'category',
                                                               lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'Category', 'categories')

        category_result = sorted(category_result, key=lambda x: x['categoryID'])
        for category in category_result:
            try:
                if category.get('name') or category.get('fullPathName'):
                    categ_vals = {
                        'name': category.get("name") if category.get("name") else category.get('fullPathName'),
                        'lightspeed_id': category.get("categoryID", False),
                        'shop_id': self.id,
                    }

                    if category.get('parentID'):
                        parent_id = categ_obj.search(
                            [('lightspeed_id', '=', str(category.get('parentID')))])
                        if parent_id:
                            categ_vals.update({'parent_id': parent_id.id})

                    category_id = categ_obj.search([
                        ('lightspeed_id', '=', str(categ_vals.get('lightspeed_id'))), ('shop_id', '=', self.id),
                    ])
                    if category_id:
                        category_id.write(categ_vals)
                        categ_ids |= category_id
                    else:
                        category_id = categ_obj.create(categ_vals)
                        categ_ids |= category_id
            except Exception as e:
                vals = {
                    'record_name': category.get("title") if category.get("title") else category.get('fulltitle'),
                    'import_obj': 'Category',
                    'failure_msg': str(e),
                    'response_json': category,
                    'lightspeed_id': self.id,
                }
                self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Product Categories', 'product.category'], categ_ids.ids)

    def import_tags(self, lightspeed_id=False):
        tag_obj = self.env['product.tag'].sudo().search([])
        tag_ids = tag_obj
        self.generate_access_token()
        tags_result = self.lightspeed_get_response_by_type('Tag', 'tag',
                                                           lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'Tag', 'tags')
        if tags_result:
            for tag in tags_result:
                try:
                    if tag.get('name'):
                        tag_vals = {
                            'name': tag.get('name'),
                            'lightspeed_id': tag.get("tagID", False),
                            'shop_id': self.id,
                        }
                        tag_id = tag_obj.search([
                            ('lightspeed_id', '=', str(tag_vals.get('lightspeed_id'))), ('shop_id', '=', self.id),
                        ])
                        if tag_id:
                            tag_id.write(tag_vals)
                        else:
                            tag_id = tag_obj.create(tag_vals)
                        tag_ids |= tag_id
                except Exception as e:
                    vals = {
                        'record_name': tag.get('name'),
                        'import_obj': 'Tag',
                        'failure_msg': str(e),
                        'response_json': tag,
                        'lightspeed_id': self.id,
                    }
                    self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Product Tags', 'product.tag'], tag_ids.ids)

    def import_attributes(self, lightspeed_id=False):
        attr_obj = self.env['product.attribute'].sudo()
        attr_val_obj = self.env['product.attribute.value'].sudo()
        attr_ids = attr_obj
        self.generate_access_token()
        sets_result = self.lightspeed_get_response_by_type('ItemAttributeSet', 'set',
                                                           lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'ItemAttributeSet', 'sets')
        for set in sets_result:
            try:
                if set.get('itemAttributeSetID'):
                    attribute_vals = {
                        'name': set.get('name'),
                        'lightspeed_id': set.get("itemAttributeSetID", False),
                        'shop_id': self.id,
                    }
                    attribute_id = attr_obj.search([
                        ('lightspeed_id', '=', str(attribute_vals.get('lightspeed_id'))), ('shop_id', '=', self.id),
                    ])
                    try:
                        if not attribute_id:
                            attribute_id = attr_obj.create(attribute_vals)
                        else:
                            attribute_id.write(attribute_vals)
                    except Exception as e:
                        vals = {
                            'record_name': set.get('name'),
                            'import_obj': 'Attribute',
                            'failure_msg': str(e),
                            'lightspeed_id': self.id,
                        }
                        self.env['lightspeed.failure.log'].sudo().create(vals)

                    attr_ids |= attribute_id
            except Exception as e:
                vals = {
                    'record_name': set.get('name'),
                    'import_obj': 'Attribute Options',
                    'failure_msg': str(e),
                    'response_json': set,
                    'lightspeed_id': self.id,
                }
                self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Product Attributes', 'product.attribute'], attr_ids.ids)

    def import_taxes(self, lightspeed_id=False):
        tax_obj = self.env['account.tax'].sudo()
        tax_ids = tax_obj
        self.generate_access_token()
        taxes_result = self.lightspeed_get_response_by_type('TaxCategory', 'tax',
                                                            lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'TaxCategory', 'taxes')
        if taxes_result:
            for tax in taxes_result:
                try:
                    if tax.get('taxCategoryID'):
                        tax_vals = {
                            'name': tax.get('tax1Name'),
                            'lightspeed_id': tax.get("taxCategoryID", False),
                            'shop_id': self.id,
                            'amount': tax.get("tax1Rate", False),
                            'type_tax_use': 'sale',
                            'price_include': tax.get("isTaxInclusive", False),
                        }
                        tax_id = tax_obj.search([
                            ('lightspeed_id', '=', str(tax_vals.get('lightspeed_id'))), ('shop_id', '=', self.id),
                        ])
                        if not tax_id:
                            tax_id = tax_obj.search([
                                ('amount', '=', tax.get("tax1Rate", False)),
                                ('type_tax_use', '=', 'sale')
                            ], limit=1)
                        if tax_id:
                            tax_id.write(tax_vals)
                            tax_ids |= tax_id
                        else:
                            tax_id = tax_obj.create(tax_vals)
                            tax_ids |= tax_id
                except Exception as e:
                    vals = {
                        'record_name': tax.get('tax1Name'),
                        'import_obj': 'Tax',
                        'failure_msg': str(e),
                        'response_json': tax,
                        'lightspeed_id': self.id,
                    }
                    self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Taxes', 'account.tax'], tax_ids.ids)


    def _create_product_attribute(self, attribute_id=False):
        if attribute_id:
            attribute = self.env['product.attribute'].browse(attribute_id)
            if attribute:
                check = True
                while check:
                    att_dict = {
                        "name": attribute.name,
                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/ItemAttributeSet.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(att_dict))
                    if responese.status_code == 200:
                        return True
                    else:
                        check = False

    def _create_tax(self, tax_id=False):
        if tax_id:
            tax = self.env['account.tax'].browse(tax_id)
            if tax:
                check = True
                while check:
                    tax_dict = {
                        "isTaxInclusive": "true" if tax.price_include else "false",
                        "tax1Name": tax.name,
                        "tax1Rate": tax.amount,
                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/TaxCategory.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(tax_dict))
                    print("responese.status_code==============", responese.status_code)
                    if responese.status_code == 200:
                        return True
                    else:
                        check = False

    def _update_vendor(self, vendor_id=False):
        if vendor_id:
            partner = self.env['res.partner'].browse(vendor_id)
            if partner:
                check = True
                while check:
                    acc_number = ''
                    if partner.bank_ids:
                        acc_number = partner.bank_ids[0].acc_number

                    vendor_dict = {

                        "name": partner.name,
                        "accountNumber": acc_number,
                        "priceLevel": "",
                        "updatePrice": "true",
                        "updateCost": "true",
                        "updateDescription": "true",
                        "shareSellThrough": "false"

                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Vendor/{}.json'.format(self.account_id,
                                                                                                  partner.lightspeed_id)

                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.put(url, headers=header, data=json.dumps(vendor_dict))
                    if responese.status_code == 200:
                        return True
                    else:
                        check = False

    def import_shops(self, lightspeed_id=False):
        warhosue_obj = self.env['lightspeed.shop.shop'].sudo()
        warhosue_ids = warhosue_obj
        self.generate_access_token()

        # https://api.lightspeedapp.com/API/V3/Account/{{accountID}}/Shop.json
        shops_result = self.lightspeed_get_response_by_type('Shop', 'shops', lightspeed_id) \
            if lightspeed_id else self.lightspeed_get_response_by_type('Shop', 'shops')
        for shop in shops_result:
            try:
                if shop.get('shopID'):
                    shop_vals = {
                        'name': shop.get('name'),
                        'lightspeed_id': shop.get("shopID", False),
                        'shop_id': self.id,
                    }
                    shop_id = warhosue_obj.search([
                        ('lightspeed_id', '=', str(shop_vals.get('lightspeed_id'))), ('shop_id', '=', self.id),
                    ])
                    if shop_id:
                        shop_id.write(shop_vals)
                        warhosue_ids |= shop_id
                    else:
                        shop_id = warhosue_obj.create(shop_vals)
                        warhosue_ids |= shop_id
            except Exception as e:
                vals = {
                    'record_name': shop.get('name'),
                    'import_obj': 'Shop',
                    'failure_msg': str(e),
                    'response_json': shop,
                    'lightspeed_id': self.id,
                }
                self.env['lightspeed.failure.log'].sudo().create(vals)
        return warhosue_ids

    def _create_product_category(self, categ_id=False):
        if categ_id:
            product_category = self.env['product.category'].browse(categ_id)
            if product_category:
                check = True
                while check:
                    categ_dict = {
                        "name": product_category.name,
                    }
                    if product_category.parent_id and product_category.parent_id.lightspeed_id:
                        categ_dict['parentID']  = product_category.parent_id.lightspeed_id

                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Category.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(categ_dict))
                    if responese.status_code == 200:
                        product_category.lightspeed_id = responese.json().get('Category').get('categoryID')
                        return True
                    else:
                        check = False

    def _update_product_category(self, categ_id=False):
        if categ_id:
            product_category = self.env['product.category'].browse(categ_id)
            if product_category:
                check = True
                while check:
                    categ_dict = {
                        "name": product_category.name,
                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Category/{}.json'.format(self.account_id,
                                                                                                    product_category.lightspeed_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.put(url, headers=header, data=json.dumps(categ_dict))
                    if responese.status_code == 200:

                        return True
                    else:
                        check = False

    def _create_product_tag(self, tag_id=False):
        if tag_id:
            tag = self.env['product.tag'].browse(tag_id)
            if tag:
                check = True
                while check:
                    tag_dict = {
                        'name': tag.name
                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Tag.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(tag_dict))
                    print("responese===============", responese)
                    if responese.status_code == 200:
                        tag.lightspeed_id = responese.json().get('Tag').get('tagID')
                        return True
                    else:
                        check = False

    def _update_product_tag(self, tag_id=False):
        if tag_id:
            tag = self.env['product.tag'].browse(tag_id)
            if tag:
                check = True
                while check:
                    tag_dict = {
                        'name': tag.name
                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Tag/{}.json'.format(self.account_id,
                                                                                               tag.lightspeed_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.put(url, headers=header, data=json.dumps(tag_dict))
                    if responese.status_code == 200:
                        return True
                    else:
                        check = False

    def unlink_partner(self, vendor_id=False):
        check = True
        while check:
            url = 'https://api.lightspeedapp.com/V3/Account/{}/Vendor/{}.json'.format(self.account_id, vendor_id)
            header = {
                "Authorization": "Bearer " + self.token,
                "Accept": "application/json"
            }
            responese = requests.delete(url, headers=header)
            print("url=======================", url)

            if responese.status_code == 200:

                return True
            else:
                check = False

    def _create_product(self, product_id=False):
        if product_id:
            product = self.env['product.product'].browse(product_id)
            if product:
                check = True
                while check:
                    product_dict = {
                        "defaultCost": product.standard_price,
                        "discountable": "true",
                        "tax": "true",
                        "itemType": "default",
                        "serialized": "false",
                        "description": product.name,
                        "modelYear": "0",
                        "upc": "",
                        "ean": "",
                        "customSku": product.default_code,
                        "manufacturerSku": "",
                        "publishToEcom": "true",
                        "categoryID": "1",
                        "taxClassID": "1",
                        "departmentID": "0",
                        "itemMatrixID": "0",
                        "manufacturerID": "0",
                        "seasonID": "0",
                        "defaultVendorID": "0",
                        "Prices": {
                            "ItemPrice": [
                                {
                                    "amount": product.lst_price,
                                    "useTypeID": "1",
                                    "useType": "Default"
                                },

                            ]}
                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Item.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(product_dict))
                    print("=ccccccccc=c======c======c", responese)
                    if responese.status_code == 200:
                        return True
                    else:
                        check = False

    def _create_customer(self, customer_id=False):
        if customer_id:
            partner = self.env['res.partner'].browse(customer_id)
            if partner:
                check = True
                while check:
                    first_name, last_name = partner.name.split(" ", 1)

                    customer_dict = {

                        "firstName": first_name,
                        "lastName": last_name,
                        "title": "",
                        "company": "",
                        "companyRegistrationNumber": "",
                        "vatNumber": partner.vat,
                        "Contact": {
                            "custom": "",
                            "noEmail": "false",
                            "noPhone": "false",
                            "noMail": "false",
                            "Addresses": {
                                "ContactAddress": {
                                    "address1": partner.street,
                                    "address2": partner.street2,
                                    "city": partner.city,
                                    "state": partner.state_id.name,
                                    "stateCode": partner.state_id.code,
                                    "zip": partner.zip,
                                    "country": partner.country_id.name,
                                    "countryCode": partner.country_id.code
                                }
                            },
                            "Phones": [{
                                "number": partner.mobile,
                                "useType": "Mobile"
                            }],
                            "Emails": partner.email,
                            "Websites": partner.website,
                        },

                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Customer.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(customer_dict))
                    print("==================c=c=c=c=c=c=", responese.status_code)
                    if responese.status_code == 200:
                        return True

                    else:
                        check = False

    def _create_vendor(self, vendor_id=False):
        if vendor_id:
            partner = self.env['res.partner'].browse(vendor_id)
            if partner:
                check = True
                while check:
                    acc_number = ''
                    if partner.bank_ids:
                        acc_number = partner.bank_ids[0].acc_number

                    vendor_dict = {

                        "name": partner.name,
                        "accountNumber": acc_number,
                        "priceLevel": "",
                        "updatePrice": "true",
                        "updateCost": "true",
                        "updateDescription": "true",
                        "shareSellThrough": "false"

                    }
                    url = 'https://api.lightspeedapp.com/API/V3/Account/{}/Vendor.json'.format(self.account_id)
                    header = {
                        "Authorization": "Bearer " + self.token,
                        "Accept": "application/json"
                    }
                    responese = requests.post(url, headers=header, data=json.dumps(vendor_dict))
                    if responese.status_code == 200:
                        data = responese.json()
                        if data.get('Vendor'):
                            partner.lightspeed_id = data['Vendor']['vendorID']
                        return True
                    else:
                        check = False

    def import_products(self, lightspeed_id=False):
        product_template_obj = self.env['product.template'].sudo()
        product_product_obj = self.env['product.product'].sudo()
        categ_obj = self.env['product.category'].sudo()
        tax_obj = self.env['account.tax'].sudo()
        product_template_ids = product_template_obj

        self.generate_access_token()
        products_result = self.lightspeed_get_response_by_type('Item', 'product',
                                                               lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'Item', 'products')

        # print("products_result------------------------", products_result)
        count = 0
        if products_result:
            for pr in products_result:
                try:
                    if pr.get('itemID'):
                        try:
                            # here comes at last
                            product_template_vals = {
                                'lightspeed_id': pr.get('itemID'),
                                'default_code': pr.get('customSku'),
                                'name': pr.get('description'),
                                'active': pr.get('archived'),
                                'description': pr.get('description'),
                                'standard_price': float(pr.get('defaultCost', 0)),
                                'shop_id': self.id,
                                'detailed_type': 'product',

                            }
                            if pr.get('ItemShops'):
                                if pr['ItemShops'].get('ItemShop'):
                                    product_template_vals.update({
                                        'qty_available': int(float(pr['ItemShops']['ItemShop'][0]['qoh']))
                                    })
                            if pr.get('Prices'):
                                if pr['Prices'].get('ItemPrice'):
                                    product_template_vals.update({
                                        'list_price': int(float(pr['Prices']['ItemPrice'][0]['amount']))
                                    })

                            if int(pr.get('taxClassID')) == 0:
                                product_template_vals.update({'taxes_id': [(6, 0, [])]})
                            else:
                                tax_id = tax_obj.search([('lightspeed_id', '=', str(pr.get('taxClassID')))])
                                if not tax_id:
                                    tax_id = self.import_taxes(pr.get('taxClassID'))
                                if tax_id and hasattr(tax_id, 'id'):
                                    product_template_vals.update({'taxes_id': [(6, 0, [tax_id.id])]})

                            product_template_obj.create(product_template_vals)

                            # if int(pr.get('taxClassID')) == 0:
                            #     product_template_vals.update({'taxes_id': [(6, 0, [])]})
                            # else:
                            #     tax_id = tax_obj.search([('lightspeed_id', '=', str(pr.get('taxClassID')))])
                            #     if not tax_id:
                            #         tax_id = self.import_taxes(pr.get('taxClassID'))
                            #     product_template_vals.update({'taxes_id': [(6, 0, [tax_id.id])]})

                            # Set Categories for product (response does not have it so commented)
                            category_ids = []
                            if int(pr.get('categoryID')) == 0:
                                category_ids = []
                            else:
                                categoryID = categ_obj.sudo().search(
                                    [('lightspeed_id', '=', str(pr.get('categoryID')))])
                                if not categoryID:
                                    categoryID = self.import_category(pr.get('categoryID'))
                                if categoryID:
                                    product_template_vals.update({'categ_id': categoryID.id})
                                    category_ids += categoryID
                            if category_ids:
                                product_template_vals.update({'categ_id': category_ids[0].id})
                            product_id = False
                            if pr.get('customSku'):
                                product_id = product_product_obj.search([
                                    ('default_code', '=', pr.get('customSku')),
                                ],limit=1)
                            if pr.get('ItemShops'):
                                list_shops = []
                                shop_dict = {}
                                shop_list = pr.get('ItemShops').get('ItemShop')[1:]
                                for shopid in shop_list:
                                    shop_dict.update({shopid.get('shopID'): shopid.get('itemShopID')})
                                    # l_shop_id = self.env['lightspeed.shop.shop'].search([
                                    #     ('lightspeed_id','in',[shopid.get('shopID')])
                                    # ], limit=1)
                                list_shops.append(shop_dict)
                            product_template_vals.update({'itemshop_dict': list_shops})
                            if not product_id:
                                product_id = product_product_obj.search([
                                    ('lightspeed_id', '=', pr.get('itemID')),
                                    ('shop_id', '=', self.id),
                                ],limit=1)
                            print("ldddddddddd", product_id)
                            if not product_id:
                                try:
                                    product_template_id = product_template_obj.create(product_template_vals)

                                    warehouse = self.env['stock.warehouse'].search(
                                        [('company_id', '=', self.env.company.id)], limit=1
                                    )
                                    self.env['stock.quant'].with_context(inventory_mode=True).create({
                                        'product_id': product_template_id.product_variant_ids[0].id,
                                        'location_id': warehouse.lot_stock_id.id,
                                        'inventory_quantity': float(product_template_vals['qty_available']),
                                    })._apply_inventory()
                                    product_template_id.product_variant_id.write({

                                        'lightspeed_id': pr.get('itemID'),
                                        'lightspeed_template_id': pr.get('itemID'),
                                        'shop_id': self.id
                                    })

                                    product_template_ids |= product_template_id
                                except Exception as e:
                                    vals = {
                                        'record_name': pr.get('description'),
                                        'import_obj': 'Product Template',
                                        'failure_msg': str(e),
                                        'response_json': pr,
                                        'lightspeed_id': self.id,
                                    }
                                    self.env['lightspeed.failure.log'].sudo().create(vals)
                            else:
                                try:
                                    product_template_id = product_id.product_tmpl_id
                                    product_template_id.write(product_template_vals)
                                    product_id.write(product_template_vals)
                                    product_id.lightspeed_id = pr.get('itemID')
                                    product_template_ids |= product_id.product_tmpl_id
                                except Exception as e:
                                    vals = {
                                        'record_name': pr.get('description'),
                                        'import_obj': 'Product Template',
                                        'failure_msg': str(e),
                                        'response_json': pr,
                                        'lightspeed_id': self.id,
                                    }
                                    self.env['lightspeed.failure.log'].sudo().create(vals)
                            self.env.cr.commit()
                        except Exception as e:
                            self.env.cr.rollback()
                            continue
                    count += 1
                except Exception as e:
                    vals = {
                        'record_name': pr.get('description'),
                        'import_obj': 'Product Template',
                        'failure_msg': str(e),
                        'response_json': pr,
                        'lightspeed_id': self.id,
                    }
                    self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Products', 'product.template'], product_template_ids.ids)

    def import_customers(self, lightspeed_id=False):
        customer_obj = self.env['res.partner']
        customer_ids = customer_obj
        self.generate_access_token()
        customers_result = self.lightspeed_get_response_by_type('Customer', 'customer',
                                                                lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'Customer', 'customer')
        print("customers_result======================", customers_result)
        if customers_result:
            for customer in customers_result:
                partner_id = customer_obj.search([
                    ('lightspeed_id', '=', customer.get('customerID')),
                    ('shop_id', '=', self.id),
                ])
                if partner_id:
                    customer_ids |= partner_id
                    continue
                try:
                    company_type = 'company' if customer.get('isCompany') else 'person'
                    customer_name = customer.get('firstName')
                    if customer.get('middleName'):
                        customer_name += ' %s' % (customer.get('middleName'))
                    if customer.get('lastName'):
                        customer_name += ' %s' % (customer.get('lastName'))
                    partner_vals = {
                        'company_type': company_type,
                        'lightspeed_id': customer.get('customerID', False),
                        'vat': customer.get('vatNumber', False),
                        'lightspeed_type': 'customer',
                        'shop_id': self.id,
                        'name': customer_name,
                        'customer_rank': 1,
                    }


                    if customer.get('Contact'):
                        contact = customer['Contact']
                        # Extract email
                        email = contact.get('Emails', {}).get('ContactEmail', {})
                        if isinstance(email, dict):
                            email = email.get('address', '')
                        elif isinstance(email, list) and email:
                            email = email[0].get('address', '')

                        # import pdb;pdb.set_trace()
                        if email:
                            partner_vals['email'] = email

                        # Extract phone
                        phones = contact.get('Phones', {}).get('ContactPhone', [])
                        if isinstance(phones, list) and phones:
                            phone = phones[0].get('number')  # Get the first phone number if the list is not empty
                            if phone:
                                partner_vals['phone'] = phone

                        # Extract address
                        address = contact.get('Addresses', {}).get('ContactAddress', {})
                        if address:
                            street = address.get('address1')
                            if street:
                                partner_vals['street'] = street
                            street2 = address.get('address2')
                            if street2:
                                partner_vals['street2'] = street2
                            city = address.get('city')
                            if city:
                                partner_vals['city'] = city

                    #     customer_phone = customer['Contact']['Phones']
                    #     customer_email = customer['Contact']['Phones']

                    partner_id = customer_obj.create(partner_vals)
                    customer_ids |= partner_id
                except Exception as e:
                    vals = {
                        'record_name': customer.get('addressBillingName'),
                        'import_obj': 'Customer',
                        'failure_msg': str(e),
                        'response_json': customer,
                        'lightspeed_id': self.id,
                    }
                    self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Customers', 'res.partner'], customer_ids.ids)

    def import_suppliers(self, lightspeed_id=False):
        supplier_obj = self.env['res.partner'].sudo()
        supplier_ids = supplier_obj
        self.generate_access_token()
        suppliers_result = self.lightspeed_get_response_by_type('Vendor', 'supplier',
                                                                lightspeed_id) if lightspeed_id else self.lightspeed_get_response_by_type(
            'Vendor', 'suppliers')
        for supplier in suppliers_result:
            try:
                if supplier.get('vendorID'):
                    s_name = supplier.get('name', False)
                    if supplier.get('Reps', False) and supplier.get('Reps').get('VendorRep', False):
                        s_name = supplier.get('Reps').get('VendorRep', {}).get('firstName', '') + ' ' + supplier.get(
                            'Reps').get('VendorRep', {}).get('lastName', '')

                    supplier_vals = {
                        'name': s_name,
                        'lightspeed_id': supplier.get('vendorID', False),
                        'shop_id': self.id,
                        'lightspeed_type': 'supplier',
                        'supplier_rank': 1,
                    }

                    if supplier.get('country_id') and supplier.get('country_id').get('code'):
                        country_id = self.env['res.country'].sudo().search(
                            [('code', '=', supplier.get('country_id').get('code').upper())], limit=1)
                        if country_id:
                            supplier_vals.update({'country_id': country_id.id})

                    if supplier.get('region') and supplier_vals.get('country_id'):
                        state_id = self.env['res.country.state'].sudo().search(
                            [('name', '=', supplier.get('region')), ('country_id', '=', supplier_vals['country_id'])],
                            limit=1)
                        if state_id:
                            supplier_vals.update({'state_id': state_id.id})

                    supplier_id = supplier_obj.search([
                        ('lightspeed_type', '=', 'supplier'),
                        ('lightspeed_id', '=', supplier.get('vendorID')),  # Correct key here
                        ('shop_id', '=', self.id)
                    ], limit=1)
                    if not supplier_id:
                        supplier_id = supplier_obj.create(supplier_vals)
                    else:
                        supplier_id.write(supplier_vals)

                    supplier_ids |= supplier_id

            except Exception as e:
                vals = {
                    'record_name': supplier.get('name', False),
                    'import_obj': 'Supplier',
                    'failure_msg': str(e),
                    'response_json': supplier,
                    'lightspeed_id': self.id,
                }
                self.env['lightspeed.failure.log'].sudo().create(vals)
        return self.action_view_results(['Vendors', 'res.partner'], supplier_ids.ids)

    def import_orders(self, lightspeed_id=False):
        sale_order_obj = self.env['sale.order'].sudo()
        sale_order_ids = sale_order_obj
        sol_obj = self.env['sale.order.line'].sudo()
        sol_ids = sol_obj

        self.generate_access_token()

        orders_result = self.lightspeed_get_response_by_type('Sale', 'order', lightspeed_id) if lightspeed_id \
            else self.lightspeed_get_response_by_type('Sale', 'orders', params={})
        if orders_result:
            for order in orders_result:
                sale_order_id = sale_order_obj
                order_date = parse(order.get('createTime')).astimezone(pytz.utc).replace(tzinfo=None)
                if order_date > self.order_fetch_from or order_date == self.order_fetch_from:
                    try:
                        if order.get('saleID') and order.get('customerID'):
                            partner_id = self.env['res.partner'].search(
                                [('lightspeed_id', '=', order.get('customerID')),
                                 ('shop_id', '=', self.id)], limit=1).id
                            if not partner_id:
                                partner_list = self.import_customers(order.get('customerID')).get('domain')[0][2]
                                if partner_list:
                                    partner_id = partner_list[0]
                            order_vals = {
                                'lightspeed_id': order.get('saleID'),
                                'shop_id': self.id,
                                'lightspeed_state': False if order.get('completed') == 'false' else True,
                                "partner_id": partner_id,
                                'date_order': parse(order.get('createTime')).astimezone(pytz.utc).replace(tzinfo=None),
                                # 'warehouse_id': self.warehouse_id.id
                            }
                            order_exist = self.env['sale.order'].sudo().search([
                                ('lightspeed_id', '=', str(order.get('saleID'))),
                                ('shop_id', '=', self.id),
                            ])
                            if order_exist:
                                continue
                            try:
                                if order_vals['partner_id']:
                                    sale_order_id = sale_order_obj.create(order_vals)

                            except Exception as e:
                                vals = {
                                    'record_name': order.get('customer'),
                                    'import_obj': 'Order Create',
                                    'failure_msg': str(e),
                                    'response_json': order,
                                    'lightspeed_id': self.id,
                                }
                                self.env['lightspeed.failure.log'].sudo().create(vals)
                            self._cr.commit()
                            sale_order_ids |= sale_order_id
                    except Exception as e:
                        vals = {
                            'record_name': order.get('customer'),
                            'import_obj': 'Order',
                            'failure_msg': str(e),
                            'response_json': order,
                            'lightspeed_id': self.id,
                        }
                        self.env['lightspeed.failure.log'].sudo().create(vals)

        # Order Lines import
        orderline_result = self.lightspeed_get_response_by_type('SaleLine', 'orderline', lightspeed_id,
                                                                params={}) if lightspeed_id else self.lightspeed_get_response_by_type(
            'SaleLine', 'orderline', params={
            })
        if orderline_result:
            for orderline in orderline_result:
                sol_id = sol_obj
                try:
                    if orderline.get('saleLineID') and orderline.get('saleID'):
                        product_id = self.env['product.product'].search(
                            [('lightspeed_id', '=', orderline.get('itemID'))], limit=1)
                        if not product_id:
                            product_list = self.import_products(orderline.get('itemID')).get('domain')[0][2]
                            if product_list:
                                product_id = product_list[0]
                        tax_id = self.env['account.tax'].search(
                            [('lightspeed_id', '=', orderline.get('taxCategoryID'))],
                            limit=1).id
                        if not tax_id:
                            tax_id = self.import_taxes(orderline.get('taxCategoryID'))
                        if orderline.get('saleID'):
                            so_id = self.env['sale.order'].search([('lightspeed_id', '=', orderline.get('saleID')),
                                                                   ('shop_id', '=', self.id)])
                            if so_id and so_id.order_line:
                                orderline_exist = self.env['sale.order.line'].sudo().search([
                                    ('lightspeed_id', '=', str(orderline.get('saleLineID'))),
                                    ('shop_id', '=', int(orderline.get('shopID'))),
                                ])
                                if orderline_exist:
                                    continue
                            print("so_id======================", so_id)
                            so_id = so_id.id
                        orderline_vals = {
                            'lightspeed_id': orderline.get('saleLineID'),
                            'shop_id': orderline.get('shopID'),
                            "product_id": product_id.id,
                            'product_uom_qty': orderline.get('unitQuantity'),
                            'price_unit': orderline.get('unitPrice'),
                            'discount': orderline.get('discountAmount'),
                            'tax_id': [(6, 0, [tax_id])],
                            'order_id': so_id,
                        }

                        try:
                            if orderline_vals['product_id'] and orderline_vals['order_id']:
                                sol_id = sol_obj.create(orderline_vals)
                        except Exception as e:
                            vals = {
                                'record_name': orderline.get('product_id'),
                                'import_obj': 'OrderLine Create',
                                'failure_msg': str(e),
                                'response_json': orderline_result,
                                'lightspeed_id': self.id,
                            }
                            self.env['lightspeed.failure.log'].sudo().create(vals)
                        self._cr.commit()
                        sol_ids |= sol_id
                except Exception as e:
                    vals = {
                        'record_name': orderline.get('saleLineID'),
                        'import_obj': 'Order',
                        'failure_msg': str(e),
                        'response_json': order,
                        'lightspeed_id': self.id,
                    }
                    self.env['lightspeed.failure.log'].sudo().create(vals)
        for sale_id in sale_order_ids:
            print("sale_id.lightspeed_state===============", sale_id.lightspeed_state)
            if self.do_complete and sale_id.lightspeed_state:
                sale_id.action_confirm()
            if self.invoice_complete and sale_id.lightspeed_state:
                if not sale_id.invoice_ids:
                    sale_id._create_invoices()
                if sale_id.invoice_ids:
                    for invoice in sale_id.invoice_ids:
                        invoice.action_post()
            if self.payment_complete and sale_id.lightspeed_state:
                self.env['account.payment.register'].with_context(active_model='account.move',
                                                                  active_ids=sale_id.invoice_ids.ids).create({
                    'group_payment': True,
                })._create_payments()
        self.write({'order_fetch_from': fields.Datetime.now()})
        return self.action_view_results(['Orders', 'sale.order'], sale_order_ids.ids)

    def _send_auto_email(self):
        self.ensure_one()
        failure_jobs = self.env['lightspeed.failure.log'].search([
            ('is_send', '=', False),
            ('lightspeed_id', '=', self.id),
        ])

        failure_jobs and self.env.ref('lightspeed_connector_cr.mail_failure_jobs_notification').with_context(
            failure_jobs=failure_jobs, email_to=self.email_to, email_from=self.env.user.email,
        ).send_mail(self.id)

    def _import_orders_cron(self):
        shop_ids = self.search([])
        for shop in shop_ids:
            shop.import_orders()
