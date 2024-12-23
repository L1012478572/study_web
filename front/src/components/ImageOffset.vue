<template>
    <div>
        <label for="x_offset">X 位置偏移:</label>
        <input type="number" v-model="x_offset" id="x_offset" step="0.01" />

        <label for="y_offset">Y 位置偏移:</label>
        <input type="number" v-model="y_offset" id="y_offset" step="0.01" />

        <label for="w_coefficient">宽度系数:</label>
        <input type="number" v-model="w_coefficient" id="w_coefficient" step="0.01" />

        <label for="h_coefficient">高度系数:</label>
        <input type="number" v-model="h_coefficient" id="h_coefficient" step="0.01" />

        <label for="x_rect">X 坐标范围:</label>
        <input type="number" v-model="x_rect" id="x_rect" step="0.01" />

        <label for="y_rect">Y 坐标范围:</label>
        <input type="number" v-model="y_rect" id="y_rect" step="0.01" />

        <label for="x_min">X 最小值:</label>
        <input type="number" v-model="x_min" id="x_min" step="0.01" />

        <label for="y_min">Y 最小值:</label>
        <input type="number" v-model="y_min" id="y_min" step="0.01" />

        <label for="x_max">X 最大值:</label>
        <input type="number" v-model="x_max" id="x_max" step="0.01" />

        <label for="y_max">Y 最大值:</label>
        <input type="number" v-model="y_max" id="y_max" step="0.01" />

        <button @click="saveSettings">保存</button>
        <button @click="loadSettings">读取</button>

        <p v-if="message" class="message">{{ message }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            x_offset: 0.1,
            y_offset: 0.1,
            w_coefficient: 0.9,
            h_coefficient: 0.9,
            x_rect: 0.2,
            y_rect: 0.2,
            x_min: 0.34,
            y_min: 0.18,
            x_max: 0.8,
            y_max: 0.78,
            message: '' // 添加一个状态变量来存储提示消息
        };
    },
    methods: {
        async saveSettings() {
            console.log('saveSettings called');
            const settings = {
                x_offset: this.x_offset,
                y_offset: this.y_offset,
                w_coefficient: this.w_coefficient,
                h_coefficient: this.h_coefficient,
                x_rect: this.x_rect,
                y_rect: this.y_rect,
                x_min: this.x_min,
                y_min: this.y_min,
                x_max: this.x_max,
                y_max: this.y_max
            };
            console.log('Saving settings', settings);

            // 创建XML结构
            const xmlBuilder = new XMLSerializer();
            const xmlDoc = document.implementation.createDocument('', '', null);
            const root = xmlDoc.createElement('Settings');
            for (const key in settings) {
                const element = xmlDoc.createElement(key);
                element.textContent = settings[key];
                root.appendChild(element);
            }
            xmlDoc.appendChild(root);

            // 增加换行和缩进
            const xmlString = xmlBuilder.serializeToString(xmlDoc);
            const formattedXmlString = xmlString.replace(/(>)(<)(\/*)/g, '$1\n$2$3');

            try {
                const host = window.location.hostname;
                const port = '8010'; // 你的后端端口号
                const url = `http://${host}:${port}/api/param/offsetinfo`;
                console.log(`Sending PUT request to ${url}`);
                const response = await axios.put(url, formattedXmlString, {
                    headers: {
                        'Content-Type': 'application/xml'
                    }
                });
                console.log('Response received:', response);

                this.message = '设置已保存'; // 更新提示消息
                setTimeout(() => this.message = '', 3000); // 3秒后清除提示消息
            } catch (error) {
                console.error('Error saving settings:', error);
                this.message = '保存设置失败'; // 更新提示消息
                setTimeout(() => this.message = '', 3000); // 3秒后清除提示消息
            }
        },
        async loadSettings() {
            console.log('loadSettings called');
            try {
                const host = window.location.hostname;
                const port = '8010'; // 你的后端端口号
                const url = `http://${host}:${port}/api/param/offsetinfo`;
                console.log(`Sending request to ${url}`);
                const response = await axios.get(url);
                console.log('Response received:', response);

                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(response.data, 'application/xml');

                this.x_offset = parseFloat(xmlDoc.getElementsByTagName('x_offset')[0].textContent);
                this.y_offset = parseFloat(xmlDoc.getElementsByTagName('y_offset')[0].textContent);
                this.w_coefficient = parseFloat(xmlDoc.getElementsByTagName('w_coefficient')[0].textContent);
                this.h_coefficient = parseFloat(xmlDoc.getElementsByTagName('h_coefficient')[0].textContent);
                this.x_rect = parseFloat(xmlDoc.getElementsByTagName('x_rect')[0].textContent);
                this.y_rect = parseFloat(xmlDoc.getElementsByTagName('y_rect')[0].textContent);
                this.x_min = parseFloat(xmlDoc.getElementsByTagName('x_min')[0].textContent);
                this.y_min = parseFloat(xmlDoc.getElementsByTagName('y_min')[0].textContent);
                this.x_max = parseFloat(xmlDoc.getElementsByTagName('x_max')[0].textContent);
                this.y_max = parseFloat(xmlDoc.getElementsByTagName('y_max')[0].textContent);

                this.message = '设置已读取'; // 更新提示消息
                setTimeout(() => this.message = '', 3000); // 3秒后清除提示消息
            } catch (error) {
                console.error('读取设置时出错:', error);
                this.message = '读取设置时出错'; // 更新提示消息
                setTimeout(() => this.message = '', 3000); // 3秒后清除提示消息
            }
        }
    },
    mounted() {
        this.loadSettings(); // 在组件挂载时调用loadSettings
    }
};
</script>

<style scoped>
label {
    display: block;
    margin-top: 10px;
}

input {
    margin-bottom: 10px;
}

button {
    margin-right: 10px;
}

.message {
    color: green;
    margin-top: 10px;
}
</style>