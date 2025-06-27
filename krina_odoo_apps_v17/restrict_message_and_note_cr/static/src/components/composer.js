/** @odoo-module **/
// Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
// See LICENSE file for full copyright and licensing details.

import { patch } from "@web/core/utils/patch";
import { Composer } from "@mail/core/common/composer";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { FollowerList } from "@mail/core/web/follower_list";

patch(Composer.prototype, {
    setup(){
        super.setup();
    },
     _onClickCountFollower() {
        var followers = [];
        $("input:checkbox[name=custom_follower]:checked").each(function() {
            followers.push($(this).val());
        });
        $('.buttonFollowersCount').text(followers.length);
     },



});

patch(Composer.prototype, {
    async sendMessage() {
        let follower_list = []
        $("input:checkbox[name=custom_follower]:checked").each(function() {
            follower_list.push($(this).val());
        });

        await this.processMessage(async (value) => {
            const postData = {
                attachments: this.props.composer.attachments,
                isNote: this.props.type === "note",
                mentionedChannels: this.props.composer.mentionedChannels,
                mentionedPartners: this.props.composer.mentionedPartners,
                cannedResponseIds: this.props.composer.cannedResponses.map((c) => c.id),
                parentId: this.props.messageToReplyTo?.message?.id,
                follower_ids: follower_list
            };

            await this._sendMessage(value, postData);
        });
    },
});



patch(Composer,{
     components: {
        ...Composer.components,
         Dropdown,
        FollowerList,
    },
    defaultProps: {
        ...Composer.defaultProps,
        hasFollowers: true,
    },
});