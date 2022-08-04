<template>
    <div class="overflow-scroll text-black" :style="{ height: height }" v-if="data">
        <div class="flex flex-col">
            <div class="flex flex-row px-2 md:my-2">
                <div
                    class="cursor-pointer text-2xl ml-1 mr-4 hover:text-highlight-dark"
                    @click="back"
                >
                    <i class="fas fa-chevron-left"></i>
                </div>
                <div class="text-2xl">{{ data.name }}</div>
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
                    :words="data.words"
                    display="languageName"
                    @finished-playing="playAllWords = false"
                />
            </div>
            <div v-if="!playAllWords">
                <div v-for="(word, idx) of data.words" :key="idx" class="m-1">
                    <information-panel-render-word-component :data="word" display="languageName" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RenderLanguageInformationPlayComponent from "./RenderLanguageInformationPlay.component.vue";
import InformationPanelRenderWordComponent from "./InformationPanelRenderWord.component.vue";
import PlayAllWordsComponent from "./PlayAllWords.component.vue";

export default {
    components: {
        RenderLanguageInformationPlayComponent,
        InformationPanelRenderWordComponent,
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
        data: function () {
            return this.$store.getters.getSelectionData();
        },
    },
    methods: {
        back() {
            this.$store.commit("setSelectionToDisplay", {
                type: undefined,
                data: undefined,
            });
        },
    },
};
</script>

<style lang="scss" scoped></style>
