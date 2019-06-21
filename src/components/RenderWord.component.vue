<template>
    <div>
        <div class="style-word-row">
            <span v-if="layout === 'popup'">
                <div class="row">
                    <div class="col-12">
                        <el-button
                            type="text"
                            class="style-button px-3 style-audio-control"
                            @click="playWord"
                            v-if="word.audio_file.length"
                        >
                            <i class="fas fa-volume-up fa-2x"></i>
                        </el-button>
                        <audio-player-control
                            :files="word.audio_file"
                            :play="play"
                            v-on:ready="ready"
                            v-on:finished-playing="stopPlaying"
                        />
                        <span class="style-english">{{word.language}}</span>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <span class="style-indigenous">{{word.indigenous}}</span>
                    </div>
                </div>
            </span>
            <span v-if="layout !== 'popup'">
                <div class="my-4">
                    <div class="row">
                        <div class="col-2">
                            <el-button
                                type="text"
                                class="style-button px-3 style-audio-control"
                                @click="playWord"
                                :disabled="playDisabled"
                                v-if="word.audio_file.length"
                            >
                                <i class="fas fa-volume-up fa-2x"></i>
                            </el-button>
                            <audio-player-control
                                :files="word.audio_file"
                                :play="play"
                                v-on:ready="ready"
                                v-on:finished-playing="stopPlaying"
                            />
                        </div>
                        <div class="col-10">
                            <div class="row style-row">
                                <div
                                    class="col-12 style-english"
                                    v-if="word.english_alternate"
                                >{{ word.english_alternate }}</div>
                                <div class="col-12 style-english" v-else>{{ word.english}}</div>
                                <div
                                    class="col-12 style-indigenous text-lowercase"
                                >{{ word.indigenous }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </span>
        </div>
    </div>
</template>

<script>
import AudioPlayerControl from "./AudioPlayerControl.component.vue";

export default {
    components: {
        AudioPlayerControl
    },
    props: {
        layout: String,
        word: Object
    },
    data() {
        return {
            playDisabled: true,
            play: [false]
        };
    },

    methods: {
        ready() {
            this.playDisabled = false;
        },
        playWord() {
            this.play = [true];
        },
        stopPlaying() {
            this.play = [false];
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-word-row {
    line-height: 40px;
}

.style-english {
    opacity: 0.8;
    font-size: 1.3em;
}

.style-indigenous {
    // border-bottom: 1px solid #000;
    font-size: 2em;
}

.style-row {
    border-bottom: 1px solid #000;
}
</style>
