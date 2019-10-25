<template>
    <el-autocomplete
        v-model="query"
        :fetch-suggestions="findLanguage"
        placeholder="locate language"
        :highlight-first-item="true"
        @select="zoomToLanguage"
    >
        <template slot-scope="{ item }">{{item.properties.name}}</template>
    </el-autocomplete>
</template>

<script>
export default {
    data() {
        return {
            query: undefined
        };
    },
    computed: {
        languages: function() {
            return this.$store.state.languages;
        }
    },
    methods: {
        findLanguage(query, cb) {
            const regexp = new RegExp(query, "gi");
            const languages = this.languages.filter(l => {
                return l.properties.name.match(regexp) && l.properties.words;
            });
            cb(languages);
        },
        zoomToLanguage(language) {
            this.$emit("zoom-to-language", language);
        }
    }
};
</script>

<style lang="scss" scoped>
</style>