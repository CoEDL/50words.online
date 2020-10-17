<template>
    <div>
        <div class="flex flex-col">
            <div class="text-lg md:text-xl">
                {{ word.indigenous }}
            </div>
            <div v-if="display === 'translation'" class="hover:text-white">
                <div
                    class="text-gray-600 group-hover:text-white text-sm md:text-base"
                    v-if="word.english_alternate"
                >
                    {{ word.english_alternate }}
                </div>
                <div
                    class="text-gray-600 group-hover:text-white text-sm md:text-base"
                    v-else
                >
                    {{ word.english }}
                </div>
            </div>
            <div
                v-if="display === 'languageName'"
                class="text-gray-600 group-hover:text-white text-sm md:text-base"
            >
                <div>
                    {{ word.language.name }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        word: {
            type: Object,
            required: true,
        },
        display: {
            type: String,
            required: true,
        },
    },
    data() {
        return {};
    },
};
</script>
