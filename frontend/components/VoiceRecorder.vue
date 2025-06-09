<!--
 * @Author: mahaoxiang mahaoxiang@xiaomi.com
 * @Date: 2025-04-20 21:36:47
 * @LastEditors: mahaoxiang mahaoxiang@xiaomi.com
 * @LastEditTime: 2025-05-11 21:46:37
 * @FilePath: \Soulwhisper\frontend\components\VoiceRecorder.vue
 * @Description: This is the default setting, please set `customMade`, open koroFileHeader to view configuration for settings: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <view class="container-chat">
  <view class="voice-recorder">
    <image src="/frontend/static/img/voice.gif" class="voice-gif" />
     <!-- Recording button -->
    <view class="record-button" @tap="handleRecord" :class="{ recording: isRecording }" :style="isRecording ? 'position: fixed; bottom: 70px; left: 50%; transform: translateX(-50%); z-index: 200;' : ''">
      <uni-icons :type="isRecording ? 'stop' : 'mic-filled'" size="30" color="#8A2BE2"></uni-icons>
    </view>
    
    <!-- Recording window -->
    <view class="record-modal" v-if="isRecording">
      <view class="modal-content">
        <text class="timer">{{formatTime}}</text>
        <text class="tip">{{recordTip}}</text>
        <view class="volume-indicator">
          <view class="volume-bar" :style="{ height: volumeHeight + 'px' }"></view>
        </view>
        <canvas type="2d" class="recwave-WaveView" style="width:300px;height:100px"></canvas>
      </view>
    </view>

    <!-- Transcription result display -->
    <view class="transcript-result" v-if="transcriptText">
      <view class="result-header">
        <text class="title">Speech Transcription Result</text>
        <view class="actions">
          <button class="action-btn" @tap="editTranscript">Edit</button>
          <button class="action-btn" @tap="confirmTranscript">Confirm</button>
        </view>
      </view>
      <view class="result-content">
        <textarea v-model="transcriptText" :disabled="!isEditing" class="transcript-textarea"></textarea>
      </view>
    </view>
  </view>
</view>
</template>

<script>
import Recorder from 'recorder-core' // Can use import or require

// Must import RecordApp core file (file path is /src/app-support/app.js)
import RecordApp from 'recorder-core/src/app-support/app'

// Must import uni-app support file for all platforms (if compilation shows path error, replace @ with ../../)
import '@/uni_modules/Recorder-UniCore/app-uni-support.js'

/** When compiling to WeChat Mini Program, import WeChat Mini Program support file **/
// #ifdef MP-WEIXIN
    import 'recorder-core/src/app-support/app-miniProgram-wx-support.js'
// #endif

/** In H5 and Mini Program environments: import required format encoders and visualization plugins, in App environment import in renderjs **/
// #ifdef H5 || MP-WEIXIN
import 'recorder-core/src/engine/mp3'
import 'recorder-core/src/engine/mp3-engine' // If this format has additional encoding engine (*-engine.js), must include it

import 'recorder-core/src/extensions/waveview'
import { api } from './api/apiPath';
// #endif

