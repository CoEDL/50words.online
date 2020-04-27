<template>
    <div class="flex flex-col">
        <div class="text-center">
            Select from the list below, then click on the words shown on the map
            to hear the audio and see the language name.
        </div>
        <div v-for="(word, idx) of words" :key="idx">
            <el-button
                type="text"
                class="text-black overflow-x-scroll hover:text-orange-200 text-sm md:text-xl"
                :class="{ 'md:text-3xl text-orange-700': styleWord(word) }"
                @click="setSelectedWord(word)"
                >{{ word }}</el-button
            >
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            watchers: {},
        };
    },
    computed: {
        selectedWord: {
            get: function() {
                return this.$store.state.selectedWord;
            },
            set: function(word) {
                this.$store.dispatch("loadWord", { word });
            },
        },

        words: function() {
            return this.$store.state.words.map((w) => {
                return w.name;
            });
        },
    },
    methods: {
        async setSelectedWord(word) {
            this.$emit("collapse-information-panel");
            this.selectedWord = word;
            this.$store.dispatch("loadWord", { word });
        },
        styleWord(word) {
            let selectedWord = this.selectedWord
                ? this.selectedWord[0]
                : undefined;
            if (selectedWord) return word === selectedWord.properties.english;
        },
    },
};
</script>

<style lang="scss" scoped></style>
