<template>
    <ui-modal
        ref="modal"
        title="Help"
        @close="close"
        size="large"
        :align-top="true"
        transition="fade"
    >
        <div :style="{ height: height }" class="overflow-scroll pr-6">
            <about-component />
        </div>
    </ui-modal>
</template>

<script>
import AboutComponent from "./About.component.vue";
export default {
    components: {
        AboutComponent,
    },
    props: {
        show: {
            required: true,
            type: Boolean,
        },
    },
    data() {
        return { height: `${window.innerHeight * 0.7}px` };
    },
    watch: {
        show: function(n, o) {
            if (n) {
                this.$refs.modal.open();
            }
        },
    },
    methods: {
        close() {
            this.$emit("close");
        },
    },
};
</script>
