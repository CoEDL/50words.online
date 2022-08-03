<template>
    <div class="flex flex-col">
        <el-select
            v-if="words.length"
            placeholder="Select a word"
            v-model="word"
            @change="displayWord"
        >
            <el-option
                v-for="word in words"
                :key="word.value"
                :label="word.label"
                :value="word.value"
            />
        </el-select>
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
        words: function () {
            return this.$store.state.words.map((w) => {
                return { label: w.name, value: w.name };
            });
        },
    },
    methods: {
        displayWord(word) {
            word = this.$store.state.words.filter((w) => w.name === word)[0];
            this.$store.dispatch("loadWord", word);
        },
    },
};
</script>
