<!--
 * @Author: mahaoxiang mahaoxiang@xiaomi.com
 * @Date: 2025-03-27 19:42:54
 * @LastEditors: mahaoxiang mahaoxiang@xiaomi.com
 * @LastEditTime: 2025-05-11 17:33:46
 * @FilePath: \Soulwhisper\frontend\pages\diary\publish\index.vue
 * @Description: This is the default setting. Please set it`customMade`, open koroFileHeader to check the configuration for Settings: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <view class="publish-container">
    <!-- diary content area -->
    <view class="content-area">
      <textarea
        v-model="content"
        placeholder="Write your diary here..."
        :maxlength="-1"
        auto-height
      />
    </view>
    
    <!-- media area -->
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
    
    <!-- bottom toolbar -->
    <view class="toolbar">
      <view class="media-picker" @click="chooseMedia">
        <uni-icons type="plusempty" size="24" color="#8A2BE2"></uni-icons>
      </view>
    </view>
    
    <!-- publish button -->
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
      content: '', // diary content
      mediaUrl: '', // media file path
      mediaType: '', // media type: image/video
      audioPath: '', // audio file path
      mood: {
        type: '', // emotion type
        intensity: 0 // emotion intensity
      },
      record: null // voice recognition result
    }
  },
  
  onLoad(options) {
    try {
      this.record = JSON.parse(decodeURIComponent(options.data));
      console.log('parsed record:',this.record); // debug
      this.processAudio(this.record);
  } catch (e) {
    console.error('parse failed:', e);
  }
  },
  
  methods: {
    // Process audio files
    processAudio(record) {
      uni.showLoading({
        title: 'Processing audio...',
        mask: true,
        duration: 200
      });
    
        this.content = record.text
        console.log('current content:', this.content); 
        this.mood = {
          type: record.emotion_type,
          intensity: record.emotion_intensity
        };
        uni.hideLoading();
      
    },
    
    // choose media file
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
    
    // choose image
    chooseImage() {
      uni.chooseImage({
        count: 1,
        success: (res) => {
          this.mediaUrl = res.tempFilePaths[0];
          this.mediaType = 'image';
        }
      });
    },
    
    // choose video
    chooseVideo() {
      uni.chooseVideo({
        maxDuration: 60,
        success: (res) => {
          this.mediaUrl = res.tempFilePath;
          this.mediaType = 'video';
        }
      });
    },
    
    // delete media file
    deleteMedia() {
      this.mediaUrl = '';
      this.mediaType = '';
    },
    
    // publish diary
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
    // construct request data
    const requestData = {
      content: this.content, // diary content
      emotion_type: this.mood.type, // emotion type
      emotion_intensity: this.mood.intensity, // emotion intensity
      mediaType: this.mediaType, // media type
      mediaUrl: this.mediaUrl, // media file path
    };
    const token = uni.getStorageSync('token'); // get token from storage

    // send request
    const res = await uni.request({
      url: api.dairyCreate,
      method: 'POST',
      data: requestData,
      header: {
        'Authorization': `Token ${token}` 
      }
    });

    // handle response
    if (res.statusCode === 200 || res.statusCode === 201) {
      uni.hideLoading();
      uni.showToast({
        title: 'Publish success!😄',
        icon: 'success',
        duration: 1500,
        success: () => {
          // navigate to diary detail page
          uni.navigateTo({
                url: `/frontend/pages/diary/detail/index?data=${encodeURIComponent(JSON.stringify(requestData))}`
          });
        }
      });
    } else {
      throw new Error(res.data.message || 'Publish failed');
    }
  } catch (err) {
    uni.hideLoading();
    uni.showToast({
      title: err.message || 'Network error',
      icon: 'none'
    });
    console.error('publish diary failed:', err);
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