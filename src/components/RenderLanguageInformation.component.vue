<template>
    <div class="flex flex-col">
        <div
            @click="displayWordList"
            class="style-button hover:text-orange-200 cursor-pointer my-2"
            type="text"
        >
            <i class="fas fa-arrow-left"></i>
            show word list
        </div>
        <div class="cursor-pointer my-4">
            <render-language-information-play-component
                class="flex-grow justify-center hover:text-orange-200"
                :data="data.properties.language"
            />
        </div>

        <div class="text-center my-2">
            <a :href="weblink" target="_blank" class="hover:text-orange-200"
                >See more information about
                {{ data.properties.language.name }} here.</a
            >
        </div>

        <render-language-information-play-component
            v-if="data.properties.speaker"
            class="hover:text-orange-200 my-2"
            :data="data.properties.speaker"
        />

        <div class="mt-8 md:mt-2" v-if="data.properties.thankyou">
            Thanks also to: {{ data.properties.thankyou }}
        </div>

        <div class="my-2">Date received: {{ dateReceived }}</div>

        <div class="flex flex-col">
            <div v-for="(word, idx) of data.properties.words" :key="idx">
                <render-word-component :word="word" v-if="word.indigenous" />
            </div>
        </div>
    </div>
</template>

<script>
import RenderWordComponent from "./RenderWord.component.vue";
import RenderLanguageInformationPlayComponent from "./RenderLanguageInformationPlay.component.vue";
import moment from "moment";

export default {
    components: {
        RenderWordComponent,
        RenderLanguageInformationPlayComponent,
    },
    props: {
        data: {
            type: Object,
        },
    },
    data() {
        return {
            loadingSpeakerAudio: false,
        };
    },
    computed: {
        weblink: function() {
            if (this.data.properties.weblink) {
                return this.data.properties.weblink;
            } else {
                return `https://collection.aiatsis.gov.au/austlang/language/${this.data.properties.code.trimRight(
                    "#"
                )}`;
            }
        },
        dateReceived: function() {
            return moment(
                this.data.properties.date_received,
                "YYYYMMDD"
            ).format("LL");
        },
    },
    methods: {
        displayWordList() {
            this.$store.commit("unsetSelectedLanguage");
        },
    },
};
</script>

<style lang="scss" scoped></style>
