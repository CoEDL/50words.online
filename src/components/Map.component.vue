<template>
    <div class="md:p-1 relative">
        <div
            ref="map"
            :class="{
                'w-full h-full': !smallDevice,
                'width-screen cursor-pointer': smallDevice,
            }"
            :style="{
                height: smallDevice ? (selection.type ? '30vh' : '45vh') : mapHeight,
            }"
        ></div>
        <map-layer-toggle-component
            v-if="layer === 'languages'"
            class="top-0 right-0 absolute md:mt-4 mr-1 md:mr-4"
            @hide-languages-without-data="hideLanguagesWithoutData"
            @show-languages-without-data="showLanguagesWithoutData"
        />
        <zoom-to-language-component
            class="hidden md:block top-0 left-0 absolute mt-4 ml-6"
            @fly-to="flyTo"
        />
        <div class="top-0 right-0 mt-8 md:mt-32 mr-1 md:mr-3 absolute">
            <div class="flex flex-col">
                <div
                    @click="centerMap"
                    size="mini"
                    class="border-2 border-gray-400 py-1 px-3 bg-white rounded-lg"
                >
                    <i class="fas fa-crosshairs style-button-image"></i>
                </div>
            </div>
        </div>
        <el-dialog v-model="showContributeDialog" ref="modal" title="Contribute">
            <contribute-component />
        </el-dialog>
        <render-word-map-popup-component
            v-if="word"
            :word="word"
            class="absolute z-10 top-0 ml-4 mt-4 p-1 rounded-lg bg-white border-2 border-highlight-dark text-center style-overlay"
            @done="word = undefined"
        />
    </div>
</template>

<script>
import Vue from "vue";
import RenderWordMapPopupComponent from "components/RenderWordMapPopup.component.vue";
import MapLayerToggleComponent from "./MapLayerToggle.component.vue";
import ZoomToLanguageComponent from "components/ZoomToLanguage.component.vue";
import ContributeComponent from "./Contribute.component.vue";

import mapboxgl from "mapbox-gl";
import { mapBoxStyle, accessToken } from "../configuration";
mapboxgl.accessToken = accessToken;
import { debounce, throttle, map, orderBy, shuffle, uniq } from "lodash";

