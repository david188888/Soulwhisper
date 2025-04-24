<template>
  <view class="register-container">
    <view class="register-box">
      <view class="logo">
        <image src="\frontend\static\img\logo.jpg" mode="aspectFit"></image>
      </view>
      
      <view class="title">Create an Account</view>
      
      <view class="form">
        <view class="input-group">
          <uni-icons type="person" size="20" color="#8A2BE2"></uni-icons>
          <input 
            type="text" 
            v-model="username" 
            placeholder="Please enter username"
            class="input"
          />
        </view>
        
        <view class="input-group">
          <uni-icons type="locked" size="20" color="#8A2BE2"></uni-icons>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password" 
            placeholder="Please enter password"
            class="input"
          />
          <uni-icons 
            :type="showPassword ? 'eye-filled' : 'eye-slash-filled'" 
            size="20" 
            color="#8A2BE2"
            @click="togglePasswordVisibility"
          ></uni-icons>
        </view>
        
        <view class="input-group">
          <uni-icons type="locked" size="20" color="#8A2BE2"></uni-icons>
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="confirmPassword" 
            placeholder="Please confirm your password"
            class="input"
          />
        </view>

        
        <view class="gender-group">
          <text class="gender-label">gender：</text>
          <view class="gender-options">
            <view 
              class="gender-option" 
              :class="{ active: sex === 'male' }"
              @click="sex = 'male'"
            >
              <text>male</text>
            </view>
            <view 
              class="gender-option" 
              :class="{ active: sex === 'female' }"
              @click="sex = 'female'"
            >
              <text>female</text>
            </view>
            <view 
              class="gender-option" 
              :class="{ active: sex === 'other' }"
              @click="sex = 'other'"
            >
              <text>others</text>
            </view>
          </view>
        </view>
        
        <button 
          class="register-btn" 
          :disabled="!isFormValid"
          @click="handleRegister"
        >
          register
        </button>
        
        <view class="login-link">
          Already have an account?
          <text class="link" @click="goToLogin">Login now!</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { api } from '../../components/api/apiPath';

export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      name: '',
      sex: '',
      showPassword: false
    }
  },
  
  computed: {
    isFormValid() {
      return this.username && 
             this.password && 
             this.confirmPassword && 
             this.sex && 
             this.password === this.confirmPassword
    }
  },
  
  methods: {
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    
    validateForm() {
      if (!this.username) {
        uni.showToast({
          title: 'please input the username',
          icon: 'none'
        })
        return false
      }
      
      if (!this.password) {
        uni.showToast({
          title: 'please input the password',
          icon: 'none'
        })
        return false
      }
      
      if (!this.confirmPassword) {
        uni.showToast({
          title: 'please confirm the password',
          icon: 'none'
        })
        return false
      }
      
      if (this.password !== this.confirmPassword) {
        uni.showToast({
          title: 'the two passwords are not consistent',
          icon: 'none'
        })
        return false
      }
      
      if (!this.sex) {
        uni.showToast({
          title: 'please select gender',
          icon: 'none'
        })
        return false
      }
      
      return true
    },
    
    async handleRegister() {
      if (!this.validateForm()) {
        return
      }
      
      try {
        const response = await uni.request({
          url: api.register,
          method: 'POST',
          header: {
            'content-type': 'application/json',
            'Accept': 'application/json'
          },
          data: {
            username: this.username,
            password: this.password,
            name: this.name || this.username,
            sex: this.sex
          }
        })
        
        if (response.statusCode === 201) {
          uni.showToast({
            title: 'register success',
            icon: 'success'
          })
          
          setTimeout(() => {
            uni.redirectTo({
              url: '/pages/login/index'
            })
          }, 1500)
        } else {
          const errorMsg = response.data?.detail || 'register failed, please try again';
          console.error('register failed:', errorMsg);
          uni.showToast({
            title: errorMsg,
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('注册请求错误:', error);
        uni.showToast({
          title: '网络错误，请稍后重试',
          icon: 'none'
        });
      }
    },
    
    goToLogin() {
      uni.navigateTo({
        url: '/frontend/pages/login/index'
      })
    }
  }
}
</script>

<style lang="scss">
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%);
  padding: 20px;
  
  .register-box {
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
        border-radius: 10px;
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
      
      .gender-group {
        margin-bottom: 20px;
        
        .gender-label {
          font-size: 16px;
          color: #333;
          margin-bottom: 10px;
          display: block;
        }
        
        .gender-options {
          display: flex;
          gap: 10px;
          
          .gender-option {
            flex: 1;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f5f5f5;
            border-radius: 12px;
            font-size: 16px;
            color: #666;
            transition: all 0.3s;
            
            &.active {
              background: #8A2BE2;
              color: #fff;
            }
            
            &:active {
              opacity: 0.8;
            }
          }
        }
      }
      
      .register-btn {
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
      
      .login-link {
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