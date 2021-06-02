<template>
    <div class="flex flex-col">
        <div>
            <el-button @click="downloadDataAsCSV">Download the data as a CSV file.</el-button>
        </div>
        <el-table
            v-if="languages.length"
            :data="languagesByProp"
            :default-sort="{ prop: 'level', order: 'ascending' }"
        >
            <el-table-column label="Language" prop="name" width="300" sortable></el-table-column>
            <el-table-column label="Long" prop="long" width="150" sortable></el-table-column>
            <el-table-column label="Lat" prop="lat" width="150" sortable></el-table-column>
            <el-table-column label="Who" prop="who"></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    data() {
        return { languages: [], languagesByProp: [] };
    },
    mounted() {
        this.processLanguagesWithData();
    },
    methods: {
        async processLanguagesWithData() {
            let languages = this.$store.state.languages.filter((l) => l.properties.words);
            this.languages = languages.map((l) => {
                return [
                    l.properties.name,
                    l.geometry.coordinates[0],
                    l.geometry.coordinates[1],
                    [l.properties.speaker.name, l.properties.thankyou].join(", "),
                ];
            });
            this.languagesByProp = this.languages.map((l) => ({
                name: l[0],
                long: l[1],
                lat: l[2],
                who: l[3],
            }));
        },
        downloadDataAsCSV() {
            let csvContent =
                "data:text/csv;charset=utf-8," + this.languages.map((e) => e.join(";")).join("\n");
            let encodedUri = encodeURI(csvContent);
            window.open(encodedUri);
        },
    },
};
</script>

<style lang="scss" scoped></style>
