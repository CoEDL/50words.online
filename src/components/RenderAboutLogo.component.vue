<template>
    <div class="row text-xl-center">
        <div class="col-12 py-2 col-md-6 col-xl-5">
            <a
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
            >
                <div class="style-logo-container">
                    <img :src="logo" class="style-logo" />
                </div>
                <div class="py-2 style-logo-text text-left">
                    RESEARCH UNIT FOR
                    <br />INDIGENOUS LANGUAGE
                </div>
            </a>
        </div>
        <div class="col-12 py-2 col-md-4 col-xl-3 ">
            <a href="https://www.firstlanguages.org.au" target="_blank">
                <img :src="firstLangLogo" class="style-logo" />
            </a>
        </div>
        <div class="col-12 py-2 col-md-2 col-xl-3">
                <a href="https://www.unimelb.edu.au" target="_blank">
                    <img :src="uomLogo" class="style-logo" />
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
            firstLangLogo: require("src/assets/firstlanguages.png")
        };
    }
};
</script>

<style lang="scss" scoped>
.style-logo-container {
    position: absolute;
    display: inline-block;
    position: relative;
}

.style-logo-text {
    position: absolute;
    display: inline;
    font-family: times, serif;
    top: 0px;
    padding-left: 10px;
    font-size: 0.8em;
    color: white;
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
        width: 300px;
        font-size: 1.1em;
    }
}
@media (min-width: 1024px) {
    .style-logo {
        display: inline-block;
        height: 80px;
    }
    .style-logo-text {
        width: 300px;
        font-size: 1.4em;
    }
}
</style>


