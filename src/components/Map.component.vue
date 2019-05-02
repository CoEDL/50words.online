<template>
    <div>
        <div id="map" class="style-map"></div>
    </div>
</template>

<script>
import mapboxgl from "mapbox-gl";
mapboxgl.accessToken =
    "pk.eyJ1IjoibWFyY29sYXJvc2EiLCJhIjoiY2pvM2pjMW9kMHhmODNxcmxsMTd2cWkzcCJ9.jpWvN4mzM5M6ijwkSI2CfA";
import { throttle, map } from "lodash";

export default {
    data() {
        return {};
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
                paint: {
                    "text-color": "#f15a22"
                },
                layout: {
                    "text-field": "{name}"
                }
            });
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
</style>


