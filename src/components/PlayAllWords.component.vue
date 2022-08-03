<template>
    <div ref="top">
        <div v-if="word" class="flex flex-row justify-center mt-6">
            <div class="flex flex-col">
                <render-word-component :word="word" :display="display" />
                <audio-player-control
                    v-if="word.audio && word.audio.length"
                    :files="word.audio"
                    :state="state"
                    @finished-playing="playWord"
                />
                <video-player-control
                    v-if="word.video && word.video.length"
                    :class="{
                        'w-full h-auto': word.video,
                        'h-0 w-0': !word.video,
                    }"
                    :files="word.video"
                    :state="state"
                    @finished-playing="playWord"
                />
            </div>
        </div>
    </div>
</template>

<script>
import { cloneDeep } from "lodash";
import AudioPlayerControl from "./AudioPlayerControl.component.vue";
import VideoPlayerControl from "./VideoPlayerControl.component.vue";
import RenderWordComponent from "./RenderWord.component.vue";
export default {
    components: {
        RenderWordComponent,
        AudioPlayerControl,
        VideoPlayerControl,
    },
    props: {
        words: {
            type: Array,
            required: true,
        },
        display: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            state: {
                play: false,
            },
            wordList: cloneDeep(this.words),
            word: undefined,
            isPlaying: false,
            map: this.$store.state.map,
        };
    },
    computed: {
        flyTo: function () {
            return this.$store.state.flyTo;
        },
    },
    watch: {
        flyTo: function (n, o) {
            if (this.flyTo.handler !== "playAllWords") return;
            if (this.flyTo?.state?.play) {
                this.state = { play: true };
            }
        },
    },
    mounted() {
        setTimeout(() => {
            this.playWord();
        }, 200);
    },
    methods: {
        async playWord() {
            if (!this.wordList.length) {
                this.$emit("finished-playing");
                return;
            }
            this.word = this.wordList.pop();
            if (this.word?.video?.length && (this.$store.state.iOS || window.innerWidth < 768)) {
                this.playWord();
            }

            this.state = { play: false };

            // tell the map to fly to the word if there are coordinates attached
            if (this.word.geometry && this.word.properties) {
                this.$store.commit("flyTo", {
                    word: this.word,
                    state: { play: false },
                    handler: "playAllWords",
                });
                this.word = this.word.properties;
            } else {
                // play the word
                this.$nextTick(() => {
                    this.state = { play: true };
                });
            }
        },
    },
};
</script>
