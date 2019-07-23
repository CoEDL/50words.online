<template>
    <div>
        <div class="row">
            <div class="col" v-if="data.properties.language">
                <h2 class="style-heading">
                    {{ data.properties.language.name }}
                    <el-button
                        type="text"
                        class="style-button px-3 style-audio-control"
                        @click="playLanguage"
                        v-if="data.properties.language.audio_file.length"
                    >
                        <i class="fas fa-volume-up fa-2x"></i>
                    </el-button>
                    <audio
                        ref="languageAudioElement"
                        v-if="data.properties.language.audio_file.length"
                    >
                        <source
                            :src="file"
                            v-for="(file, idx) of data.properties.language.audio_file"
                            :key="idx"
                        />Your browser does not support the
                        <code>audio</code> element.
                    </audio>
                </h2>
            </div>
        </div>
        <div class="row my-3">
            <div class="col">
                <a
                    :href="aiatsisLink"
                    target="_blank"
                >See more information about {{data.properties.language.name}} here.</a>
            </div>
        </div>
        <div class="row">
            <div class="col style-speaker" v-if="data.properties.speaker">
                Speaker(s): {{ data.properties.speaker.name }}
                <el-button
                    type="text"
                    class="style-button px-3 style-audio-control"
                    @click="playSpeaker"
                    v-if="data.properties.speaker.audio_file.length"
                >
                    <i class="fas fa-volume-up fa-2x"></i>
                </el-button>
                <audio ref="speakerAudioElement" v-if="data.properties.speaker.audio_file.length">
                    <source
                        :src="file"
                        v-for="(file, idx) of data.properties.speaker.audio_file"
                        :key="idx"
                    />Your browser does not support the
                    <code>audio</code> element.
                </audio>
            </div>
        </div>
        <div class="row mt-3">
            <div
                class="col style-speaker"
                v-if="data.properties.thankyou"
            >Thanks also to: {{ data.properties.thankyou }}</div>
        </div>
        <div class="row my-3">
            <div class="col">Date received: {{dateReceived}}</div>
        </div>
        <span v-for="(word, idx) of data.properties.words" :key="idx">
            <render-word-component :word="word" v-if="word.indigenous" />
        </span>
    </div>
</template>

<script>
import RenderWordComponent from "./RenderWord.component.vue";
import moment from "moment";

export default {
    components: {
        RenderWordComponent
    },
    props: {
        data: Object
    },
    data() {
        return {
            watchers: {}
        };
    },
    computed: {
        aiatsisLink: function() {
            return `https://collection.aiatsis.gov.au/austlang/language/${this.data.properties.code}`;
        },
        dateReceived: function() {
            return moment(
                this.data.properties.date_received,
                "YYYYMMDD"
            ).format("LL");
        }
    },
    mounted() {
        // console.log(JSON.stringify(this.data, null, 2));
        this.watchers.language = this.$watch(
            "data.properties.language.audio_file",
            () => {
                if (this.$refs.languageAudioElement)
                    this.$refs.languageAudioElement.load();
            }
        );
        this.watchers.speaker = this.$watch(
            "data.properties.speaker.audio_file",
            () => {
                if (this.$refs.speakerAudioElement)
                    this.$refs.speakerAudioElement.load();
            }
        );
    },
    beforeDestroy() {
        this.watchers.language();
        this.watchers.speaker();
    },
    methods: {
        reset() {
            this.$store.commit("setSelectedLanguage", undefined);
        },
        playSpeaker() {
            setTimeout(() => {
                this.$refs.speakerAudioElement.play();
            }, 200);
        },
        playLanguage() {
            setTimeout(() => {
                this.$refs.languageAudioElement.play();
            }, 200);
        }
    }
};
</script>

<style lang="scss" scoped>
.style-speaker {
    font-size: 1.5em;
}
</style>
