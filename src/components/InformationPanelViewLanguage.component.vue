<template>
    <div id="informationPanel" class="overflow-scroll" :style="{ height: height }" v-if="data">
        <div class="flex flex-col">
            <div class="flex flex-row md:my-2">
                <div
                    class="cursor-pointer text-lg text-2xl mr-2 hover:text-highlight-dark"
                    @click="back"
                >
                    <i class="fas fa-chevron-left"></i>
                </div>
                <div class="text-2xl">
                    {{ data.properties.language.name }}
                </div>
                <div class="flex flex-grow"></div>
            </div>
        </div>
        <div class="flex flex-col space-y-2 border-b-2 mb-4">
            <div class="my-2 flex flex-row">
                <language-information-component :code="data.properties.code" class="flex-grow" />
                <render-language-information-play-component :data="data.properties.language" />
            </div>
            <div class="text-sm md:text-base flex flex-row">
                <div class="text-gray-600 flex-grow pt-1">
                    {{ data.properties.speaker.name }}
                </div>
                <render-language-information-play-component :data="data.properties.speaker" />
            </div>
        </div>
        <div class="flex flex-row justify-around my-2">
            <ui-button @click="playAllWords = !playAllWords" color="default">
                <div v-show="!playAllWords">
                    <i class="fas fa-play"></i>
                    <div class="inline-block ml-1">play all words</div>
                </div>
                <div v-show="playAllWords">
                    <i class="fas fa-stop"></i>
                    <div class="inline-block ml-1">stop playing</div>
                </div>
            </ui-button>
        </div>

        <div v-if="playAllWords">
            <play-all-words-component
                :words="data.words"
                display="translation"
                @finished-playing="playAllWords = false"
            />
        </div>
        <div v-else>
            <div
                v-for="word of data.words"
                :key="index(word)"
                class="mx-1 hover:bg-highlight-dark hover:text-white p-1 px-2 md:p-2 md:my-1 rounded-lg"
            >
                <information-panel-render-word-component :data="word" display="translation" />
            </div>
        </div>
    </div>
</template>

<script>
import RenderLanguageInformationPlayComponent from "./RenderLanguageInformationPlay.component.vue";
import InformationPanelRenderWordComponent from "./InformationPanelRenderWord.component.vue";
import LanguageInformationComponent from "./LanguageInformation.component.vue";
import PlayAllWordsComponent from "./PlayAllWords.component.vue";

export default {
    components: {
        RenderLanguageInformationPlayComponent,
        InformationPanelRenderWordComponent,
        LanguageInformationComponent,
        PlayAllWordsComponent,
    },
    data() {
        return {
            playAllWords: false,
            height:
                window.innerWidth < 768
                    ? `${window.innerHeight - (window.innerHeight * 0.4 + 60)}px`
                    : `${window.innerHeight - 170}px`,
        };
    },
    computed: {
        data: function() {
            let data = this.$store.getters.getSelectionData();
            return data;
        },
    },
    methods: {
        back() {
            this.$store.commit("setSelectionToDisplay", {
                type: undefined,
                data: undefined,
            });
        },
        index(word) {
            return `${word.english}${word.indigenous}`;
        },
    },
};
</script>

<style lang="scss" scoped></style>
