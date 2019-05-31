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
                        v-if="data.language.audio_file"
                    >
                        <i class="fas fa-volume-up fa-2x"></i>
                    </el-button>
                    <audio
                        ref="languageAudioElement"
                        v-if="data.language.audio_file"
                    >
                        <source :src="data.language.audio_file" />
                        Your browser does not support the
                        <code>audio</code> element.
                    </audio>
                    <el-button
                        type="text"
                        class="style-button"
                        circle
                        @click="reset"
                    >
                        <i class="fas fa-times fa-2x"></i>
                    </el-button>
                </h2>
            </div>
        </div>
        <div class="row">
            <div class="col style-speaker" v-if="data.speaker">
                Speaker(s): {{ data.speaker.name }}
                <el-button
                    type="text"
                    class="style-button px-3"
                    @click="playSpeaker"
                    v-if="data.speaker.audio_file"
                >
                    <i class="fas fa-volume-up fa-2x"></i>
                </el-button>
                <audio ref="speakerAudioElement" v-if="data.speaker.audio_file">
                    <source :src="data.speaker.audio_file" />
                    Your browser does not support the
                    <code>audio</code> element.
                </audio>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col style-speaker" v-if="data.thankyou">
                Thanks also to {{ data.thankyou }}
            </div>
        </div>
        <span v-for="(word, idx) of data.words" :key="idx">
            <render-word-component :word="word" v-if="word.indigenous" />
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
        return {};
    },
    mounted() {
        // console.log(JSON.stringify(this.data, null, 2));
    },
    methods: {
        playWord() {
            setTimeout(() => {
                this.$refs["audioElement"].play();
            }, 500);
        },
        reset() {
            this.$store.commit("setSelectedLanguage", undefined);
        },
        playSpeaker() {
            setTimeout(() => {
                this.$refs.speakerAudioElement.play();
            }, 500);
        },
        playLanguage() {
            setTimeout(() => {
                this.$refs.languageAudioElement.play();
            }, 500);
        }
    }
};
</script>

<style lang="scss" scoped>
.style-speaker {
    font-size: 1.5em;
}
</style>
