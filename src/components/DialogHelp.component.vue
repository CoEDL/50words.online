<template>
    <ui-modal
        ref="modal"
        title="Help"
        @close="close"
        size="large"
        :align-top="true"
        transition="fade"
    >
        <help-component v-if="show" />
    </ui-modal>
</template>

<script>
import HelpComponent from "./Help.component.vue";
export default {
    components: {
        HelpComponent,
    },
    props: {
        show: {
            required: true,
            type: Boolean,
        },
    },

    data() {
        return {};
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
