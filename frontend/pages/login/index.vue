<template>
  <view class="login-container">
    <view class="login-box">
      <view class="logo">
        <image src="\frontend\static\img\logo.jpg" mode="aspectFit"></image>
      </view>
      
      <view class="title">Welcome back</view>
      
      <view class="form">
        <view class="input-group">
          <uni-icons type="person" size="20" color="#8A2BE2"></uni-icons>
          <input 
            type="text" 
            v-model="username" 
            placeholder="Please enter user name"
            class="input"
          />
        </view>
        
        <view class="input-group">
          <uni-icons type="locked" size="20" color="#8A2BE2"></uni-icons>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password" 
            placeholder="Please enter the password"
            class="input"
          />
          <uni-icons 
            :type="showPassword ? 'eye-filled' : 'eye-slash-filled'" 
            size="20" 
            color="#8A2BE2"
            @click="togglePasswordVisibility"
          ></uni-icons>
        </view>
        
        <button 
          class="login-btn" 
          :disabled="!username || !password"
          @click="handleLogin"
        >
          Login
        </button>
        
        <view class="register-link">
          Still have no account?
          <text class="link" @click="goToRegister">Register Now</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      showPassword: false
    }
  },
  
  computed: {
    isFormValid() {
      return this.username && this.password
    }
  },
  
  methods: {
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    
    async handleLogin() {
      if (!this.username || !this.password) {
        uni.showToast({
          title: '请填写完整信息',
          icon: 'none'
        })
        return
      }
      
      try {
        const response = await uni.request({
          url: 'http://localhost:8000/api/account/login/',
          method: 'POST',
          data: {
            username: this.username,
            password: this.password
          }
        })
        
        if (response.statusCode === 200) {
          const { token, user } = response.data
          
          // 保存token和用户信息
          uni.setStorageSync('token', token)
          uni.setStorageSync('userInfo', user)
          
          // 显示成功提示
          uni.showToast({
            title: '登录成功',
            icon: 'success'
          })
          // 跳转到首页
          setTimeout(() => {
            uni.switchTab({
              url: '/frontend/pages/tabbar/tabbar-1/tabbar-1'
            })
          }, 1500)
        } else {
          throw new Error(response.data.error || '登录失败')
        }
      } catch (error) {
        uni.showToast({
          title: error.message || '登录失败，请重试',
          icon: 'none'
        })
      }
    },
    
    goToRegister() {
      uni.navigateTo({
        url: '/frontend/pages/register/index'
      })
    }
  }
}
</script>

<style lang="scss">
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%);
  padding: 20px;
  
  .login-box {
    width: 100%;
    max-width: 400px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 40px 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    
    .logo {
      text-align: center;
      margin-bottom: 20px;
      
      image {
        width: 120px;
        height: 120px;
      }
    }
    
    .title {
      font-size: 24px;
      font-weight: bold;
      color: #333;
      text-align: center;
      margin-bottom: 30px;
    }
    
    .form {
      .input-group {
        display: flex;
        align-items: center;
        background: #f5f5f5;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 20px;
        
        .input {
          flex: 1;
          margin: 0 12px;
          font-size: 16px;
        }
      }
      
      .login-btn {
        width: 100%;
        height: 50px;
        background: #8A2BE2;
        color: #fff;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 30px;
        
        &:disabled {
          background: #ccc;
        }
        
        &:active {
          opacity: 0.9;
        }
      }
      
      .register-link {
        text-align: center;
        margin-top: 20px;
        color: #666;
        font-size: 14px;
        
        .link {
          color: #8A2BE2;
          font-weight: bold;
          
          &:active {
            opacity: 0.8;
          }
        }
      }
    }
  }
}
</style> 