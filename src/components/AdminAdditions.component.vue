<template>
    <div class="flex flex-col">
        <el-pagination layout="prev, pager, next, total" :total="total" @current-change="update"></el-pagination>
        <el-table
            v-if="additions"
            :data="additions"
            :default-sort="{ prop: 'name', order: 'ascending' }"
        >
            <el-table-column prop="name" label="Language Name" width="300" sortable></el-table-column>
            <el-table-column prop="property" label="Property Updated" width="300"></el-table-column>
            <el-table-column prop="value" label="Value Set"></el-table-column>
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
            data: {}
        };
    },
    computed: {
        additions: function() {
            if (!this.data.additions) return [];
            return this.data.additions.additions.slice(
                this.page * this.pageSize,
                this.page * this.pageSize + this.pageSize
            );
        },
        total: function() {
            if (!this.data.additions) return 0;
            return this.data.additions.additions.length;
        }
    },
    async mounted() {
        this.data = await loadProcessingData();
    },
    methods: {
        update(page) {
            this.page = page - 1;
        }
    }
};
</script>

<style lang="scss" scoped></style>
