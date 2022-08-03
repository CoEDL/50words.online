<template>
    <div class="flex flex-col style-panel">
        <el-input placeholder="Filter words" v-model="data.filter"></el-input>
        <div v-for="word of words" :key="word.index">
            <div
                class="py-1 px-2 hover:bg-highlight-dark hover:text-white md:text-lg rounded cursor-pointer"
                @click="displayWord(word)"
            >
                {{ word.name }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, computed } from "vue";
import { useStore } from "vuex";
const store = useStore();

const data = reactive({
    filter: "",
});
let words = computed(() => {
    const regexp = new RegExp(data.filter, "i");
    return store.state.words.filter((w) => w.name.match(regexp));
});
function displayWord(word) {
    store.dispatch("loadWord", word);
}
</script>

<style lang="scss" scoped>
.style-panel {
    height: calc(100vh - 150px);
    overflow: scroll;
}

@media (min-width: 768px) {
    .style-panel {
        height: calc(100vh - 200px);
        overflow: scroll;
    }
}
</style>
