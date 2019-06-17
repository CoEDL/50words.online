<template>
    <div>
        <div class="style-logo-text-background"></div>
        <a
            href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
        >
            <div class="style-logo-container">
                <img :src="logo" class="style-logo">
            </div>
            <div class="style-logo-text">
                RESEARCH UNIT FOR
                <br>INDIGENOUS LANGUAGE
            </div>
        </a>
        <div class="style-firstlang-logo-container">
            <a href="https://www.firstlanguages.org.au" target="_blank">
                <img :src="firstLangLogo" class="style-logo">
            </a>
        </div>
        <div class="style-uom-logo-container">
            <a href="https://www.unimelb.edu.au" target="_blank">
                <img :src="uomLogo" class="style-logo">
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
    position: relative;
    width: 70px;
}
.style-uom-logo-container {
    position: relative;
    top: calc(100vh - 210px);
    left: calc(100vw - 138px);
    width: 80px;
}

.style-firstlang-logo-container {
    position: relative;
    top: calc(100vh - 210px);
    left: calc(100vw - 138px);
    width: 80px;
}

.style-logo {
    display: inline;
    width: 100%;
}

.style-logo-text-background {
    position: absolute;
    background-color: #191a1a;
    width: 280px;
    height: 48px;
    top: 0px;
    left: 0px;
}

.style-logo-text {
    position: absolute;
    font-family: times, serif;
    top: 0px;
    width: 210px;
    left: 80px;
    font-size: 1.2em;
    color: white;
}
@media (min-width: 768px) {
    .style-uom-logo-container {
        position: relative;
        top: calc(100vh - 190px);
        left: calc(100vw - 140px);
        width: 80px;
    }
    .style-firstlang-logo-container {
        position: relative;
        top: calc(100vh - 190px);
        left: calc(100vw - 140px);
        width: 80px;
    }
}
@media (min-width: 1024px) {
    .style-logo-container {
        position: relative;
        width: 100px;
    }

    .style-logo {
        display: inline;
        width: 100%;
    }

    .style-logo-text-background {
        position: absolute;
        background-color: #191a1a;
        width: 420px;
        height: 75px;
        top: 0px;
        left: 0px;
        opacity: 0.5;
    }

    .style-logo-text {
        position: absolute;
        font-family: times, serif;
        width: 310px;
        top: 0px;
        left: 110px;
        font-size: 1.8em;
        color: white;
    }
    .style-uom-logo-container {
        position: relative;
        top: calc(100vh - 269px);
        left: calc(100vw - 182px);
        width: 120px;
    }
    .style-firstlang-logo-container {
        position: relative;
        top: calc(100vh - 150px);
        left: calc(100vw - 304px);
        width: 120px;
    }
}
</style>


