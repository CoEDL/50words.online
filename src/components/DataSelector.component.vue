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
            textColor: styles.textColor
        };
    },
    computed: {
        selectedWord: function() {
            return this.$store.state.selectedWord;
        }
    },
    mounted() {
        this.watchers.selectedWord = this.$watch("selectedWord", () => {
            this.selector = this.selectedWord ? false : true;
            this.storeSwitchState();
        });
        this.storeSwitchState();
    },
    beforeDestroy() {
        this.watchers.selectedWord();
    },
    methods: {
        storeSwitchState() {
            if (this.selector) {
                this.$store.commit("show", "languages");
                this.$store.commit("unsetSelectedWord");
            } else {
                this.$store.commit("show", "words");
                this.$store.commit("unsetSelectedLanguage");
            }
        }
    }
};
</script>

<style lang="scss" scoped>
.data-selector-background {
    position: absolute;
    width: 300px;
    border-radius: 99em;
    height: 60px;
    top: 0;
    left: 0;
    background-color: #000;
}

.data-selector-switch {
    position: absolute;
    padding: 12px 0 0 10px;
    width: 300px;
    height: 60px;
    top: 0;
    left: 0;
}
</style>

<style lang="scss">
@import "assets/variables.scss";

.el-switch__core {
    margin: 12px 0 0 0;
}

.el-switch__label > span {
    font-size: 2em;
}

.el-switch__label {
    color: $primary-color;
}

.el-switch__label.is-active {
    color: $text-color;
}
</style>

