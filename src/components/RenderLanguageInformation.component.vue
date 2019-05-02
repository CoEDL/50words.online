<template>
    <div>
        <div class="row">
            <div class="col">
                <h2 class="style-heading">
                    {{data.asciiName}}
                    <el-button type="text" class="style-button" circle @click="reset">
                        <i class="fas fa-times fa-2x"></i>
                    </el-button>
                </h2>
            </div>
        </div>
        <div v-for="(word, idx) of data.words" :key="idx">
            <render-word-component :word="word"/>
        </div>
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
    methods: {
        playWord() {
            setTimeout(() => {
                this.$refs["audioElement"].play();
            }, 500);
        },
        reset() {
            this.$store.commit("setSelectedLanguage", undefined);
        }
    }
};
</script>

<style lang="scss" scoped>
</style>


