<template>
    <div class="flex flex-col space-y-2">
        <div class="text-2xl">Learning Resources</div>
        <div class="break-normal">
            Download a set of learning activities to accompany the 50 Words map. These are designed
            for students of all ages and can be used at home or in the classroom.
        </div>
        <a
            class="text-blue-700"
            href="https://arts.unimelb.edu.au/__data/assets/pdf_file/0005/3352838/50_Words-Lockdown-activities.pdf"
            target="_blank"
            >Find out more.</a
        >
        <div class="text-2xl">How to use the site</div>
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
