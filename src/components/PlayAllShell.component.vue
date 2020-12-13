<template>
    <div class="flex flex-col">
        <header-component class="hidden md:flex p-2" />
        <header-mobile-component class="md:hidden px-2" />
        <div class="flex-grow mt-2 flex flex-col" :style="{ height: height }">
            <map-component class="flex-grow" />
        </div>
    </div>
</template>

<script>
import HeaderComponent from "./Header.component.vue";
import HeaderMobileComponent from "./HeaderMobile.component.vue";
import MapComponent from "./PlayAllMap.component.vue";

export default {
    components: {
        HeaderComponent,
        HeaderMobileComponent,
        MapComponent,
    },
    data() {
        return {};
    },
    computed: {
        smallDevice: function() {
            return window.innerWidth < 768 ? true : false;
        },
        height: function() {
            return this.smallDevice
                ? `${window.innerHeight - 140}px`
                : `${window.innerHeight - 90}px`;
        },
    },
    mounted() {
        this.$store.dispatch("loadData");
    },
    methods: {},
};
</script>

<style scoped lang="scss"></style>
