<template>
    <div>
        <div class="row style-word-row">
            <div class="col-1">
                <el-button
                    type="text"
                    class="style-button"
                    @click="playWord"
                    v-if="word.audio_file"
                >
                    <i class="fas fa-volume-up"></i>
                </el-button>
                <audio ref="audioElement" v-if="word.audio_file">
                    <source :src="word.audio_file">Your browser does not support the
                    <code>audio</code> element.
                </audio>
            </div>
            <div class="col-5">{{word.language}}</div>
            <div class="col-6">{{word.indigenous}}</div>
        </div>
    </div>
</template>

<script>
import { mapRepositoryRoot } from "src/data-loader.service";
export default {
    props: {
        word: Object
    },
    data() {
        return {};
    },
    mounted() {
        this.word.audio_file = mapRepositoryRoot(this.word.audio_file);
    },
    methods: {
        playWord() {
            setTimeout(() => {
                this.$refs["audioElement"].play();
            }, 500);
        }
    }
};
</script>

<style lang="scss" scoped>
.style-word-row {
    line-height: 40px;
    border-bottom: 1px solid #000;
}
</style>


