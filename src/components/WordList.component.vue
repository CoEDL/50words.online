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
            <div class="row" v-if="selectedWord === word">
                <div class="col">
                    <div v-for="(w, idx2) of wordData" :key="idx2">
                        <render-word-data-component :word="w"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RenderWordDataComponent from "./RenderWordData.component.vue";
import { loadWordData } from "../data-loader.service";

export default {
    components: {
        RenderWordDataComponent
    },
    data() {
        return {
            selectedWord: undefined,
            wordData: []
        };
    },
    computed: {
        words: function() {
            return this.$store.state.words.map(w => {
                return w.name;
            });
        }
    },
    methods: {
        async setSelectedWord(word) {
            this.selectedWord = word;
            word = this.$store.state.words.filter(w => {
                return w.name === word;
            })[0];
            this.wordData = await loadWordData({ index: word.index });
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-selected-word {
    color: $brand-primary-color;
    font-size: 3em;
}
</style>


