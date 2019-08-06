<template>
    <video ref="videoElement" controls>
        <source v-for="(file, idx) of videoFiles" :src="file" :key="idx" />Your browser does not support the
        <code>video</code> element.
    </video>
</template>

<script>
export default {
    props: {
        files: {
            type: Array | String,
            required: true
        },
        play: {
            type: Boolean | undefined,
            required: true
        }
    },
    data() {
        return {
            watchers: {},
            videoFiles: []
        };
    },
    mounted() {
        this.$refs.videoElement.addEventListener("canplay", () => {
            this.$emit("ready");
        });
        this.watchers.play = this.$watch("play", (n, o) => {
            this.playWord();
        });
        this.watchers.audio = this.$watch("files", this.load);
        this.load();
    },
    beforeDestroy() {
        if (this.watchers.audio) this.watchers.audio();
        this.watchers.play();
    },
    methods: {
        load() {
            if (typeof this.files === "string" && this.files) {
                this.audioFiles = JSON.parse(this.files);
            } else {
                this.videoFiles = [...this.files];
            }
            this.$refs.videoElement.load();
        },
        playWord() {
            if (this.play[0]) this.$refs.videoElement.play();
            this.$emit("finished playing");
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
