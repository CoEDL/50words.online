<template>
    <div class="flex flex-col">
        <video controls class="hidden md:block">
            <source :src="helpVideoDesktop" type="video/mp4" />
        </video>
        <video controls class="block md:hidden">
            <source :src="helpVideoPhone" type="video/mp4" />
        </video>
    </div>
</template>

<script>
import helpVideoDesktop from "src/assets/help_video_desktop.mp4";
import helpVideoPhone from "src/assets/help_video_phone.mp4";
export default {
    data() {
        return {
            helpVideoDesktop,
            helpVideoPhone,
        };
    },
};
</script>
