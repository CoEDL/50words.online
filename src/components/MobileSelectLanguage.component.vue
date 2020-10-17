<template>
    <div class="flex flex-col">
        <ui-select
            v-if="languages.length"
            help="Select a language"
            :options="languages"
            v-model="code"
            @change="displayLanguage"
        ></ui-select>
    </div>
</template>

<script>
export default {
    data() {
        return {
            code: "",
        };
    },
    computed: {
        languages: function() {
            const languages = this.$store.state.languages
                .map((language) => language.properties)
                .filter((language) => language.words)
                .map((l) => {
                    return {
                        label: l.language.name,
                        value: l.code,
                    };
                });
            return languages;
        },
    },
    methods: {
        displayLanguage(language) {
            if (!language?.value) return;
            this.$store.dispatch("loadLanguage", { code: language.value });
        },
    },
};
</script>
