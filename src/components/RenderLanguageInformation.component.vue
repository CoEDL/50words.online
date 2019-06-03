<template>
    <div>
        <div class="row">
            <div class="col" v-if="data.language">
                <h2 class="style-heading">
                    {{ data.language.name }}
                    <el-button
                        type="text"
                        class="style-button px-3"
                        @click="playLanguage"
                        v-if="data.language.audio_file.length"
                    >
                        <i class="fas fa-volume-up fa-2x"></i>
                    </el-button>
                    <audio ref="languageAudioElement" v-if="data.language.audio_file.length">
                        <source
                            :src="file"
                            v-for="(file, idx) of data.language.audio_file"
                            :key="idx"
                        >Your browser does not support the
                        <code>audio</code> element.
                    </audio>
                    <el-button type="text" class="style-button" circle @click="reset">
                        <i class="fas fa-times fa-2x"></i>
                    </el-button>
                </h2>
            </div>
        </div>
        <div class="row my-3">
            <div class="col">
                See more information about {{data.language.name}} here:
                <a
                    :href="aiatsisLink"
                    target="_blank"
                >https://collection.aiatsis.gov.au/austlang/language/{{data.code}}</a>
            </div>
        </div>
        <div class="row">
            <div class="col style-speaker" v-if="data.speaker">
                Speaker(s): {{ data.speaker.name }}
                <el-button
                    type="text"
                    class="style-button px-3"
                    @click="playSpeaker"
                    v-if="data.speaker.audio_file.length"
                >
                    <i class="fas fa-volume-up fa-2x"></i>
                </el-button>
                <audio ref="speakerAudioElement" v-if="data.speaker.audio_file.length">
                    <source :src="file" v-for="(file, idx) of data.speaker.audio_file" :key="idx">Your browser does not support the
                    <code>audio</code> element.
                </audio>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col style-speaker" v-if="data.thankyou">Thanks also to {{ data.thankyou }}</div>
        </div>
        <span v-for="(word, idx) of data.words" :key="idx">
            <render-word-component :word="word" v-if="word.indigenous"/>
        </span>
    </div>
</template>

<script>
import RenderWordComponent from "./RenderWord.component.vue";
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
            return `https://collection.aiatsis.gov.au/austlang/language/${
                this.data.code
            }`;
        }
    },
    mounted() {
        // console.log(JSON.stringify(this.data, null, 2));
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
