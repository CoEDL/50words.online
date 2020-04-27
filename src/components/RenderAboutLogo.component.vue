<template>
    <div class="flex flex-row justify-around my-4">
        <div class="flex flex-row">
            <a
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
            >
                <div class="inline-block">
                    <img
                        :src="logo"
                        class="inline-block h-10 md:h-20"
                        alt="Research Unit for Indigenous Languages, Aboriginal Languages, Australian Languages"
                    />
                </div>
                <div class="text-white style-logo-text">
                    RESEARCH UNIT FOR
                    <br />INDIGENOUS LANGUAGE
                </div>
            </a>
        </div>
        <div>
            <a href="https://www.firstlanguages.org.au" target="_blank">
                <img
                    :src="firstLangLogo"
                    class="inline-block h-10 md:h-20"
                    alt="First Languages Australia, First Nations Languages"
                />
            </a>
        </div>
        <div>
            <a href="https://www.unimelb.edu.au" target="_blank">
                <img :src="uomLogo" class="inline-block h-10 md:h-20" />
            </a>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            logo: require("src/assets/logo-image.png"),
            uomLogo: require("src/assets/UOMLogo.jpg"),
            firstLangLogo: require("src/assets/firstlanguages.png"),
        };
    },
};
</script>

<style lang="scss" scoped>
.style-logo-text {
    display: inline-block;
    font-family: times, serif;
    font-size: 0.5em;
}

.style-logo {
    display: inline-block;
    height: 40px;
}
@media (min-width: 768px) {
    .style-logo {
        display: inline-block;
        height: 50px;
    }
    .style-logo-text {
        margin-width: 300px;
        font-size: 1.1em;
    }
}
@media (min-width: 1024px) {
    .style-logo {
        display: inline-block;
        height: 100px;
    }
    .style-logo-text {
        width: 300px;
        font-size: 1.4em;
    }
}
</style>
