<template>
	<view class="container">
		<view class="header">
			<text class="title">本周情绪报告</text>
		</view>

		<view class="card">
			<text class="subtitle">情绪关键词云</text>
			<view class="word-cloud-container">
				<image v-if="wordcloudImage" :src="'data:image/png;base64,' + wordcloudImage" mode="aspectFit" class="word-cloud-image"/>
				<view v-else class="loading">加载中...</view>
			</view>
		</view>

		<view class="card">
			<text class="subtitle">心情分布</text>
			<view class="emotion-stats">
				<view v-for="(emotion, index) in emotions" :key="index" class="emotion-item">
					<view class="emotion-row">
						<view class="emotion-icon-box" :style="{ backgroundColor: emotion.color }">
							<text class="emotion-icon">{{emotion.icon}}</text>
						</view>
						<text class="emotion-name">{{emotion.label}}</text>
						<text class="emotion-percentage">{{emotion.percentage}}%</text>
					</view>
					<view class="progress-bar" :style="{ width: emotion.percentage + '%', backgroundColor: emotion.color }"></view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				wordcloudImage: '',
				emotions: [],
				emotionConfig: {
					happy: { label: '乐', icon: '😊', color: '#FFB74D' },
					angry: { label: '怒', icon: '😠', color: '#FF7043' },
					sad: { label: '哀', icon: '😢', color: '#4FC3F7' },
					neutral: { label: '乐', icon: '😊', color: '#81C784' }
				}
			}
		},
		onShow() {
			this.fetchStatistics()
		},
		methods: {
			async fetchStatistics() {
				try {
					const token = uni.getStorageSync('token')
					if (!token) {
						uni.showToast({
							title: '请先登录',
							icon: 'none'
						})
						return
					}

					const response = await uni.request({
						url: 'http://localhost:8000/api/diary/statistics/',
						method: 'GET',
						header: {
							'Authorization': `Token ${token}`
						}
					});
					
					if (response.statusCode === 200 && response.data) {
						const data = response.data;
						this.wordcloudImage = data.wordcloud;
						
						// 处理情绪数据
						const emotionStats = data.emotion_stats || {};
						const total = Object.values(emotionStats).reduce((a, b) => a + b, 0);
						
						this.emotions = Object.entries(emotionStats).map(([type, count]) => {
							const config = this.emotionConfig[type] || {};
							const percentage = total > 0 ? Math.round((count / total) * 100) : 0;
							return {
								type,
								label: config.label || type,
								icon: config.icon || '😐',
								color: config.color || '#999',
								percentage
							};
						});
					} else {
						throw new Error(response.data?.error || '获取数据失败');
					}
				} catch (error) {
					console.error('获取统计数据失败:', error);
					uni.showToast({
						title: error.message || '网络请求失败',
						icon: 'none'
					});
				}
			}
		}
	}
</script>

<style>
.container {
	padding: 30rpx;
	background-color: #F8F9FD;
	min-height: 100vh;
}

.header {
	margin-bottom: 30rpx;
}

.title {
	font-size: 36rpx;
	font-weight: bold;
	color: #333;
}

.card {
	background-color: #FFFFFF;
	border-radius: 20rpx;
	padding: 30rpx;
	margin-bottom: 30rpx;
	box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.subtitle {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 20rpx;
	display: block;
}

.word-cloud-container {
	width: 100%;
	height: 300rpx;
	display: flex;
	justify-content: center;
	align-items: center;
	background-color: #FFFFFF;
	border-radius: 12rpx;
	overflow: hidden;
}

.word-cloud-image {
	width: 100%;
	height: 100%;
	object-fit: contain;
}

.emotion-stats {
	margin-top: 20rpx;
}

.emotion-item {
	margin-bottom: 30rpx;
}

.emotion-row {
	display: flex;
	align-items: center;
	margin-bottom: 10rpx;
}

.emotion-icon-box {
	width: 50rpx;
	height: 50rpx;
	border-radius: 25rpx;
	display: flex;
	justify-content: center;
	align-items: center;
	margin-right: 20rpx;
}

.emotion-icon {
	font-size: 28rpx;
}

.emotion-name {
	flex: 1;
	font-size: 28rpx;
	color: #333;
}

.emotion-percentage {
	font-size: 28rpx;
	color: #666;
	margin-left: 20rpx;
}

.progress-bar {
	height: 6rpx;
	border-radius: 3rpx;
	transition: width 0.3s ease;
}

.loading {
	color: #999;
	font-size: 28rpx;
}
</style>
