# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from imaplib import IMAP4, IMAP4_SSL
from poplib import POP3, POP3_SSL
from odoo.exceptions import UserError
from email.message import EmailMessage
from email import message_from_string, policy
import logging
import poplib
import base64
import email
try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib
_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50
MAIL_TIMEOUT = 60
poplib._MAXLINE = 65536


class IrAttachmentInherit(models.Model):
    _inherit = "ir.attachment"

    directory_id = fields.Many2one('system.directory', string="Directory")
    file_tags = fields.Many2many('file.tags', string="File Tags")


class SystemDirectory(models.Model):
    _name = "system.directory"
    _description = 'System Directory'

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image")
    is_root = fields.Boolean(string="Is Root Directory")
    subject_line = fields.Char(string="Subject Line")
    file_location = fields.Char(
        string="Location", compute="_get_file_location")
    files_count = fields.Integer(string="Files Count", compute="_files_count")
    subdirectories_count = fields.Integer(
        string="Subdirectories Count", compute="_subdirectories_count")
    files = fields.Integer(string="Files", related="files_count")
    subdirectories = fields.Integer(
        string="Subdirectories", related="subdirectories_count")
    parent_directory_id = fields.Many2one(
        'system.directory', string="Parent Directory", required=False)
    directory_tag_ids = fields.Many2many(
        'directory.tags', string="Directory Tags")
    subdirectories_ids = fields.One2many(
        'system.directory', 'parent_directory_id', string="Subdirectories Records")
    file_ids = fields.One2many(
        'ir.attachment', 'directory_id', string="Files Records")

    @api.model
    def create(self, vals):
        res = super(SystemDirectory, self).create(vals)
        exist_directory = res.mapped(
            'parent_directory_id.subdirectories_ids.name')
        if exist_directory and res.name:
            del exist_directory[-1]
            if res.name in exist_directory:
                raise ValidationError(_("Directory name already exists."))
            else:
                return res
        else:
            return res

    @api.onchange('subject_line')
    def _onchange_subject_line(self):
        for rec in self:
            if rec.subject_line:
                subject_line_rec = self.search(
                    [('subject_line', '=', rec.subject_line)])
                if len(subject_line_rec) == 1:
                    raise ValidationError(
                        _("Given Subject Line is already exists."))

    def _get_file_location(self):
        for rec in self:
            if rec.parent_directory_id.is_root == True:
                rec.file_location = "/%s/%s" % (
                    rec.parent_directory_id.name, rec.name)
            elif rec.parent_directory_id.is_root == False:
                if not rec.parent_directory_id:
                    rec.file_location = ''
                val = [rec.name, rec.parent_directory_id.name]
                if rec.parent_directory_id.parent_directory_id.is_root == True:
                    val.append(
                        rec.parent_directory_id.parent_directory_id.name)
                    val.reverse()
                    path = "/"+"/".join(val)
                    rec.file_location = path
                else:
                    if rec.parent_directory_id:
                        if rec.parent_directory_id.file_location:
                            rec.file_location = rec.parent_directory_id.file_location + \
                                "/%s" % (rec.name)
                        else:
                            rec.file_location = "/%s/%s" % (
                                rec.parent_directory_id.name, rec.name)

                    elif rec.is_root == True:
                        rec.file_location = "/%s" % (rec.name)

    @api.depends('file_ids')
    def _files_count(self):
        for rec in self:
            if rec.file_ids:
                rec.files_count = len(rec.file_ids.ids)
            else:
                rec.files_count = 0

    @api.depends('subdirectories_ids')
    def _subdirectories_count(self):
        for rec in self:
            if rec.subdirectories_ids:
                rec.subdirectories_count = len(rec.subdirectories_ids.ids)
            else:
                rec.subdirectories_count = 0

    def action_view_subdirectories(self):
        self.ensure_one()
        kanban_id = self.env.ref(
            'mail_attachments_extractor_cr.system_directory_kanban_view').id
        tree_id = self.env.ref(
            'mail_attachments_extractor_cr.system_directory_tree_view').id
        form_id = self.env.ref(
            'mail_attachments_extractor_cr.system_directory_form_view').id
        subdirectories_rec = self.mapped('subdirectories_ids')
        return {'type': 'ir.actions.act_window',
                'name': _('Subdirectories'),
                'res_model': 'system.directory',
                'view_mode': 'kanban,tree,form',
                'views': [(kanban_id, 'kanban'), (tree_id, 'tree'), (form_id, 'form')],
                'domain': [('id', 'in', subdirectories_rec.ids or [])]
                }

    def action_view_files(self):
        self.ensure_one()
        kanban_id = self.env.ref(
            'mail_attachments_extractor_cr.all_files_kanban_view').id
        tree_id = self.env.ref(
            'mail_attachments_extractor_cr.all_files_tree_view').id
        form_id = self.env.ref(
            'mail_attachments_extractor_cr.all_files_form_view').id
        files_rec = self.mapped('file_ids')
        return {'type': 'ir.actions.act_window',
                'name': _('Files'),
                'res_model': 'ir.attachment',
                'view_mode': 'kanban,tree,form',
                'views': [(kanban_id, 'kanban'), (tree_id, 'tree'), (form_id, 'form')],
                'domain': [('id', 'in', files_rec.ids or [])]
                }


