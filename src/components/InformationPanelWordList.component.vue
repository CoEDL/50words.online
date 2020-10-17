<template>
    <div class="flex flex-col style-panel">
        <ui-textbox placeholder="Filter words" v-model="filter"></ui-textbox>
        <div v-for="word of words" :key="word.index">
            <div
                class="p-2 hover:bg-highlight-dark hover:text-white md:text-lg rounded cursor-pointer"
                @click="displayWord(word)"
            >
                {{ word.name }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return { filter: "" };
    },
    computed: {
        words: function() {
            const regexp = new RegExp(this.filter, "i");
            return this.$store.state.words.filter((w) => w.name.match(regexp));
        },
    },
    methods: {
        displayWord(word) {
            this.$store.dispatch("loadWord", word);
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
