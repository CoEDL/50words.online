<template>
    <div class="flex flex-col">
        <ui-autocomplete
            help="Search for a word or a language"
            :suggestions="options"
            v-model="query"
            @select="handleSelect"
        ></ui-autocomplete>
    </div>
</template>

<script>
export default {
    data() {
        return {
            query: "",
        };
    },
    computed: {
        options: function() {
            const options = [
                ...this.$store.state.languages
                    .map((language) => language.properties)
                    .filter((language) => language.words)
                    .map((l) => {
                        return {
                            label: l.language.name,
                            type: "language",
                            value: l.language.name,
                            code: l.code,
                        };
                    }),
                ...this.$store.state.words.map((w) => {
                    return { label: w.name, type: "word", value: w.name };
                }),
            ];
            return options;
        },
    },
    methods: {
        displayWord({ word }) {
            word = this.$store.state.words.filter((w) => w.name === word)[0];
            this.$store.dispatch("loadWord", word);
        },
        displayLanguage({ code }) {
            this.$store.dispatch("loadLanguage", { code });
        },
        handleSelect(selection) {
            if (selection.type === "language") {
                this.displayLanguage({ code: selection.code });
            } else if (selection.type === "word") {
                this.displayWord({ word: selection.value });
            }
        },
    },
};
</script>
