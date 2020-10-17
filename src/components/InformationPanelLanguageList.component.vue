<template>
    <div class="flex flex-col style-panel">
        <ui-textbox
            placeholder="Filter languages"
            v-model="filter"
        ></ui-textbox>
        <div v-for="language of languages" :key="language.id">
            <div
                class="py-1 px-2 hover:bg-highlight-dark hover:text-white md:text-lg rounded cursor-pointer"
                @click="displayLanguage(language)"
            >
                {{ language.name }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            filter: "",
        };
    },
    computed: {
        languages: function() {
            const regexp = new RegExp(this.filter, "i");
            return this.$store.state.languages
                .map((language) => language.properties)
                .filter((language) => language.words)
                .filter((l) => l.language.name.match(regexp));
        },
    },
    methods: {
        displayLanguage(language) {
            this.$store.dispatch("loadLanguage", { code: language.code });
        },
    },
};
</script>

<style lang="scss" scoped>
.style-panel {
    height: calc(100vh - 120px);
    overflow: scroll;
}

@media (min-width: 768px) {
    .style-panel {
        height: calc(100vh - 170px);
        overflow: scroll;
    }
}
</style>
