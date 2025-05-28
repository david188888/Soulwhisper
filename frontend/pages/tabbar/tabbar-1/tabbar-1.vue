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
				:end-date="'2025-12-31'"
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
					url = '/frontend/pages/tabbar/tabbar-3/tabbar-3';
					uni.switchTab({ url });
					break;
				case 'bottle':
					url = '/frontend/pages/tabbar/tabbar-4/tabbar-4';
					uni.switchTab({ url });
					break;
				case 'aichat':
					url = '/frontend/pages/home-3-detial/aichat/aichat';
					uni.navigateTo({ url });
					break;
				default:
					url = '/';
					uni.navigateTo({ url });
			}
		},
		async fetchHighlightDays(year, month) {
			try {
				const userInfo = uni.getStorageSync('userInfo');
				if (!userInfo || !userInfo.token) {
					console.error('No token found');
					uni.showToast({
						title: 'Please login first',
						icon: 'none'
					});
					return;
				}

				const res = await uni.request({
					url: api.diaryDays + `?year=${year}&month=${month}`,
					header: {
						'Authorization': `Token ${userInfo.token}`,
						'Content-Type': 'application/json'
					},
					method: 'GET'
				});


				if (res.statusCode === 200 && Array.isArray(res.data)) {
					this.highlightDays = res.data.map(dateStr => {
						// 确保日期格式为 YYYY-MM-DD
						const [y, m, d] = dateStr.split('-');
						const formattedDate = `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`;
						return {
							date: formattedDate
						};
					});

				} else {
					console.error('Failed to get dates:', res);
					uni.showToast({
						title: 'Failed to get dates',
						icon: 'none'
					});
				}
			} catch (error) {
				console.error('Request error:', error);
				console.error('Error details:', error.message);
				uni.showToast({
					title: 'Network request failed',
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
					console.error('User token not found');
					uni.showToast({
						title: 'Please login first',
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
						console.log('Retrieved diary content:', this.selectedDiary);
					} else {
						// 如果响应成功但没有数据
						this.selectedDiary = null;
						uni.showToast({
							title: 'No diary for this date',
							icon: 'none'
						});
					}
				} else if (res.statusCode === 400) {
					// 处理参数错误
					console.error('Request parameter error:', res.data?.error || 'Parameter error');
					this.selectedDiary = null;
					uni.showToast({
						title: res.data?.error || 'Request parameter error',
						icon: 'none'
					});
				} else {
					// 处理其他错误
					console.error('Server response error:', res.statusCode, res.data?.error);
					this.selectedDiary = null;
					uni.showToast({
						title: res.data?.error || 'Failed to get diary',
						icon: 'none'
					});
				}
			} catch (error) {
				console.error('Failed to get diary details:', error);
				this.selectedDiary = null;
				uni.showToast({
					title: 'Network request failed',
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
	background: #fff;
	min-height: 100vh;
	font-weight: 600;
	border: 8px solid #fff;
	border-radius: 36px;
	box-sizing: border-box;
}

.header {
	background: url('frontend/static/img/tabbar/background.jpg') no-repeat center center;
	background-size: cover;
	background-color: rgba(255, 255, 255, 0.20);
	backdrop-filter: blur(10px) saturate(180%);
	-webkit-backdrop-filter: blur(10px) saturate(180%);
	border-radius: 28px;
	box-shadow: 0 0 12px rgba(0,0,0,0.08);
	padding: 30px 38px;
	margin-bottom: 30px;
	position: relative;
	overflow: hidden;
}

.keyword {
	font-size: 22px;
	color: #222;
	font-weight: 700;
	display: block;
	margin-bottom: 18px;
	text-shadow: 0 2px 8px rgba(0,0,0,0.08);
	letter-spacing: 1px;
}

.healing-section text {
	display: block;
	margin: 8px 0;
	font-size: 13px;
	color: #222;
}

.calendar {
	background: white;
	border-radius: 24px;
	padding: 16px;
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
	padding: 14px;
	background: linear-gradient(145deg, #f8f9fa, #ffffff);
	box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
	backdrop-filter: blur(8px);
	border-radius: 28px;
	gap: 24px;
}

.nav-btn {
	display: flex;
	flex-direction: column;
	justify-content: center;
	background: white;
	border: none;
	padding: 12px 20px;
	font-size: 14px;
	width:100px;
	height:100px;
	border-radius: 24px;
	box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.nav-text {
	font-size: 12px;
	color: #222;
	font-weight: 600;
	text-shadow: 0 1px 4px rgba(0,0,0,0.06);
	margin-top: 8px;
}
.popup-content {
	background: white;
	border-radius: 28px;
	padding: 28px;
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

.nav-btn span {
	font-size: 20px;
	display: block;
	margin-bottom: 0px;
	line-height: 1
}
</style>
