<template>
  <view class="help-container">
    <text class="help-text">If you need assistance, please send an email to:</text>
    <text class="email" @click="copyEmail">2873804973@qq.com</text>
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

.help-container {
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .help-text {
    font-size: 16px;
    color: #333;
    margin-bottom: 15px;
    text-align: center;
  }
  
  .email {
    color: #8A2BE2;
    font-size: 16px;
  }
}
</style> 