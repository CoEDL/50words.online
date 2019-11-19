<template>
    <div>
        <information-panel-component />
        <map-component />
        <data-selector-component class="style-data-selector" />
        <render-selected-word-component class="style-selected-word" />
        <render-main-logo-component class="style-logo-container" />
    </div>
</template>

<script>
import { loadData } from "src/data-loader.service";
import MapComponent from "./Map.component.vue";
import InformationPanelComponent from "./InformationPanel.component.vue";
import DataSelectorComponent from "./DataSelector.component.vue";
import RenderSelectedWordComponent from "components/RenderSelectedWord.component.vue";
import RenderMainLogoComponent from "components/RenderMainLogo.component.vue";

export default {
    components: {
        MapComponent,
        InformationPanelComponent,
        DataSelectorComponent,
        RenderSelectedWordComponent,
        RenderMainLogoComponent
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
    top: 50px;
    left: calc(100vw - 260px);
}

.style-selected-word {
    position: fixed;
    top: 90px;
    width: 300px;
    left: calc(100vw - 370px);
}

.style-logo-container {
    position: absolute;
    top: 5px;
    left: 55px;
}
@media (min-width: 400px) {
    .style-data-selector {
        position: fixed;
        top: 10px;
        left: calc(100vw - 250px);
    }
    .style-selected-word {
        top: 50px;
    }
}
@media (min-width: 768px) {
    .style-data-selector {
        position: fixed;
        top: 15px;
        left: calc(100vw - 250px);
    }

    .style-selected-word {
        position: fixed;
        top: 50px;
        width: 420px;
        left: calc(100vw - 500px);
    }

    .style-logo-container {
        top: 5px;
        left: 55px;
    }
}

@media (min-width: 1024px) {
    .style-data-selector {
        position: fixed;
        top: 15px;
        left: calc(100vw - 370px);
    }

    .style-selected-word {
        position: fixed;
        top: 50px;
        width: 420px;
        left: calc(100vw - 500px);
    }

    .style-logo-container {
        top: 5px;
        left: 55px;
    }
}
</style>
