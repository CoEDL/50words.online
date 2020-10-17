<template>
    <div class="flex flex-row h-16 py-4">
        <div class="flex-grow"></div>
        <div class="mx-4">
            <a
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                target="_blank"
            >
                <img :src="ruilLogo" class="h-10" />
            </a>
        </div>
        <div class="mx-4">
            <a href="https://www.firstlanguages.org.au" target="_blank">
                <img :src="firstLangLogo" class="h-10" />
            </a>
        </div>
        <div class="mx-4">
            <a href="https://www.dynamicsoflanguage.edu.au/" target="_blank">
                <img :src="coedlLogo" class="h-10" />
            </a>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            ruilLogo: require("src/assets/logo-ruil.png"),
            uomLogo: require("src/assets/logo-uom.jpg"),
            firstLangLogo: require("src/assets/logo-firstlanguages.png"),
            coedlLogo: require("src/assets/logo-coedl.png"),
        };
    },
    methods: {
        showHelp() {
            if (window.innerWidth < 768) {
                this.$router.push({ name: "help" });
            } else {
                this.showHelpDialog = true;
            }
        },
        showAbout() {
            console.log("show about");
        },
        showContribute() {
            console.log("show contribute");
        },
    },
};
</script>
