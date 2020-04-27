<template>
    <div>
        <div class="data-selector-background"></div>
        <div class="data-selector-switch">
            <el-switch
                v-model="selector"
                active-text="Languages"
                inactive-text="Words"
                :active-color="textColor"
                @change="storeSwitchState()"
            ></el-switch>
        </div>
    </div>
</template>

<script>
import styles from "assets/variables.scss";

export default {
    data() {
        return {
            watchers: {},
            selector: true,
            textColor: styles.textColor,
        };
    },
    computed: {
        selectedWord: function() {
            return this.$store.state.selectedWord;
        },
    },
    watch: {
        selectedWord: function() {
            this.selector = this.selectedWord ? false : true;
        },
    },
    mounted() {
        this.selector = this.selectedWord ? false : true;
    },
    methods: {
        async storeSwitchState() {
            if (this.selector) {
                this.$store.commit("unsetSelectedWord");
            } else {
                this.$store.commit("unsetSelectedLanguage");
                this.$store.dispatch("loadWord", { word: "hand" });
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.data-selector-background {
    position: absolute;
    width: 205px;
    border-radius: 99em;
    height: 41px;
    top: 0;
    left: 0;
    background-color: #000;
}

.data-selector-switch {
    position: relative;
    padding: 5px 0 0 10px;
    width: 200px;
    height: 40px;
    top: 2px;
    left: 5px;
}
</style>

<style lang="scss">
@import "assets/variables.scss";
.el-switch__core {
    margin: 5px 0 0 0;
}

.el-switch__label > span {
    font-size: 1em;
}

.el-switch__label {
    color: $primary-color;
}

.el-switch__label.is-active {
    color: $text-color;
}
</style>
