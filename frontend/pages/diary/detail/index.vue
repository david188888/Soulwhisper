<template>
  <view class="detail-container">
    <!-- diary content -->
    <view class="content">
      <text>{{content}}</text>
    </view>
    
    <!-- media content -->
    <view class="media" v-if="mediaUrl">
      <image
        v-if="mediaType === 'image'"
        :src="mediaUrl"
        mode="widthFix"
        class="media-content"
      />
      <video
        v-else-if="mediaType === 'video'"
        :src="mediaUrl"
        class="media-content"
      />
    </view>
    
    <!-- mood indicator -->
    <view class="mood-indicator">
      <view class="mood-type">
        <text>{{getMoodEmoji}}</text>
      </view>
      <view class="mood-intensity">
        <text>Intensity: {{(mood.intensity * 10).toFixed(0)}}%</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      content: '',
      mediaUrl: '',
      mediaType: '',
      mood: {
        type: '',
        intensity: 0
      }
    }
  },
  
  computed: {
    getMoodEmoji() {
      const moodEmojis = {
        happy: '😊',
        sad: '😢',
        angry: '😠'
      };
      return moodEmojis[this.mood.type] || '😐';
    }
  },

  onLoad(options) {
      const record = JSON.parse(decodeURIComponent(options.data));
      console.log('detail====',record);
      this.content = record.content;
      this.mood.type = record.emotion_type;
      this.mood.intensity = record.emotion_intensity;
      this.mediaUrl = record.mediaUrl;
      this.mediaType = record.mediaType;
  },

  onBackPress() {
    uni.switchTab({
      url: '/frontend/pages/tabbar/tabbar-1/tabbar-1'
    });
    return true;
  }
}
</script>

<style lang="scss">
.detail-container {
  min-height: 100vh;
  background-color: #fff;
  padding: 20px;
  box-sizing: border-box;
  
  .content {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
    max-width: 280px;
  }
  
  .media {
    margin-bottom: 20px;
    
    .media-content {
      width: 100%;
      border-radius: 8px;
    }
  }
  
  .mood-indicator {
    position: fixed;
    top: 44px;
    right: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .mood-type {
      font-size: 24px;
      margin-bottom: 4px;
    }
    
    .mood-intensity {
      font-size: 12px;
      color: #666;
    }
  }
}
</style> 