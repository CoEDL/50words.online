<template>
    <div>
        <div class="pt-4 px-6 flex flex-col hidden md:flex">
            <header-component />
            <div class="flex flex-row">
                <information-panel-component class="mt-4 w-3/12" />
                <div class="flex flex-col w-full md:w-9/12 hidden md:flex">
                    <div class="flex-grow mt-2 ml-2 flex flex-col">
                        <map-component class="flex-grow" />
                    </div>

                    <footer-component class="hidden md:flex" />
                </div>
            </div>
        </div>
        <div class="flex flex-col md:hidden w-screen h-screen">
            <header-mobile-component class="px-2" />
            <div
                class="flex-grow flex flex-col justify-evenly my-2 px-2"
                v-if="!selection"
            >
                <mobile-select-language-component />
                <mobile-select-word-component />
                <mobile-search-for-word-language-component />
            </div>
            <div v-else class="mt-6 mb-2">
                <information-panel-view-language-component
                    v-if="layer === 'languages'"
                />
                <information-panel-view-word-component
                    v-if="layer === 'words'"
                />
            </div>
            <div class="relative">
                <map-component class="bottom-0 absolute" />
            </div>
        </div>
    </div>
</template>

<script>
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

export default {
    components: {
        MapComponent,
        HeaderComponent,
        InformationPanelComponent,
        FooterComponent,
        HeaderMobileComponent,
        MobileSelectLanguageComponent,
        MobileSelectWordComponent,
        MobileSearchForWordLanguageComponent,
        InformationPanelViewLanguageComponent,
        InformationPanelViewWordComponent,
    },
    data() {
        return {};
    },
    computed: {
        selection: function() {
            return this.$store.getters.getSelectionData();
        },
        layer: function() {
            return this.$store.state.layer;
        },
    },
    mounted() {
        this.$store.dispatch("loadData");
    },
};
</script>

<style scoped lang="scss"></style>
