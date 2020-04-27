<template>
    <el-table
        :data="languages"
        :height="tableHeight"
        :default-sort="{ prop: 'properties.words', order: 'descending' }"
    >
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column
            prop="properties.code"
            label="Code"
            width="100"
            sortable
        ></el-table-column>
        <el-table-column
            prop="properties.name"
            label="Language Name"
            width="300"
            sortable
        ></el-table-column>
        <el-table-column prop="geometry.coordinates" label="Coordinates">
            <template slot-scope="scope"
                >{{ scope.row.geometry.coordinates[0] }},
                {{ scope.row.geometry.coordinates[1] }}</template
            >
        </el-table-column>
        <el-table-column
            prop="properties.source"
            label="Source Dataset"
            sortable
        ></el-table-column>
        <el-table-column prop="properties.words" label="Has Data?" sortable>
            <template slot-scope="scope">
                <span v-show="scope.row.properties.words">
                    <i class="fas fa-check style-true"></i>
                </span>
                <span v-show="!scope.row.properties.words">
                    <i class="fas fa-times style-false"></i>
                </span>
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
import { uniq } from "lodash";

export default {
    props: {
        languages: {
            type: Array,
            required: true,
        },
        tableHeight: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {};
    },
    mounted() {},
};
</script>

<style lang="scss" scoped>
.style-true {
    color: green;
}
.style-false {
    color: red;
}
</style>
