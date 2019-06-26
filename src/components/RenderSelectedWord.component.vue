<template>
    <div v-if="word">
        <div class="style-selected-word text-right">
            <el-button type="text" @click="play" class="style-audio-control">
                <span v-show="!playAll">
                    <i class="fas fa-play fa-2x fa-fw"></i>
                    &nbsp;
                </span>
                <span v-show="playAll">
                    <i class="fas fa-stop fa-2x fa-fw"></i>
                    &nbsp;
                </span>
            </el-button>
            {{word}}
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isPlaying: false
        };
    },
    computed: {
        playAll: function() {
            return this.$store.state.playAll.play;
        },
        word: function() {
            return this.$store.state.selectedWord
                ? this.$store.state.selectedWord[0].properties.english
                : undefined;
        }
    },
    methods: {
        play() {
            this.isPlaying = !this.isPlaying;
            this.$store.commit("setPlayAll", this.isPlaying);
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-selected-word {
    font-size: 1.5em;
    color: $text-color;
}
@media (min-width: 1024px) {
    .style-selected-word {
        color: $text-color;
    }
}
</style>


