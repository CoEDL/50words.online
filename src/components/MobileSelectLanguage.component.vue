<template>
    <div class="flex flex-col">
        <el-select
            v-if="languages.length"
            placeholder="Select a language"
            v-model="code"
            @change="displayLanguage"
        >
            <el-option
                v-for="language in languages"
                :key="language.value"
                :label="language.label"
                :value="language.value"
            />
        </el-select>
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
        languages: function () {
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
        displayLanguage(code) {
            this.$store.dispatch("loadLanguage", { code });
        },
    },
};
</script>
