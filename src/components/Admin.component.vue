<template>
    <div class="bg-white w-full style-container -mt-1">
        <div class="flex flex-col p-4">
            <router-link to="/" class="my-2">back to site</router-link>
            <!-- <div class="text-xl my-2">Last Updated: {{ lastUpdated }}</div> -->

            <el-tabs type="border-card" v-model="tab" class="mt-4">
                <el-tab-pane label="Languages" name="languages">
                    <admin-languages-component v-if="tab === 'languages'" />
                </el-tab-pane>
                <el-tab-pane label="Data Processing Errors" name="errors">
                    <admin-errors-component v-if="tab === 'errors'" />
                </el-tab-pane>
                <el-tab-pane label="Languages With Data" name="languagesWithData">
                    <admin-languages-with-data-component v-if="tab === 'languagesWithData'" />
                </el-tab-pane>
                <!-- <el-tab-pane label="Gambay Additions" name="gambayAdditions">
                    <admin-additions-component
                        v-if="tab === 'gambayAdditions'"
                    />
                </el-tab-pane> -->
                <!-- <el-tab-pane label="Word / Language Mapping" name="stats">
                    <admin-word-stats-component v-if="tab === 'stats'" />
                </el-tab-pane> -->
            </el-tabs>
        </div>
    </div>
</template>

<script>
import AdminErrorsComponent from "./AdminErrors.component.vue";
import AdminAdditionsComponent from "./AdminAdditions.component.vue";
import AdminLanguagesComponent from "./AdminLanguages.component.vue";
import AdminLanguagesWithDataComponent from "./AdminLanguagesWithData.component.vue";

export default {
    components: {
        AdminErrorsComponent,
        AdminAdditionsComponent,
        AdminLanguagesComponent,
        AdminLanguagesWithDataComponent,
    },
    data() {
        return {
            tab: "languages",
        };
    },
    async mounted() {
        this.$store.dispatch("loadData");
    },
};
</script>

<style lang="scss" scoped>
.style-container {
    min-height: 100vh;
}
</style>
