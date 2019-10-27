<template>
    <el-autocomplete
        v-model="query"
        :fetch-suggestions="findLanguage"
        placeholder="locate language"
        @select="zoomToLanguage"
    >
        <template slot-scope="{ item }">
            <span :class="{ 'style-has-words': item.properties.words} ">{{item.properties.name}}</span>
        </template>
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
            if (!query || query.length < 2) {
                cb([]);
                return;
            }
            const regexp = new RegExp(query, "gi");
            const languages = this.languages.filter(l => {
                return l.properties.name.match(regexp);
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
@import "assets/variables.scss";

.style-has-words {
    color: $text-color;
    font-size: 25px;
    line-height: 40px;
}
</style>