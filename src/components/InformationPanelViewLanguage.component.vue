<template>
    <div
        id="informationPanel"
        class="overflow-scroll text-black"
        :style="{ height: height }"
        v-if="language"
    >
        <div class="flex flex-col">
            <div class="flex flex-row md:my-2">
                <div class="cursor-pointer text-lg mr-2 hover:text-highlight-dark" @click="back">
                    <i class="fas fa-chevron-left"></i>
                </div>
                <div class="text-2xl">
                    {{ language.properties.language.name }}
                </div>
                <div class="flex flex-grow"></div>
            </div>
        </div>
        <div class="flex flex-col space-y-2 border-b-2 mb-4">
            <div class="my-2 flex flex-row">
                <language-information-component
                    :code="language.properties.code"
                    class="flex-grow"
                />
                <render-language-information-play-component :data="language.properties.language" />
            </div>
            <div class="text-sm md:text-base flex flex-row">
                <div class="text-gray-600 flex-grow pt-1">
                    {{ language.properties.speaker.name }}
                </div>
                <render-language-information-play-component :data="language.properties.speaker" />
            </div>
        </div>
        <div class="flex flex-row justify-around my-2">
            <el-button @click="playAllWords = !playAllWords" size="large" :text="true" :bg="true">
                <div v-show="!playAllWords">
                    <i class="fas fa-play"></i>
                    <div class="inline-block ml-1">play all words</div>
                </div>
                <div v-show="playAllWords">
                    <i class="fas fa-stop"></i>
                    <div class="inline-block ml-1">stop playing</div>
                </div>
            </el-button>
        </div>

        <div v-if="playAllWords">
            <play-all-words-component
                :words="language.words"
                display="translation"
                @finished-playing="playAllWords = false"
            />
        </div>
        <div v-else>
            <div
                v-for="word of language.words"
                :key="index(word)"
                class="mx-1 hover:bg-highlight-dark hover:text-white p-1 px-2 md:p-2 md:my-1 rounded-lg"
            >
                <information-panel-render-word-component :data="word" display="translation" />
            </div>
        </div>
    </div>
</template>

<script setup>
import RenderLanguageInformationPlayComponent from "./RenderLanguageInformationPlay.component.vue";
import InformationPanelRenderWordComponent from "./InformationPanelRenderWord.component.vue";
import LanguageInformationComponent from "./LanguageInformation.component.vue";
import PlayAllWordsComponent from "./PlayAllWords.component.vue";
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
const $store = useStore();
const $router = useRouter();

let playAllWords = ref(false);
let height = ref(
    window.innerWidth < 768
        ? `${window.innerHeight - (window.innerHeight * 0.4 + 60)}px`
        : `${window.innerHeight - 170}px`
);
let language = computed(() => $store.getters.getSelectionData());
function back() {
    $router.push("/languages");
    setTimeout(() => {
        $store.commit("setSelectionToDisplay", {
            type: undefined,
            data: undefined,
        });
    }, 100);
}
function index(word) {
    return `${word.english}${word.indigenous}`;
}
</script>
