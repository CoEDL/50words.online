<template>
    <div class="flex flex-col">
        <ui-select
            v-if="words.length"
            help="Select a word"
            :options="words"
            v-model="word"
            @change="displayWord"
        ></ui-select>
    </div>
</template>

<script>
export default {
    data() {
        return {
            word: "",
        };
    },
    computed: {
        words: function() {
            return this.$store.state.words.map((w) => {
                return { label: w.name, value: w.name };
            });
        },
    },
    methods: {
        displayWord(word) {
            if (!word?.value) return;
            word = this.$store.state.words.filter(
                (w) => w.name === word.value
            )[0];
            this.$store.dispatch("loadWord", word);
        },
    },
};
</script>