class MailThreadInherit(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_process(self, model, message, custom_values=None, save_original=False, strip_attachments=False,
                        thread_id=None):
        if isinstance(message, xmlrpclib.Binary):
            message = bytes(message.data)
        if isinstance(message, str):
            message = message.encode('utf-8')
        message = email.message_from_bytes(message, policy=email.policy.SMTP)
        msg_dict = self.message_parse(message, save_original=save_original)
        if strip_attachments:
            msg_dict.pop('attachments', None)
        fetch_mail_rec = self.env['fetch.mail.config'].search(
            [('subject_line', '=', msg_dict.get('subject'))])
        if fetch_mail_rec:
            directory_rec = self.env['system.directory'].search(
                [('name', '=', fetch_mail_rec.name)])
            if directory_rec:
                fetch_mail_rec.write({'directory_id': directory_rec.id})
            else:
                directory_rec = self.env['system.directory'].create(
                    {'name': fetch_mail_rec.name})
                fetch_mail_rec.write({'directory_id': directory_rec.id})

            for attachment in msg_dict.get('attachments'):
                cid = False
                if len(attachment) == 2:
                    name, content = attachment
                elif len(attachment) == 3:
                    name, content, info = attachment
                    cid = info and info.get('cid')
                else:
                    continue
                if isinstance(content, str):
                    content = content.encode('utf-8')
                elif content is None:
                    continue
                attachement_values = {
                    'name': name,
                    'datas': base64.b64encode(content),
                    'type': 'binary',
                    'description': name,
                    'res_model': 'fetch.mail.config',
                    'res_id': fetch_mail_rec.id,
                    'directory_id': directory_rec.id,
                }
                attachment_rec = self.env['ir.attachment'].create(
                    attachement_values)
        existing_msg_ids = self.env['mail.message'].search(
            [('message_id', '=', msg_dict['message_id'])], limit=1)
        if existing_msg_ids:
            _logger.info('Ignored mail from %s to %s with Message-Id %s: found duplicated Message-Id during processing',
                         msg_dict.get('email_from'), msg_dict.get('to'), msg_dict.get('message_id'))
            return False
        routes = self.message_route(
            message, msg_dict, model, thread_id, custom_values)
        thread_id = self._message_route_process(message, msg_dict, routes)
        return thread_id


class FetchMailConfig(models.Model):
    _name = "fetch.mail.config"
    _description = 'Fetch Mail Config'

    name = fields.Char(string="Name")
    subject_line = fields.Char(string="Mail Subject Line")
    directory_id = fields.Many2one('system.directory', string="Directory")

    @api.onchange('subject_line', 'name')
    def _onchange_subject_line(self):
        for rec in self:
            subject_line_rec = self.search(
                [('subject_line', '=', rec.subject_line)])
            name_rec = self.search([('name', '=', rec.name)])
            if len(subject_line_rec) == 1:
                raise ValidationError(
                    _("Given Subject Line is already exists."))
            elif len(name_rec) == 1:
                raise ValidationError(_("Given Name is already exists."))


class DirectoryTags(models.Model):
    _name = "directory.tags"
    _description = 'Directory Tags'

    name = fields.Char(string="Name", required=True)


class FileTags(models.Model):
    _name = "file.tags"
    _description = 'File Tags'

    name = fields.Char(string="Name", required=True)
