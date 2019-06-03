<template>
    <div>
        <div class="style-word-row">
            <span v-if="layout === 'popup'">
                <div class="row">
                    <div class="col">{{ word.language }}</div>
                </div>
                <div class="row">
                    <div class="col-4">
                        <el-button
                            type="text"
                            class="style-button px-3"
                            @click="playWord"
                            v-if="word.audio_file.length"
                        >
                            <i class="fas fa-volume-up fa-2x"></i>
                        </el-button>
                        <audio ref="audioElement" v-if="word.audio_file.length">
                            <source
                                :src="file"
                                v-for="(file, idx) of JSON.parse(word.audio_file)"
                                :key="idx"
                            >Your browser does not support the
                            <code>audio</code> element.
                        </audio>
                    </div>
                    <div class="col-8 text-lowercase">{{ word.indigenous }}</div>
                </div>
            </span>
            <span v-if="layout !== 'popup'">
                <div class="my-4">
                    <div class="row">
                        <div class="col-2">
                            <el-button
                                type="text"
                                class="style-button px-3"
                                @click="playWord"
                                v-if="word.audio_file.length"
                            >
                                <i class="fas fa-volume-up fa-2x"></i>
                            </el-button>
                            <audio ref="audioElement" v-if="word.audio_file.length">
                                <source
                                    :src="file"
                                    v-for="(file, idx) of word.audio_file"
                                    :key="idx"
                                >Your browser does not support the
                                <code>audio</code> element.
                            </audio>
                        </div>
                        <div class="col-10">
                            <div class="row">
                                <div
                                    class="col-12 style-english text-lowercase"
                                    v-if="word.english_alternate"
                                >{{ word.english_alternate }}</div>
                                <div
                                    class="col-12 style-english text-lowercase"
                                    v-else
                                >{{ word.english}}</div>
                                <div
                                    class="col-12 style-indigenous text-lowercase"
                                >{{ word.indigenous }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </span>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        layout: String,
        word: Object
    },
    data() {
        return {
            watchers: {}
        };
    },
    mounted() {
        this.watchers.audio = this.$watch("word.audio_file", () => {
            if (this.$refs.audioElement) this.$refs.audioElement.load();
        });
    },
    beforeDestroy() {
        if (this.watchers.audio) this.watchers.audio();
    },
    methods: {
        playWord() {
            setTimeout(() => {
                this.$refs.audioElement.play();
            }, 200);
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-word-row {
    line-height: 40px;
}

.style-english {
    opacity: 0.8;
    font-size: 1.3em;
}

.style-indigenous {
    border-bottom: 1px solid #000;
    font-size: 2em;
}
</style>
