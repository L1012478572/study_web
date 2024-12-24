<template>
    <div>
        <label for="x_reversal">X轴反向:</label>
        <input type="number" v-model="x_reversal" id="x_reversal" step="1" />

        <label for="y_reversal">Y轴反向:</label>
        <input type="number" v-model="y_reversal" id="y_reversal" step="1" />

        <label for="x_maxSpeed">X轴最大速度:</label>
        <input type="number" v-model="x_maxSpeed" id="x_maxSpeed" step="0.1" />

        <label for="y_maxSpeed">Y轴最大速度:</label>
        <input type="number" v-model="y_maxSpeed" id="y_maxSpeed" step="0.1" />

        <label for="x_kp">X轴P参数:</label>
        <input type="number" v-model="x_kp" id="x_kp" step="0.1" />

        <label for="x_ki">X轴I参数:</label>
        <input type="number" v-model="x_ki" id="x_ki" step="0.1" />

        <label for="x_kd">X轴D参数:</label>
        <input type="number" v-model="x_kd" id="x_kd" step="0.1" />

        <label for="y_kp">Y轴P参数:</label>
        <input type="number" v-model="y_kp" id="y_kp" step="0.1" />

        <label for="y_ki">Y轴I参数:</label>
        <input type="number" v-model="y_ki" id="y_ki" step="0.1" />

        <label for="y_kd">Y轴D参数:</label>
        <input type="number" v-model="y_kd" id="y_kd" step="0.1" />

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
            x_reversal: 0,
            y_reversal: 0,
            x_maxSpeed: 200.0,
            y_maxSpeed: 200.0,
            x_kp: 100.0,
            x_ki: 1.0,
            x_kd: 10.0,
            y_kp: 100.0,
            y_ki: 1.0,
            y_kd: 10.0,
            message: '' // 添加一个状态变量来存储提示消息
        };
    },
    methods: {
        async saveSettings() {
            console.log('saveSettings called');
            const settings = {
                x_reversal: this.x_reversal,
                y_reversal: this.y_reversal,
                x_maxSpeed: this.x_maxSpeed,
                y_maxSpeed: this.y_maxSpeed,
                x_kp: this.x_kp,
                x_ki: this.x_ki,
                x_kd: this.x_kd,
                y_kp: this.y_kp,
                y_ki: this.y_ki,
                y_kd: this.y_kd
            };
            console.log('Saving settings', settings);

            // 创建XML结构
            const xmlBuilder = new XMLSerializer();
            const xmlDoc = document.implementation.createDocument('', '', null);
            const root = xmlDoc.createElement('Control');
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
                const url = `http://${host}:${port}/api/param/ptzcontrol`;
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
                const url = `http://${host}:${port}/api/param/ptzcontrol`;
                console.log(`Sending request to ${url}`);
                const response = await axios.get(url);
                console.log('Response received:', response);

                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(response.data, 'application/xml');

                this.x_reversal = parseInt(xmlDoc.getElementsByTagName('x_reversal')[0].textContent);
                this.y_reversal = parseInt(xmlDoc.getElementsByTagName('y_reversal')[0].textContent);
                this.x_maxSpeed = parseFloat(xmlDoc.getElementsByTagName('x_maxSpeed')[0].textContent);
                this.y_maxSpeed = parseFloat(xmlDoc.getElementsByTagName('y_maxSpeed')[0].textContent);
                this.x_kp = parseFloat(xmlDoc.getElementsByTagName('x_kp')[0].textContent);
                this.x_ki = parseFloat(xmlDoc.getElementsByTagName('x_ki')[0].textContent);
                this.x_kd = parseFloat(xmlDoc.getElementsByTagName('x_kd')[0].textContent);
                this.y_kp = parseFloat(xmlDoc.getElementsByTagName('y_kp')[0].textContent);
                this.y_ki = parseFloat(xmlDoc.getElementsByTagName('y_ki')[0].textContent);
                this.y_kd = parseFloat(xmlDoc.getElementsByTagName('y_kd')[0].textContent);

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