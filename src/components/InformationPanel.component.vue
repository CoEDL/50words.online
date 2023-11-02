<template>
    <div class="flex flex-col">
        <div class="text-sm text-gray-600">View by</div>
        <el-tabs v-model="activeTab" @tab-click="handleTabSelect" class="text-gray-700">
            <el-tab-pane name="languages">
                <template #label>
                    <span
                        :class="{
                            'text-black': activeTab === 'language',
                            'text-gray-600': activeTab !== 'language',
                        }"
                    >
                        LANGUAGE
                    </span>
                </template>
                <div v-if="activeTab === 'languages'">
                    <information-panel-language-list-component v-if="show === 'list'" />
                    <information-panel-view-language-component v-if="show === 'language'" />
                </div>
            </el-tab-pane>
            <el-tab-pane label="word" name="words">
                <template #label>
                    <span
                        :class="{
                            'text-black': activeTab === 'word',
                            'text-gray-600': activeTab !== 'word',
                        }"
                        >WORD</span
                    >
                </template>
                <div v-if="activeTab === 'words'">
                    <information-panel-word-list-component v-if="show === 'list'" />
                    <information-panel-view-word-component v-if="show === 'word'" />
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import InformationPanelLanguageListComponent from "./InformationPanelLanguageList.component.vue";
import InformationPanelViewLanguageComponent from "./InformationPanelViewLanguage.component.vue";
import InformationPanelWordListComponent from "./InformationPanelWordList.component.vue";
import InformationPanelViewWordComponent from "./InformationPanelViewWord.component.vue";
import { ref, reactive, watch, computed } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
const $store = useStore();
const $route = useRoute();
const $router = useRouter();

let activeTab = ref("languages");
let show = ref("list");

// this watcher handles loading the correct component
//  as a result of back / forward navigation events
watch(
    () => $route.path,
    () => {
        if ($route.name === "home") $router.push("languages");
        if ($route.path.match(/\languages/)) activeTab.value = "languages";
        if ($route.path.match(/\/words/)) activeTab.value = "words";
        if (["/languages", "/words"].includes($route.path)) {
            handleTabSelect({ props: { name: $route.name } });
        }
    },
    { immediate: true }
);

// this watcher handles route updates as the user selects
//  languages / words to interact with
watch(
    () => $store.state.selection,
    () => {
        const selection = $store.state.selection;
        show.value = selection?.type ?? "list";

        if (show.value === "list") {
            $router.push({ path: `/${activeTab.value}` });
        } else {
            let name =
                activeTab.value === "languages"
                    ? selection.data?.properties?.name
                    : selection.data?.name;
            $router.push({ path: `/${activeTab.value}/${name}` });
        }
    },
    { deep: true }
);

function handleTabSelect(tab) {
    $router.push(`/${tab.props.name}`);
    activeTab.value = tab.props.name;
    setTimeout(() => {
        $store.commit("setSelectionToDisplay", {
            type: undefined,
            data: undefined,
        });
        show.value = "list";
        if (tab.props.name === "languages") {
            $store.commit("setLayer", "languages");
        } else {
            $store.commit("setLayer", "words");
        }
    }, 100);
}
</script>
