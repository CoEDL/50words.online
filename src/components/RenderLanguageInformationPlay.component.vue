<template>
    <div class="w-10">
        <audio ref="audioElement" v-if="audioFiles.length">
            <source :src="file" v-for="(file, idx) of audioFiles" :key="idx" />
            Your browser does not support the
            <code>audio</code> element.
        </audio>

        <div @click="load" class="flex flex-row cursor-pointer" v-if="audioFiles.length">
            <div
                class="text-2xl"
                :class="{
                    'transition duration-500 ease-in-out blinking': loading,
                }"
            >
                <i class="fas fa-volume-up"></i>
            </div>
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
        };
    },
    computed: {
        audioFiles: function () {
            return [...this.data.audio];
        },
    },
    methods: {
        load() {
            this.loading = true;
            setTimeout(() => {
                this.$refs.audioElement.addEventListener("canplaythrough", () => {
                    if (this.loading) this.play();
                });
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
        @apply text-highlight-dark;
    }
}
</style>
