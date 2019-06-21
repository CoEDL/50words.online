<template>
    <audio ref="audioElement">
        <source v-for="(file, idx) of audioFiles" :src="file" :key="idx">Your browser does not support the
        <code>audio</code> element.
    </audio>
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
            audioFiles: []
        };
    },
    mounted() {
        this.$refs.audioElement.addEventListener("canplay", () => {
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
                this.audioFiles = [...this.files];
            }
            this.$refs.audioElement.load();
        },
        playWord() {
            if (this.play[0]) this.$refs.audioElement.play();
            this.$emit("finished playing");
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
