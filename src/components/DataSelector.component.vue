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
        this.watchers.selectedWord = this.$watch("selectedWord", d => {
            this.selector = this.selectedWord ? false : true;
        });
        this.storeSwitchState();
    },
    beforeDestroy() {
        this.watchers.selectedWord();
    },
    methods: {
        async storeSwitchState() {
            if (this.selector) {
                this.$store.commit("unsetSelectedWord");
            } else {
                this.$store.commit("unsetSelectedLanguage");
                this.$store.dispatch("loadWord", { word: "hello" });
            }
        }
    }
};
</script>

<style lang="scss" scoped>
.data-selector-background {
    position: absolute;
    width: 200px;
    border-radius: 99em;
    height: 40px;
    top: 0;
    left: 0;
    background-color: #000;
}

.data-selector-switch {
    position: absolute;
    padding: 5px 0 0 10px;
    width: 200px;
    height: 40px;
    top: 0;
    left: 0;
}
@media only screen and (min-width: 1024px) {
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

@media (min-width: 1024px) {
    .el-switch__core {
        margin: 12px 0 0 0;
    }

    .el-switch__label > span {
        font-size: 2em;
    }
}

.el-switch__label {
    color: $primary-color;
}

.el-switch__label.is-active {
    color: $text-color;
}
</style>

