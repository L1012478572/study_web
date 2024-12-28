<template>
  <div>
    <div class="button-container">
      <button @click="switchStream('mppstream')">切换到 mppstream</button>
      <button @click="switchStream('teststream')">切换到 teststream</button>
    </div>
    <div class="iframe-container">
      <iframe id="webrtc-iframe" :src="iframeSrc" frameborder="0" allowfullscreen></iframe>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      iframeSrc: ''
    };
  },
  mounted() {
    this.initIframe('mppstream');
  },
  methods: {
    initIframe(stream) {
      const host = window.location.hostname;
      this.iframeSrc = `http://${host}:8889/${stream}`;
      const iframe = document.getElementById('webrtc-iframe');
      iframe.style.width = '100%';
      iframe.style.height = '100%';
    },
    switchStream(stream) {
      this.initIframe(stream);
    }
  },
};
</script>

<style>
.button-container {
  margin-bottom: 10px;
}

.iframe-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}
</style>