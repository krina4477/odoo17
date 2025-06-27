/** @odoo-module **/

import { useState, Component, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useComponent } from "@odoo/owl";
import { onWillStart } from "@odoo/owl";

class RecorderButton extends Component {
    static template = "screen_recorder_cr.ScreenRecorder";

    async setup() {
        super.setup();
        this.user = useService("user");
        onWillStart(async () => {
            this.canRecord = await this.user.hasGroup("screen_recorder_cr.group_screen_record");
        });
        this.icon = useRef('record');
        this.action = useService("action");
        const component = useComponent();
    }

    async _onClickStop(){
        $('.start_record').removeClass('d-none')
        $('.stop_record').addClass('d-none')

        // Stop the media recorder
        if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
            this.mediaRecorder.stop();
        }

        // Stop all tracks in the combined stream
        if (this.combinedStream) {
            this.combinedStream.getTracks().forEach(track => track.stop());
        }
    }

    async _onClickRecord() {
        var icon = this.icon;
        var action = this.action;
        $('.stop_record').removeClass('d-none')
        $('.start_record').addClass('d-none')
        try {
            // Capture screen video
            let screenStream = await navigator.mediaDevices.getDisplayMedia({
                video: true,
                preferCurrentTab: true,
                displaySurface: {
                    "surface": "window",
                    "stopSharingButton": false
                }
            });

            // Listen for when the user stops sharing the screen
            screenStream.getVideoTracks()[0].addEventListener('ended', () => {
                this._onClickStop();
            });
            // Capture user audio
            let audioStream = await navigator.mediaDevices.getUserMedia({
                audio: true,
                video: false  // Important: set this to false since we only need audio here
            });
            // Merge screen video and user audio into one stream
            this.combinedStream = new MediaStream([
                ...screenStream.getVideoTracks(),
                ...audioStream.getAudioTracks()
            ]);

            icon.el.style.color = "#28a745";
            const videoMime = MediaRecorder.isTypeSupported("video/webm; codecs=vp9")
                ? "video/webm; codecs=vp9"
                : "video/webm";

            this.mediaRecorder = new MediaRecorder(this.combinedStream, {
                mimeType: videoMime,
            });

            let record = [];
            this.mediaRecorder.addEventListener("dataavailable", function (e) {
                record.push(e.data);
            });

            this.mediaRecorder.addEventListener("stop", async function () {
                let screenRecord = new Blob(record, {
                    type: record[0].type,
                });

                const recordToBase64 = (screenRecord) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(screenRecord);
                    return new Promise((resolve) => {
                        reader.onloadend = () => {
                            resolve(reader.result);
                        };
                    });
                };

                var url = await recordToBase64(screenRecord);
                action.doAction("screen_recorder_cr.wizard_task_name_action_view", {
                    additionalContext: {
                        url: url,
                    },
                });
            });

            this.mediaRecorder.start();
        } catch (e) {
            console.error("Error:", e);
        }
    }
}

RecorderButton.props = {};
export const recorderItem = {
    Component: RecorderButton,
};
registry.category("systray").add("screen_recorder_cr.video_widget", recorderItem);