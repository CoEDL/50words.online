<template>
    <div class="flex flex-col">
        <div class="text-sm text-gray-800">Filter languages</div>

        <div>
            <el-autocomplete
                v-model="query"
                :fetch-suggestions="findLanguage"
                placeholder=""
                @select="zoomToLanguage"
            >
                <div slot="prefix" class="pt-1 pl-1 text-lg text-gray-800">
                    <i class="fas fa-search"></i>
                </div>
                <template slot-scope="{ item }">
                    <span :class="{ 'style-has-words': item.properties.words }">{{
                        item.properties.name
                    }}</span>
                </template>
            </el-autocomplete>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            query: undefined,
        };
    },
    computed: {
        languages: function() {
            return this.$store.state.languages;
        },
    },
    methods: {
        findLanguage(query, cb) {
            if (!query || query.length < 2) {
                cb([]);
                return;
            }
            const regexp = new RegExp(query, "gi");
            const languages = this.languages.filter((l) => {
                return l.properties.name.match(regexp);
            });
            cb(languages);
        },
        zoomToLanguage(language) {
            this.$emit("fly-to", {
                coordinates: language.geometry.coordinates,
            });
        },
    },
};
</script>

<style lang="scss" scoped></style>
