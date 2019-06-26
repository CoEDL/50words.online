<template>
    <div>
        <div class="row my-4">
            <div class="col">
                <el-select
                    v-model="filterErrorType"
                    clearable
                    placeholder="Show only the following error types"
                    class="style-select"
                    @change="filterErrors"
                >
                    <el-option
                        v-for="(item, idx) in errorTypes"
                        :key="idx"
                        :label="item"
                        :value="item"
                    ></el-option>
                </el-select>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <el-table
                    :data="errors.errors"
                    :height="tableHeight"
                    :default-sort="{ prop: 'level', order: 'ascending'}"
                    :row-style="setRowColour"
                >
                    <el-table-column type="index" width="50"></el-table-column>

                    <el-table-column prop="type" label="Type" width="300" sortable></el-table-column>
                    <el-table-column prop="level" label="Level" width="100" sortable></el-table-column>
                    <el-table-column prop="msg" label="Message" sortable></el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>

<script>
import { uniq } from "lodash";

export default {
    props: {
        errors: {
            type: Object,
            required: true
        },
        data: {
            type: Object,
            required: true
        },
        tableHeight: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            filterErrorType: undefined,
            errorTypes: []
        };
    },
    async beforeMount() {
        this.errorTypes = uniq(this.errors.errors.map(e => e.type)).sort();
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
</style>
