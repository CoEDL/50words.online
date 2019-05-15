<template>
    <div>
        <information-panel-component/>
        <map-component/>
        <data-selector-component class="style-data-selector"/>
    </div>
</template>

<script>
import { loadData } from "src/data-loader.service";
import MapComponent from "./Map.component.vue";
import InformationPanelComponent from "./InformationPanel.component.vue";
import DataSelectorComponent from "./DataSelector.component.vue";

export default {
    components: {
        MapComponent,
        InformationPanelComponent,
        DataSelectorComponent
    },
    data() {
        return {};
    },
    mounted() {
        loadData({ store: this.$store });
    }
};
</script>

<style scoped lang="scss">
.style-data-selector {
    position: fixed;
    top: 15px;
    left: calc(100vw - 370px);
}
</style>