<template>
    <div>
        <h2>预制信息管理</h2>
        <button @click="fetchPresetList">读取预制信息列表</button>
        <ul>
            <li v-for="(preset, index) in paginatedPresets" :key="preset.id">
                <div @click="toggleExpand(index)" class="preset-header">
                    <p>预制名称: {{ preset.preset_name }} ({{ preset.id }})</p>
                    <span class="arrow">{{ expandedIndex === index ? '▼' : '▶' }}</span>
                </div>
                <div v-if="expandedIndex === index" class="preset-details">
                    <p>模型名称: {{ preset.modle_name }}</p>
                    <p>红外模型名称: {{ preset.ir_model_name }}</p>
                    <p>分类名称: {{ preset.cla_name }}</p>
                    <p>分类ID: {{ preset.cla_id }}</p>
                    <p>分数: {{ preset.score_val }}</p>
                    <p>目标ID: {{ preset.object_id }}</p>
                    <p>红外目标ID: {{ preset.ir_object_id }}</p>
                    <p>位置: {{ preset.location }}</p>
                    <p>图像通道: {{ preset.image_channel }}</p>
                    <p>是否运行红外模型: {{ preset.isRunIrModel }}</p>
                    <p>是否控制云台: {{ preset.isControlPtz }}</p>
                    <p>测温次数: {{ preset.thermal_num }}</p>
                    <button @click="editPreset(preset.id)">修改预制信息</button>
                    <button @click="deletePreset(preset.id)">删除预制信息</button>
                </div>
            </li>
        </ul>
        <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
            <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
        <button @click="addPreset">增加预制信息</button>
        <p v-if="message" class="message">{{ message }}</p>
        <presetEditModal v-if="showModal" :presetId="selectedPresetId" @close="showModal = false" />
    </div>
</template>

<script>
import axios from 'axios';
import presetEditModal from './presetEditModal.vue';

export default {
    components: {
        presetEditModal
    },
    data() {
        return {
            presets: [],
            message: '', // 添加一个状态变量来存储提示消息
            expandedIndex: null, // 添加一个状态变量来存储展开的索引
            currentPage: 1, // 当前页码
            itemsPerPage: 10, // 每页显示的条目数
            message: '',    // 添加一个状态变量来存储提示消息
            showModal: false,
            selectedPresetId: null
        };
    },
    computed: {
        paginatedPresets() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.presets.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.presets.length / this.itemsPerPage);
        }
    },
    methods: {
        async fetchPresetList() {
            try {
                const host = window.location.hostname;
                const port = '8010'; // 你的后端端口号
                const url_send = `http://${host}:${port}/api/param/presetlist`;
                const response = await axios.get(url_send);
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(response.data, 'application/xml');
                const items = xmlDoc.getElementsByTagName('Item');
                this.presets = Array.from(items).map(item => ({
                    id: item.getAttribute('id'),
                    preset_name: item.getAttribute('preset_name'),
                    modle_name: item.getAttribute('model_name'),
                    ir_model_name: item.getAttribute('ir_model_name'),
                    cla_id: item.getAttribute('cla_id'),
                    cla_name: item.getAttribute('cla_name'),
                    score_val: item.getAttribute('score_val'),
                    object_id: item.getAttribute('object_id'),
                    ir_object_id: item.getAttribute('ir_object_id'),
                    location: item.getAttribute('location'),
                    image_channel: item.getAttribute('image_channel'),
                    isRunIrModel: item.getAttribute('isRunIrModel'),
                    isControlPtz: item.getAttribute('isControlPtz'),
                    thermal_num: item.getAttribute('thermal_num')
                }));
                // 按照标号排序
                this.presets.sort((a, b) => parseInt(a.id) - parseInt(b.id));
                this.message = '预制信息列表已更新';
                setTimeout(() => this.message = '', 3000); // 3秒后清除提示消息
            } catch (error) {
                console.error('获取预制信息列表时出错:', error);
                this.message = '获取预制信息列表时出错';
                setTimeout(() => this.message = '', 3000); // 3秒后清除提示消息
            }
        },
        toggleExpand(index) {
            this.expandedIndex = this.expandedIndex === index ? null : index;
        },
        editPreset(id) {
            // 修改预制信息功能暂留
            console.log('修改预制信息', id);
            this.selectedPresetId = id;
            this.showModal = true;
        },
        deletePreset(id) {
            // 删除预制信息功能暂留
            console.log('删除预制信息', id);
        },
        addPreset() {
            // 增加预制信息功能暂留
            console.log('增加预制信息');
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        }
    },
    mounted() {
        this.fetchPresetList(); // 在组件挂载时获取预制信息列表
    }
};
</script>

<style scoped>
h2 {
    margin-bottom: 20px;
}

button {
    margin-right: 10px;
    margin-top: 10px;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin-bottom: 20px;
    border: 1px solid #ccc;
    padding: 10px;
}

.preset-header {
    display: flex;
    justify-content: space-between;
    cursor: pointer;
}

.preset-details {
    margin-top: 10px;
}

.message {
    color: green;
    margin-top: 10px;
}

.pagination {
    margin-top: 20px;
}

.arrow {
    font-size: 20px;
}
</style>