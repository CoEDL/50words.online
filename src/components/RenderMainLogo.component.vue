<template>
    <div>
        <div class="style-ruil-logo-container style-background mt-2">
            <a
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
            >
                <div class="flex flex-row">
                    <img
                        :src="logo"
                        class="my-auto h-8 md:h-16 lg:h-20"
                        alt="Research Unit for Indigenous Languages, Aboriginal Languages, Australian Languages"
                    />
                    <div
                        class="pl-1 style-logo-text text-xs md:text-xl lg:text-2xl text-white"
                    >
                        RESEARCH UNIT FOR
                        <br />INDIGENOUS LANGUAGE
                    </div>
                </div>
            </a>
        </div>
        <div class="hidden md:block style-firstlang-logo-container">
            <a href="https://www.firstlanguages.org.au" target="_blank">
                <img
                    :src="firstLangLogo"
                    alt="First Languages Australia, First Nations Languages"
                />
            </a>
        </div>
        <div class="hidden md:block style-uom-logo-container">
            <a href="https://www.unimelb.edu.au" target="_blank">
                <img :src="uomLogo" />
            </a>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        styleBackground: {
            type: Boolean,
        },
    },
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
.style-background {
    background-color: #191a1a;
}

.style-ruil-logo-container {
    position: fixed;
    left: 55px;
}

.style-logo-text {
    font-family: times, serif;
}
// @media (min-width: 768px) {
//     .style-uom-logo-container {
//         position: fixed;
//         top: calc(100vh - 180px);
//         left: calc(100vw - 90px);
//     }
//     .style-firstlang-logo-container {
//         position: fixed;
//         top: calc(100vh - 200px);
//         left: calc(100vw - 90px);
//     }
// }
@media (min-width: 768px) {
    .style-uom-logo-container {
        position: fixed;
        top: calc(100vh - 150px);
        left: calc(100vw - 130px);
        width: 120px;
    }
    .style-firstlang-logo-container {
        position: fixed;
        top: calc(100vh - 200px);
        left: calc(100vw - 130px);
        width: 118px;
    }
}
</style>
