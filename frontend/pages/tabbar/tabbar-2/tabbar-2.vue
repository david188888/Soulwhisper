<template>
	<view class="container">
		<view class="header">
			<text class="title">This Week's Emotion Report</text>
		</view>

		<view class="card">
			<text class="subtitle">Emotional Keyword Cloud</text>
			<view class="word-cloud-container">
				<image v-if="wordcloudImage" :src="'data:image/png;base64,' + wordcloudImage" mode="aspectFit" class="word-cloud-image"/>
				<view v-else class="loading">Loading...</view>
			</view>
		</view>

		<view class="card">
			<text class="subtitle">Mood Distribution</text>
			<view class="charts-box">
				<qiun-data-charts 
					type="pie"
					:opts="opts"
					:chartData="chartData"
				/>
			</view>
		</view>

		<view class="ai-bubble" @click="goToAIChat">
			<image src="/static/ai-bubble.png" mode="aspectFill" class="ai-bubble-icon"/>
		</view>
	</view>
</template>

<script>
import { api } from '../../../components/api/apiPath';
// 你需要确保已安装qiun-data-charts组件，并已在pages.json中全局注册
	export default {
		data() {
			return {
				wordcloudImage: '',
			chartData: {},
			opts: {
				color: ["#1890FF","#91CB74","#FAC858","#EE6666","#73C0DE","#3CA272","#FC8452","#9A60B4","#ea7ccc"],
				padding: [5,5,5,5],
				enableScroll: false,
				extra: {
					pie: {
						activeOpacity: 0.5,
						activeRadius: 10,
						offsetAngle: 0,
						labelWidth: 15,
						border: true,
						borderWidth: 3,
						borderColor: "#FFFFFF",
						linearType: "custom"
					}
				}
			},
			emotionConfig: {
				happy: { label: 'happy' },
				angry: { label: 'angry' },
				sad: { label: 'sad' },
				neutral: { label: 'neutral' }
				}
			}
		},
		onShow() {
		this.fetchStatistics();
		},
		methods: {
			
			async fetchStatistics() {
				try {
					const token = uni.getStorageSync('token')
					if (!token) {
						uni.showToast({
							title: 'Please log in first',
							icon: 'none'
						})
						return
					}

					const response = await uni.request({
						url: api.diaryStatistics,
						method: 'GET',
						header: {
							'Authorization': `Token ${token}`,
							'content-type': `application/json`
						}
					});
					
					if (response.statusCode === 200 && response.data) {
						const data = response.data;
						this.wordcloudImage = data.wordcloud;
						const emotionStats = data.emotion_stats || {};
					// 组装饼图数据
					this.chartData = {
						series: [
							{
								data: Object.entries(emotionStats).map(([type, count]) => {
							const config = this.emotionConfig[type] || {};
							return {
										name: config.label || type,
										value: count
									}
								})
							}
						]
					};
					} else {
						throw new Error(response.data?.error || 'fail to fetch data');
					}
				} catch (error) {
					console.error('fail to fetch statistics:', error);
					uni.showToast({
						title: error.message || 'network error',
						icon: 'none'
					});
				}
			},
			goToAIChat() {
				uni.navigateTo({
					url: '/frontend/pages/home-3-detial/aichat/aichat'
				});
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

.loading {
	color: #999;
	font-size: 28rpx;
}

.charts-box {
	width: 100%;
	height: 300px;
}

.ai-bubble {
	position: fixed;
	right: 20px;
	bottom: 25%;
	width: 56px;
	height: 56px;
	background: #fff;
	border-radius: 50%;
	box-shadow: 0 4px 16px rgba(0,0,0,0.15);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 999;
	cursor: pointer;
	transition: box-shadow 0.2s;
}
.ai-bubble:active {
	box-shadow: 0 2px 8px rgba(0,0,0,0.10);
}
.ai-bubble-icon {
	width: 32px;
	height: 32px;
}
</style>
