<template>
    <div class="flex flex-col">
        <div class="text-sm text-gray-600">View by</div>
        <el-tabs v-model="activeTab" @tab-click="handleTabSelect">
            <el-tab-pane label="" name="language">
                <span
                    slot="label"
                    :class="{
                        'text-black border-b-4 border-black pb-2': activeTab === 'language',
                        'text-gray-600': activeTab !== 'language',
                    }"
                    >LANGUAGE</span
                >
                <div v-if="activeTab === 'language'">
                    <information-panel-language-list-component v-if="show === 'list'" />
                    <information-panel-view-language-component v-if="show === 'language'" />
                </div>
            </el-tab-pane>
            <el-tab-pane label="" name="word">
                <span
                    slot="label"
                    :class="{
                        'text-black  border-b-4 border-black pb-2 ': activeTab === 'word',
                        'text-gray-600': activeTab !== 'word',
                    }"
                    >WORD</span
                >
                <div v-if="activeTab === 'word'">
                    <information-panel-word-list-component v-if="show === 'list'" />
                    <information-panel-view-word-component v-if="show === 'word'" />
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import InformationPanelLanguageListComponent from "./InformationPanelLanguageList.component.vue";
import InformationPanelViewLanguageComponent from "./InformationPanelViewLanguage.component.vue";
import InformationPanelWordListComponent from "./InformationPanelWordList.component.vue";
import InformationPanelViewWordComponent from "./InformationPanelViewWord.component.vue";

export default {
    components: {
        InformationPanelLanguageListComponent,
        InformationPanelViewLanguageComponent,
        InformationPanelWordListComponent,
        InformationPanelViewWordComponent,
    },
    data() {
        return {
            activeTab: "language",
            show: "list",
            language: undefined,
        };
    },
    computed: {
        selection: function() {
            return this.$store.state.selection;
        },
    },
    watch: {
        selection: function() {
            this.show = this.$store.state.selection.type
                ? this.$store.state.selection.type
                : "list";
        },
    },
    methods: {
        handleTabSelect(tab) {
            this.$store.commit("setSelectionToDisplay", {
                type: undefined,
                data: undefined,
            });
            if (tab.$options.propsData.name === "language") {
                this.$store.commit("setLayer", "languages");
                this.show = "list";
            } else {
                this.$store.commit("setLayer", "words");
            }
        },
    },
};
</script>
