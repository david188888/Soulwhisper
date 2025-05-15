<template>
  <view class="privacy-container">
    <view class="privacy-item">
      <text>Receive Push Notifications</text>
      <switch :checked="notificationEnabled" @change="toggleNotification" color="#8A2BE2" />
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      notificationEnabled: true
    }
  },
  methods: {
    toggleNotification(e) {
      this.notificationEnabled = e.detail.value
      // Call backend API to save settings
      uni.showToast({
        title: this.notificationEnabled ? 'Notifications enabled' : 'Notifications disabled',
        icon: 'none'
      })
    }
  }
}
</script>

<style lang="scss">
page {
  background-color: #fff;
}

.privacy-container {
  padding: 0 20px;
  
  .privacy-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #f5f5f5;
    
    text {
      font-size: 16px;
      color: #333;
    }
  }
}
</style> 