export default {
    components: {
        ContributeComponent,
        MapLayerToggleComponent,
        ZoomToLanguageComponent,
        RenderWordMapPopupComponent,
    },
    data() {
        return {
            popup: undefined,
            emptyWordsLanguageLayerShowing: true,
            showContributeDialog: false,
            debouncedRenderLanguageLayers: debounce(this.renderLanguageLayers, 200),
            debouncedRenderWordLayer: debounce(this.renderWordLayer, 200),
            debouncedCenterMap: debounce(this.centerMap, 1000),
            debouncedLayerUpdate: debounce(this.layerUpdate, 200),
            layerProperties: {
                withData: {
                    color: "#c44d2b",
                },
                withoutData: {
                    zoomedOut: {
                        color: "#ffffff",
                        opacity: 0.6,
                    },
                    zoomedIn: {
                        color: "#2d3748",
                        opacity: 0.6,
                    },
                },
            },
            word: undefined,
        };
    },
    computed: {
        mapHeight: function () {
            return `${window.innerHeight - 200}px`;
        },
        languagesWithData: function () {
            return this.$store.state.languages.filter((l) => l.properties.words);
        },
        languagesWithoutData: function () {
            return this.$store.state.languages.filter((l) => !l.properties.words);
        },
        selection: function () {
            return this.$store.getters.getSelection();
        },
        layer: function () {
            return this.$store.state.layer;
        },
        flyToCoordinates: function () {
            return this.$store.state.flyTo;
        },
        playAll: function () {
            return this.$store.state.playAll;
        },
        smallDevice: function () {
            return window.innerWidth < 768 ? true : false;
        },
    },
    watch: {
        layer: function () {
            if (this.layer === "languages") {
                this.debouncedRenderLanguageLayers();
            } else {
                this.debouncedRenderWordLayer();
            }
        },
        selection: function (n) {
            setTimeout(() => {
                if (this.selection.type === "word") {
                    this.debouncedRenderWordLayer();
                } else if (this.selection.type === "language") {
                    if (this.selection?.data?.geometry?.coordinates) {
                        this.flyTo({
                            coordinates: this.selection.data.geometry.coordinates,
                        });
                    }
                } else {
                    this.debouncedCenterMap();
                }
            }, 300);
        },
        flyToCoordinates: function () {
            if (this.flyToCoordinates?.word?.geometry?.coordinates) {
                this.flyTo({
                    coordinates: this.flyToCoordinates.word.geometry.coordinates,
                });
            }
        },
    },
    mounted() {
        setTimeout(() => {
            this.renderMap();
        }, 200);
    },
    methods: {
        async centerMap() {
            this.map.resize();

            // if (this.popup) this.popup.remove();
            // centerCountry({ map: this.map });
            // let position;
            // if ("geolocation" in navigator) {
            //     try {
            //         position = await new Promise((resolve, reject) => {
            //             navigator.geolocation.getCurrentPosition(
            //                 (position) => resolve(position),
            //                 (error) => reject(error)
            //             );
            //         });
            //     } catch (error) {
            //         centerCountry({ map: this.map });
            //     }
            //     // const latitude  = position.coords.latitude;
            //     // const longitude = position.coords.longitude;

            //     // Melbourne
            //     // position = [144.948743, -37.790136];
            //     if (position) {
            //         position = [
            //             position.coords.longitude,
            //             position.coords.latitude,
            //         ];
            //         centerLocation({ map: this.map, position });
            //     } else {
            //         centerCountry({ map: this.map });
            //     }
            // } else {
            //     centerCountry({ map: this.map });
            // }

            centerCountry({ map: this.map });

            function centerCountry({ map }) {
                map.fitBounds([
                    [96, -45],
                    [168, -8],
                ]);
            }

            // function centerLocation({ map, position }) {
            //     map.flyTo({
            //         center: position,
            //         zoom: window.innerwidth < 768 ? 8 : 6,
            //         bearing: 0,
            //     });
            // }
        },
        renderMap() {
            this.map = new mapboxgl.Map({
                container: this.$refs.map,
                style: mapBoxStyle,
                dragRotate: false,
                touchPitch: false,
                center: [0, 0],
            });
            if (this.smallDevice) {
                // this.map.addControl(new mapboxgl.FullscreenControl());
            } else {
                this.map.addControl(
                    new mapboxgl.NavigationControl({
                        showCompass: false,
                    })
                );
            }
            this.debouncedCenterMap();
            this.map.on("load", () => {
                this.addLanguageLayerSources();
                this.renderLanguageLayers();
                this.addLanguageLayerEventHandlers();
            });
            this.map.on("moveend", () => {
                const flyToState = this.$store.state.flyTo;
                if (flyToState?.word && !flyToState.state.play) {
                    this.$store.commit("flyTo", {
                        ...flyToState,
                        state: {
                            play: true,
                        },
                    });
                }
            });
            this.map.on("zoom", () => {
                this.debouncedLayerUpdate();
            });
        },
        addLanguageLayerSources() {
            this.map.addSource("languagesWithData", {
                type: "geojson",
                data: {
                    type: "FeatureCollection",
                    features: this.languagesWithData,
                },
            });
            this.map.addSource("languagesWithoutData", {
                type: "geojson",
                data: {
                    type: "FeatureCollection",
                    features: this.languagesWithoutData,
                },
            });
        },
        addLanguageLayerEventHandlers() {
            // languages with data event handlers
            this.map.on("click", "languagesWithData", (e) => {
                const language = e.features[0].properties;
                this.$store.dispatch("loadLanguage", { code: language.code });
            });
            this.map.on("mouseenter", "languagesWithData", () => {
                this.map.getCanvas().style.cursor = "pointer";
            });
            this.map.on("mouseleave", "languagesWithData", () => {
                this.map.getCanvas().style.cursor = "";
            });

            // languages without data event handlers
            this.map.on("mouseenter", "languagesWithoutData", () => {
                const zoomLevel = this.map.getZoom();
                if (zoomLevel > 5.5) {
                    this.map.getCanvas().style.cursor = "pointer";
                }
            });
            this.map.on("mouseleave", "languagesWithoutData", () => {
                this.map.getCanvas().style.cursor = "";
            });
            this.map.on("click", "languagesWithoutData", (e) => {
                const zoomLevel = this.map.getZoom();
                if (zoomLevel > 5.5) {
                    this.showContributeDialog = true;
                }
            });
        },
        addWordLayerEventHandlers() {
            // word event handlers
            this.map.on("mouseenter", "words", () => {
                this.map.getCanvas().style.cursor = "pointer";
            });
            this.map.on("mouseleave", "words", () => {
                this.map.getCanvas().style.cursor = "";
            });
            this.map.on("click", "words", (e) => {
                const properties = e.features[0].properties;
                if (properties.audio) properties.audio = JSON.parse(properties.audio);
                if (properties.video) properties.video = JSON.parse(properties.video);
                properties.language = JSON.parse(properties.language);
                if (!this.smallDevice) {
                    this.word = { ...properties };
                }

                // const RenderWordClass = Vue.extend(RenderWordMapPopupComponent);
                // const popupInstance = new RenderWordClass({
                //     propsData: {
                //         word: properties,
                //     },
                // });

                // if (this.popup) this.popup = this.popup.remove();
                // this.popup = new mapboxgl.Popup({
                //     maxWidth: "none",
                // })
                //     .setText("popup")
                //     .setLngLat(e.lngLat)
                //     .addTo(this.map);
                // .setHTML('<divid="vue-popup-content"></div>')
                // popupInstance.$mount("#popup-content");
                // this.popup._update();
            });
        },
        renderLanguageLayers() {
            this.map.resize();
            if (this.map.getLayer("words")) {
                this.map.removeLayer("words");
                this.map.removeSource("words");
            }
            this.renderLanguagesWithData();
            this.renderLanguagesWithoutData({});
            if (this.smallDevice) {
                this.toggleLayerWithoutData();
            }
        },
        renderLanguagesWithData() {
            if (!this.map.getLayer("languagesWithData")) {
                this.map.addLayer({
                    id: "languagesWithData",
                    type: "symbol",
                    source: "languagesWithData",
                    paint: {
                        "text-color": this.layerProperties.withData.color,
                    },
                    layout: {
                        visibility: "visible",
                        "text-field": "{name}",
                        "text-size": 16,
                        "text-max-width": 40,
                        "text-allow-overlap": true,
                        "icon-allow-overlap": true,
                    },
                });
            }
        },
        renderLanguagesWithoutData() {
            if (!this.map.getLayer("languagesWithoutData")) {
                this.map.addLayer(
                    {
                        id: "languagesWithoutData",
                        type: "symbol",
                        source: "languagesWithoutData",
                        paint: {
                            "text-color": this.layerProperties.withoutData.zoomedOut.color,
                            "text-opacity": this.layerProperties.withoutData.zoomedOut.opacity,
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
                    "languagesWithData"
                );
            }
        },
        renderWordLayer() {
            this.map.resize();

            if (this.map.getLayer("languagesWithData")) {
                this.map.removeLayer("languagesWithData");
            }
            if (this.map.getLayer("languagesWithoutData")) {
                this.map.removeLayer("languagesWithoutData");
            }

            if (this.map.getLayer("words")) {
                this.map.removeLayer("words");
                this.map.removeSource("words");
            }
            const words = this.$store.getters.getSelectionData()?.words;
            if (!words) return;
            this.map.addSource("words", {
                type: "geojson",
                data: {
                    type: "FeatureCollection",
                    features: words,
                },
            });
            this.map.addLayer({
                id: "words",
                type: "symbol",
                source: "words",
                paint: {
                    "text-color": this.layerProperties.withData.color,
                },
                layout: {
                    "text-field": "{indigenous}",
                    "text-size": 15,
                    "text-max-width": 40,
                    "text-allow-overlap": true,
                    "icon-allow-overlap": true,
                    "text-variable-anchor": ["top", "bottom", "left", "right"],
                },
            });
            this.addWordLayerEventHandlers();
        },
        flyTo({ coordinates }) {
            this.map.flyTo({
                center: coordinates,
                zoom: 7,
                bearing: 0,
            });
        },
        toggleLayerWithoutData() {
            if (this.emptyWordsLanguageLayerShowing) {
                this.map.setLayoutProperty("languagesWithoutData", "visibility", "none");
                this.emptyWordsLanguageLayerShowing = false;
            } else {
                this.renderLanguagesWithoutData();
                this.map.setLayoutProperty("languagesWithoutData", "visibility", "visible");
                this.emptyWordsLanguageLayerShowing = true;
            }
        },
        layerUpdate() {
            if (this.$store.state.layer !== "languages") return;
            if (!this.map.getLayer("languagesWithoutData")) return;
            const zoomLevel = this.map.getZoom();
            if (zoomLevel < 5.5) {
                this.map.setPaintProperty(
                    "languagesWithoutData",
                    "text-opacity",
                    this.layerProperties.withoutData.zoomedOut.opacity
                );
                this.map.setPaintProperty(
                    "languagesWithoutData",
                    "text-color",
                    this.layerProperties.withoutData.zoomedOut.color
                );
            } else {
                this.map.setPaintProperty(
                    "languagesWithoutData",
                    "text-color",
                    this.layerProperties.withoutData.zoomedIn.color
                );
                this.map.setPaintProperty(
                    "languagesWithoutData",
                    "text-opacity",
                    this.layerProperties.withoutData.zoomedIn.opacity
                );
            }
        },
        hideLanguagesWithoutData() {
            if (this.map.getLayer("languagesWithoutData")) {
                this.map.setLayoutProperty("languagesWithoutData", "visibility", "none");
            }
        },
        showLanguagesWithoutData() {
            if (this.map.getLayer("languagesWithoutData")) {
                this.map.setLayoutProperty("languagesWithoutData", "visibility", "visible");
            }
        },
    },
};
</script>

<style lang="scss" scoped></style>

<style lang="scss">
.style-overlay {
    width: 400px;
}

.mapboxgl-popup-tip {
}

.mapboxgl-popup-content {
    text-align: center;
    width: unset;
    padding: 15px 25px;
    font-size: 0.8em;
    white-space: nowrap;
}

.mapboxgl-popup-close-button {
    display: none;
}

.mapboxgl-ctrl-top-right {
    margin: -5px calc(100vw - 45px) 0 0;
}

@media (min-width: 768px) {
    .mapboxgl-ctrl-top-right {
        margin: 41px 6px 0 0;
    }
    .mapboxgl-popup-content {
        text-align: center;
        font-size: 1.2em;
    }
}

@media (min-width: 1024px) {
    .mapboxgl-ctrl-top-right {
        margin: 41px 6px 0 0;
    }
    .mapboxgl-popup-content {
        text-align: center;
        font-size: 1.5em;
    }
}
</style>
