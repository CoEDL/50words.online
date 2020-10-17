<template>
    <div v-if="word" class="mt-2 p-4">
        <div class="flex flex-col">
            <div class="flex flex-row">
                <div class="style-word text-lg md:text-xl lg:text-2xl">
                    {{ word }}
                </div>
                <div class="flex flex-grow"></div>
            </div>
            <div class="flex flex-row justify-start mt-3 pb-2">
                <play-all-controls-component
                    :map="map"
                    @center-map="$emit('center-map')"
                />
            </div>
        </div>
    </div>
</template>

<script>
import { orderBy, shuffle } from "lodash";
import { randomBytes } from "crypto";
import { stringify } from "querystring";
import AudioPlayerControl from "./AudioPlayerControl.component.vue";
import PlayAllControlsComponent from "./PlayAllControls.component.vue";

export default {
    components: {
        PlayAllControlsComponent,
    },
    props: {
        map: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {};
    },

    computed: {
        word: function() {
            return this.$store.state.selectedWord &&
                this.$store.state.selectedWord.length
                ? this.$store.state.selectedWord[0].properties.english
                : undefined;
        },
    },
};
</script>

<style lang="scss" scoped>
// @import "assets/variables.scss";

// .style-button {
//     border-color: black;
//     background-color: black;
//     color: $text-color;
// }

// .style-button-deselected {
//     color: $primary-color;
// }

// .style-word {
//     color: $text-color;
// }
// @media (min-width: 1024px) {
//     .style-selected-word {
//         font-size: 1.5em;
//         color: $text-color;
//         padding-top: 10px;
//     }
// }
</style>
