<template>
    <div>
        <button @click="currentView = 'PTZConfig'">云台设置</button>
        <button @click="currentView = 'ImageOffset'">图像偏移设置</button>
        <button @click="currentView = 'PTZMoveConfig'">云台控制参数设置</button>
        <button @click="currentView = 'ModelConfig'">模型文件管理</button>
        <button @click="currentView = 'PresetConfig'">预制信息管理</button>
        <button @click="currentView = 'WebrtcPlayer'">测试视频</button>
        <!-- <button @click="currentView = 'OtherConfig2'">Other Config 2</button> -->

        <component :is="currentViewComponent"></component>
    </div>
</template>

<script>
import ImageOffset from './ImageOffset.vue';
import PTZConfig from './PTZConfig.vue';
import PTZMoveConfig from './PTZMoveConfig.vue';
import ModelConfig from './ModelConfig.vue';
import PresetConfig from './PresetConfig.vue';
import WebrtcPlayer from './WebrtcPlayer.vue';
// import other components here
// import OtherConfig1 from './OtherConfig1.vue';
// import OtherConfig2 from './OtherConfig2.vue';

export default {
    components: {
        ImageOffset,
        PTZConfig,
        PTZMoveConfig,
        ModelConfig,
        PresetConfig,
        WebrtcPlayer
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
                case 'PresetConfig':
                    return 'PresetConfig';
                case 'WebrtcPlayer':
                    return 'WebrtcPlayer';
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