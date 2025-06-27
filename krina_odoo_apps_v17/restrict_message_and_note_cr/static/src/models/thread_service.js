/** @odoo-module **/

// Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
// See LICENSE file for full copyright and licensing details.

import { _t } from "@web/core/l10n/translation";
import { ThreadService } from "@mail/core/common/thread_service";
import { patch } from "@web/core/utils/patch";

patch(ThreadService.prototype,{
    setup(){
        super.setup();
    },
    async getMessagePostParams({
        attachments,
        body,
        cannedResponseIds,
        isNote,
        mentionedChannels,
        mentionedPartners,
        thread,
    }) {

        const subtype = isNote ? "mail.mt_note" : "mail.mt_comment";
        const validMentions = this.store.user
            ? this.messageService.getMentionsFromText(body, {
                  mentionedChannels,
                  mentionedPartners,
              })
            : undefined;
        const partner_ids = validMentions?.partners.map((partner) => partner.id);
        let recipientEmails = [];
        if (!isNote) {
            const recipientIds = thread.suggestedRecipients
                .filter((recipient) => recipient.persona && recipient.checked)
                .map((recipient) => recipient.persona.id);
            recipientEmails = thread.suggestedRecipients
                .filter((recipient) => recipient.checked && !recipient.persona)
                .map((recipient) => recipient.email);
            partner_ids?.push(...recipientIds);
        }
        return {
            context: {
                mail_post_autofollow: !isNote && thread.hasWriteAccess,
            },
            post_data: {
                body: await prettifyMessageContent(body, validMentions),
                attachment_ids: attachments.map(({ id }) => id),
                attachment_tokens: attachments.map((attachment) => attachment.accessToken),
                canned_response_ids: cannedResponseIds,
                message_type: "comment",
                partner_ids,
                subtype_xmlid: subtype,
                partner_emails: recipientEmails,
            },
            thread_id: thread.id,
            thread_model: thread.model,
        };
    },
});
