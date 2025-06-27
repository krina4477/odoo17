# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
import base64
import io
import os
import mimetypes
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request


class DownloadAttachment(http.Controller):

    @http.route(['/attachment/download'], type='http', auth='public')
    def download_attachment(self, attachment_id):
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "mimetype", "res_model", "res_id", "type", "url"]
        )
        if attachment:
            attachment = attachment[0]
        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            extension = os.path.splitext('')[1]
            extension = extension if extension else mimetypes.guess_extension(attachment["mimetype"] or '')
            filename = attachment['name']
            filename = filename if os.path.splitext(filename)[1] else filename + extension
            return http.send_file(data, filename=filename, as_attachment=True)
        else:
            return request.not_found()