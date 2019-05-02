<template>
    <div>
        <div v-if="isCollapsed">Select</div>
        <div v-if="!isCollapsed"></div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            collapsed: true
        };
    }
};
</script>

<style lang="scss" scoped>
</style>

