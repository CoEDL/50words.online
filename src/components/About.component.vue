<template>
    <div class="flex flex-col space-y-4 lg:text-lg break-normal text-justify">
        <p>
            This project from the
            <a
                class="style-link"
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                target="_blank"
            >
                Research Unit for Indigenous Language</a
            >
            aims to provide fifty words in Indigenous languages of Australia The
            map is intended to be a useful resource for schools and educational
            organisations to learn 50 words in their local languages, and for
            the general public to discover the diversity of languages around
            Australia. For the best experience, the map should be viewed on a
            computer or tablet.
        </p>
        <p>
            We are continually adding words in new languages, and are asking for
            speakers of any language that is not already represented to contact
            us (<a class="style-link" href="mailto:ruil-contact@unimelb.edu.au"
                >RUIL-contact@unimelb.edu.au</a
            >) and we will help get their recordings on the map.
        </p>
        <p>
            All words, audio, and video recordings are provided by language
            speakers and are included here with permission. Australian
            Indigenous languages have many thousands of words but we are
            displaying just some on this site, with audio or video.
        </p>
        <p>
            The 50 Words Project is led by the Research Unit for Indigenous
            Language at the University of Melbourne, and funded by the Duncan
            Leary Trust for Australian Indigenous Languages.
        </p>
        <p>
            This research project has been approved by the Human Research Ethics
            Committee of the University of Melbourne. Project number: 1853186.1
        </p>
        <p>
            For more information see our

            <a
                class="style-link"
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                target="_blank"
                >project website</a
            >.
        </p>
        <render-about-logo-component />
    </div>
</template>

<script>
import RenderAboutLogoComponent from "components/RenderAboutLogo.component.vue";
export default {
    components: {
        RenderAboutLogoComponent,
    },
    data() {
        return {
            view50words: require("src/assets/view50words.png"),
        };
    },
};
</script>
