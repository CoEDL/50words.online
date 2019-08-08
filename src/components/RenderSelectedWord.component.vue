<template>
    <div v-if="word">
        <div class="style-selected-word text-right">
            <el-button type="text" @click="play" class="style-button">
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
            <el-button
                type="text"
                @click="loop =! loop"
                :class="{ 'style-button': loop, 'style-button-deselected': !loop }"
            >
                <span v-show="!loop">
                    <i class="fal fa-repeat fa-2x fa-fw"></i>
                    &nbsp;
                </span>
                <span v-show="loop">
                    <i class="fas fa-repeat fa-2x fa-fw"></i>
                    &nbsp;
                </span>
            </el-button>
        </div>
    </div>
</template>

<script>
import { orderBy, shuffle } from "lodash";
import { randomBytes } from "crypto";

export default {
    data() {
        return {
            watchers: [],
            isPlaying: false,
            loop: false
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
                if (this.loop && n.play) {
                    let words = this.$store.state.words.filter(
                        word => !this.playedWords.includes(word.name)
                    );
                    console.log("words left to play", words.length);
                    if (!words.length) {
                        this.playedWords = [];
                        words = this.$store.state.words.filter(
                            word => !this.playedWords.includes(word.name)
                        );
                    }
                    let word = shuffle(words).pop();
                    this.$store.dispatch("loadWord", { word: word.name });
                    setTimeout(() => {
                        this.words = orderBy(
                            [...this.$store.state.selectedWord],
                            "properties.language.code"
                        );
                        let word = this.words.pop();
                        this.playedWords.push(word.properties.english);
                        this.$store.commit("setPlayAll", {
                            play: true,
                            word,
                            state: "playing"
                        });
                    }, 1000);
                } else {
                    setTimeout(() => {
                        this.$store.commit("setPlayAll", {
                            play: false,
                            word: undefined,
                            state: "stopped"
                        });
                        this.isPlaying = false;
                    }, 2000);
                }
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
    beforeDestroy() {
        this.watchers.playAll();
    },
    methods: {
        play() {
            this.isPlaying = !this.isPlaying;
            if (this.isPlaying) {
                this.playedWords = [];
                this.words = orderBy(
                    [...this.$store.state.selectedWord],
                    "properties.language.code"
                );
                let word = this.words.pop();
                this.playedWords.push(word.properties.english);

                this.$store.commit("setPlayAll", {
                    play: true,
                    word,
                    state: "playing"
                });
            } else {
                this.$store.commit("setPlayAll", {
                    play: false,
                    word: undefined,
                    state: "stopped"
                });
            }
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-button {
    color: $text-color;
}

.style-button-deselected {
    color: #ccc;
}

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


