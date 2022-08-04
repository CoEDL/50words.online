<template>
    <div class="flex flex-col">
        <header-mobile-component class="px-2" />
        <div class="mt-2 p-2 text-black">
            <div v-if="$route.name === 'about'" class="overflow-scroll style-content pr-4">
                <about-component />
            </div>
            <div v-else-if="$route.name === 'help'" class="overflow-scroll style-content pr-4">
                <help-component class="p-6 border-2" />
            </div>
            <div
                v-else-if="$route.name === 'contribute'"
                class="overflow-scroll style-content pr-4"
            >
                <contribute-component />
            </div>
        </div>
    </div>
</template>

<script>
import HeaderMobileComponent from "./HeaderMobile.component.vue";
import AboutComponent from "components/About.component.vue";
import HelpComponent from "components/Help.component.vue";
import ContributeComponent from "components/Contribute.component.vue";

export default {
    components: {
        HeaderMobileComponent,
        AboutComponent,
        HelpComponent,
        ContributeComponent,
    },
    data() {
        return {};
    },
};
</script>

<style lang="scss" scoped>
.style-content {
    height: calc(100vh - 115px);
}
</style>
