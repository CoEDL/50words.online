<template>
    <div>
        <div id="map" class="style-map"></div>
        <data-selector-component class="style-data-selector hidden md:block" />
        <render-selected-word-component
            v-if="map && selectedWord"
            :map="map"
            class="style-render-selected-word"
            @center-map="centerMap"
        />

        <zoom-to-language-component
            v-if="!selectedWord"
            class="style-language-finder hidden md:block"
            @zoom-to-language="zoomToLanguage"
        />
        <div class="style-map-reset pt-2 md:pt-0">
            <div class="flex flex-col">
                <div>
                    <el-button
                        type="default"
                        @click="centerMap"
                        size="mini"
                        class="style-reset-button"
                    >
                        <i class="fas fa-crosshairs style-button-image"></i>
                    </el-button>
                </div>
                <div class="h-4"></div>
                <div>
                    <el-button
                        type="default"
                        @click="toggleLayerWithoutData"
                        size="mini"
                        class="style-reset-button"
                    >
                        <i class="fas fa-layer-group style-button-image"></i>
                    </el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import styles from "assets/variables.scss";
import Vue from "vue";
import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/en";
import RenderWordComponent from "components/RenderWord.component.vue";
import ZoomToLanguageComponent from "components/ZoomToLanguage.component.vue";
import DataSelectorComponent from "./DataSelector.component.vue";
import RenderSelectedWordComponent from "./RenderSelectedWord.component.vue";

Vue.use(ElementUI, { locale });
import mapboxgl from "mapbox-gl";
mapboxgl.accessToken =
    "pk.eyJ1IjoibWFyY29sYXJvc2EiLCJhIjoiY2p2NGhzMzFkMnFsbzQwandhNmJ2MWI2eCJ9.qxu6U_HfPFd-4BZ85eNCvw";
import { throttle, map, orderBy, shuffle, uniq } from "lodash";

