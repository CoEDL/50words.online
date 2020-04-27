<template>
    <video ref="videoElement" v-if="videoFiles.length">
        <source v-for="(file, idx) of videoFiles" :src="file" :key="idx" />
        Your browser does not support the <code>video</code> element.
    </video>
</template>

<script>
export default {
    props: {
        files: {
            type: Array | String,
            required: true,
        },
        play: {
            type: Boolean | undefined,
            required: true,
        },
        store: Object | undefined,
    },
    data() {
        return {
            videoFiles: [],
            loading: false,
        };
    },
    watch: {
        play: function() {
            this.load();
        },
    },
    methods: {
        load() {
            this.loading = true;
            if (typeof this.files === "string" && this.files) {
                this.videoFiles = JSON.parse(this.files);
            } else {
                this.videoFiles = [...this.files];
            }
            setTimeout(() => {
                this.$refs.videoElement.addEventListener(
                    "canplaythrough",
                    () => {
                        if (this.loading) this.playWord();
                    }
                );
                this.$refs.videoElement.addEventListener(
                    "ended",
                    this.endedHandler
                );
                this.$refs.videoElement.addEventListener(
                    "error",
                    this.endedHandler
                );
                this.$refs.videoElement.load();
            }, 200);
        },
        playWord() {
            this.$emit("loaded");
            this.loading = false;
            if (this.play[0]) this.$refs.videoElement.play();
        },
        endedHandler() {
            if (!this.store) return;
            const playAll = this.store.state.playAll;
            setTimeout(() => {
                if (this.store.state.playAll.state === "next")
                    this.store.commit("setPlayState", {
                        state: "next",
                    });
            }, 1000);
        },
    },
};
</script>

<style lang="scss" scoped></style>
