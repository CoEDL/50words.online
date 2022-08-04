<template>
    <div>
        <audio ref="audioElement">
            <source v-for="(file, idx) of data.audioFiles" :src="file" :key="idx" />
            Your browser does not support the <code>audio</code> element.
        </audio>
    </div>
</template>

<script setup>
import { debounce } from "lodash";
import { reactive, ref, watch, nextTick, onMounted } from "vue";

const props = defineProps({
    files: {
        type: [Array, String],
        required: true,
    },
    state: {
        type: Object,
        required: true,
    },
});
const emit = defineEmits(["loaded", "finished-playing"]);
const data = reactive({
    debouncedLoad: debounce(load, 500),
    audioFiles: [],
    loading: false,
});
const audioElement = ref(null);

onMounted(() => {
    if (ios()) {
        audioElement.value.addEventListener("loadedmetadata", () => {
            playWord();
        });
    } else {
        audioElement.value.addEventListener("canplaythrough", () => {
            playWord();
        });
    }
    audioElement.value.addEventListener("ended", endedHandler);
    audioElement.value.addEventListener("error", endedHandler);
});

watch(
    () => props.state,
    () => {
        if (props.state.play) data.debouncedLoad();
    }
);
function load() {
    data.loading = true;
    if (typeof props.files === "string" && props.files) {
        data.audioFiles = JSON.parse(props.files);
    } else {
        data.audioFiles = [...props.files];
    }

    nextTick(() => {
        audioElement.value.load();
    });
}
function playWord() {
    emit("loaded");
    data.loading = false;
    audioElement.value.play();
}
async function endedHandler() {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    emit("finished-playing");
}

function ios() {
    if (typeof window === `undefined` || typeof navigator === `undefined`) return false;

    return /iPhone|iPad|iPod/i.test(
        navigator.userAgent ||
            navigator.vendor ||
            (window.opera && opera.toString() === `[object Opera]`)
    );
}
</script>
