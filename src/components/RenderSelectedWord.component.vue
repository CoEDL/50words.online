<template>
    <div v-if="word">
        <div class="style-selected-word text-right">
            <el-button type="text" @click="play" class="style-audio-control">
                <span v-show="!isPlaying">
                    <i class="fas fa-play fa-2x fa-fw"></i>
                    &nbsp;
                </span>
                <span v-show="isPlaying">
                    <i class="fas fa-stop fa-2x fa-fw"></i>
                    &nbsp;
                </span>
            </el-button>
            {{word}}
        </div>
    </div>
</template>

<script>
import { orderBy } from "lodash";

export default {
    data() {
        return {
            watchers: [],
            isPlaying: false
        };
    },

    computed: {
        playAll: function() {
            return this.$store.state.playAll;
        },
        word: function() {
            return this.$store.state.selectedWord
                ? this.$store.state.selectedWord[0].properties.english
                : undefined;
        }
    },
    mounted() {
        this.watchers.playAll = this.$watch("playAll", (n, o) => {
            if (n.state === "next" && !this.words.length) {
                setTimeout(() => {
                    this.$store.commit("setPlayAll", {
                        play: false,
                        word: undefined,
                        state: "stopped"
                    });
                    this.isPlaying = false;
                }, 2000);
            }
            if (n.state === "next" && n.play === true && this.words.length) {
                setTimeout(() => {
                    this.$store.commit("setPlayAll", {
                        play: true,
                        word: this.words.pop(),
                        state: "playing"
                    });
                }, 2000);
            }
        });
    },
    beforeDestroy() {},
    methods: {
        play() {
            this.isPlaying = !this.isPlaying;
            if (this.isPlaying) {
                this.words = orderBy(
                    [...this.$store.state.selectedWord],
                    "properties.language.code"
                );

                this.$store.commit("setPlayAll", {
                    play: true,
                    word: this.words.pop(),
                    state: "playing"
                });
            } else {
                this.$store.commit("setPlayAll", {
                    play: false,
                    word: undefined
                });
            }
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


