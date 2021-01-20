<template>
    <div>
        <div :ref="reference.button" class="text-2xl cursor-pointer" @click="toggleInformation">
            <i class="fas fa-info-circle"></i>
        </div>
        <div :ref="reference.template" style="display: none;">
            <div
                class="bg-highlight-dark text-white style-information-panel p-4 rounded-lg flex flex-col space-y-4"
                v-if="selection"
            >
                <div class="flex flex-col space-y-4">
                    <div v-if="selection.speaker.name">
                        <div>
                            Recordings provided by:
                        </div>
                        <div>- {{ selection.speaker.name }}</div>
                    </div>
                    <span v-if="selection.thankyou">
                        <div>Thanks also to:</div>
                        <div>- {{ selection.thankyou }}</div>
                    </span>
                    <span>
                        You can find more information about this language in the
                        <a :href="austLangLink" target="_blank" class="underline">
                            AustLang website.
                        </a>
                    </span>
                    <span v-if="selection.weblink">
                        See also:
                        <a :href="selection.weblink" target="_blank" class="underline">
                            {{ selection.weblink }}
                        </a>
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import tippy, { roundArrow } from "tippy.js";
import "tippy.js/dist/svg-arrow.css";
import { loadLanguageMetadata } from "src/data-loader.service.js";

export default {
    props: {
        code: {
            type: String,
        },
        offset: {
            type: Array,
            default: () => {
                return [0, 10];
            },
        },
    },
    data() {
        return {
            selection: undefined,
            reference: {
                button: this.code,
                template: `template_${this.code}`,
            },
        };
    },
    mounted() {},
    computed: {
        austLangLink: function() {
            return `https://collection.aiatsis.gov.au/austlang/language/${this.selection?.code}`;
        },
    },
    methods: {
        async loadLanguage() {
            let type = this.$store.state.selection.type;
            let selection = this.$store.getters.getSelectionData();
            if (type === "word") {
                selection = await loadLanguageMetadata({ code: this.code });
            }
            this.selection = selection.properties;
        },
        async toggleInformation() {
            await this.loadLanguage();
            const instance = tippy(this.$refs[this.reference.button], {
                trigger: "manual",
                content: this.$refs[this.reference.template].innerHTML,
                interactive: true,
                appendTo: document.body,
                allowHTML: true,
                placement: "right-start",
                offset: this.offset,
                arrow: roundArrow,
            });
            instance.show();
        },
    },
};
</script>

<style lang="scss" scoped>
.style-information-panel {
    width: 300px;
}
@media screen and (min-width: 768px) {
    .style-information-panel {
        width: 500px;
    }
}
</style>

<style lang="scss">
.tippy-svg-arrow {
    fill: #c44d2b;
}
</style>
