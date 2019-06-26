<template>
    <div>
        <div class="row my-5 style-text">
            <div class="col">Last Updated: {{lastUpdated}}</div>
        </div>

        <div class="row">
            <div class="col">
                <el-tabs type="border-card">
                    <el-tab-pane label="Data Processing Errors">
                        <admin-errors-component
                            :data="data"
                            :errors="errors"
                            :table-height="tableHeight"
                            v-if="ready"
                        />
                    </el-tab-pane>
                    <el-tab-pane label="Gambay Additions">
                        <admin-additions-component
                            :additions="additions"
                            :table-height="tableHeight"
                            v-if="ready"
                        />
                    </el-tab-pane>
                    <el-tab-pane label="Languages">
                        <admin-languages-component
                            :languages="languages"
                            :table-height="tableHeight"
                            v-if="ready"
                        />
                    </el-tab-pane>
                </el-tabs>
            </div>
        </div>
    </div>
</template>

<script>
import { loadData, loadProcessingData } from "src/data-loader.service";
import { uniq } from "lodash";
import AdminErrorsComponent from "./AdminErrors.component.vue";
import AdminAdditionsComponent from "./AdminAdditions.component.vue";
import AdminLanguagesComponent from "./AdminLanguages.component.vue";
import moment from "moment";

export default {
    components: {
        AdminErrorsComponent,
        AdminAdditionsComponent,
        AdminLanguagesComponent
    },
    data() {
        return {
            data: {},
            tableHeight: window.innerHeight - 350,
            filterErrorType: undefined,
            errorTypes: [],
            errors: {},
            additions: {},
            languages: [],
            ready: false
        };
    },
    computed: {
        lastUpdated: function() {
            return moment(this.errors.date).format("LLL");
        }
    },
    async beforeMount() {
        await loadData({ store: this.$store });
        this.languages = this.$store.state.languages;

        this.data = await loadProcessingData();
        this.errors = { ...this.data.errors };
        this.errorTypes = uniq(this.errors.errors.map(e => e.type)).sort();
        this.additions = this.data.additions;
        this.ready = true;
    },
    methods: {
        filterErrors() {
            if (!this.filterErrorType) {
                this.errors = { ...this.data.errors };
            } else {
                this.errors.errors = this.data.errors.errors.filter(
                    e => e.type === this.filterErrorType
                );
            }
        },
        setRowColour(row) {
            if (row.row.level === "error") {
                return { color: "red" };
            } else if (row.row.level === "warning") {
                return { color: "#e67e22" };
            }
        }
    }
};
</script>

<style lang="scss" scoped>
.style-select {
    width: 500px;
}
.style-text {
    font-size: 1.4em;
}
</style>
