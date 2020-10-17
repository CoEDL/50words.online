<template>
    <audio ref="audioElement">
        <source v-for="(file, idx) of audioFiles" :src="file" :key="idx" />
        Your browser does not support the <code>audio</code> element.
    </audio>
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
            audioFiles: [],
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
                this.audioFiles = JSON.parse(this.files);
            } else {
                this.audioFiles = [...this.files];
            }
            this.$nextTick(() => {
                this.$refs.audioElement.addEventListener(
                    "canplaythrough",
                    () => {
                        if (this.loading) this.playWord();
                    }
                );
                this.$refs.audioElement.addEventListener(
                    "ended",
                    this.endedHandler
                );
                this.$refs.audioElement.addEventListener(
                    "error",
                    this.endedHandler
                );
                this.$refs.audioElement.load();
            });
        },
        playWord() {
            this.$emit("loaded");
            this.loading = false;
            this.$refs.audioElement.play();
        },
        async endedHandler() {
            await new Promise((resolve) => setTimeout(resolve, 1000));
            this.$emit("finished-playing");
        },
    },
};
</script>

<style lang="scss" scoped></style>
