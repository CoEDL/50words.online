<template>
    <div>
        <div id="map" class="style-map"></div>
        <div class="style-map-reset">
            <div class="row">
                <div class="col">
                    <el-button type="primary" circle @click="centerMap">
                        <i class="fas fa-crosshairs"></i>
                    </el-button>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col">
                    <el-button type="primary" circle @click="addLanguageLayer">
                        <i class="fas fa-undo"></i>
                    </el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/en";
Vue.use(ElementUI, { locale });
import RenderWordComponent from "components/RenderWord.component.vue";
import mapboxgl from "mapbox-gl";
mapboxgl.accessToken =
    "pk.eyJ1IjoibWFyY29sYXJvc2EiLCJhIjoiY2p2NGhzMzFkMnFsbzQwandhNmJ2MWI2eCJ9.qxu6U_HfPFd-4BZ85eNCvw";
import { throttle, map } from "lodash";

export default {
    components: {
        RenderWordComponent
    },
    data() {
        return {};
    },
    computed: {
        words: function() {
            return this.$store.state.selectedWord;
        }
    },
    watch: {
        words: function() {
            this.renderWordLayer();
        }
    },
    mounted() {
        this.map = new mapboxgl.Map({
            container: "map",
            style: "mapbox://styles/mapbox/dark-v10",
            center: [0, 0]
        });
        // this.map.addControl(new mapboxgl.NavigationControl());
        // this.map.addControl(new mapboxgl.FullscreenControl());
        this.centerMap();
        this.map.on("load", () => {
            this.addLanguageLayer();
        });
        this.map.on("click", "languages", e => {
            this.$store.commit("setSelectedLanguage", {
                ...e.features[0].properties
            });
        });
        this.map.on("click", "words", e => {
            const RenderWordClass = Vue.extend(RenderWordComponent);
            const popup = new mapboxgl.Popup()
                .setLngLat(e.lngLat)
                .setHTML('<div id="vue-popup-content"></div>')
                .addTo(this.map);
            const popupInstance = new RenderWordClass({
                propsData: {
                    layout: "popup",
                    word: e.features[0].properties
                }
            });
            popupInstance.$mount("#vue-popup-content");
            popup._update();
        });
        // Change the cursor to a pointer when the mouse is over the places layer.
        this.map.on("mouseenter", "languages", () => {
            this.map.getCanvas().style.cursor = "pointer";
        });

        // Change it back to a pointer when it leaves.
        this.map.on("mouseleave", "languages", () => {
            this.map.getCanvas().style.cursor = "";
        });
    },
    beforeMount() {
        window.addEventListener("resize", throttle(this.centerMap, 300));
    },
    beforeDestroy() {
        window.removeEventListener("resize", this.centerMap);
    },
    methods: {
        centerMap() {
            this.map.fitBounds([[96, -45], [168, -8]]);
        },
        addLanguageLayer() {
            this.$store.commit("unsetSelectedWord");
            if (this.map.getLayer("words"))
                this.map.setLayoutProperty("words", "visibility", "none");
            const features = this.$store.state.languages.map(language => {
                return {
                    type: "Feature",
                    properties: {
                        ...language
                    },
                    geometry: {
                        type: "Point",
                        coordinates: [language.lng, language.lat]
                    }
                };
            });
            // console.log(JSON.stringify(features, null, 2));
            if (!this.map.getLayer("languages")) {
                this.map.addLayer({
                    id: "languages",
                    type: "symbol",
                    source: {
                        type: "geojson",
                        data: {
                            type: "FeatureCollection",
                            features
                        }
                    },
                    layout: {
                        visibility: "visible"
                    },
                    paint: {
                        "text-color": "#f15a22"
                    },
                    layout: {
                        "text-field": "{name}"
                    }
                });
            }
            this.map.setLayoutProperty("languages", "visibility", "visible");
        },
        renderWordLayer() {
            if (!this.words) return;
            if (this.map.getLayer("languages"))
                this.map.setLayoutProperty("languages", "visibility", "none");
            const features = this.words.map(word => {
                return {
                    type: "Feature",
                    properties: {
                        ...word
                    },
                    geometry: {
                        type: "Point",
                        coordinates: [word.lng, word.lat]
                    }
                };
            });
            // console.log(JSON.stringify(features, null, 2));

            if (!this.map.getLayer("words")) {
                this.map.addSource("words", {
                    type: "geojson",
                    data: { type: "FeatureCollection", features }
                });
                this.map.addLayer({
                    id: "words",
                    type: "symbol",
                    source: "words",
                    paint: {
                        "text-color": "#f15a22"
                    },
                    layout: {
                        "text-field": "{indigenous}"
                    }
                });
            } else {
                this.map
                    .getSource("words")
                    .setData({ type: "FeatureCollection", features });
            }
            this.map.setLayoutProperty("words", "visibility", "visible");
        }
    }
};
</script>

<style lang="scss" scoped>
.style-map {
    position: fixed;
    top: 0;
    left: 50px;
    width: calc(100vw - 50px);
    height: 100vh;
}

.style-map-reset {
    position: fixed;
    z-index: 2;
    top: 10px;
    left: calc(100vw - 50px);
}
</style>

<style lang="scss">
.mapboxgl-popup-content {
    width: 400px;
}
</style>

