<template>
    <div>
        <div class="row mt-5">
            <div
                class="col"
            >Select a word to see the list of languages for that word and audio samples.</div>
        </div>
        <div v-for="(word, idx) of words" :key="idx">
            <div class="row">
                <div class="col">
                    <el-button
                        type="text"
                        class="style-button"
                        :class="{'style-selected-word': selectedWord === word }"
                        @click="setSelectedWord(word)"
                    >{{word}}</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { loadWordData } from "../data-loader.service";

export default {
    data() {
        return {
            watchers: {},
            selectedWord: undefined,
            wordData: []
        };
    },
    computed: {
        storeSelectedWord: function() {
            if (!this.$store.state.selectedWord) this.selectedWord = undefined;
            return this.$store.state.selectedWord;
        },
        words: function() {
            return this.$store.state.words.map(w => {
                return w.name;
            });
        }
    },
    mounted() {
        this.watchers.selectedWord = this.$watch("storeSelectedWord", () => {});
    },
    beforeDestroy() {
        this.watchers.selectedWord();
    },
    methods: {
        async setSelectedWord(word) {
            this.selectedWord = word;
            word = this.$store.state.words.filter(w => {
                return w.name === word;
            })[0];
            const wordData = await loadWordData({ index: word.index });
            this.$store.commit("setSelectedWord", { word: wordData });
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-selected-word {
    color: $text-color;
    font-size: 3em;
}
</style>


