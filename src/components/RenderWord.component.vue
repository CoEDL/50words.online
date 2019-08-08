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
                        >
                            <i class="fas fa-volume-up fa-2x"></i>
                        </el-button>
                        <span v-if="word.properties.audio">
                            <audio-player-control
                                :files="word.properties.audio"
                                :play="play"
                                :store="store"
                                v-on:ready="ready"
                                v-on:finished-playing="stopPlaying"
                            />
                        </span>
                        <span class="style-english">{{word.properties.language.name}}</span>
                        <div v-if="word.properties.video">
                            <video-player-control
                                class="style-video-popup"
                                :files="word.properties.video"
                                :play="play"
                                :store="store"
                                v-on:ready="ready"
                                v-on:finished-playing="stopPlaying"
                            />
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <span class="style-indigenous">{{word.properties.indigenous}}</span>
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
                            >
                                <i class="fas fa-volume-up fa-2x"></i>
                            </el-button>
                            <span v-if="word.audio">
                                <audio-player-control
                                    :files="word.audio"
                                    :play="play"
                                    v-on:ready="ready"
                                    v-on:finished-playing="stopPlaying"
                                />
                            </span>
                        </div>
                        <div class="col-10">
                            <div class="row" :class="{ 'style-row': word.audio }">
                                <div
                                    class="col-12 style-english"
                                    v-if="word.english_alternate"
                                >{{ word.english_alternate }}</div>
                                <div class="col-12 style-english" v-else>{{ word.english}}</div>
                                <div
                                    class="col-12 style-indigenous text-lowercase"
                                >{{ word.indigenous }}</div>
                            </div>
                            <div class="row" :class="{ 'style-row': word.video }" v-if="word.video">
                                <video-player-control
                                    class="style-video"
                                    :files="word.video"
                                    :play="play"
                                    v-on:ready="ready"
                                    v-on:finished-playing="stopPlaying"
                                />
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
import VideoPlayerControl from "./VideoPlayerControl.component.vue";

export default {
    components: {
        AudioPlayerControl,
        VideoPlayerControl
    },
    props: {
        layout: String,
        word: Object,
        store: Object | undefined
    },
    data() {
        return {
            playDisabled: true,
            play: [false]
        };
    },
    mounted() {
        // console.log(JSON.stringify(this.word, null, 2));
        setTimeout(() => {
            if (!this.word.properties.audio && !this.word.properties.video) {
                this.store.commit("setPlayAll", {
                    play: true,
                    word: undefined,
                    state: "next"
                });
            }
        }, 2000);
    },
    methods: {
        ready() {
            this.playDisabled = false;
            if (this.layout === "popup") setTimeout(this.playWord, 500);
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

.style-video-popup {
    width: 150px;
    max-width: 150px;
}
@media (min-width: 768px) {
    .style-video-popup {
        width: 300px;
        max-width: 300px;
    }
}

.style-video {
    width: 100%;
}
</style>
