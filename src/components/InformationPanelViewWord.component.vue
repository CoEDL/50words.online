<template>
    <div class="overflow-scroll text-black" :style="{ height: height }">
        <div class="flex flex-col">
            <div class="flex flex-row px-2 md:my-2">
                <div
                    class="cursor-pointer text-2xl ml-1 mr-4 hover:text-highlight-dark"
                    @click="back"
                >
                    <i class="fas fa-chevron-left"></i>
                </div>
                <div class="text-2xl">{{ selection.name }}</div>
                <div class="flex flex-grow"></div>
            </div>

            <div class="flex flex-row justify-around my-2">
                <el-button
                    @click="playAllWords = !playAllWords"
                    :text="true"
                    :bg="true"
                    size="large"
                >
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
                    :words="selection.words"
                    display="languageName"
                    @finished-playing="playAllWords = false"
                />
            </div>
            <div v-if="!playAllWords">
                <div v-for="(word, idx) of selection.words" :key="idx" class="m-1">
                    <information-panel-render-word-component :data="word" display="languageName" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import RenderLanguageInformationPlayComponent from "./RenderLanguageInformationPlay.component.vue";
import InformationPanelRenderWordComponent from "./InformationPanelRenderWord.component.vue";
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
let selection = computed(() => $store.getters.getSelectionData());
function back() {
    $router.push("/words");
    setTimeout(() => {
        $store.commit("setSelectionToDisplay", {
            type: undefined,
            data: undefined,
        });
    }, 100);
}
</script>
