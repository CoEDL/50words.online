<template>
    <div>
        <div
            class="style-panel style-collapsed-panel"
            :class="{'style-collapsed-panel': isCollapsed, 'style-open-panel': !isCollapsed}"
        >
            <div class="row">
                <div class="col">
                    <el-button type="text" class="px-2 style-button" @click="toggleCollapse">
                        <span v-show="isCollapsed">
                            <i class="fal fa-info-circle fa-2x"></i>
                        </span>
                        <span v-show="!isCollapsed" class="px-2">
                            <i class="fal fa-arrow-left fa-2x"></i>
                        </span>
                    </el-button>
                </div>
            </div>

            <div class="px-4 style-content-section" v-if="showContent">
                <div class="row">
                    <div class="col">
                        <a
                            href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                        >
                            <img :src="logo" class="style-logo py-2" />
                        </a>
                    </div>
                </div>
                <div class="row">
                    <div class="col text-center">
                        <h1 class="style-heading">50 Words</h1>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12 style-more-information text-justify">
                        <p>
                            This project aims to provide fifty words in every Indigenous language of Australia.
                            We hope that this will be a useful resource for schools and educational organisations to
                            learn 50 words in their local languages, and for the general public to discover the diversity of
                            languages around Australia.
                        </p>
                        <p>
                            All words, audio and video recordings are provided by
                            language speakers and are included here with permission. Australian Indigenous languages
                            have many thousands of words but we are displaying just some on this site, with audio or video.
                            Once you select a language (in orange) on this page you will get a link to "See more
                            information about" that language.
                        </p>
                        <p class="text-center">
                            <router-link to="/about">find out more about this site</router-link>
                        </p>
                    </div>
                </div>
                <span v-if="!showLanguageData">
                    <div class="row">
                        <div class="col">
                            <word-list-component
                                v-on:collapse-information-panel="collapseInformationPanel"
                            />
                        </div>
                    </div>
                </span>
                <span v-else>
                    <render-language-information :data="languageData" />
                </span>
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
        WordListComponent
    },
    data() {
        return {
            watchers: {},
            isCollapsed: true,
            showContent: false,
            showLanguageData: false,
            languageData: {},
            logo: require("src/assets/logo.png")
        };
    },
    computed: {
        selectedLanguage: function() {
            if (!this.$store.state.selectedLanguage)
                this.showLanguageData = false;
            return this.$store.state.selectedLanguage;
        }
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
                        code: this.selectedLanguage.code
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
        }
    }
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
    background-color: $primary-color;
    transition: 0.3s;
}

.style-collapsed-panel {
    width: 50px;
    transition-timing-function: ease-out;
}

.style-open-panel {
    width: 100vw;
}
@media only screen and (min-width: 600px) {
    .style-open-panel {
        width: calc(100vw * 0.5);
        max-width: 500px;
        transition-timing-function: ease-in;
    }
}
.style-content-section {
    height: calc(100vh - 100px);
    overflow: scroll;
}

.style-logo {
    width: 100%;
}

.style-button {
    color: #000;
}

.style-more-information {
    padding: 15px;
    font-size: 1.2em;
}

.style-link {
    color: $text-color;
}
</style>


