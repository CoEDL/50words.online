<template>
    <div>
        <div
            class="flex flex-col lg:flex-row items-center space-y-4 lg:space-y-0 lg:space-x-8"
        >
            <div class="">
                <a href="https://www.unimelb.edu.au" target="_blank">
                    <img :src="uomLogo" class="object-contain h-16" />
                </a>
            </div>
            <div class="">
                <a
                    href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                >
                    <div class="inline-block">
                        <img
                            :src="ruilLogo"
                            class="object-contain h-16"
                            alt="Research Unit for Indigenous Languages, Aboriginal Languages, Australian Languages"
                        />
                    </div>
                </a>
            </div>
            <div class="">
                <a
                    href="https://www.dynamicsoflanguage.edu.au/"
                    target="_blank"
                >
                    <img :src="coedlLogo" class="object-contain h-16" />
                </a>
            </div>
            <div class="">
                <a href="https://www.firstlanguages.org.au" target="_blank">
                    <img
                        :src="firstLangLogo"
                        alt="First Languages Australia, First Nations Languages"
                        class="object-contain h-16"
                    />
                </a>
            </div>
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
};
</script>
