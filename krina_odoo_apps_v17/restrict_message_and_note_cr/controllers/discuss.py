# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.mail.controllers.thread import ThreadController
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
import datetime
from werkzeug.exceptions import NotFound
from markupsafe import Markup, escape

class ThreadControllerInherit(ThreadController):


    @http.route("/mail/message/post", methods=["POST"], type="json", auth="public")
    @add_guest_to_context
    def mail_message_post(self, thread_model, thread_id, post_data, context=None):

        guest = request.env["mail.guest"]._get_guest_from_context()
        guest.env["ir.attachment"].browse(post_data.get("attachment_ids", []))._check_attachments_access(
            post_data.get("attachment_tokens")
        )
        if context:
            request.update_context(**context)
        canned_response_ids = tuple(cid for cid in post_data.pop('canned_response_ids', []) if isinstance(cid, int))
        if canned_response_ids:
            # Avoid serialization errors since last used update is not
            # essential and should not block message post.
            request.env.cr.execute("""
                        UPDATE mail_shortcode SET last_used=%(last_used)s
                        WHERE id IN (
                            SELECT id from mail_shortcode WHERE id IN %(ids)s
                            FOR NO KEY UPDATE SKIP LOCKED
                        )
                    """, {
                'last_used': datetime.now(),
                'ids': canned_response_ids,
            })
        thread = request.env[thread_model].with_context(active_test=False).search([("id", "=", thread_id)])
        if not thread:
            raise NotFound()
        if "body" in post_data:
            post_data["body"] = Markup(post_data["body"])  # contains HTML such as @mentions
        new_partners = []
        if "partner_emails" in post_data:
            new_partners = [
                record.id
                for record in request.env["res.partner"]._find_or_create_from_emails(post_data["partner_emails"])
            ]
        post_data["partner_ids"] = list(set((post_data.get("partner_ids", [])) + new_partners))

        allowed_params = self._get_allowed_message_post_params()

        if allowed_params:
            if post_data['follower_ids']:
                tmp_list = post_data['follower_ids']
                post_data['follower_ids'] = []
                for follower in tmp_list:
                    post_data['follower_ids'].append(int(follower))
                allowed_params.update({
                        'follower_ids': post_data['follower_ids']
                    })
            else:
                post_data.pop("follower_ids")


        message_data = thread.message_post(**{key: value for key, value in post_data.items() if key in allowed_params}).message_format()[0]
        if "temporary_id" in request.context:
            message_data["temporary_id"] = request.context["temporary_id"]
        return message_data

    @http.route("/mail/thread/messages", methods=["POST"], type="json", auth="user")
    def mail_thread_messages(self, thread_model, thread_id, search_term=None, before=None, after=None, around=None, limit=30):
        domain = [
            ("res_id", "=", int(thread_id)),
            ("model", "=", thread_model),
            ("message_type", "!=", "user_notification"),'|',
            ('follower_ids.partner_id', '=', request.env.user.partner_id.id), '|',
            ('author_id', '=', request.env.user.partner_id.id),
            ('follower_ids', '=', False)
        ]
        res = request.env["mail.message"]._message_fetch(domain, search_term=search_term, before=before, after=after,
                                                         around=around, limit=limit)
        if not request.env.user._is_public():
            res["messages"].set_message_done()
        return {**res, "messages": res["messages"].message_format()}
