<template>
    <div>
        <button @click="currentView = 'PTZConfig'">云台设置</button>
        <button @click="currentView = 'imageOffsetConfig'">图像偏移设置</button>
        <button @click="currentView = 'otherConfig2'">Other Config 2</button>

        <component :is="currentViewComponent"></component>
    </div>
</template>

<script>
import ImageOffset from './ImageOffset.vue';
// import other components here
// import OtherConfig1 from './OtherConfig1.vue';
// import OtherConfig2 from './OtherConfig2.vue';

export default {
    components: {
        ImageOffset,
        // OtherConfig1,
        // OtherConfig2
    },
    data() {
        return {
            currentView: 'imageOffsetConfig'
        };
    },
    computed: {
        currentViewComponent() {
            switch (this.currentView) {
                case 'imageOffsetConfig':
                    return 'ImageOffset';
                case 'otherConfig1':
                    return 'OtherConfig1';
                case 'otherConfig2':
                    return 'OtherConfig2';
                default:
                    return null;
            }
        }
    }
};
</script>

<style scoped>
button {
    margin-right: 10px;
}
</style>