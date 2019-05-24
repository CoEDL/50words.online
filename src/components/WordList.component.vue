<template>
    <div>
        <div class="row my-3">
            <div class="col style-help-text text-center px-5">
                Select a word to see the list of
                languages
                <br>for that word and audio samples.
            </div>
        </div>
        <div v-for="(word, idx) of words" :key="idx">
            <div class="row">
                <div class="col">
                    <el-button
                        type="text"
                        class="style-button style-word"
                        :class="{'style-selected-word': styleWord(word)}"
                        @click="setSelectedWord(word)"
                    >{{word}}</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            watchers: {}
        };
    },
    computed: {
        selectedWord: {
            get: function() {
                return this.$store.state.selectedWord;
            },
            set: function(word) {
                this.$store.dispatch("loadWord", { word });
            }
        },

        words: function() {
            return this.$store.state.words.map(w => {
                return w.name;
            });
        }
    },
    methods: {
        async setSelectedWord(word) {
            this.selectedWord = word;
            this.$store.dispatch("loadWord", { word });
        },
        styleWord(word) {
            let selectedWord = this.selectedWord ? this.selectedWord[0] : {};
            return word === selectedWord.english;
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-word {
    font-size: 1.4em;
}

.style-selected-word {
    color: $text-color;
    font-size: 3em;
}

.style-help-text {
    font-size: 1.2em;
}
</style>


