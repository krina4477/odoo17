# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

import logging
import requests
from datetime import timedelta

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.addons.google_account.models.google_service import GOOGLE_TOKEN_ENDPOINT

_logger = logging.getLogger(__name__)

class GoogleCredentials(models.Model):
    """"Google Account of res_users"""

    _inherit = 'google.calendar.credentials'


    def _refresh_google_calendar_token(self):
        # LUL TODO similar code exists in google_drive. Should be factorized in google_account
        self.ensure_one()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        client_id = self.env.user.cal_client_id
        client_secret = self.env.user.cal_client_secret

        if not client_id or not client_secret:
            raise UserError(_("The account for the Google Calendar service is not configured."))

        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            'refresh_token': self.calendar_rtoken,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
        }

        try:
            _dummy, response, _dummy = self.env['google.service']._do_request(GOOGLE_TOKEN_ENDPOINT, params=data, headers=headers, method='POST', preuri='')
            ttl = response.get('expires_in')
            self.write({
                'calendar_token': response.get('access_token'),
                'calendar_token_validity': fields.Datetime.now() + timedelta(seconds=ttl),
            })
        except requests.HTTPError as error:
            if error.response.status_code in (400, 401):  # invalid grant or invalid client
                # Delete refresh token and make sure it's commited
                self.env.cr.rollback()
                self._set_auth_tokens(False, False, 0)
                self.env.cr.commit()
            error_key = error.response.json().get("error", "nc")
            error_msg = _("An error occurred while generating the token. Your authorization code may be invalid or has already expired [%s]. "
                          "You should check your Client ID and secret on the Google APIs plateform or try to stop and restart your calendar synchronisation.",
                          error_key)
            raise UserError(error_msg)
