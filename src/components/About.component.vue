<template>
    <div class="flex flex-col space-y-4 lg:text-lg break-normal text-justify">
        <div class="bg-blue-100 p-2 flex flex-col space-y-2">
            <div class="flex flex-row space-x-4 items-center">
                <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"
                    ><img
                        class="w-96"
                        alt="Creative Commons License"
                        src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png"
                /></a>
                <div>
                    The material in this site is made available under a Creative Commons BY-NC
                    licence. The words provided on this site are not to be used for commercial
                    purposes. The permission and guidance of local communities should always be
                    sought before using Aboriginal languages.
                </div>
            </div>
        </div>
        <p>
            This project from the
            <a
                class="style-link"
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                target="_blank"
            >
                Research Unit for Indigenous Language</a
            >
            aims to provide fifty words in Indigenous languages of Australia The map is intended to
            be a useful resource for schools and educational organisations to learn 50 words in
            their local languages, and for the general public to discover the diversity of languages
            around Australia. For the best experience, the map should be viewed on a computer or
            tablet.
        </p>
        <p>
            We are continually adding words in new languages, and are asking for speakers of any
            language that is not already represented to contact us (<a
                class="style-link"
                href="mailto:ruil-contact@unimelb.edu.au"
                >RUIL-contact@unimelb.edu.au</a
            >) and we will help get their recordings on the map.
        </p>
        <p>
            Note that there is not always a one-to-one correspondence between words in English and
            the Aboriginal language. For example, ‘brother’ in English corresponds to two words in
            Wik-Mungkan, older brother and younger brother, so we have included just one: “wuny”
            older brother.
        </p>
        <p>
            All words, audio, and video recordings are provided by language speakers and are
            included here with permission. Australian Indigenous languages have many thousands of
            words but we are displaying just some on this site, with audio.
        </p>
        <p>
            The 50 Words Project is led by the Research Unit for Indigenous Language at the
            University of Melbourne, and funded by the Duncan Leary Trust for Australian Indigenous
            Languages.
        </p>
        <p class="text-sm">
            This research project has been approved by the Human Research Ethics Committee of the
            University of Melbourne. Project number: 2024-28141-49151-4
        </p>
        <p>
            <a
                class="style-link text-blue-600"
                href="https://arts.unimelb.edu.au/research-unit-for-indigenous-language/research/current-research-projects/50-words-project"
                target="_blank"
                >For more information see our project website.</a
            >
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
