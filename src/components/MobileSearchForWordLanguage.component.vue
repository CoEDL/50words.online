<template>
    <el-autocomplete
        placeholder="Search for a word or a language"
        v-model="query"
        @select="handleSelect"
        :fetch-suggestions="querySearch"
    ></el-autocomplete>
</template>

<script>
export default {
    data() {
        return {
            query: "",
        };
    },
    methods: {
        querySearch(query, cb) {
            let options = [
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
            if (query.length > 3)
                options = options.filter((o) => {
                    let re = new RegExp(query, "i");
                    return o.value.match(re);
                });
            console.log(options[0]);
            cb(options);
        },
        displayWord({ word }) {
            word = this.$store.state.words.filter((w) => w.name === word)[0];
            this.$store.dispatch("loadWord", word);
        },
        displayLanguage({ code }) {
            this.$store.dispatch("loadLanguage", { code });
        },
        handleSelect(selection) {
            console.log(selection);
            if (selection.type === "language") {
                this.displayLanguage({ code: selection.code });
            } else if (selection.type === "word") {
                this.displayWord({ word: selection.value });
            }
        },
    },
};
</script>
