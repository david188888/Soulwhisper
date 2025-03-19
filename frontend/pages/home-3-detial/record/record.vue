<template>
	<view class="record-page">
	  <!-- 导航栏 -->
	  <view class="custom-nav">
		<view class="left-btn" @tap="handleBack">
		  <text class="iconfont icon-back">&#xe679;</text>
		</view>
		<view class="center-title">
		  <text>录音日记</text>
		</view>
		<view class="right-btn"></view>
	  </view>
	  
	  <!-- 录音组件 -->
	  <view class="content">
		<voice-recorder></voice-recorder>
	  </view>
	</view>
  </template>
  
  <script>
  import VoiceRecorder from '@/frontend/components/VoiceRecorder.vue'
  
  export default {
	components: {
	  VoiceRecorder
	},
	
	onShow() {
	  // 隐藏底部导航栏
	  uni.hideTabBar();
	},
	
	onHide() {
	  // 离开页面时显示底部导航栏
	  uni.showTabBar();
	},
  
	methods: {
	  handleBack() {
		// 返回上一页
		uni.navigateBack({
		  delta: 1,
		  fail: () => {
			// 如果返回失败（没有上一页），则跳转到首页
			uni.switchTab({
			  url: '/frontend/pages/tabbar/tabbar-1/tabbar-1'
			});
		  }
		});
	  }
	}
  }
  </script>
  
  <style lang="scss">
  .record-page {
	min-height: 100vh;
	background-color: #f8f8f8;
	
	.custom-nav {
	  position: fixed;
	  top: 0;
	  left: 0;
	  right: 0;
	  height: 44px;
	  background-color: #fff;
	  display: flex;
	  align-items: center;
	  padding: 0 15px;
	  z-index: 100;
	  
	  .left-btn {
		width: 44px;
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
		
		.iconfont {
		  font-size: 20px;
		  color: #333;
		}
	  }
	  
	  .center-title {
		flex: 1;
		text-align: center;
		font-size: 18px;
		color: #333;
		
		text {
		  font-weight: 500;
		}
	  }
	  
	  .right-btn {
		width: 44px;
		height: 44px;
	  }
	}
	
	.content {
	  margin-top: 44px;
	  padding: 20px;
	}
  }
  
  /* 字体图标 */
  @font-face {
	font-family: 'iconfont';
	src: url('data:font/woff2;charset=utf-8;base64,d09GMgABAAAAAAKAAAsAAAAABlAAAAI0AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHFQGYACCcApcdgE2AiQDCAsGAAQgBYRnBzYbpQXInpo8KVKUNpHs/0fCDd97QUiqWDV3d0kW12pEqEwmFEKFyKQzIROe0Hj+38e9L4YsTlJNJhNNk0ymhEjxQoVCoTohVEgkJEJ9/ptzL0BCOJ3O6YH+vgO0yPyW5TLXoC7qxQEFOjZGkVWQxA1jF7zAjwkM6pYqsbe6fYIpY7YKxLk0JZiG86GMlFJQqNmzMcYDFepSn9IjwH38/fgvholKUmVm6+HpxQCWv3RvD8oW/xegIQI46XOQsYQUYq82T6UYxksNRqkmxl7V4Ev3/79ltiJr9S+PkFVm1QbQg07Il+5SmAR8aVaC4JhZBQbvgB1wvLPpqFqRZjIvp3bOk/nxccPo7vMhM/p2PtwO1kd7d0PG9+/Xd/fukVvDR2/uQUhXj3tVnr2vkt4/6C7fXnV5/PgFfJQO//c3d/Yvf3nZN/5p6er3X6UAnprGf27s4H/NLgT4r7/RAn5rLvx2KoWtzlBVYGYHOEQZgPzrG6ogf0yVYVKVIakYQlY1TlO4JVTqLaOm6gCDFu0fHtKjRIkR5cDCGwChzSaSZh+RtbmkKdwHKvX5Q003FA36SnLHkGHxjE4TqUNR4B/UHaEUpdwj5y+YmotIqZXkb5gYJYjLPPI3zEgOLNk1UR1hQRxjjvuYc7FEKc7QGdwjxnGEIp3Ccd5Qr1cq3h5lSHIYcRqR5EEhgfcD6RyCSqJIdw/y+QtMmiYEKdMvlN5gRFHZg3E5j/gbzKE0wCPLzRYdoYLYQ5mG8zHOiUoQKeowyCngHorhsAhK6EjIJ55BerpKP71dZfz8FgzMa2ZkFBe9NsfsOAAAAA==') format('woff2');
  }
  
  .iconfont {
	font-family: "iconfont" !important;
	font-style: normal;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
  }
  
  .icon-back:before {
	content: "\e679";
  }
  </style> 