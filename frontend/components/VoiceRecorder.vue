<template>
  <view class="voice-recorder">
    <!-- 返回按钮 -->
    <view class="back-button" @tap="goBack">
      <uni-icons type="left" size="24" color="#8A2BE2"></uni-icons>
    </view>
    
    <!-- 录音按钮 -->
    <view class="record-button" @tap="handleRecord" :class="{ recording: isRecording }">
      <uni-icons :type="isRecording ? 'stop' : 'mic-filled'" size="30" color="#8A2BE2"></uni-icons>
    </view>
    
    <!-- 录音窗口 -->
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

    <!-- 转写结果展示 -->
    <view class="transcript-result" v-if="transcriptText">
      <view class="result-header">
        <text class="title">语音转写结果</text>
        <view class="actions">
          <button class="action-btn" @tap="editTranscript">编辑</button>
          <button class="action-btn" @tap="confirmTranscript">确认</button>
        </view>
      </view>
      <view class="result-content">
        <textarea v-model="transcriptText" :disabled="!isEditing" class="transcript-textarea"></textarea>
      </view>
    </view>
  </view>
</template>

<script>
import Recorder from 'recorder-core' //使用import、require都行

//必须引入的RecordApp核心文件（文件路径是 /src/app-support/app.js）
import RecordApp from 'recorder-core/src/app-support/app'

//所有平台必须引入的uni-app支持文件（如果编译出现路径错误，请把@换成 ../../ 这种）
import '@/uni_modules/Recorder-UniCore/app-uni-support.js'

/** 需要编译成微信小程序时，引入微信小程序支持文件 **/
// #ifdef MP-WEIXIN
    import 'recorder-core/src/app-support/app-miniProgram-wx-support.js'
// #endif

/** H5、小程序环境中：引入需要的格式编码器、可视化插件，App环境中在renderjs中引入 **/
// #ifdef H5 || MP-WEIXIN
import 'recorder-core/src/engine/mp3'
import 'recorder-core/src/engine/mp3-engine' //如果此格式有额外的编码引擎（*-engine.js）的话，必须要加上

