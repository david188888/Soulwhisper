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
				:start-date="'2025-01-01'"
				:end-date="'2025-05-31'"
				:selected="highlightDays"
				:showMonth="false"
				:lunar="false"
				:insert="true"
				@change="onCalendarChange"
				@monthSwitch="onMonthSwitch"
			/>
		</view>

		<!-- 日记内容弹出框 -->
		<uni-popup ref="diaryPopup" type="center">
			<view class="popup-content" v-if="selectedDiary">
				<view class="popup-header">
					<text class="popup-title">Diary Content</text>
					<text class="popup-date">{{ formatDate(selectedDiary.created_at) }}</text>
				</view>
				<view class="popup-emotion">
					<text class="emotion-text">Mood: {{ getEmotionEmoji(selectedDiary.emotion_type) }}</text>
					<text class="emotion-intensity">(Level: {{ selectedDiary.emotion_intensity }})</text>
				</view>
				<view class="popup-body">
					<text class="diary-content">{{ selectedDiary.content }}</text>
				</view>
			</view>
			<view class="popup-content" v-else>
				<text>No diary for this day.</text>
			</view>
		</uni-popup>
	</view>
</template>

<script>
import { api } from '../../../components/api/apiPath.js';
export default {
	data() {
		return {
			highlightDays: [],
			selectedDiary: null,
			currentYear: new Date().getFullYear(),
			currentMonth: new Date().getMonth() + 1,
			emotionEmojis: {
				happy: '😊',
				sad: '😢',
				angry: '😠',
				neutral: '😐'
			}
		};
	},
	onShow() {
		this.highlightDays = [];
		this.fetchHighlightDays(this.currentYear, this.currentMonth);
	},
	mounted() {
		this.highlightDays = [];
		this.fetchHighlightDays(this.currentYear, this.currentMonth);
	},
	methods: {
		navigate(page) {
			let url = '';
			switch(page) {
				case 'record':
					url = '/frontend/pages/home-3-detial/record/record';
					break;
				case 'bottle':
					url = '/frontend/pages/home-3-detial/bottle/bottle';
					break;
				case 'aichat':
					url = '/frontend/pages/home-3-detial/aichat/aichat';
					break;
				default:
					url = '/';
			}
			uni.navigateTo({ url });
		},
		async fetchHighlightDays(year, month) {
			try {
				const userInfo = uni.getStorageSync('userInfo');
				if (!userInfo || !userInfo.token) {
					console.error('No token found');
					uni.showToast({
						title: '请先登录',
						icon: 'none'
					});
					return;
				}

				console.log('请求高亮日期，年月:', year, month);

				const res = await uni.request({
					url: api.diaryDays + `?year=${year}&month=${month}`,
					header: {
						'Authorization': `Token ${userInfo.token}`,
						'Content-Type': 'application/json'
					},
					method: 'GET'
				});

				console.log('获取到的日期数据:', res.data);

				if (res.statusCode === 200 && Array.isArray(res.data)) {
					this.highlightDays = res.data.map(dateStr => {
						// 确保日期格式为 YYYY-MM-DD
						const [y, m, d] = dateStr.split('-');
						const formattedDate = `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`;
						console.log('处理后的日期:', formattedDate);
						return {
							date: formattedDate
						};
					});
					console.log('最终高亮日期数组:', this.highlightDays);
				} else {
					console.error('获取日期失败:', res);
					uni.showToast({
						title: '获取日期失败',
						icon: 'none'
					});
				}
			} catch (error) {
				console.error('请求错误:', error);
				console.error('错误详情:', error.message);
				uni.showToast({
					title: '网络请求失败',
					icon: 'none'
				});
				this.highlightDays = [];
			}
		},
		onCalendarChange(e) {
			const date = e.fulldate;
			this.fetchDiaryDetail(date);
		},
		onMonthSwitch(e) {
			const [year, month] = e.yearMonth.split('-');
			this.currentYear = parseInt(year);
			this.currentMonth = parseInt(month);
			this.highlightDays = [];
			this.fetchHighlightDays(this.currentYear, this.currentMonth);
		},
		async fetchDiaryDetail(date) {
			try {
				const userInfo = uni.getStorageSync('userInfo');
				if (!userInfo || !userInfo.token) {
					console.error('未找到用户token');
					uni.showToast({
						title: '请先登录',
						icon: 'none'
					});
					return;
				}

				const requestUrl = api.diaryDayDetail + `?date=${date}`;

				const res = await uni.request({
					url: requestUrl,
					header: { 
						'Authorization': `Token ${userInfo.token}`,
						'Content-Type': 'application/json'
					},
					method: 'GET'
				});

				// 检查响应状态码和数据
				if (res.statusCode === 200) {
					// 如果响应成功且有数据
					if (res.data && !res.data.error) {
						this.selectedDiary = res.data;
						this.$refs.diaryPopup.open();
						console.log('获取到的日记内容:', this.selectedDiary);
					} else {
						// 如果响应成功但没有数据
						this.selectedDiary = null;
						uni.showToast({
							title: '该日期没有日记',
							icon: 'none'
						});
					}
				} else if (res.statusCode === 400) {
					// 处理参数错误
					console.error('请求参数错误:', res.data?.error || '参数错误');
					this.selectedDiary = null;
					uni.showToast({
						title: res.data?.error || '请求参数错误',
						icon: 'none'
					});
				} else {
					// 处理其他错误
					console.error('服务器响应错误:', res.statusCode, res.data?.error);
					this.selectedDiary = null;
					uni.showToast({
						title: res.data?.error || '获取日记失败',
						icon: 'none'
					});
				}
			} catch (error) {
				console.error('获取日记详情失败:', error);
				this.selectedDiary = null;
				uni.showToast({
					title: '网络请求失败',
					icon: 'none'
				});
			}
		},
		// 格式化日期
		formatDate(dateStr) {
			const date = new Date(dateStr);
			return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
		},
		// 获取情绪对应的表情
		getEmotionEmoji(emotion) {
			return this.emotionEmojis[emotion] || '😐';
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
.popup-content {
	background: white;
	border-radius: 15px;
	padding: 20px;
	width: 80vw;
	max-width: 500px;
}
.popup-header {
	margin-bottom: 15px;
}
.popup-title {
	font-size: 18px;
	font-weight: bold;
	color: #333;
	display: block;
}
.popup-date {
	font-size: 14px;
	color: #666;
	margin-top: 5px;
	display: block;
}
.popup-emotion {
	display: flex;
	align-items: center;
	margin-bottom: 15px;
	padding: 8px;
	background: #f8f9fa;
	border-radius: 8px;
}
.emotion-text {
	font-size: 16px;
	margin-right: 10px;
}
.emotion-intensity {
	font-size: 14px;
	color: #666;
}
.popup-body {
	padding: 15px;
	background: #f8f9fa;
	border-radius: 8px;
}
.diary-content {
	font-size: 16px;
	line-height: 1.6;
	color: #333;
}
</style>
