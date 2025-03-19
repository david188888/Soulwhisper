<template>
  <view class="voice-recorder">
    <!-- 返回按钮 -->
    <view class="back-button" @tap="goBack">
      <uni-icons type="left" size="24" color="#8A2BE2"></uni-icons>
    </view>
    
    <!-- 录音按钮 -->
    <view class="record-button" @tap="startRecord" :class="{ recording: onlineConf.onlineStep === 2 }">
      <uni-icons :type="onlineConf.onlineStep === 2 ? 'stop' : 'mic-filled'" size="30" color="#8A2BE2"></uni-icons>
    </view>
    
    <!-- 录音窗口 -->
    <view class="record-modal" v-if="onlineConf.onlineStep === 2">
      <view class="modal-content">
        <text class="timer">{{formatTime}}</text>
        <text class="tip">点击方形按钮停止录音</text>
        <!-- 添加波形图显示 -->
        <canvas type="2d" class="recwave-WaveView" style="width:300px;height:100px"></canvas>
      </view>
    </view>
  </view>
</template>

<script>
//必须引入的Recorder核心
import Recorder from 'recorder-core'

//必须引入的RecordApp核心文件
import RecordApp from 'recorder-core/src/app-support/app'

//所有平台必须引入的uni-app支持文件
import '@/uni_modules/Recorder-UniCore/app-uni-support.js'

// #ifdef MP-WEIXIN
import 'recorder-core/src/app-support/app-miniProgram-wx-support.js'
// #endif

// #ifdef H5 || MP-WEIXIN
//按需引入录音格式支持文件
import 'recorder-core/src/engine/mp3'
import 'recorder-core/src/engine/mp3-engine'

//可选的插件支持项
import 'recorder-core/src/extensions/waveview'
// #endif

export default {
  name: 'VoiceRecorder',
  
  data() {
    return {
      isMounted: false,
      waveView: null,
      audioHasClicked: false,
      onlineConf: {
        onlineStep: 1, // 1 开始录音 2录音中 3结束录音
        isfinish: false,
        isRecord: false,
        tipsTime: 0
      }
    }
  },
  
  computed: {
    formatTime() {
      const minutes = Math.floor(this.onlineConf.tipsTime / 60);
      const seconds = Math.floor(this.onlineConf.tipsTime % 60);
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
  },
  
  methods: {
    // 添加返回方法
    goBack() {
      if (this.onlineConf.onlineStep === 2) {
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
      RecordApp.UniWebViewActivate(this); // App环境下必须先切换成当前页面WebView
      RecordApp.RequestPermission(() => {
        console.log("已获得录音权限，可以开始录音了");
        this.startRecording();
      }, (msg, isUserNotAllow) => {
        if(isUserNotAllow) {
          uni.showModal({
            title: '提示',
            content: '需要麦克风权限才能录音，请在设置中允许使用麦克风',
            showCancel: false
          });
        }
        console.error("请求录音权限失败：" + msg);
        this.audioHasClicked = false;
      });
    },
    
    // 开始录音
    startRecord() {
      if (this.audioHasClicked) return;
      
      switch (this.onlineConf.onlineStep) {
        case 1: // 开始录音
          this.audioHasClicked = true;
          this.onlineConf.tipsTime = 0;
          this.requestPermission();
          break;
          
        case 2: // 停止录音
          this.stopRecord();
          break;
      }
    },
    
    // 开始录音处理
    startRecording() {
      const set = {
        type: "mp3",
        sampleRate: 16000,
        bitRate: 16,
        onProcess: (buffers, powerLevel, duration, sampleRate, newBufferIdx, asyncEnd) => {
          // #ifdef H5 || MP-WEIXIN
          if(this.waveView) this.waveView.input(buffers[buffers.length-1], powerLevel, sampleRate);
          // #endif
          
          this.onlineConf.tipsTime = Math.floor(duration/1000);
          if(duration >= 600000) { // 10分钟自动停止
            this.stopRecord();
          }
        },
        onProcess_renderjs: `function(buffers,powerLevel,duration,sampleRate,newBufferIdx,asyncEnd){
          if(this.waveView) this.waveView.input(buffers[buffers.length-1],powerLevel,sampleRate);
        }`,
        start_renderjs: `function(){
          RecordApp.UniFindCanvas(this,[".recwave-WaveView"],
            "this.waveView=Recorder.WaveView({compatibleCanvas:canvas1, width:300, height:100});"
          );
        }`
      };
      
      RecordApp.UniWebViewActivate(this);
      RecordApp.Start(set, () => {
        console.log("已开始录音");
        this.onlineConf.onlineStep = 2;
        this.audioHasClicked = false;
        
        // 创建波形显示
        RecordApp.UniFindCanvas(this, [".recwave-WaveView"], `
          this.waveView=Recorder.WaveView({compatibleCanvas:canvas1, width:300, height:100});
        `, (canvas1) => {
          this.waveView = Recorder.WaveView({compatibleCanvas:canvas1, width:300, height:100});
        });
      }, (msg) => {
        console.error("开始录音失败：" + msg);
        this.audioHasClicked = false;
      });
    },
    
    // 停止录音
    stopRecord() {
      if (this.onlineConf.onlineStep !== 2) return;
      
      RecordApp.Stop((arrayBuffer, duration, mime) => {
        console.log("录音结束", duration, mime);
        this.onlineConf.onlineStep = 3;
        this.onlineConf.isfinish = true;
        
        if(arrayBuffer && arrayBuffer.byteLength > 0) {
          uni.showLoading({
            title: '处理中...',
            mask: true
          });
          
          // 上传录音文件
          uni.request({
            url: "上传接口地址", // 这里需要替换为实际的上传接口
            method: "POST",
            header: { "content-type": "application/x-www-form-urlencoded" },
            data: {
              audio: uni.arrayBufferToBase64(arrayBuffer)
            },
            success: () => {
              uni.hideLoading();
              uni.navigateTo({
                url: '/frontend/pages/diary/publish/index?content=' + encodeURIComponent('早上好')
              });
            },
            fail: (err) => {
              console.error("上传录音失败", err);
              uni.hideLoading();
              uni.showToast({
                title: '上传失败',
                icon: 'none'
              });
            }
          });
        }
      }, (msg) => {
        console.error("结束录音失败：" + msg);
        uni.showToast({
          title: '录音失败',
          icon: 'none'
        });
      });
    }
  },
  
  mounted() {
    this.isMounted = true;
    RecordApp.UniPageOnShow(this);
  },
  
  onShow() {
    if(this.isMounted) RecordApp.UniPageOnShow(this);
  },
  
  beforeDestroy() {
    if (this.onlineConf.onlineStep === 2) {
      this.stopRecord();
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
      
      .recwave-WaveView {
        width: 300px;
        height: 100px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
      }
    }
  }
}
</style> 