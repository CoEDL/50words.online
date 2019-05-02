<template>
    <div>
        <div
            class="style-panel style-collapsed-panel"
            :class="{'style-collapsed-panel': isCollapsed, 'style-open-panel': !isCollapsed}"
        >
            <div class="row">
                <div class="col">
                    <el-button type="text" circle class="style-button" @click="toggleCollapse">
                        <i class="fal fa-info-circle fa-2x"></i>
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
import { loadLanguageData } from "../data-loader.service.js";

export default {
    components: {
        RenderLanguageInformation
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
                    this.showContent = true;
                }, 400);
            } else {
                this.showContent = false;
            }
            this.isCollapsed = !this.isCollapsed;
        }
    }
};
</script>

<style lang="scss" scoped>
.style-panel {
    position: fixed;
    z-index: 2;
    top: 0;
    left: 0;
    height: 100vh;
    background-color: #049372;
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
        transition-timing-function: ease-in;
    }
}

.style-button {
    color: #000;
}
</style>


