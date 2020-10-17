<template>
    <div class="flex flex-row">
        <div class="flex flex-col">
            <div class="text-xl font-bold cursor-pointer" @click="home">
                50 WORDS PROJECT
            </div>
            <div class="text-sm text-gray-600">
                Hear 50 words in Australian Indigenous languages
            </div>
        </div>
        <div class="flex flex-grow"></div>
        <el-button
            type="text"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="playAll"
        >
            PLAY ALL
        </el-button>
        <el-button
            type="text"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="showHelp"
        >
            HELP
        </el-button>
        <el-button
            type="text"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="showAbout"
        >
            ABOUT
        </el-button>
        <el-button
            type="text"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="showContribute"
        >
            CONTRIBUTE
        </el-button>
        <div class="mx-2">
            <a href="https://www.unimelb.edu.au" target="_blank">
                <img :src="uomLogo" class="h-12" />
            </a>
        </div>
        <help-dialog-component
            class="hidden md:block"
            :show="showHelpDialog"
            @close="showHelpDialog = false"
        ></help-dialog-component>
        <about-dialog-component
            class="hidden md:block"
            :show="showAboutDialog"
            @close="showAboutDialog = false"
        ></about-dialog-component>
        <contribute-dialog-component
            class="hidden md:block"
            :show="showContributeDialog"
            @close="showContributeDialog = false"
        ></contribute-dialog-component>
    </div>
</template>

<script>
import HelpDialogComponent from "./DialogHelp.component.vue";
import AboutDialogComponent from "./DialogAbout.component.vue";
import ContributeDialogComponent from "./DialogContribute.component.vue";

export default {
    components: {
        HelpDialogComponent,
        AboutDialogComponent,
        ContributeDialogComponent,
    },
    data() {
        return {
            uomLogo: require("src/assets/logo-uom.jpg"),
            showHelpDialog: false,
            showAboutDialog: false,
            showContributeDialog: false,
        };
    },
    methods: {
        showHelp() {
            this.showHelpDialog = true;
        },
        showAbout() {
            this.showAboutDialog = true;
        },
        showContribute() {
            this.showContributeDialog = true;
        },
        playAll() {
            this.$router.push({ name: "playall" });
        },
        home() {
            this.$router.push({ name: "home" });
        },
    },
};
</script>
