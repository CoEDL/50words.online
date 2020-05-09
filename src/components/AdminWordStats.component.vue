<template>
    <div class="flex flex-col set-container-width overflow-scroll">
        <div class="flex flex-row text-xl font-bold" v-if="data.length">
            <div class="style-cell">English</div>
            <div
                v-for="(word, idx) of data[0].data"
                :key="idx"
                class="style-cell"
            >
                <div>{{ word.languageName }}</div>
            </div>
        </div>
        <div class="set-content-height">
            <div
                v-for="(entry, idx) of data"
                :key="idx"
                class="my-1 hover:bg-orange-200"
            >
                <div class="flex flex-row">
                    <div class="style-cell">
                        {{ entry.english }}
                    </div>
                    <div
                        v-for="(word, idx2) of entry.data"
                        :key="idx2"
                        class="style-cell"
                    >
                        <div>{{ word.indigenous }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { loadLanguageData } from "src/data-loader.service";
import { debounce, groupBy, flattenDeep } from "lodash";
export default {
    data() {
        return {
            debouncedDataLoader: debounce(this.loadData, 1000),
            data: [],
        };
    },
    computed: {
        languages: function() {
            return this.$store.state.languages;
        },
    },
    watch: {
        languages: function() {
            this.debouncedDataLoader();
        },
    },
    mounted() {
        this.debouncedDataLoader();
    },
    methods: {
        async loadData() {
            let wordData = [];
            const codes = this.$store.state.languages
                .filter((l) => l.properties.words)
                .map((l) => l.properties.code);
            for (let code of codes) {
                let data = await loadLanguageData({ code });
                data = data.words.map((word) => {
                    return {
                        languageName: data.properties.language.name,
                        english: word.english,
                        indigenous: word.indigenous,
                    };
                });
                wordData.push(data);
            }
            wordData = flattenDeep(wordData);
            wordData = groupBy(wordData, "english");
            this.data = Object.keys(wordData).map((key) => {
                return {
                    english: key,
                    data: wordData[key],
                };
            });
        },
    },
};
</script>

<style lang="scss" scoped>
.set-container-width {
    width: 100%;
    padding: 10px;
}
.set-content-height {
    height: calc(100vh - 250px);
}

.style-cell {
    min-width: 250px;
}
</style>
