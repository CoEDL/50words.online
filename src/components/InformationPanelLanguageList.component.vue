<template>
    <div class="flex flex-col style-panel">
        <el-input placeholder="Filter languages" v-model="data.filter"></el-input>
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

<script setup>
import { reactive, computed, watch } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
const $store = useStore();
const $route = useRoute();

// this watcher handles language loading in response to nav events
watch(
    () => $route.path,
    () => {
        if ($route.params?.language) {
            let language = $store.state.languages
                .map((language) => language.properties)
                .filter((language) => language.name === $route.params.language);
            if (language.length) displayLanguage(language[0]);
        }
    },
    { immediate: true }
);

const data = reactive({
    filter: "",
});
let languages = computed(() => {
    const regexp = new RegExp(data.filter, "i");
    return $store.state.languages
        .map((language) => language.properties)
        .filter((language) => language.words)
        .filter((l) => l.language.name.match(regexp));
});

function displayLanguage(language) {
    $store.dispatch("loadLanguage", { code: language.code });
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
