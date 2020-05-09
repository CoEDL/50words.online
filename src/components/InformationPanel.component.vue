<template>
    <div>
        <div
            class="style-panel flex flex-col pt-2 md:pt-1"
            :class="{
                'style-collapsed-panel': isCollapsed,
                'w-full style-open-panel': !isCollapsed,
            }"
        >
            <div class="flex flex-row mb-4">
                <div class="lg:pt-2">
                    <div
                        type="text"
                        class="text-white pl-3 mt-2"
                        @click="toggleCollapse"
                    >
                        <span v-show="isCollapsed">
                            <i class="fal fa-info-circle fa-2x"></i>
                        </span>
                        <span v-show="!isCollapsed">
                            <i class="fal fa-arrow-left fa-2x"></i>
                        </span>
                    </div>
                </div>

                <div class="" v-if="showContent">
                    <a
                        href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                    >
                        <img :src="logo" class="h-16 lg:pt-2" />
                    </a>
                </div>
            </div>
            <div
                class="flex flex-col mx-4 style-content-section"
                v-if="showContent"
            >
                <div class="text-3xl text-center">50 Words</div>

                <p class="my-2">
                    This project aims to provide fifty words in every Indigenous
                    language of Australia. We hope that this will be a useful
                    resource for schools and educational organisations to learn
                    50 words in their local languages, and for the general
                    public to discover the diversity of languages around
                    Australia.
                </p>
                <p class="my-2">
                    We are continually adding new languages, and are asking for
                    speakers of any language that is not already represented to
                    contact us
                    <a href="mailto:RUIL-contact@unimelb.edu.au"
                        >RUIL-contact@unimelb.edu.au</a
                    >
                    and we will help get their recordings on the map.
                </p>
                <p class="my-2">
                    All words, audio and video recordings are provided by
                    language speakers and are included here with permission.
                    Australian Indigenous languages have many thousands of words
                    but we are displaying just some on this site, with audio or
                    video. Once you select a language (in orange) on this page
                    you will get a link to "See more information about" that
                    language.
                </p>
                <p class="text-center my-2 text-xl">
                    <router-link to="/about" class="hover:text-orange-200"
                        >find out more about this site</router-link
                    >
                </p>
                <word-list-component
                    v-if="!showLanguageData"
                    v-on:collapse-information-panel="collapseInformationPanel"
                />
                <render-language-information :data="languageData" v-else />
            </div>
        </div>
    </div>
</template>

<script>
import RenderLanguageInformation from "./RenderLanguageInformation.component.vue";
import WordListComponent from "./WordList.component.vue";
import { loadLanguageData } from "src/data-loader.service.js";

export default {
    components: {
        RenderLanguageInformation,
        WordListComponent,
    },
    data() {
        return {
            watchers: {},
            isCollapsed: true,
            showContent: false,
            showLanguageData: false,
            languageData: {},
            logo: require("src/assets/logo.png"),
        };
    },
    computed: {
        selectedLanguage: function() {
            if (!this.$store.state.selectedLanguage)
                this.showLanguageData = false;
            return this.$store.state.selectedLanguage;
        },
    },
    mounted() {
        this.watchers.selectedLanguage = this.$watch(
            "selectedLanguage",
            async () => {
                this.showLanguageData = this.selectedLanguage ? true : false;
                if (this.selectedLanguage && this.selectedLanguage.code) {
                    this.isCollapsed = false;
                    setTimeout(() => {
                        this.showContent = true;
                    }, 400);
                    this.languageData = await loadLanguageData({
                        code: this.selectedLanguage.code,
                    });
                }
            }
        );
    },
    beforeDestroy() {
        this.watchers.selectedLanguage();
    },
    methods: {
        toggleCollapse() {
            if (this.isCollapsed) {
                setTimeout(() => {
                    this.$store.commit("unsetSelectedLanguage");
                    this.showContent = true;
                }, 400);
            } else {
                this.showContent = false;
                this.$store.commit("setSelectedLanguage", undefined);
            }
            this.isCollapsed = !this.isCollapsed;
        },
        collapseInformationPanel() {
            if (window.innerWidth < 768) {
                this.isCollapsed = true;
                this.showContent = false;
            }
        },
    },
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";
.style-panel {
    position: fixed;
    z-index: 2;
    top: 0;
    left: 0;
    height: 100vh;
    transition: 0.3s;
}

.style-collapsed-panel {
    width: 50px;
    transition-timing-function: ease-out;
}

.style-open-panel {
    background-color: $primary-color;
}

@media only screen and (min-width: 768px) {
    .style-open-panel {
        width: calc(100vw * 0.5);
        transition-timing-function: ease-in;
    }
}
.style-content-section {
    height: calc(100vh - 110px);
    overflow: scroll;
}
</style>