export default {
  name: 'VoiceRecorder',
  
  data() {
    return {
      isMounted: false,
      waveView: null,
      isRecording: false,
      recordTime: 0,
      timer: null,
      currentVolume: 0,
      transcriptText: '',
      isEditing: false,
      recordTip: 'Click the square button to start recording',
      processTimer: null,
      isProcessing: false,
      currentRequest: null
    }
  },
  
  computed: {
    formatTime() {
      const minutes = Math.floor(this.recordTime / 60);
      const seconds = Math.floor(this.recordTime % 60);
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    },
    volumeHeight() {
      return Math.max(10, Math.min(100, this.currentVolume * 100));
    }
  },

  mounted() {
    this.isMounted = true;
    // Initialize recording functionality
    RecordApp.UniPageOnShow(this);
    // Pre-request recording permission
    this.requestPermission();
  },

  onShow() {
    if(this.isMounted) RecordApp.UniPageOnShow(this);

    // #ifdef APP-PLUS
    // App 环境下提前请求权限
    setTimeout(() => {
      try {
        const main = plus.android.runtimeMainActivity();
        const ContextCompat = plus.android.importClass('androidx.core.content.ContextCompat');
        const PackageManager = plus.android.importClass('android.content.pm.PackageManager');

        const permission = 'android.permission.RECORD_AUDIO';
        const result = ContextCompat.checkSelfPermission(main, permission);

        if (result !== PackageManager.PERMISSION_GRANTED) {
          const ActivityCompat = plus.android.importClass('androidx.core.app.ActivityCompat');
          ActivityCompat.requestPermissions(main, [permission], 1);
          console.log('Request microphone permission');
        } else {
          console.log('Microphone permission granted');
          // 已有权限，可以初始化录音
          RecordApp.UniWebViewActivate(this);
        }
      } catch (error) {
        console.error('权限检查异常:', error);
      }
    }, 1000);
    // #endif
  },

  methods: {
    goBack() {
      if (this.isRecording) {
        uni.showModal({
          title: 'Tip',
          content: 'You are recording, are you sure to return?',
          success: (res) => {
            if (res.confirm) {
              this.stopRecord();
              uni.switchTab({
                url: '/frontend/pages/tabbar/tabbar-1/tabbar-1'
              });
            }
          }
        });
      } else {
        uni.switchTab({
          url: '/frontend/pages/tabbar/tabbar-1/tabbar-1'
        });
      }
    },

    // Request recording permission
    requestPermission() {
      // #ifdef APP-PLUS
      const main = plus.android.runtimeMainActivity();
      const ContextCompat = plus.android.importClass('androidx.core.content.ContextCompat');
      const PackageManager = plus.android.importClass('android.content.pm.PackageManager');

      // Check permission status
      const permission = 'android.permission.RECORD_AUDIO';
      const result = ContextCompat.checkSelfPermission(main, permission);

      if (result !== PackageManager.PERMISSION_GRANTED) {
        // Request permission
        const ActivityCompat = plus.android.importClass('androidx.core.app.ActivityCompat');
        ActivityCompat.requestPermissions(main, [permission], 1);

        console.log("Request microphone permission");
      } else {
        console.log("Microphone permission granted");
        // Permission granted, initialize recording
        RecordApp.UniWebViewActivate(this);
        RecordApp.RequestPermission(() => {
          console.log("Recording permission granted");
        }, (msg, isUserNotAllow) => {
          console.error("Failed to request recording permission: " + msg);
        });
      }
      // #endif

      // #ifndef APP-PLUS
      RecordApp.UniWebViewActivate(this);
      RecordApp.RequestPermission(() => {
        console.log("Recording permission granted");
      }, (msg, isUserNotAllow) => {
        if(isUserNotAllow) {
          uni.showModal({
            title: 'Tip',
            content: 'Microphone permission is required to record',
            showCancel: false
          });
        }
        console.error("Failed to request recording permission: " + msg);
      });
      // #endif
    },

    handleRecord() {
      if (this.isRecording) {
        this.stopRecord();
      } else {
        // #ifdef APP-PLUS
        try {
          const main = plus.android.runtimeMainActivity();
          const ContextCompat = plus.android.importClass('androidx.core.content.ContextCompat');
          const PackageManager = plus.android.importClass('android.content.pm.PackageManager');

          const permission = 'android.permission.RECORD_AUDIO';
          const result = ContextCompat.checkSelfPermission(main, permission);

          if (result !== PackageManager.PERMISSION_GRANTED) {
            const ActivityCompat = plus.android.importClass('androidx.core.app.ActivityCompat');
            ActivityCompat.requestPermissions(main, [permission], 1);

            uni.showModal({
              title: 'Notice',
              content: 'Recording requires microphone permission. Please click "Allow" in the dialog box.',
              showCancel: false
            });
          } else {
            // Permission granted, start recording
              this.startRecord();
          }
        } catch (error) {
          console.error('Permission request error:', error);
          // If permission check fails, try to start recording directly
          this.startRecord();
        }
        // #endif
        
        // #ifndef APP-PLUS
        RecordApp.UniWebViewActivate(this);
        RecordApp.RequestPermission(() => {
          this.startRecord();
        }, (msg, isUserNotAllow) => {
          if(isUserNotAllow) {
            uni.showModal({
              title: 'Tip',
              content: 'Microphone permission is required to record',
              showCancel: false
            });
          }
          console.error("Failed to request recording permission: " + msg);
        });
            // #endif
            }
          },

    startRecord() {
      try {
        // #ifdef APP-PLUS

        RecordApp.UniWebViewActivate(this);


        RecordApp.RequestPermission(() => {
          console.log("verify permission success in APP environment");
          this.initRecording();
        }, (msg) => {
          console.error("fail to request permission in APP environment:", msg);
          this.initRecording();
        });
        return;
        // #endif


        this.initRecording();
      } catch (error) {
        console.error("Recording initialization error:", error);
        uni.showToast({
          title: 'Recording initialization error',
          icon: 'none',
          duration: 2000
        });
        this.resetRecording();
      }
    },


    initRecording() {
      try {
        const set = {
          type: "mp3",
          sampleRate: 16000,
          bitRate: 16,
          onProcess: (buffers, powerLevel, duration, sampleRate) => {
            // Update volume display
            this.currentVolume = powerLevel / 100;
            this.recordTime = Math.floor(duration/1000);
          
            // #ifdef H5 || MP-WEIXIN
            if(this.waveView) {
              this.waveView.input(buffers[buffers.length-1], powerLevel, sampleRate);
            }
            // #endif

            if(duration >= 600000) { // Auto stop after 10 minutes
              this.stopRecord();
            }
          },
          onProcess_renderjs: `function(buffers,powerLevel,duration,sampleRate){
            if(this.waveView) {
              this.waveView.input(buffers[buffers.length-1],powerLevel,sampleRate);
            }
          }`,
          start_renderjs: `function(){
            RecordApp.UniFindCanvas(this,[".recwave-WaveView"],
              "this.waveView=Recorder.WaveView({compatibleCanvas:canvas1, width:300, height:100});"
            );
          }`
        };

        // Add timeout handling
        let initTimeout = setTimeout(() => {
          uni.showToast({
            title: 'Recording initialization timeout, please try again',
            icon: 'none',
            duration: 2000
          });
          this.resetRecording();
        }, 5000);

        RecordApp.Start(set, () => {
          clearTimeout(initTimeout); // Clear timeout
          console.log("Recording started");
          this.isRecording = true;
          this.recordTime = 0;
          this.recordTip = 'Recording...';

          // create wave view code remains the same...
        }, (msg) => {
          clearTimeout(initTimeout); // Clear timeout
          console.error("Failed to start recording: " + msg);

          // More detailed error prompt
          if(msg.includes("permission")) {
            uni.showToast({
              title: 'Please grant microphone permission',
              icon: 'none',
              duration: 2000
            });
          } else {
            uni.showToast({
              title: 'Recording failed: ' + msg,
              icon: 'none',
              duration: 2000
            });
          }
          this.resetRecording();
        });
      } catch (error) {
        console.error("Recording initialization error:", error);
        uni.showToast({
          title: 'Recording initialization error',
          icon: 'none',
          duration: 2000
        });
        this.resetRecording();
      }
    },

    stopRecord() {
      if (!this.isRecording) return;

      RecordApp.Stop((arrayBuffer, duration, mime) => {
        this.isRecording = false;
        this.isProcessing = true;

        if(arrayBuffer && arrayBuffer.byteLength > 0) {
          // Show processing loading prompt
          uni.showLoading({
            title: 'Speech To Text...',
            mask: true
          });

          // Upload to ASR interface
          // Use multipart/form-data form to upload file
          const token = uni.getStorageSync('token')
          console.log('token',token)

// #ifdef H5
	//H5 directly use the browser's File interface to construct a file
	uni.uploadFile({
		url: api.asr
		,file: new File([arrayBuffer], "recorder.mp3")
		,name: "audio_file"
		,formData: {},
    header: {
    'Authorization': `Token ${token}`
    },
		success: (res) => {
      console.log('======🚀',res);
      res.data = JSON.parse(res.data);
      uni.hideLoading();
      uni.navigateTo({
        url: `/frontend/pages/diary/publish/index?data=${encodeURIComponent(JSON.stringify(res.data))}`
    });
  }
		,fail: (err)=>{ console.log('======😭',err) }
	});
// #endif

// #ifdef APP
	//App directly save binary data to local file, then upload
	RecordApp.UniSaveLocalFile("recorder.mp3", arrayBuffer, (savePath) => {
		console.log("Recording file saved:", savePath);
		const token = uni.getStorageSync('token');
		uni.uploadFile({
			url: api.asr,
			filePath: savePath,
			name: "audio_file",
			header: {
				'Authorization': `Token ${token}`
			},
			formData: {},
			success: (res) => {
				console.log('上传成功:', res);
				try {
					// parse the returned data
					let data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
					uni.hideLoading();
					uni.navigateTo({
						url: `/frontend/pages/diary/publish/index?data=${encodeURIComponent(JSON.stringify(data))}`
					});
				} catch (e) {
					console.error('Failed to parse response data:', e);
					uni.hideLoading();
					uni.showToast({
						title: 'Failed to process response',
						icon: 'none'
					});
}
			},
			fail: (err) => {
				console.error('Upload failed:', err);
				uni.hideLoading();
				uni.showToast({
					title: 'Upload failed',
					icon: 'none'
				});
			}
		});
	}, (err) => {
		console.error('Failed to save recording file:', err);
		uni.hideLoading();
		uni.showToast({
			title: 'Failed to save recording file',
			icon: 'none'
		});
	});
// #endif

// #ifdef MP-WEIXIN
	//mini program need to save binary data to local file, then upload
	var savePath=wx.env.USER_DATA_PATH+"/recorder.mp3";
	wx.getFileSystemManager().writeFile({
		filePath:savePath
		,data:arrayBuffer
		,encoding:"binary"
		,success:()=>{
			wx.uploadFile({
				url: api.asr
				,filePath: savePath
				,name: "audio_file"
				,formData: {
				}
				,success: (res) => { }
				,fail: (err)=>{ }
			});
		}
		,fail:(e)=>{  }
	});
// #endif

        } else {
          uni.showToast({
            title: 'You speek nothing?',
            icon: 'none',
            duration: 2000
          });
          this.resetRecording();
        }
      }, (msg) => {
        uni.showToast({
          title: 'Fail to record',
          icon: 'none',
          duration: 2000
        });
        this.resetRecording();
      });
    },

    editTranscript() {
      this.isEditing = true;
    },

    confirmTranscript() {
      this.isEditing = false;
      // navigate to publish page
      uni.navigateTo({
        url: `/frontend/pages/diary/publish/index?content=${encodeURIComponent(this.transcriptText)}&emotion_type=${this.emotionType}&emotion_intensity=${this.emotionIntensity}&diary_id=${this.diaryId}`
      });
    },

    // reset recording status
    resetRecording() {
      // ensure close loading prompt
      uni.hideLoading();
      
      this.isRecording = false;
      this.isProcessing = false;
      this.recordTime = 0;
      this.currentVolume = 0;
      this.recordTip = 'Click the square button to start recording';
      if (this.waveView) {
        this.waveView.clear(); // clear wave view
      }

      // clean request
      if (this.currentRequest) {
        this.currentRequest.abort();
        this.currentRequest = null;
      }
    },

    // clean up when component is destroyed
    beforeDestroy() {
      if (this.isRecording) {
        this.stopRecord();
      }
      this.resetRecording();
    }
  },

  beforeDestroy() {
    if (this.isRecording) {
      this.stopRecord();
    }
    if (this.processTimer) {
      clearTimeout(this.processTimer);
      this.processTimer = null;
    }
    if (this.currentRequest) {
      this.currentRequest.abort();
      this.currentRequest = null;
    }
  }
}
</script>

