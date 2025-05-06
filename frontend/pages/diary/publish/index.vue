<!--
 * @Author: mahaoxiang mahaoxiang@xiaomi.com
 * @Date: 2025-03-27 19:42:54
 * @LastEditors: mahaoxiang mahaoxiang@xiaomi.com
 * @LastEditTime: 2025-05-06 23:32:53
 * @FilePath: \Soulwhisper\frontend\pages\diary\publish\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <view class="publish-container">
    <!-- 日记内容区域 -->
    <view class="content-area">
      <textarea
        v-model="content"
        placeholder="Write your diary here..."
        :maxlength="-1"
        auto-height
      />
    </view>
    
    <!-- 媒体区域 -->
    <view class="media-area" v-if="mediaUrl">
      <image
        v-if="mediaType === 'image'"
        :src="mediaUrl"
        mode="aspectFill"
        class="media-preview"
      />
      <video
        v-else-if="mediaType === 'video'"
        :src="mediaUrl"
        class="media-preview"
      />
      <view class="delete-media" @click="deleteMedia">×</view>
    </view>
    
    <!-- 底部工具栏 -->
    <view class="toolbar">
      <view class="media-picker" @click="chooseMedia">
        <uni-icons type="plusempty" size="24" color="#8A2BE2"></uni-icons>
      </view>
    </view>
    
    <!-- 发布按钮 -->
    <view class="publish-button" @click="publishDiary">
      <text>Publish</text>
    </view>
  </view>
</template>

<script>
import { api } from '../../../components/api/apiPath';
export default {
  data() {
    return {
      content: '', // 日记内容
      mediaUrl: '', // 媒体文件路径
      mediaType: '', // 媒体类型：image/video
      audioPath: '', // 语音文件路径
      mood: {
        type: '', // 情绪类型
        intensity: 0 // 情绪强度
      },
      record: null // 语音识别结果
    }
  },
  
  onLoad(options) {
    try {
      this.record = JSON.parse(decodeURIComponent(options.data));
      console.log('解析后的 record:',this.record); // 调试用
      this.processAudio(this.record);
  } catch (e) {
    console.error('解析fail:', e);
  }
  },
  
  methods: {
    // 处理音频文件
    processAudio(record) {
      uni.showLoading({
        title: 'Processing audio...',
        mask: true,
        duration: 200
      });
    
        this.content = record.text
        console.log('当前 content:', this.content); 
        this.mood = {
          type: record.emotion_type,
          intensity: record.emotion_intensity
        };
        uni.hideLoading();
      
    },
    
    // 选择媒体文件
    chooseMedia() {
      uni.showActionSheet({
        itemList: ['Photo', 'Video'],
        success: (res) => {
          if (res.tapIndex === 0) {
            this.chooseImage();
          } else {
            this.chooseVideo();
          }
        }
      });
    },
    
    // 选择图片
    chooseImage() {
      uni.chooseImage({
        count: 1,
        success: (res) => {
          this.mediaUrl = res.tempFilePaths[0];
          this.mediaType = 'image';
        }
      });
    },
    
    // 选择视频
    chooseVideo() {
      uni.chooseVideo({
        maxDuration: 60,
        success: (res) => {
          this.mediaUrl = res.tempFilePath;
          this.mediaType = 'video';
        }
      });
    },
    
    // 删除媒体文件
    deleteMedia() {
      this.mediaUrl = '';
      this.mediaType = '';
    },
    
    // 发布日记
    async publishDiary() {
  if (!this.content.trim()) {
    uni.showToast({
      title: 'Please write something',
      icon: 'none'
    });
    return;
  }

  uni.showLoading({
    title: 'Publishing...',
    mask: true
  });

  try {
    // 构造请求数据
    const requestData = {
      content: this.content, // 日记内容
      emotion_type: this.mood.type, // 情绪类型
      emotion_intensity: this.mood.intensity, // 情绪强度
      mediaType: this.mediaType, // 媒体类型
      mediaUrl: this.mediaUrl, // 媒体文件路径
    };
    const token = uni.getStorageSync('token'); // 或从 Vuex 获取

    // 发起请求
    const res = await uni.request({
      url: api.createDiary, // 替换为你的实际 API 地址
      method: 'POST',
      data: requestData,
      header: {
        'Content-Type': 'text/plain',
        'Authorization': `Token ${token}` 
      }
    });

    // 处理响应
    if (res.statusCode === 200 || res.statusCode === 201) {
      uni.hideLoading();
      uni.showToast({
        title: '发布成功',
        icon: 'success',
        duration: 1500,
        success: () => {
          // 跳转到日记详情页
          uni.navigateTo({
                url: `/frontend/pages/diary/detail/index?data=${encodeURIComponent(JSON.stringify(requestData))}`
          });
        }
      });
    } else {
      throw new Error(res.data.message || '发布失败');
    }
  } catch (err) {
    uni.hideLoading();
    uni.showToast({
      title: err.message || '网络错误',
      icon: 'none'
    });
    console.error('发布日记失败:', err);
  }
}
  }
}
</script>

<style lang="scss">
.publish-container {
  min-height: 100vh;
  background-color: #fff;
  padding: 20px;
  box-sizing: border-box;
  
  .content-area {
    margin-bottom: 20px;
    
    textarea {
      width: 70%;
      min-height: 200px;
      font-size: 16px;
      line-height: 1.6;
      padding: 0;
    }
  }
  
  .media-area {
    position: relative;
    margin-bottom: 20px;
    
    .media-preview {
      width: 200rpx;
      height: 200rpx;
      border-radius: 8px;
    }
    
    .delete-media {
      position: absolute;
      top: -10px;
      right: -10px;
      width: 24px;
      height: 24px;
      background-color: rgba(0, 0, 0, 0.5);
      color: #fff;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }
  }
  
  .toolbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px 20px;
    background-color: #fff;
    border-top: 1px solid #f5f5f5;
    
    .media-picker {
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
  
  .publish-button {
    position: fixed;
    top: 44px;
    right: 20px;
    padding: 8px 20px;
    background-color: #8A2BE2;
    color: #fff;
    border-radius: 20px;
    font-size: 14px;
  }
}
</style> 