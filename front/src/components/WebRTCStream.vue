<template>
  <div>
    <div v-if="streaming">
      <video ref="video" autoplay playsinline></video>
    </div>
    <div v-else>
      <p>Video stream stopped</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "WebRTCStream",
  data() {
    return {
      streaming: false,
      peerConnection: null,
    };
  },
  mounted() {
    this.startStream();
  },
  beforeUnmount() {
    this.stopStream();
  },
  methods: {
    async startStream() {
      try {
        console.log("Initializing WebRTC stream...");
        this.streaming = true;
        this.peerConnection = new RTCPeerConnection();

        const video = this.$refs.video;
        if (!video) {
          throw new Error("Video element not found");
        }

        const streamUrl = "http://192.168.31.50:8889/teststream";
        console.log("Fetching SDP offer from:", streamUrl);

        const response = await fetch(`${streamUrl}/offer`);
        if (!response.ok) {
          throw new Error(`Failed to fetch SDP: ${response.statusText}`);
        }
        const { sdp } = await response.json();

        console.log("Received SDP:", sdp);

        await this.peerConnection.setRemoteDescription(
          new RTCSessionDescription({
            type: "offer",
            sdp,
          })
        );

        const answer = await this.peerConnection.createAnswer();
        await this.peerConnection.setLocalDescription(answer);

        console.log("Local description set. Waiting for tracks...");

        this.peerConnection.ontrack = (event) => {
          console.log("Track received:", event.streams[0]);
          video.srcObject = event.streams[0];
        };

        this.peerConnection.onicecandidate = (event) => {
          if (event.candidate) {
            console.log("ICE Candidate:", event.candidate);
          }
        };
      } catch (error) {
        console.error("Error in startStream:", error);
        this.streaming = false;
      }
    },
    stopStream() {
      this.streaming = false;
      if (this.peerConnection) {
        this.peerConnection.close();
        this.peerConnection = null;
      }
    },
  },
};
</script>

<style scoped>
video {
  width: 100%;
  height: auto;
}
</style>
  