<template>
    <div class="flex flex-row">
        <div class="flex flex-col">
            <div class="text-xl font-bold cursor-pointer" @click="home">50 WORDS PROJECT</div>
            <div class="text-sm text-gray-600">
                Hear 50 words in Australian Indigenous languages
            </div>
        </div>
        <div class="flex flex-grow"></div>
        <el-button
            :link="true"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="playAll"
        >
            PLAY ALL
        </el-button>
        <el-button
            :link="true"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="showHelp"
        >
            HELP
        </el-button>
        <el-button
            :link="true"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="showAbout"
        >
            ABOUT
        </el-button>
        <el-button
            :link="true"
            class="text-gray-600 mx-2 text-lg -mt-1 cursor-pointer hover:text-highlight-dark"
            @click="showContribute"
        >
            CONTRIBUTE
        </el-button>
        <div class="mx-2">
            <a href="https://www.unimelb.edu.au" target="_blank">
                <img :src="data.uomLogo" class="h-12" />
            </a>
        </div>
        <el-dialog v-model="data.showHelpDialog" title="Help" width="80%">
            <help-component v-if="data.showHelpDialog" />
        </el-dialog>
        <el-dialog v-model="data.showAboutDialog" ref="modal" title="About" width="80%">
            <about-component />
        </el-dialog>
        <el-dialog v-model="data.showContributeDialog" ref="modal" title="Contribute">
            <contribute-component />
        </el-dialog>
    </div>
</template>

<script setup>
import HelpComponent from "./Help.component.vue";
import AboutComponent from "./About.component.vue";
import ContributeComponent from "./Contribute.component.vue";
import { reactive } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const data = reactive({
    uomLogo: require("src/assets/logo-uom.jpg"),
    showHelpDialog: false,
    showAboutDialog: false,
    showContributeDialog: false,
    aboutDialogHeight: `${window.innerHeight * 0.7}px`,
});
function showHelp() {
    data.showHelpDialog = true;
}
function showAbout() {
    data.showAboutDialog = true;
}
function showContribute() {
    data.showContributeDialog = true;
}
function playAll() {
    router.push({ name: "playall" });
}
function home() {
    router.push({ name: "languages" });
}
</script>
