<template>
    <div class="flex flex-col">
        <div class="text-lg md:text-xl mb-2">
            {{ word.indigenous }}
        </div>
        <div class="text-lg md:text-xl mb-4" v-if="word.english_alternate">
            {{ word.english_alternate }}
        </div>
        <div class="text-lg md:text-xl mb-4" v-else>
            {{ word.english }}
        </div>
        <div class="text-gray-600 group-hover:text-white text-sm md:text-base">
            <div>
                {{ word.language.name }}
            </div>
        </div>
        <audio-player-control
            v-if="word.audio && word.audio.length"
            :files="word.audio"
            :state="state"
            @loaded="loading = false"
            @finished-playing="$emit('done')"
        />
        <video-player-control
            v-if="word.video && word.video.length"
            :files="word.video"
            :state="state"
            @finished-playing="$emit('done')"
        />
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
        word: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            timeout: undefined,
            state: { play: false },
        };
    },
    mounted() {
        this.playWord();
        this.timeout = setTimeout(() => {
            this.$emit("done");
        }, 10000);
    },
    beforeDestroy() {
        clearTimeout(this.timeout);
    },
    methods: {
        playWord() {
            setTimeout(() => {
                this.state = { play: true };
            }, 400);
        },
    },
};
</script>
