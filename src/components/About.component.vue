<template>
    <div class="page-style">
        <div class="row">
            <div class="col">
                <router-link to="/">
                    <i class="fas fa-arrow-left"></i>&nbsp;back to site
                </router-link>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col style-heading text-center">About 50 words</div>
        </div>
        <div class="text-center my-2">
            <img :src="view50words" class="style-screenshot" />
        </div>
        <!-- <div class="row">
            <div class="col">
                <render-about-logo-component />
            </div>
        </div>-->
        <div class="row style-content-container">
            <div class="col text-justify">
                <p class="my-4">
                    The words included here are just a small sample to give an idea of what
                    Australian languages sound like. In some languages, words are more specific, for example,
                    you have to say if a grey kangaroo is male or female in Murrinhpatha, so we have included
                    only the word for the male grey kangaroo in that list. In some languages, the word for
                    'thigh' is the same as the word for 'leg' so they are both shown in those lists.
                </p>
                <p class="my-4">
                    When you listen to these words you will notice that Australian languages have many
                    sounds that are not found in English, and these can be tricky for English speakers to pronounce.
                    For an explanation of these sounds, and help in pronouncing them we recommend you watch the
                    short video series we put online at the
                    <a
                        class="style-link"
                        href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/training/australian-indigenous-languages/sounds-of-aboriginal-languages"
                        target="_blank"
                    >RUIL website.</a>
                </p>
                <p class="my-4">
                    For more information about Australian Indigenous languages, see our pages
                    <a
                        class="style-link"
                        href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/training/australian-indigenous-languages"
                        target="_blank"
                    >here</a>
                    and also
                    <a
                        class="style-link"
                        href="https://www.firstlanguages.org.au"
                        target="_blank"
                    >First Languages Australia</a> or
                    <a
                        class="style-link"
                        href="https://collection.aiatsis.gov.au/austlang/search"
                        target="_blank"
                    >Austlang</a>.
                </p>
                <p class="my-4">
                    The 50-word project is led by the Research Unit for Indigenous Language at the University of
                    Melbourne, funded by the Duncan Leary Trust for Australian Indigenous Languages.
                    For further information see:
                    <a
                        class="style-link"
                        href="http://indiglang.arts.unimelb.edu.au"
                        target="_blank"
                    >http://indiglang.arts.unimelb.edu.au</a>
                </p>
                <p class="my-4">
                    Words are added to the 50 words site as we receive them, and we are asking for
                    speakers of any language that is not already represented to contact us
                    (RUIL-contact @ unimelb.edu.au) and we will help get their recordings into the site.
                    We will send out the word list, instructions, and a consent form, so that speakers
                    can give their permission for the words to be used here.
                </p>

                <p class="my-4">
                    This project is led by
                    <a
                        href="https://www.findanexpert.unimelb.edu.au/display/person14513"
                        target="_blank"
                    >Professor Rachel Nordlinger</a>
                    and
                    <a
                        href="https://www.findanexpert.unimelb.edu.au/display/person18278"
                        target="_blank"
                    >Associate Professor Nick Thieberger</a>
                    in the Research Unit
                    for Indigenous Language at the University of Melbourne with
                    Katie Jepson and Allyra Murray. Site design and development was by
                    <a
                        href="https://www.linkedin.com/in/marcolarosa/"
                        target="_blank"
                    >Dr Marco La Rosa</a>
                    and the code is available @
                    <a
                        href="https://github.com/CoEDL/50words.online"
                        target="_blank"
                    >https://github.com/CoEDL/50words.online</a>.
                    You will find instructions there for reusing the code if you want to build a
                    similar project with different geography.
                </p>

                <p class="my-4">
                    The map uses information from
                    <a
                        href="https://www.firstlanguages.org.au/"
                        target="_blank"
                    >Austlang (AIATSIS)</a> and from
                    <a href="https://gambay.com.au/" target="_blank">Gambay</a>
                    produced by First Languages Australia.
                </p>

                <p class="my-4">
                    This research project has been approved by the Human Research Ethics
                    Committee of The University of Melbourne. Project number:1853186.2
                </p>
            </div>
        </div>
        <render-about-logo-component />
    </div>
</template>

<script>
import RenderAboutLogoComponent from "components/RenderAboutLogo.component.vue";
export default {
    components: {
        RenderAboutLogoComponent
    },
    data() {
        return {
            view50words: require("src/assets/view50words.png")
        };
    }
};
</script>

<style lang="scss" scoped>
@import "assets/variables.scss";

.page-style {
    padding: 15px;
    font-size: 1.2em;
}

.style-link {
    color: $text-color;
}

.style-heading {
    font-size: 30px;
}

.style-screenshot {
    max-width: 80vw;
    max-height: 500px;
}
.style-content-container {
    font-size: 16px;
    padding: 5px;
}
@media (min-width: 768px) {
    .style-content-container {
        padding: 10px;
    }
}
@media (min-width: 1024px) {
    .style-content-container {
        padding: 20px;
    }
}
</style>