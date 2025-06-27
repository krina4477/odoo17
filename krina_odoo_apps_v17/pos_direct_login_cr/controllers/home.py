# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.web.controllers.home import Home


class HomeInherit(Home):

    @http.route('/web/login', auth="public", sitemap=False)
    def web_login(self,*args, **kw):
        res = super(HomeInherit, self).web_login(*args, **kw)
        Users = request.env['res.users']
        user_rec = Users.sudo().browse(request.uid)
        if user_rec.pos_config_id and user_rec.has_group('base.group_user'):
            session_rec = user_rec.pos_config_id.current_session_id
            session_ids = request.env['pos.session'].sudo().search([
                ('config_id', '=', user_rec.pos_config_id.id)])

            if session_ids.filtered(lambda r: r.state == 'opened'):
                return request.redirect('/pos/ui?config_id=%s#cids=1'%(user_rec.pos_config_id.id))
            if not session_rec and 'login' in kw:
                request.env['pos.session'].sudo().create({
                    'user_id': user_rec.id,
                    'config_id': user_rec.pos_config_id.id
                })
                return request.redirect('/pos/ui?config_id=%s#cids=1'%(user_rec.pos_config_id.id))
        return res