export default {
    components: {
        RenderWordComponent,
        ZoomToLanguageComponent,
        DataSelectorComponent,
        RenderSelectedWordComponent,
    },
    data() {
        return {
            watchers: {},
            map: undefined,
            popup: undefined,
            mediaElement: {
                audio: false,
                video: false,
                files: [],
            },
            emptyWordsLanguageLayerShowing: false,
        };
    },
    computed: {
        words: function() {
            return this.$store.state.selectedWord;
        },
        show: function() {
            return this.$store.state.show;
        },
        selectedLanguage: function() {
            return this.$store.state.selectedLanguage;
        },
        selectedWord: function() {
            return this.$store.state.selectedWord;
        },
        playAll: function() {
            return this.$store.state.playAll;
        },
        largeDevice: function() {
            return window.innerWidth < 768 ? false : true;
        },
    },
    mounted() {
        this.renderMap();
        this.watchers.words = this.$watch("words", (d) => {
            if (d) {
                this.played = {
                    allWords: [],
                    thisWord: [],
                };
                this.renderWordLayer();
            } else {
                this.renderLanguageLayer();
            }
        });
        this.watchers.words = this.$watch("playAll", this.playAllWords);
    },
    beforeMount() {
        window.addEventListener("resize", throttle(this.centerMap, 300));
    },
    beforeDestroy() {
        this.watchers.words();
        window.removeEventListener("resize", this.centerMap);
    },
    methods: {
        async centerMap() {
            if (this.popup) this.popup.remove();

            centerCountry({ map: this.map });
            let position;
            if ("geolocation" in navigator) {
                try {
                    position = await new Promise((resolve, reject) => {
                        navigator.geolocation.getCurrentPosition(
                            (position) => resolve(position),
                            (error) => reject(error)
                        );
                    });
                } catch (error) {
                    centerCountry({ map: this.map });
                }
                // const latitude  = position.coords.latitude;
                // const longitude = position.coords.longitude;

                // Melbourne
                // position = [144.948743, -37.790136];
                if (position) {
                    position = [
                        position.coords.longitude,
                        position.coords.latitude,
                    ];
                    centerLocation({ map: this.map, position });
                } else {
                    centerCountry({ map: this.map });
                }
            } else {
                centerCountry({ map: this.map });
            }

            function centerCountry({ map }) {
                map.fitBounds([
                    [96, -45],
                    [168, -8],
                ]);
            }

            function centerLocation({ map, position }) {
                map.flyTo({
                    center: position,
                    zoom: window.innerwidth < 768 ? 8 : 6,
                    bearing: 0,
                });
            }
        },
        renderMap() {
            this.map = new mapboxgl.Map({
                container: "map",
                style: "mapbox://styles/mapbox/dark-v10",
                center: [0, 0],
            });
            if (this.largeDevice) {
                this.map.addControl(
                    new mapboxgl.NavigationControl({
                        showCompass: false,
                    })
                );
            }
            // this.map.addControl(new mapboxgl.FullscreenControl());
            this.centerMap();
            this.map.on("load", () => {
                this.renderLanguageLayer();
            });
            this.map.on("click", "languages", (e) => {
                this.$store.commit("setSelectedLanguage", {
                    ...e.features[0].properties,
                });
            });
            this.map.on("click", "words", (e) => {
                if (this.popup) this.popup.remove();
                const RenderWordClass = Vue.extend(RenderWordComponent);
                this.popup = new mapboxgl.Popup({ maxWidth: "none" })
                    .setLngLat(e.lngLat)
                    .setHTML('<div id="vue-popup-content"></div>')
                    .addTo(this.map);
                const properties = e.features[0].properties;
                if (properties.audio)
                    properties.audio = JSON.parse(properties.audio);
                if (properties.video)
                    properties.video = JSON.parse(properties.video);
                properties.language = JSON.parse(properties.language);
                const popupInstance = new RenderWordClass({
                    propsData: {
                        layout: "popup",
                        word: { properties },
                    },
                });
                popupInstance.$mount("#vue-popup-content");
                this.popup._update();
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
        renderLanguageLayer() {
            if (this.popup) this.popup.remove();
            if (this.map.getLayer("words"))
                this.map.setLayoutProperty("words", "visibility", "none");

            let languages = this.$store.state.languages.filter((l) => !l.words);

            this.renderLanguagesWithData();
            this.map.setLayoutProperty("languages", "visibility", "visible");

            if (this.largeDevice) {
                this.emptyWordsLanguageLayerShowing = true;
                this.renderLanguagesWithoutData();
                this.map.setLayoutProperty(
                    "languagesWithoutData",
                    "visibility",
                    "visible"
                );
            }
        },

        renderLanguagesWithData() {
            const features = this.$store.state.languages.filter(
                (l) => l.properties.words
            );
            if (!this.map.getLayer("languages")) {
                this.map.addLayer({
                    id: "languages",
                    type: "symbol",
                    source: {
                        type: "geojson",
                        data: {
                            type: "FeatureCollection",
                            features,
                        },
                    },
                    paint: {
                        "text-color": styles.textColor,
                    },
                    layout: {
                        visibility: "visible",
                        "text-field": "{name}",
                        "text-size": 15,
                        "text-max-width": 40,
                        "text-allow-overlap": true,
                        "icon-allow-overlap": true,
                    },
                });
            }
        },
        renderLanguagesWithoutData() {
            const features = this.$store.state.languages.filter(
                (l) => !l.properties.words
            );
            if (!this.map.getLayer("languagesWithoutData")) {
                this.map.addLayer(
                    {
                        id: "languagesWithoutData",
                        type: "symbol",
                        source: {
                            type: "geojson",
                            data: {
                                type: "FeatureCollection",
                                features,
                            },
                        },
                        paint: {
                            "text-color": styles.primaryColor,
                            "text-opacity": 0.4,
                        },
                        layout: {
                            visibility: "visible",
                            "text-field": "{name}",
                            "text-size": 15,
                            "text-max-width": 40,
                            "text-allow-overlap": true,
                            "icon-allow-overlap": true,
                        },
                    },
                    "languages"
                );
            }
        },
        renderWordLayer() {
            if (this.popup) this.popup.remove();
            this.map.setLayoutProperty("languages", "visibility", "none");
            this.map.setLayoutProperty(
                "languagesWithoutData",
                "visibility",
                "none"
            );
            if (!this.words) return;

            if (!this.map.getLayer("words")) {
                this.map.addSource("words", {
                    type: "geojson",
                    data: { type: "FeatureCollection", features: this.words },
                });
                this.map.addLayer({
                    id: "words",
                    type: "symbol",
                    source: "words",
                    paint: {
                        "text-color": styles.textColor,
                    },
                    layout: {
                        "text-field": "{indigenous}",
                        "text-size": 15,
                        "text-max-width": 40,
                        "text-allow-overlap": true,
                        "icon-allow-overlap": true,
                        "text-variable-anchor": [
                            "top",
                            "bottom",
                            "left",
                            "right",
                        ],
                    },
                });
            } else {
                this.map.getSource("words").setData({
                    type: "FeatureCollection",
                    features: this.words,
                });
            }
            this.map.setLayoutProperty("words", "visibility", "visible");
        },
        zoomToLanguage(language) {
            this.map.flyTo({
                center: language.geometry.coordinates,
                zoom: 11,
                bearing: 0,
            });
        },
        toggleLayerWithoutData() {
            if (this.emptyWordsLanguageLayerShowing) {
                this.map.setLayoutProperty(
                    "languagesWithoutData",
                    "visibility",
                    "none"
                );
                this.emptyWordsLanguageLayerShowing = false;
            } else {
                this.renderLanguagesWithoutData();
                this.map.setLayoutProperty(
                    "languagesWithoutData",
                    "visibility",
                    "visible"
                );
                this.emptyWordsLanguageLayerShowing = true;
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.style-map {
    position: fixed;
    top: 0;
    left: 0px;
    width: 100vw;
    height: 100vh;
    cursor: pointer;
}

.style-map-reset {
    position: fixed;
    top: 8px;
    left: calc(100vw - 40px);
}

.style-reset-button {
    max-width: 8px;
    font-size: 12px;
}

.style-button-image {
    margin-left: -6px;
}

.style-data-selector {
    position: fixed;
    top: 50px;
    left: calc(100vw - 260px);
}

.style-render-selected-word {
    position: fixed;
    z-index: 1000;
    top: calc(100% - 115px);
    left: 0px;
    width: 100vw;
    background-color: #191a1a;
}

@media (min-width: 768px) {
    .style-map {
        position: fixed;
        top: 0;
        left: 50px;
        width: calc(100vw - 50px);
        height: 100vh;
        cursor: pointer;
    }

    .style-data-selector {
        position: fixed;
        top: 15px;
        left: calc(100vw - 250px);
    }

    .style-map-reset {
        position: fixed;
        top: 80px;
        left: calc(100vw - 41px);
    }
    .style-language-finder {
        position: fixed;
        width: 200px;
        top: 65px;
        left: calc(100vw - 250px);
    }
    .style-render-selected-word {
        position: fixed;
        top: 50px;
        left: calc(100vw - 300px);
        width: 250px;
    }
}

@media (min-width: 1024px) {
    .style-data-selector {
        position: fixed;
        top: 15px;
        left: calc(100vw - 370px);
    }

    .style-map-reset {
        position: fixed;
        top: 80px;
        left: calc(100vw - 41px);
    }
    .style-language-finder {
        position: fixed;
        width: 290px;
        top: 80px;
        left: calc(100vw - 364px);
    }
    .style-render-selected-word {
        position: fixed;
        top: 55px;
        left: calc(100vw - 370px);
        width: 300px;
    }
}
</style>

<style lang="scss">
@import "assets/variables.scss";

.mapboxgl-popup-tip {
    border-top-color: $primary-color !important;
}

.mapboxgl-popup-content {
    text-align: center;
    width: unset;
    padding: 15px 25px;
    font-size: 0.8em;
    background-color: $primary-color;
    white-space: nowrap;
}

.mapboxgl-popup-close-button {
    display: none;
}

.mapboxgl-ctrl-top-right {
    margin: 0px 5px 0 0;
}

@media (min-width: 768px) {
    .mapboxgl-ctrl-top-right {
        margin: 0px 0 0 0;
    }
    .mapboxgl-popup-content {
        text-align: center;
        font-size: 1.2em;
        background-color: $primary-color;
    }
}

@media (min-width: 1024px) {
    .mapboxgl-ctrl-top-right {
        margin: 0px 0px 0 0;
    }
    .mapboxgl-popup-content {
        text-align: center;
        font-size: 1.5em;
        background-color: $primary-color;
    }
}
</style>
