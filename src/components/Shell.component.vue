<template>
    <div>
        <information-panel-component/>
        <map-component/>
        <data-selector-component class="style-data-selector"/>
        <render-selected-word-component class="style-selected-word"/>
    </div>
</template>

<script>
import { loadData } from "src/data-loader.service";
import MapComponent from "./Map.component.vue";
import InformationPanelComponent from "./InformationPanel.component.vue";
import DataSelectorComponent from "./DataSelector.component.vue";
import RenderSelectedWordComponent from "components/RenderSelectedWord.component.vue";

export default {
    components: {
        MapComponent,
        InformationPanelComponent,
        DataSelectorComponent,
        RenderSelectedWordComponent
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

.style-selected-word {
    position: fixed;
    top: 70px;
    width: 420px;
    left: calc(100vw - 500px);
}
</style>