<template>
	<view class="container">
		<!-- 顶部幸运关键词区域 -->
		<view class="header">
			<text class="keyword">🌟 Today's Lucky Keyword：</text>
			<view class="healing-section">
				<text class="sentence">✨ Healing phrases：</text>
				<text class="activity">🌈 Recommended Healing Activities：</text>
			</view>
		</view>
		
		<!-- 顶部小部件 -->
		<view class="nav-bar">
			<button class="nav-btn" @click="navigate('record')">
					<span>🎤</span>
				<text class="nav-text"> New Record</text>
			</button>
			<button class="nav-btn" @click="navigate('bottle')">
				<span>📮</span>
				<text class="nav-text"> Message Bottle</text>
			</button>
			<button class="nav-btn" @click="navigate('aichat')">
				<span>🤖 </span>
				<text class="nav-text"> AI Chat</text>
			</button>
		</view>

		<!-- 情绪日历 -->
		<view class="calendar">
			<text class="month">Mood Calendar</text>
			
			<uni-calendar
			:start-date="'2025-1-1'"
			:end-date="'2025-5-31'"
			 :month-names="enLocale.monthNames"
			  :week-days="enLocale.weekDays"
			@change="change"
			 />
			
		</view>
		
	</view>
</template>

<script>
export default {
	data() {
		return {
			enLocale: {
			  monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
			  weekDays: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
			},
		};
	},
	methods: {
		navigate(page) {
			uni.navigateTo({
				url: `/pages/home-3-detial/${page}/${page}`
			});
		}
	}
};
</script>

<style scoped>
.container {
	padding: 20px;
	background-color: #f8fafc;
	min-height: 100vh;
}

.header {
	  background-image: linear-gradient(135deg, #a559f7 0%, #62a3fa 100%);
	  padding: 20px;
	  border-radius: 12px;
	  margin-bottom: 30px;
}

.keyword {
	font-size: 18px;
	color: #2c3e50;
	font-weight: 600;
	display: block;
	margin-bottom: 15px;
	color: white;
}

.healing-section text {
	display: block;
	margin: 8px 0;
	font-size: 14px;
	color: white;;
}

.calendar {
	background: white;
	border-radius: 12px;
	padding: 10px;
	box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.month {
	font-size: 16px;
	font-weight: bold;
	color: #2d3748;
	display: block;
	margin-bottom: 12px;
}

.nav-bar {
	margin-bottom: 20px;
	left: 0;
	right: 0;
	display: flex;
	justify-content: space-around;
	padding: 10px;
	background: linear-gradient(145deg, #f8f9fa, #ffffff);
	  box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
	  backdrop-filter: blur(8px);
	  border-radius: 20px;
}

.nav-btn {
	display: flex;
	flex-direction: column;
	justify-content: center;
	background: white;
	border: none;
	padding: 8px 15px;
	font-size: 12px;
	width:90px;
	height:90px
}
.nav-text {
	  font-size: 11px;
	  color: #4a5568;
	  font-weight: 500;
	  text-shadow: 0 1px 2px rgba(0,0,0,0.05);
	}
</style>
