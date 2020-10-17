<template>
    <div class="md:p-1 relative">
        <div ref="map" class="w-full h-full" :style="{ height }"></div>
        <render-word-map-popup-component
            v-if="currentWord"
            :word="currentWord"
            class="absolute z-10 top-0 ml-1 md:ml-4 mt-1 md:mt-4 p-1 rounded-lg bg-white border-2 border-highlight-dark text-center style-overlay"
            @done="playWord"
        />
        <div
            class="absolute z-10 top-0 right-0 mt-1 md:mt-4 mr-1 md:mr-4 h-12 rounded-lg bg-white border-2 border-highlight-dark text-center pt-2 px-6 text-gray-600 cursor-pointer"
            @click="togglePlay"
        >
            <div v-show="!play">
                <i class="fas fa-play"></i>
            </div>
            <div v-show="play">
                <i class="fas fa-pause"></i>
            </div>
        </div>
    </div>
</template>

<script>
import RenderWordMapPopupComponent from "components/RenderWordMapPopup.component.vue";

import mapboxgl from "mapbox-gl";
mapboxgl.accessToken =
    "pk.eyJ1IjoibWFyY29sYXJvc2EiLCJhIjoiY2pvM2pjMW9kMHhmODNxcmxsMTd2cWkzcCJ9.jpWvN4mzM5M6ijwkSI2CfA";
const mapBoxStyle = "mapbox://styles/marcolarosa/ckdxwicb42opj19mu7tlt23hn";
import { debounce, throttle, map, orderBy, shuffle, uniq } from "lodash";
import styles from "assets/variables.scss";
import { loadWordData } from "../data-loader.service";

export default {
    components: {
        RenderWordMapPopupComponent,
    },
    data() {
        return {
            play: true,
            layerProperties: {
                withData: {
                    color: styles.highlightDark,
                },
                withoutData: {
                    zoomedOut: {
                        color: "#ffffff",
                        opacity: 0.6,
                    },
                    zoomedIn: {
                        color: styles.gray,
                        opacity: 0.6,
                    },
                },
            },
            wordList: [],
            selectedWord: [],
            currentWord: undefined,
        };
    },
    computed: {
        smallDevice: function() {
            return window.innerWidth < 768 ? true : false;
        },
        height: function() {
            return this.smallDevice
                ? `${window.innerHeight - 100}px`
                : `${window.innerHeight - 90}px`;
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
            this.map.fitBounds([
                [96, -45],
                [168, -8],
            ]);
        },
        renderMap() {
            this.map = new mapboxgl.Map({
                container: this.$refs.map,
                style: mapBoxStyle,
                dragRotate: false,
                touchPitch: false,
                center: [0, 0],
            });
            this.centerMap();
            this.map.on("load", () => {
                setTimeout(() => {
                    this.loadWord();
                }, 500);
            });
        },
        async loadWord() {
            if (!this.wordList.length) {
                this.wordList = this.$store.getters.getWordList();
            }
            this.selectedWord = await loadWordData({
                index: this.wordList.pop().index,
            });
            this.renderWordLayer();
        },
        async renderWordLayer() {
            if (this.map.getLayer("words")) {
                this.map.removeLayer("words");
                this.map.removeSource("words");
            }
            this.map.addSource("words", {
                type: "geojson",
                data: {
                    type: "FeatureCollection",
                    features: this.selectedWord,
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
            await this.playWord();
        },
        togglePlay() {
            if (this.play) {
                this.play = false;
            } else {
                this.play = true;
                this.playWord();
            }
        },
        async playWord() {
            if (!this.play) return;
            if (!this.selectedWord.length) {
                this.loadWord();
                return;
            }
            this.currentWord = undefined;
            const word = this.selectedWord.pop();
            this.map.flyTo({
                center: word.geometry.coordinates,
                zoom: 6,
                bearing: 0,
            });
            await sleep(2000);
            this.currentWord = word.properties;

            async function sleep(time) {
                await new Promise((resolve) => setTimeout(resolve, time));
            }
        },
        flyTo({ coordinates }) {
            this.map.flyTo({
                center: coordinates,
                zoom: 7,
                bearing: 0,
            });
        },
    },
};
</script>

<style lang="scss" scoped>
.style-overlay {
    width: 250px;
}
@media (min-width: 768px) {
    .style-overlay {
        width: 400px;
    }
}
</style>

<style lang="scss">
@import "assets/variables.scss";
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
