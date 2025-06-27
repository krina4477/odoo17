# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from datetime import datetime
import json
import logging

import requests
from werkzeug import urls

from odoo import api, fields, models, registry, _
from odoo.exceptions import UserError
from odoo.http import request


_logger = logging.getLogger(__name__)

TIMEOUT = 20

GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_API_BASE_URL = 'https://www.googleapis.com'


class GoogleService(models.AbstractModel):
    _inherit = 'google.service'

    def _get_client_id(self, service):
        # client id is not a secret, and can be leaked without risk. e.g. in clear in authorize uri.
        return self.env.user.cal_client_id

    @api.model
    def _get_authorize_uri(self, service, scope, redirect_uri, state=None, approval_prompt=None, access_type=None):
        """ This method return the url needed to allow this instance of Odoo to access to the scope
			of gmail specified as parameters
		"""
        params = {
            'response_type': 'code',
            'client_id': self.env.user.cal_client_id,
            'scope': scope,
            'redirect_uri': redirect_uri,
        }
    
        if state:
            params['state'] = state
    
        if approval_prompt:
            params['approval_prompt'] = approval_prompt
    
        if access_type:
            params['access_type'] = access_type
    
        encoded_params = urls.url_encode(params)
        return "%s?%s" % (GOOGLE_AUTH_ENDPOINT, encoded_params)

    @api.model
    def _get_google_tokens(self, authorize_code, service, redirect_uri):
        """ Call Google API to exchange authorization code against token, with POST request, to
			not be redirected.
		"""
        ICP = self.env['ir.config_parameter'].sudo()
    
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            'code': authorize_code,
            'client_id': self.env.user.cal_client_id,
            'client_secret': self.env.user.cal_client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        try:
            dummy, response, dummy = self._do_request(GOOGLE_TOKEN_ENDPOINT, params=data, headers=headers,
                                                      method='POST', preuri='')
            return response.get('access_token'), response.get('refresh_token'), response.get('expires_in')
        except requests.HTTPError as e:
            _logger.error(e)
            error_msg = _(
                "Something went wrong during your token generation. Maybe your Authorization Code is invalid or already expired")
            raise self.env['res.config.settings'].get_config_warning(error_msg)
