<template>
    <div class="flex flex-col">
        <div class="flex flex-row">
            <el-pagination
                layout="prev, pager, next, total"
                :total="total"
                @current-change="update"
            ></el-pagination>
        </div>
        <el-table
            v-if="languages.length"
            :data="languages"
            :default-sort="{ prop: 'properties.words', order: 'descending' }"
            @sort-change="sort"
        >
            <el-table-column prop="properties.code" label="Code" width="100" sortable="custom"></el-table-column>
            <el-table-column
                prop="properties.name"
                label="Language Name"
                width="300"
                sortable="custom"
            ></el-table-column>
            <el-table-column prop="geometry.coordinates" label="Coordinates">
                <template slot-scope="scope">
                    {{ scope.row.geometry.coordinates[0] }},
                    {{ scope.row.geometry.coordinates[1] }}
                </template>
            </el-table-column>
            <el-table-column prop="properties.source" label="Source Dataset" sortable="custom"></el-table-column>
            <el-table-column prop="properties.words" label="Has Data?" sortable="custom">
                <template slot-scope="scope">
                    <span v-show="scope.row.properties.words">
                        <i class="fas fa-check text-green-600"></i>
                    </span>
                    <span v-show="!scope.row.properties.words">
                        <i class="fas fa-times text-red-600"></i>
                    </span>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import { orderBy } from "lodash";

export default {
    data() {
        return {
            page: 0,
            pageSize: 10,
            sortColumn: "properties.words",
            sortOrder: "desc"
        };
    },
    computed: {
        languages: function() {
            return orderBy(
                this.$store.state.languages,
                [this.sortColumn],
                [this.sortOrder]
            ).slice(
                this.page * this.pageSize,
                this.page * this.pageSize + this.pageSize
            );
        },
        total: function() {
            return this.$store.state.languages.length;
        }
    },
    methods: {
        update(page) {
            this.page = page - 1;
        },
        sort(data) {
            this.page = 0;
            this.sortColumn = data.prop;
            this.sortOrder = data.order === "ascending" ? "asc" : "desc";
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
