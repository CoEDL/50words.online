<template>
    <div class="flex flex-col">
        <div class="text-lg md:text-xl mb-2">
            {{ word.indigenous }}
        </div>
        <div class="text-lg md:text-xl mb-4">
            {{ word.english }}
        </div>
        <div class="text-gray-600 group-hover:text-white text-sm md:text-base">
            <div>
                {{ word.language.name }}
            </div>
        </div>
        <audio-player-control
            :files="word.audio"
            :play="state"
            v-if="word.audio"
            @loaded="loading = false"
            @finished-playing="$emit('done')"
        />
        <div v-if="word.video">
            <video-player-control
                :files="word.video"
                :play="state"
                @finished-playing="$emit('done')"
            />
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
