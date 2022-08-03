<template>
    <div class="flex flex-col">
        <div class="flex flex-row justify-between">
            <el-button
                :link="true"
                class="text-gray-600"
                @click="home"
                v-if="$route.name !== 'home'"
            >
                <i class="fas fa-home"></i>
            </el-button>
            <span v-if="!$store.state.iOS">
                <el-button
                    :link="true"
                    class="text-gray-600 hover:text-highlight-dark"
                    :class="{
                        'text-highlight-dark': $route.name === 'playall',
                    }"
                    @click="playAll"
                >
                    PLAY ALL
                </el-button>
            </span>
            <el-button
                :link="true"
                class="text-gray-600 hover:text-highlight-dark"
                :class="{
                    'text-highlight-dark': $route.name === 'about',
                }"
                @click="showAbout"
            >
                ABOUT
            </el-button>
            <el-button
                :link="true"
                class="text-gray-600 hover:text-highlight-dark"
                :class="{
                    'text-highlight-dark': $route.name === 'contribute',
                }"
                @click="showContribute"
            >
                CONTRIBUTE
            </el-button>
            <!-- <div class="flex flex-grow"></div> -->
            <el-button
                :link="true"
                class="text-gray-600 hover:text-highlight-dark"
                :class="{
                    'text-highlight-dark': $route.name === 'help',
                }"
                @click="showHelp"
            >
                HELP
            </el-button>
        </div>
        <div class="flex flex-col cursor-pointer" @click="unsetSelection">
            <div class="text-lg font-bold text-highlight-dark">50 WORDS PROJECT</div>
            <div class="text-sm text-gray-700">
                Hear 50 words in Australian Indigenous languages
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            uomLogo: require("src/assets/logo-uom.jpg"),
            showHelpDialog: false,
            showAboutDialog: false,
            showContributeDialog: false,
        };
    },
    methods: {
        home() {
            this.$router.push({ name: "home" }).catch(() => {});
        },
        showHelp() {
            this.$router.push({ name: "help" }).catch(() => {});
        },
        showAbout() {
            this.$router.push({ name: "about" }).catch(() => {});
        },
        showContribute() {
            this.$router.push({ name: "contribute" }).catch(() => {});
        },
        playAll() {
            this.$router.push({ name: "playall" });
        },
        unsetSelection() {
            this.$store.commit("setSelectionToDisplay", {
                type: undefined,
                data: undefined,
            });
            this.$router.push({ name: "home" }).catch(() => {});
        },
    },
};
</script>
