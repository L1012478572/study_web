<template>
    <div>
        <button @click="currentView = 'PTZConfig'">云台设置</button>
        <button @click="currentView = 'ImageOffset'">图像偏移设置</button>
        <button @click="currentView = 'PTZMoveConfig'">云台控制参数设置</button>
        <button @click="currentView = 'ModelConfig'">模型文件管理</button>
        <!-- <button @click="currentView = 'OtherConfig2'">Other Config 2</button> -->

        <component :is="currentViewComponent"></component>
    </div>
</template>

<script>
import ImageOffset from './ImageOffset.vue';
import PTZConfig from './PTZConfig.vue';
import PTZMoveConfig from './PTZMoveConfig.vue';
import ModelConfig from './ModelConfig.vue';
// import other components here
// import OtherConfig1 from './OtherConfig1.vue';
// import OtherConfig2 from './OtherConfig2.vue';

export default {
    components: {
        ImageOffset,
        PTZConfig,
        PTZMoveConfig,
        ModelConfig,
        // OtherConfig1,
        // OtherConfig2
    },
    data() {
        return {
            currentView: 'PTZConfig'
        };
    },
    computed: {
        currentViewComponent() {
            switch (this.currentView) {
                case 'ImageOffset':
                    return 'ImageOffset';
                case 'PTZConfig':
                    return 'PTZConfig';
                case 'PTZMoveConfig':
                    return 'PTZMoveConfig';
                case 'ModelConfig':
                    return 'ModelConfig';
                case 'OtherConfig1':
                    return 'OtherConfig1';
                case 'OtherConfig2':
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