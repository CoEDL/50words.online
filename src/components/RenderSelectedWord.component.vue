<template>
    <div v-if="word">
        <div class="text-right">
            <div class="style-selected-word">{{word}}</div>
            <el-button circle @click="play" class="style-button" v-if="!disablePlayAllOnIOS">
                <span v-show="!isPlaying">
                    <i class="fas fa-play fa-fw"></i>
                </span>
                <span v-show="isPlaying">
                    <i class="fas fa-stop fa-fw"></i>
                </span>
            </el-button>
            <el-button
                circle
                @click="pause"
                class="style-button"
                :class="{ 'style-button-deselected': isPaused}"
                v-if="!disablePlayAllOnIOS && isPlaying"
            >
                <i class="fas fa-pause fa-fw"></i>
            </el-button>
            <el-button
                circle
                @click="loop =! loop"
                class="style-button"
                :class="{ 'style-button': loop, 'style-button-deselected': !loop }"
                v-if="!disablePlayAllOnIOS"
            >
                <i class="fas fa-repeat fa-fw"></i>
            </el-button>&nbsp;
        </div>
    </div>
</template>

<script>
import { orderBy, shuffle } from "lodash";
import { randomBytes } from "crypto";
import { stringify } from "querystring";

export default {
    data() {
        return {
            watchers: [],
            isPlaying: false,
            isPaused: false,
            loop: false,
            disablePlayAllOnIOS: !!navigator.platform.match(/iPhone|iPod|iPad/)
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
        this.watchers.playAll = this.$watch("playAll", this.continue);
        this.watchers.word = this.$watch("word", () => {
            this.isPlaying = false;
            this.isPaused = false;
            this.$store.commit("setPlayAll", {
                play: false,
                word: undefined,
                state: "stopped"
            });
        });
    },
    beforeDestroy() {
        this.watchers.playAll();
        this.watchers.word();
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
        },
        pause() {
            if (this.playAll.state === "paused") {
                this.$store.commit("setPlayAll", {
                    play: true,
                    word: undefined,
                    state: "next"
                });
                this.isPaused = false;
            } else {
                this.$store.commit("setPlayAll", {
                    play: true,
                    word: undefined,
                    state: "paused"
                });
                this.isPaused = true;
            }
        },
        continue(n, o) {
            if (
                (!this.playAll.play && this.playAll.state === "stopped") ||
                !this.isPlaying
            ) {
                this.isPaused = false;
                this.isPlaying = false;
                this.loop = false;
                return;
            }
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
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-button {
    border-color: black;
    background-color: black;
    color: $text-color;
}

.style-button-deselected {
    color: $primary-color;
}

.style-selected-word {
    font-size: 1.5em;
    color: $text-color;
}
@media (min-width: 1024px) {
    .style-selected-word {
        color: $text-color;
        padding-top: 10px;
    }
}
</style>


