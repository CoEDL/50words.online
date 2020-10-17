<template>
    <div class="flex flex-col">
        <el-pagination
            layout="prev, pager, next, total"
            :total="total"
            @current-change="update"
        ></el-pagination>
        <el-select
            v-model="filterErrorType"
            clearable
            placeholder="Show only the following error types"
            class="style-select"
        >
            <el-option
                v-for="(item, idx) in errorTypes"
                :key="idx"
                :label="item"
                :value="item"
            ></el-option>
        </el-select>
        <el-table
            v-if="errors.length"
            :data="errors"
            :default-sort="{ prop: 'level', order: 'ascending' }"
            :row-style="setRowColour"
        >
            <el-table-column
                prop="language"
                label="Language"
                width="300"
                sortable
            ></el-table-column>
            <el-table-column
                prop="msg"
                label="Message"
                sortable
            ></el-table-column>
        </el-table>
    </div>
</template>

<script>
import { uniq } from "lodash";
import { loadProcessingData } from "src/data-loader.service";

export default {
    data() {
        return {
            page: 0,
            pageSize: 10,
            filterErrorType: undefined,
            data: {},
            errorTypes: [],
        };
    },
    computed: {
        errors: function() {
            if (!this.data.errors) return [];
            return this.data.errors.errors
                .filter((e) => e.type === this.filterErrorType)
                .slice(
                    this.page * this.pageSize,
                    this.page * this.pageSize + this.pageSize
                );
        },
        total: function() {
            if (!this.data.errors) return 0;
            return this.data.errors.errors.filter(
                (e) => e.type === this.filterErrorType
            ).length;
        },
    },
    async mounted() {
        this.data = await loadProcessingData();
        this.errorTypes = uniq(
            this.data.errors.errors.map((e) => e.type)
        ).sort();
        this.filterErrorType = this.errorTypes[0];
    },
    methods: {
        setRowColour(row) {
            if (row.row.level === "error") {
                return { color: "red" };
            } else if (row.row.level === "warning") {
                return { color: "#e67e22" };
            }
        },
        update(page) {
            this.page = page - 1;
        },
    },
};
</script>

<style lang="scss" scoped>
.style-select {
    width: 500px;
}
</style>
