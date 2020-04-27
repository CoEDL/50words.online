<template>
    <div class="w-full md:w-auto">
        <div class="flex flex-row">
            <div class="mr-2">
                <el-button
                    circle
                    @click="play"
                    class="style-button"
                    v-if="!isPlaying"
                    :key="'play'"
                >
                    <i class="fas fa-play fa-fw"></i>
                </el-button>
            </div>
            <div class="mr-2">
                <el-button
                    circle
                    @click="stop"
                    class="style-button"
                    v-if="isPlaying"
                    :key="'stop'"
                >
                    <i class="fas fa-stop fa-fw"></i>
                </el-button>
            </div>
            <div class="mr-2">
                <el-button
                    circle
                    @click="pause"
                    class="style-button"
                    :class="{ 'style-button-deselected': isPaused }"
                    v-if="isPlaying"
                    :key="'pause'"
                >
                    <i class="fas fa-pause fa-fw"></i>
                </el-button>
            </div>
            <div>
                <el-button
                    circle
                    @click="setLoopState"
                    class="style-button"
                    :class="{
                        'style-button': loop,
                        'style-button-deselected': !loop,
                    }"
                >
                    <i class="fas fa-repeat fa-fw"></i>
                </el-button>
            </div>
            <div class="flex-grow"></div>
            <div @click="displayLanguages" class="style-word md:hidden">
                <i class="fas fa-times fa-2x"></i>
            </div>
        </div>
        <span v-if="playAll.selectedWord">
            <audio-player-control
                v-if="playAll.selectedWord.audio"
                :files="playAll.selectedWord.audio"
                :play="playAll.play"
                @loaded="loading = false"
                @finishedPlaying="flyToWord"
            />
            <video-player-control
                v-if="playAll.selectedWord.video"
                class="w-64"
                :files="playAll.selectedWord.video"
                :play="playAll.play"
                @loaded="loading = false"
                @finishedPlaying="flyToWord"
            />
        </span>
    </div>
</template>

<script>
import { orderBy, shuffle, uniq } from "lodash";
import { randomBytes } from "crypto";
import { stringify } from "querystring";
import AudioPlayerControl from "./AudioPlayerControl.component.vue";
import VideoPlayerControl from "./VideoPlayerControl.component.vue";
import Vue from "vue";
import RenderWordComponent from "./RenderWord.component.vue";
import mapboxgl from "mapbox-gl";

export default {
    props: {
        map: {
            type: Object,
            required: true,
        },
    },
    components: {
        AudioPlayerControl,
        VideoPlayerControl,
    },
    data() {
        return {
            watchers: [],
            isPlaying: false,
            isPaused: false,
            loop: false,
            playAll: {
                words: [],
                selectedWord: undefined,
                play: [false],
                playedWords: [],
            },
        };
    },
    methods: {
        pause() {},
        setLoopState() {
            this.loop = !this.loop;
            this.$store.commit("setPlayState", {
                loop: this.loop,
            });
        },
        async play() {
            this.isPlaying = true;
            this.playAll.words = this.$store.getters.getSelectedWord();
            this.flyToWord();
        },

        async flyToWord() {
            var self = this;

            await this.loadNextWord();
            if (!this.isPlaying || this.isPaused) return;
            this.playAll.play = [false];

            if (this.popup) this.popup.remove();

            var word = this.playAll.words.shift();
            if (!word) {
                // no word; not looping - done
                this.isPlaying = false;
                this.$emit("center-map");
                return;
            }
            if (word.properties.video) {
                setTimeout(this.flyToWord, 3000);
            }

            this.playAll.playedWords.push(word.properties.english);
            this.playAll.playedWords = uniq(this.playAll.playedWords);
            self.playAll.selectedWord = word;
            console.log(`Flying to: ${word.properties.indigenous}`);
            this.map.flyTo({
                center: word.geometry.coordinates,
                zoom: window.innerwidth < 768 ? 8 : 6,
                bearing: 0,
            });

            this.map.once("moveend", renderPopup);

            async function renderPopup() {
                const word = self.playAll.selectedWord;

                const RenderWordClass = Vue.extend(RenderWordComponent);
                self.popup = new mapboxgl.Popup({ maxWidth: "none" })
                    .setLngLat(word.geometry.coordinates)
                    .setHTML('<div id="vue-popup-content"></div>')
                    .addTo(self.map);
                const popupInstance = new RenderWordClass({
                    propsData: {
                        layout: "popup",
                        word,
                        playOnMount: false,
                    },
                });
                popupInstance.$mount("#vue-popup-content");
                self.popup._update();
                await new Promise((resolve) => setTimeout(resolve, 500));
                self.playAll.play = [true];
            }
        },

        async stop() {
            this.playAll = {
                words: [],
                selectedWord: undefined,
                play: [false],
                playedWords: [],
            };
            this.isPlaying = false;
            await new Promise((resolve) => setTimeout(resolve, 1000));
            if (this.popup) this.popup.remove();
            this.$emit("center-map");
        },

        pause() {
            this.isPaused = !this.isPaused;
            if (!this.isPaused) this.flyToWord();
        },

        setLoopState() {
            this.loop = !this.loop;
        },

        async loadNextWord() {
            if (this.loop && this.playAll.words.length === 0) {
                const words = this.$store.getters.getWordList();
                for (let word of words) {
                    if (!this.playAll.playedWords.includes(word.name)) {
                        this.$store.dispatch("loadWord", { word: word.name });
                        await new Promise((resolve) =>
                            setTimeout(resolve, 1500)
                        );
                        this.playAll.words = this.$store.getters.getSelectedWord();

                        break;
                    }
                }
            }
        },

        displayLanguages() {
            this.stop();
            setTimeout(() => {
                this.$store.commit("unsetSelectedWord");
            }, 1200);
        },
    },
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-button {
    border-color: black;
    background-color: black;
    color: $text-color;
}

.style-button-deselected {
    color: $primary-color;
}

.style-word {
    color: $text-color;
}
@media (min-width: 1024px) {
    .style-selected-word {
        font-size: 1.5em;
        color: $text-color;
        padding-top: 10px;
    }
}
</style>
