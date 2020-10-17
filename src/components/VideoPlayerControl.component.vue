<template>
    <video ref="videoElement">
        <source v-for="(file, idx) of videoFiles" :src="file" :key="idx" />
        Your browser does not support the <code>video</code> element.
    </video>
</template>

<script>
import { debounce } from "lodash";
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
    },
    data() {
        return {
            debouncedLoad: debounce(this.load, 500),
            videoFiles: [],
            loading: false,
        };
    },
    watch: {
        play: function(n, o) {
            if (n.play) this.debouncedLoad();
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
            this.$refs.videoElement.play();
        },
        async endedHandler() {
            await new Promise((resolve) => setTimeout(resolve, 1000));
            this.$emit("finished-playing");
        },
    },
};
</script>

<style lang="scss" scoped></style>
