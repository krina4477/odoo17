# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from . import models
from . import controllers
from odoo.addons.payment import  reset_payment_provider

def uninstall_hook(env):
    reset_payment_provider(env, 'cielo')
