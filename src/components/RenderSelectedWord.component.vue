<template>
    <div class="style-selected-word text-right">{{word}}</div>
</template>

<script>
export default {
    data() {
        return {};
    },
    computed: {
        word: function() {
            return this.$store.state.selectedWord
                ? this.$store.state.selectedWord[0].english
                : this.$store.state.selectedWord;
        }
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.style-selected-word {
    font-size: 2.5em;
    color: $text-color;
}
</style>