import 'recorder-core/src/extensions/waveview'

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
      recordTip: '点击方形按钮开始录音',
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
    // 初始化录音功能
    RecordApp.UniPageOnShow(this);
    // 预请求录音权限
    this.requestPermission();
  },

  onShow() {
    if(this.isMounted) RecordApp.UniPageOnShow(this);
  },

  methods: {
    goBack() {
      if (this.isRecording) {
        uni.showModal({
          title: '提示',
          content: '正在录音中，确定要返回吗？',
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

    // 请求录音权限
    requestPermission() {
      RecordApp.UniWebViewActivate(this);
      RecordApp.RequestPermission(() => {
        console.log("已获得录音权限");
      }, (msg, isUserNotAllow) => {
        if(isUserNotAllow) {
          uni.showModal({
            title: '提示',
            content: '需要麦克风权限才能录音，请在设置中允许使用麦克风',
            showCancel: false
          });
        }
        console.error("请求录音权限失败：" + msg);
      });
    },

    handleRecord() {
      if (this.isRecording) {
        this.stopRecord();
      } else {
        // 再次确认权限并开始录音
        RecordApp.UniWebViewActivate(this);
        RecordApp.RequestPermission(() => {
          this.startRecord();
        }, (msg, isUserNotAllow) => {
          if(isUserNotAllow) {
            uni.showModal({
              title: '提示',
              content: '需要麦克风权限才能录音，请在设置中允许使用麦克风',
              showCancel: false
            });
          }
          console.error("请求录音权限失败：" + msg);
        });
      }
    },

    startRecord() {
      RecordApp.UniWebViewActivate(this);
      const set = {
        type: "mp3",
        sampleRate: 16000,
        bitRate: 16,
        onProcess: (buffers, powerLevel, duration, sampleRate) => {
          // 更新音量显示
          this.currentVolume = powerLevel / 100;
          this.recordTime = Math.floor(duration/1000);
          
          // #ifdef H5 || MP-WEIXIN
          if(this.waveView) {
            this.waveView.input(buffers[buffers.length-1], powerLevel, sampleRate);
          }
          // #endif

          if(duration >= 600000) { // 10分钟自动停止
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

      RecordApp.Start(set, () => {
        console.log("开始录音");
        this.isRecording = true;
        this.recordTime = 0;
        this.recordTip = '正在录音...';
        
        // 创建波形显示
        RecordApp.UniFindCanvas(this, [".recwave-WaveView"], `
          this.waveView=Recorder.WaveView({compatibleCanvas:canvas1, width:300, height:100});
        `, (canvas1) => {
          this.waveView = Recorder.WaveView({
            compatibleCanvas: canvas1,
            width: 300,
            height: 100,
            lineWidth: 2,
            linear: true,
            centerHeight: 0.5,
            drawType: 2
          });
        });
      }, (msg) => {
        console.error("开始录音失败：" + msg);
        uni.showToast({
          title: '录音失败',
          icon: 'none'
        });
      });
    },

    stopRecord() {
      if (!this.isRecording) return;

      RecordApp.Stop((arrayBuffer, duration, mime) => {
        this.isRecording = false;
        this.isProcessing = true;

        if(arrayBuffer && arrayBuffer.byteLength > 0) {
          // 显示处理中的加载提示
          uni.showLoading({
            title: '语音转写中...',
            mask: true
          });

          // 设置超时定时器
          const timeoutTimer = setTimeout(() => {
            // 如果请求还在进行中，则取消请求
            if (this.currentRequest) {
              this.currentRequest.abort();
            }
            uni.hideLoading();
            uni.showToast({
              title: '语音转写超时，请重试',
              icon: 'none',
              duration: 2000
            });
            this.resetRecording();
          }, 10000); // 10秒超时

          // 将arrayBuffer转换为Blob对象
          const blob = new Blob([arrayBuffer], { type: 'audio/mp3' });

          // 创建FormData对象
          const formData = new FormData();
          formData.append('audio_file', blob, 'recording.mp3');

          // 上传到ASR接口
          this.currentRequest = uni.request({
            url: '/api/diary/asr/',
            method: 'POST',
            data: formData,
            header: {
              'content-type': 'multipart/form-data'
            },
            success: (res) => {
              clearTimeout(timeoutTimer); // 清除超时定时器
              if (res.statusCode === 201) {
                const { text, emotion_type, emotion_intensity, diary_id } = res.data;

                // 隐藏加载提示
                uni.hideLoading();
                                // 直接跳转到日记页面
                uni.navigateTo({
                  url: `/frontend/pages/diary/publish/index?content=${encodeURIComponent(text)}&emotion_type=${emotion_type}&emotion_intensity=${emotion_intensity}&diary_id=${diary_id}`,
                  success: () => {
                    // 跳转成功后重置录音状态
                    this.resetRecording();
                  }
                });
              } else {
                throw new Error(res.data.error || '处理失败');
              }
            },
            fail: (err) => {
              clearTimeout(timeoutTimer); // 清除超时定时器
              console.error("语音转写失败", err);
              uni.hideLoading();
              uni.showToast({
                title: err.data?.error || '语音转写失败，请重试',
                icon: 'none',
                duration: 2000
              });
              this.resetRecording();
            },
            complete: () => {
              this.currentRequest = null;
            }
          });
        } else {
          uni.showToast({
            title: '录音内容为空',
            icon: 'none',
            duration: 2000
          });
          this.resetRecording();
        }
      }, (msg) => {
        uni.showToast({
          title: '录音失败',
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
      // 跳转到日记发布页面，携带所有必要参数
      uni.navigateTo({
        url: `/frontend/pages/diary/publish/index?content=${encodeURIComponent(this.transcriptText)}&emotion_type=${this.emotionType}&emotion_intensity=${this.emotionIntensity}&diary_id=${this.diaryId}`
      });
    },

    // 重置录音状态
    resetRecording() {
      // 确保关闭加载提示
      uni.hideLoading();
      
      this.isRecording = false;
      this.isProcessing = false;
      this.recordTime = 0;
      this.currentVolume = 0;
      this.recordTip = '点击方形按钮开始录音';
      if (this.waveView) {
        this.waveView.clear(); // 清除波形图
      }

      // 清理请求
      if (this.currentRequest) {
        this.currentRequest.abort();
        this.currentRequest = null;
      }
    },

    // 在组件销毁时清理
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
.voice-recorder {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
  position: relative;
  
  .back-button {
    position: absolute;
    left: 20px;
    top: 20px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 100;
    
    &:active {
      transform: scale(0.95);
    }
  }
  
  .record-button {
    width: 80px;
    height: 80px;
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    
    &.recording {
      border-radius: 0;
      background-color: #8A2BE2;
      transform: scale(1.1);
      .uni-icons {
        color: #fff !important;
      }
    }
    
    &:not(.recording) {
      border-radius: 40px;
    }
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