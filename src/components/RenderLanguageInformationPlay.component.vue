<template>
    <div @click="load" class="flex flex-row cursor-pointer">
        <audio ref="audioElement" v-if="audioFiles.length">
            <source :src="file" v-for="(file, idx) of audioFiles" :key="idx" />
            Your browser does not support the
            <code>audio</code> element.
        </audio>

        <div
            class="mr-2 style-audio-control hover:text-orange-200"
            :class="{
                'transition duration-500 ease-in-out blinking ': loading,
            }"
        >
            <i class="fas fa-volume-up fa-2x"></i>
        </div>
        <div class="text-lg md:text-2xl md:-mt-1">
            {{ data.name }}
        </div>
    </div>
</template>

<script>
export default {
    props: {
        data: {
            type: Object,
        },
    },
    data() {
        return {
            loading: false,
            audioFiles: [],
        };
    },
    computed: {},
    mounted() {},
    methods: {
        load() {
            this.loading = true;
            this.audioFiles = [...this.data.audio];
            setTimeout(() => {
                this.$refs.audioElement.addEventListener(
                    "canplaythrough",
                    () => {
                        if (this.loading) this.play();
                    }
                );
                this.$refs.audioElement.load();
            }, 200);
        },
        play() {
            this.loading = false;
            this.$refs.audioElement.play();
        },
    },
};
</script>

<style lang="scss" scoped>
.blinking {
    animation: blinkingBackground 0.8s infinite;
}
@keyframes blinkingBackground {
    0% {
        @apply text-orange-400;
    }
}
</style>
