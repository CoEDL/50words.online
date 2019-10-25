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
                @click="loop = !loop"
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
        this.watchers.playAll = this.$watch("playAll", this.updateState);
    },
    beforeDestroy() {
        this.watchers.playAll();
    },
    methods: {
        play() {
            this.isPlaying = !this.isPlaying;
            if (this.isPlaying) {
                this.$store.commit("setPlayAll", {
                    state: "next",
                    loop: this.loop
                });
                this.isPaused = false;
            } else {
                this.$store.commit("setPlayAll", {
                    state: "stopped",
                    loop: this.loop
                });
                this.isPaused = false;
            }
        },
        pause() {
            if (this.isPaused) {
                this.$store.commit("setPlayAll", {
                    state: "next"
                });
            } else {
                this.$store.commit("setPlayAll", {
                    state: "paused"
                });
            }
            this.isPaused = !this.isPaused;
        },
        setLoopAll() {
            this.$store.commit("setPlayAll", {
                loop: this.loop
            });
        },
        updateState() {
            if (this.$store.state.playAll.state === "ready")
                this.isPlaying = false;
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


