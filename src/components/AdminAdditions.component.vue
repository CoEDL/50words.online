<template>
    <el-table
        :data="additions"
        :height="tableHeight"
        :default-sort="{ prop: 'name', order: 'ascending' }"
    >
        <el-table-column type="index" width="50"></el-table-column>

        <el-table-column
            prop="name"
            label="Language Name"
            width="300"
            sortable
        ></el-table-column>
        <el-table-column
            prop="property"
            label="Property Updated"
            width="300"
        ></el-table-column>
        <el-table-column prop="value" label="Value Set"></el-table-column>
    </el-table>
</template>

<script>
import { uniq } from "lodash";

export default {
    props: {
        additions: {
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
};
</script>

<style lang="scss" scoped></style>
