<template>
  <view class="about-container">
    <image class="logo" src="/frontend/static/img/logo.jpg" mode="aspectFit"></image>
    <view class="info">
      <text class="address">South China Normal University</text>
      <text class="email" @click="copyEmail">2873804973@qq.com</text>
    </view>
  </view>
</template>

<script>
export default {
  methods: {
    copyEmail() {
      uni.setClipboardData({
        data: '2873804973@qq.com',
        success: () => {
          uni.showToast({
            title: 'Email copied',
            icon: 'success'
          })
        }
      })
    }
  }
}
</script>

<style lang="scss">
page {
  background-color: #fff;
}

.about-container {
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .logo {
    width: 400rpx;
    height: 400rpx;
    margin-bottom: 40px;
  }
  
  .info {
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .address {
      font-size: 16px;
      color: #333;
      margin-bottom: 15px;
    }
    
    .email {
      color: #8A2BE2;
      font-size: 16px;
    }
  }
}
</style> 