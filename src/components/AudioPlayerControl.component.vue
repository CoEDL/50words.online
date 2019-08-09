<template>
    <audio ref="audioElement">
        <source v-for="(file, idx) of audioFiles" :src="file" :key="idx" />Your browser does not support the
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
        },
        store: Object | undefined
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
        this.watchers.files = this.$watch("files", this.load);
        this.load();

        this.$refs.audioElement.addEventListener("ended", this.endedHandler);
        this.$refs.audioElement.addEventListener("error", this.endedHandler);
    },
    beforeDestroy() {
        if (this.watchers.files) this.watchers.files();
        this.watchers.play();

        this.$refs.audioElement.removeEventListener("ended", this.endedHandler);
        this.$refs.audioElement.removeEventListener("error", this.endedHandler);
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
        },
        endedHandler() {
            if (!this.store) return;
            const playAll = this.store.state.playAll;
            if (["stopped", "paused"].includes(playAll.state)) return;
            this.store.commit("setPlayAll", {
                play: true,
                word: undefined,
                state: "next"
            });
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
