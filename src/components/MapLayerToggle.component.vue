<template>
    <div class="flex flex-row">
        <div class="mr-1 text-sm text-gray-800 pt-1">
            Show only complete entries
        </div>
        <div>
            <el-switch
                v-model="state"
                :active-color="activeColor"
                :inactive-color="inactiveColor"
                @change="handleStateChange"
            >
            </el-switch>
        </div>
    </div>
</template>

<script>
import styles from "assets/variables.scss";

export default {
    data() {
        return {
            state: window.innerWidth < 768 ? true : false,
            activeColor: styles.highlightDark,
            inactiveColor: styles.gray,
        };
    },
    methods: {
        handleStateChange() {
            if (this.state) {
                this.$emit("hide-languages-without-data");
            } else {
                this.$emit("show-languages-without-data");
            }
        },
    },
};
</script>
