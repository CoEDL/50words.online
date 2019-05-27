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
    </div>
</template>

<script>
export default {
    data() {
        return {
            logo: require("src/assets/logo-image.png")
        };
    }
};
</script>

<style lang="scss" scoped>
.style-logo-container {
    position: relative;
    width: 70px;
}

.style-logo {
    display: inline;
    width: 100%;
}

.style-logo-text-background {
    position: absolute;
    background-color: #191a1a;
    width: 290px;
    height: 48px;
    top: 0px;
    left: 0px;
}

.style-logo-text {
    position: absolute;
    font-family: times, serif;
    width: 500px;
    top: 0px;
    left: 80px;
    font-size: 1.2em;
    color: white;
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
        width: 500px;
        top: 0px;
        left: 110px;
        font-size: 1.8em;
        color: white;
    }
}
</style>


