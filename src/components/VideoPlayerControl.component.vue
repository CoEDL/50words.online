<template>
    <video ref="videoElement">
        <source v-for="(file, idx) of data.videoFiles" :src="file" :key="idx" />
        Your browser does not support the <code>video</code> element.
    </video>
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
    videoFiles: [],
    loading: false,
});
const videoElement = ref(null);

onMounted(() => {
    if (ios()) {
        videoElement.value.addEventListener("loadedmetadata", () => {
            playWord();
        });
    } else {
        videoElement.value.addEventListener("canplaythrough", () => {
            playWord();
        });
    }
    videoElement.value.addEventListener("ended", endedHandler);
    videoElement.value.addEventListener("error", endedHandler);
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
        data.videoFiles = JSON.parse(props.files);
    } else {
        data.videoFiles = [...props.files];
    }
    nextTick(() => {
        videoElement.value.load();
    });
}
function playWord() {
    emit("loaded");
    data.loading = false;
    videoElement.value.play();
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
