<template>
    <div v-if="ready">
        <!-- visible on medium sized screens and larger -->
        <div class="pt-4 px-6 hidden md:flex md:flex-col">
            <header-component />
            <div class="flex flex-row">
                <information-panel-component class="mt-4 w-3/12" />
                <div class="flex flex-col w-full md:w-9/12 md:flex">
                    <div class="flex-grow mt-2 ml-2 flex flex-col">
                        <map-component class="flex-grow" />
                    </div>
                    <footer-component class="hidden md:flex" />
                </div>
            </div>
        </div>

        <!-- visible only on small screens - hidden on medium sized screens and larger -->
        <div class="flex flex-col space-y-4 md:hidden w-screen h-screen">
            <header-mobile-component class="px-2" />
            <div class="flex-grow flex flex-col space-y-4 px-2" v-if="!selection">
                <mobile-select-language-component />
                <mobile-select-word-component />
                <mobile-search-for-word-language-component />
                <div class="text-sm text-gray-800 text-center">
                    Attribution-NonCommercial 4.0 International
                    <a
                        href="https://creativecommons.org/licenses/by-nc/4.0/"
                        target="_blank"
                        class="text-highlight-dark"
                    >
                        https://creativecommons.org/licenses/by-nc/4.0/
                    </a>
                </div>
            </div>
            <div v-else class="p-2">
                <information-panel-view-language-component v-if="layer === 'languages'" />
                <information-panel-view-word-component v-if="layer === 'words'" />
            </div>
            <map-component class="" />
        </div>
    </div>
</template>

<script setup>
import { loadLanguages, loadWords } from "../data-loader.service";

import MapComponent from "./Map.component.vue";
import HeaderComponent from "./Header.component.vue";
import InformationPanelComponent from "./InformationPanel.component.vue";
import FooterComponent from "./Footer.component.vue";

import HeaderMobileComponent from "./HeaderMobile.component.vue";
import MobileSelectLanguageComponent from "./MobileSelectLanguage.component.vue";
import MobileSearchForWordLanguageComponent from "./MobileSearchForWordLanguage.component.vue";
import MobileSelectWordComponent from "./MobileSelectWord.component.vue";
import InformationPanelViewLanguageComponent from "./InformationPanelViewLanguage.component.vue";
import InformationPanelViewWordComponent from "./InformationPanelViewWord.component.vue";
import { computed, ref, onBeforeMount } from "vue";
import { useStore } from "vuex";
const $store = useStore();

let selection = computed(() => $store.getters.getSelectionData());
let layer = computed(() => $store.state.layer);
let ready = ref(false);
onBeforeMount(async () => {
    console.time();
    let languages = await loadLanguages();
    $store.commit("setLanguages", languages);

    let words = await loadWords();
    $store.commit("setWords", words);
    console.timeEnd();
    ready.value = true;
});
</script>
