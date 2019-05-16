<template>
    <div>
        <div class="style-word-row">
            <span v-if="layout === 'popup'">
                <div class="row">
                    <div class="col">{{word.language}}</div>
                </div>
                <div class="row">
                    <div class="col-4">
                        <el-button
                            type="text"
                            class="style-button px-3"
                            @click="playWord"
                            v-if="word.audio_file"
                        >
                            <i class="fas fa-volume-up fa-2x"></i>
                        </el-button>
                        <audio ref="audioElement" v-if="word.audio_file">
                            <source :src="word.audio_file">Your browser does not support the
                            <code>audio</code> element.
                        </audio>
                    </div>
                    <div class="col-8">{{word.indigenous}}</div>
                </div>
                <!-- <div class="row">
                    <div class="col-4"></div>
                    <div class="col-8">{{word.indigenous}}</div>
                </div>-->
            </span>
            <span v-if="layout !=='popup'">
                <div class="row">
                    <div class="col-2">
                        <el-button
                            type="text"
                            class="style-button px-3"
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
                    <div class="col-5">{{word.english}}</div>
                    <div class="col-5">{{word.indigenous}}</div>
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
            console.log("changed");
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
            }, 500);
        }
    }
};
</script>

<style lang="scss" scoped>
.style-word-row {
    line-height: 40px;
}
</style>


