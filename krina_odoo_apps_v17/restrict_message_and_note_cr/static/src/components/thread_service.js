/** @odoo-module **/
//Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
//See LICENSE file for full copyright and licensing details.

import { ThreadService } from "@mail/core/common/thread_service";
import { patch } from "@web/core/utils/patch";
import { prettifyMessageContent } from "@mail/utils/common/format";

patch(ThreadService.prototype,{
    async getMessagePostParams({
        attachments,
        body,
        cannedResponseIds,
        isNote,
        mentionedChannels,
        mentionedPartners,
        thread,
        follower_ids,
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
                follower_ids: follower_ids,
            },
            thread_id: thread.id,
            thread_model: thread.model,
        };
    },

    async post(
        thread,
        body,
        {
            attachments = [],
            isNote = false,
            parentId,
            mentionedChannels = [],
            mentionedPartners = [],
            cannedResponseIds,
            follower_ids,
        } = {}
    ) {
        let tmpMsg;
        const params = await this.getMessagePostParams({
            attachments,
            body,
            cannedResponseIds,
            isNote,
            mentionedChannels,
            mentionedPartners,
            thread,
            follower_ids,
        });
        const tmpId = this.messageService.getNextTemporaryId();
        params.context = { ...this.user.context, ...params.context, temporary_id: tmpId };
        if (parentId) {
            params.post_data.parent_id = parentId;
        }
        if (thread.type === "chatter") {
            params.thread_id = thread.id;
            params.thread_model = thread.model;
        } else {
            const tmpData = {
                id: tmpId,
                attachments: attachments,
                res_id: thread.id,
                model: "discuss.channel",
            };
            tmpData.author = this.store.self;
            if (parentId) {
                tmpData.parentMessage = this.store.Message.get(parentId);
            }
            const prettyContent = await prettifyMessageContent(
                body,
                this.messageService.getMentionsFromText(body, {
                    mentionedChannels,
                    mentionedPartners,
                })
            );
            const { emojis } = await loadEmoji();
            const recentEmojis = JSON.parse(
                browser.localStorage.getItem("web.emoji.frequent") || "{}"
            );
            const emojisInContent =
                prettyContent.match(/\p{Emoji_Presentation}|\p{Emoji}\uFE0F/gu) ?? [];
            for (const codepoints of emojisInContent) {
                if (emojis.some((emoji) => emoji.codepoints === codepoints)) {
                    recentEmojis[codepoints] ??= 0;
                    recentEmojis[codepoints]++;
                }
            }
            browser.localStorage.setItem("web.emoji.frequent", JSON.stringify(recentEmojis));
            tmpMsg = this.store.Message.insert(
                {
                    ...tmpData,
                    body: prettyContent,
                    res_id: thread.id,
                    model: thread.model,
                    temporary_id: tmpId,
                },
                { html: true }
            );
            thread.messages.push(tmpMsg);
            thread.seen_message_id = tmpMsg.id;
        }
        const data = await this.rpc(this.getMessagePostRoute(thread), params);
        tmpMsg?.delete();
        if (!data) {
            return;
        }
        if (data.id in this.store.Message.records) {
            data.temporary_id = null;
        }
        const message = this.store.Message.insert(data, { html: true });
        thread.messages.add(message);
        if (!message.isEmpty && this.store.hasLinkPreviewFeature) {
            this.rpc("/mail/link_preview", { message_id: data.id }, { silent: true });
        }
        return message;
    },
});
