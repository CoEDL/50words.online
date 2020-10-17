<template>
    <ui-modal
        ref="modal"
        title="Contribute"
        @close="close"
        size="large"
        :align-top="true"
        transition="fade"
    >
        <contribute-component />
    </ui-modal>
</template>

<script>
import ContributeComponent from "./Contribute.component.vue";
export default {
    components: {
        ContributeComponent,
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
