<template>
    <video ref="videoElement">
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
        },
        store: Object | undefined
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
        this.watchers.files = this.$watch("files", this.load);
        this.load();

        this.$refs.videoElement.addEventListener("ended", this.endedHandler);
        this.$refs.videoElement.addEventListener("error", this.endedHandler);
    },
    beforeDestroy() {
        if (this.watchers.files) this.watchers.files();
        this.watchers.play();

        this.$refs.videoElement.removeEventListener("ended", this.endedHandler);
        this.$refs.videoElement.removeEventListener("error", this.endedHandler);
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
        },
        endedHandler() {
            if (!this.store) return;
            const playAll = this.store.state.playAll;
            if (!["paused", "stopped"].includes(this.store.state.playAll.state))
                this.store.commit("setPlayAll", {
                    state: "next"
                });
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
