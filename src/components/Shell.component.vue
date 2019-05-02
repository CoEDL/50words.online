<template>
    <div>
        <information-panel-component/>
        <map-component/>
    </div>
</template>

<script>
import { loadData } from "src/data-loader.service";
import MapComponent from "./Map.component.vue";
import InformationPanelComponent from "./InformationPanel.component.vue";

export default {
    components: {
        MapComponent,
        InformationPanelComponent
    },
    data() {
        return {};
    },
    mounted() {
        loadData({ store: this.$store });
    }
};
</script>

<style scoped lang="scss"></style>
