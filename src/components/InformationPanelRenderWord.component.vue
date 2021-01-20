<template>
    <div class="flex flex-col pr-2">
        <div class="flex flex-row">
            <div
                class="flex flex-row flex-grow cursor-pointer group hover:text-white hover:bg-highlight-dark p-2 rounded-lg"
                @click="playWord"
            >
                <render-word-component :word="word" :display="display" />
                <div class="flex-grow"></div>

                <div @click="playWord">
                    <div class="text-2xl">
                        <span v-show="word.audio">
                            <i class="fas fa-volume-up"></i>
                        </span>
                        <span v-show="word.video">
                            <i class="fas fa-video"></i>
                        </span>
                    </div>
                </div>

                <audio-player-control
                    :files="word.audio"
                    :play="state"
                    v-if="word.audio"
                    @loaded="loading = false"
                />
            </div>
            <language-information-component
                class="p-2 hidden md:block"
                :code="word.language.code"
                :offset="[0, 10]"
                v-if="display === 'languageName'"
            />
        </div>
        <div v-if="word.video">
            <video-player-control
                :class="{
                    'w-full h-auto': ready,
                    'h-0 w-0': !ready,
                }"
                :files="word.video"
                :play="state"
                @loaded="videoReady"
                @finished-playing="ready = false"
            />
        </div>
    </div>
</template>

<script>
import RenderWordComponent from "./RenderWord.component.vue";
import AudioPlayerControl from "./AudioPlayerControl.component.vue";
import VideoPlayerControl from "./VideoPlayerControl.component.vue";
import LanguageInformationComponent from "./LanguageInformation.component.vue";

export default {
    components: {
        RenderWordComponent,
        AudioPlayerControl,
        VideoPlayerControl,
        LanguageInformationComponent,
    },
    props: {
        data: {
            type: Object,
            required: true,
        },
        display: {
            type: String,
            required: true,
            default: "translation",
            validator: function(value) {
                // The value must match one of these strings
                return ["translation", "languageName"].includes(value) !== -1;
            },
        },
    },
    data() {
        return {
            state: { play: false },
            loading: false,
            ready: false,
            word: this.data.properties ? this.data.properties : this.data,
        };
    },
    computed: {
        smallDevice: function() {
            return window.innerWidth < 768 ? true : false;
        },
        flyTo: function() {
            return this.$store.state.flyTo;
        },
    },
    watch: {
        flyTo: function() {
            const flyTo = this.$store.state.flyTo;
            if (flyTo.handler !== "informationPanelRenderWord") return;
            if (this.word.language.code === flyTo?.word?.properties?.language.code) {
                if (!this.$store.state.iOS && flyTo.state.play) {
                    this.state = { play: true };
                }
            }
        },
    },
    beforeMount() {
        if (this.data.properties) {
            // this is a word -> language mapping
            this.word = this.data.properties;
        } else {
            // this is a language -> word mapping
            this.word = this.data;
        }
    },
    methods: {
        playWord() {
            this.loading = true;
            if (this.$store.state.layer === "languages") {
                this.state = { play: true };
            } else {
                const code = this.word.language.code;
                const word = this.$store.getters
                    .getSelectionData()
                    .words.filter((word) => word.properties.language.code === code)[0];

                this.$store.commit("flyTo", {
                    word,
                    state: { play: false },
                    handler: "informationPanelRenderWord",
                });
                if (this.$store.state.iOS) {
                    setTimeout(() => {
                        this.state = { play: true };
                    }, 200);
                }
            }
        },
        videoReady() {
            this.loading = false;
            this.ready = true;
        },
    },
};
</script>

<style lang="scss" scoped>
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

.blinking {
    animation: blinkingBackground 0.8s infinite;
}
@keyframes blinkingBackground {
    0% {
        @apply text-yellow-500;
    }
}
</style>
