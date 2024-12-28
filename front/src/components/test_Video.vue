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
          this.streaming = true;
          this.peerConnection = new RTCPeerConnection();
  
          const video = this.$refs.video;
  
          // Assuming this WebRTC stream uses a signaling server (not included here).
          const streamUrl = "http://192.168.31.50:8889/teststream";
  
          // Fetch SDP offer (example only, you must use your WebRTC signaling process)
          const response = await fetch(`${streamUrl}/offer`);
          const { sdp } = await response.json();
  
          // Set remote description
          await this.peerConnection.setRemoteDescription(
            new RTCSessionDescription({
              type: "offer",
              sdp,
            })
          );
  
          // Create and send an answer back (not implemented here for simplicity)
          const answer = await this.peerConnection.createAnswer();
          await this.peerConnection.setLocalDescription(answer);
  
          // Handle incoming video track
          this.peerConnection.ontrack = (event) => {
            video.srcObject = event.streams[0];
          };
  
          // Example ICE candidate handling (signal server needed)
          this.peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
              console.log("ICE Candidate:", event.candidate);
              // Send ICE candidate to server
            }
          };
        } catch (error) {
          console.error("Error starting WebRTC stream:", error);
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
  