<style lang="scss">

.container-chat{
  // background-image: linear-gradient(135deg, #a559f7 0%, #62a3fa 100%);
  height: 800px;
}
.voice-recorder {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  position: relative;

  .voice-gif {
    display: block;
    margin: 0 auto;
    margin-top: 10px;
    width: 80%;
    max-width: 320px;
    height: 320px;
    object-fit: cover;
    border-radius: 24px;
    box-shadow: 0 4px 24px rgba(138, 43, 226, 0.12), 0 1.5px 6px rgba(0,0,0,0.08);
    border: 2px solid #f3eaff;
    background: #f8f6ff;
  }
  
  .record-button {
    width: 50px;
    height: 50px;
    background-color: #7fd5ecd2;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    margin-top: 30px;
    margin-left: 0;
    align-self: center;
    
    &.recording {
      border-radius: 0;
      background-color: #e22b2b;
      border-radius: 20px;
      transform: scale(1.1);
      z-index: 100;
      margin-top: 80px;
      margin-left: 0px;
      .uni-icons {
        color: #fff !important;
      }
    }
    
    &:not(.recording) {
      border-radius: 40px;
    }
  }
  .description {
    color: #fff;
    font-size: 18px;
    font-weight: 500;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .chat{
    width:320px;
    height: fit-content;
    margin-bottom:60px;
  }
  
  .record-modal {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.8);
    padding: 30px;
    z-index: 99;
    
    .modal-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      
      .timer {
        font-size: 48px;
        color: #fff;
        margin-bottom: 10px;
        font-family: monospace;
      }
      
      .tip {
        color: #fff;
        font-size: 14px;
        opacity: 0.8;
        margin-bottom: 20px;
      }

      .volume-indicator {
        width: 20px;
        height: 100px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 20px;
        overflow: hidden;
        position: relative;

        .volume-bar {
          position: absolute;
          bottom: 0;
          width: 100%;
          background-color: #8A2BE2;
          transition: height 0.1s ease;
        }
      }
      
      .recwave-WaveView {
        width: 300px;
        height: 100px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
      }
    }
  }

  .transcript-result {
    width: 100%;
    padding: 20px;
    background-color: #fff;
    border-radius: 12px;
    margin-top: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

    .result-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;

      .title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
      }

      .actions {
        display: flex;
        gap: 10px;

        .action-btn {
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 14px;
          background-color: #8A2BE2;
          color: #fff;
          border: none;

          &:active {
            opacity: 0.8;
          }
        }
      }
    }

    .result-content {
      .transcript-textarea {
        width: 100%;
        min-height: 150px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 16px;
        line-height: 1.5;
        background-color: #f9f9f9;

        &:disabled {
          background-color: #fff;
        }
      }
    }
  }
}
</style> 