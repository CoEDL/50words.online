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

            <div class="px-3" v-if="showContent">
                <div class="row">
                    <div class="col">
                        <h1 class="style-heading">50 Words</h1>
                    </div>
                </div>
                <span v-if="!showLanguageData">
                    <div class="row">
                        <div class="col">more information to come...</div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <word-list-component/>
                        </div>
                    </div>
                </span>
                <span v-if="showLanguageData">
                    <render-language-information :data="languageData"/>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
import RenderLanguageInformation from "./RenderLanguageInformation.component.vue";
import WordListComponent from "./WordList.component.vue";
import { loadLanguageData } from "../data-loader.service.js";

export default {
    components: {
        RenderLanguageInformation,
        WordListComponent
    },
    data() {
        return {
            isCollapsed: true,
            showContent: false,
            showLanguageData: false,
            languageData: {}
        };
    },
    computed: {
        selectedLanguage: function() {
            if (!this.$store.state.selectedLanguage)
                this.showLanguageData = false;
            return this.$store.state.selectedLanguage;
        }
    },
    watch: {
        selectedLanguage: async function() {
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
    overflow-y: scroll;
    overflow-x: hidden;
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

.style-button {
    color: #000;
}
</style>


