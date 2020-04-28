<template>
    <div>
        <div v-if="layout === 'popup'">
            <div class="flex flex-col">
                <div class="flex flex-row cursor-pointer" @click="playWord">
                    <div class="mr-2 pt-4 style-audio-control ">
                        <i class="fas fa-volume-up fa-2x"></i>
                    </div>
                    <div class="flex flex-col">
                        <div class="text-lg opacity-75">
                            {{ word.properties.language.name }}
                        </div>

                        <div class="text-3xl my-2 hover:text-orange-200">
                            {{ word.properties.indigenous }}
                        </div>
                    </div>
                </div>
                <audio-player-control
                    :files="word.properties.audio"
                    :play="play"
                    :store="store"
                    v-if="word.properties.audio"
                />
                <video-player-control
                    class="style-video-popup py-2"
                    :files="word.properties.video"
                    :play="play"
                    :store="store"
                    v-if="word.properties.video"
                />
            </div>
        </div>
        <div v-if="layout !== 'popup'">
            <div
                class="flex flex-row border-b border-gray-600 md:py-2 cursor-pointer hover:text-orange-200"
                @click="playWord"
            >
                <div
                    class="mr-2 pt-4 md:pt-6 style-audio-control"
                    :class="{
                        'transition duration-500 ease-in-out blinking ': loading,
                    }"
                >
                    <i class="fas fa-volume-up fa-2x"></i>
                </div>
                <div class="flex flex-col py-2">
                    <div
                        class="text-xs md:text-base text-gray-700"
                        v-if="word.english_alternate"
                    >
                        {{ word.english_alternate }}
                    </div>
                    <div class="text-xs  md:text-base text-gray-700" v-else>
                        {{ word.english }}
                    </div>
                    <div class="text-lg md:text-2xl text-lowercase">
                        {{ word.indigenous }}
                    </div>
                    <audio-player-control
                        :files="word.audio"
                        :play="play"
                        v-if="word.audio"
                        @loaded="loading = false"
                    />
                    <div :class="{ 'style-row': word.video }" v-if="word.video">
                        <video-player-control
                            class="style-video"
                            :files="word.video"
                            :play="play"
                            @loaded="loading = false"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AudioPlayerControl from "./AudioPlayerControl.component.vue";
import VideoPlayerControl from "./VideoPlayerControl.component.vue";

export default {
    components: {
        AudioPlayerControl,
        VideoPlayerControl,
    },
    props: {
        layout: {
            type: String,
        },
        word: {
            type: Object,
        },
        store: {
            type: Object | undefined,
        },
        playOnMount: { type: Boolean, default: true },
    },
    data() {
        return {
            play: [false],
            loading: false,
        };
    },
    mounted() {
        if (this.layout === "popup" && this.playOnMount) {
            this.playWord();
        }
    },
    methods: {
        playWord() {
            this.loading = true;
            this.play = [true];
        },
    },
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";
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

.blinking {
    animation: blinkingBackground 0.8s infinite;
}
@keyframes blinkingBackground {
    0% {
        @apply text-orange-400;
    }
}
</style>
