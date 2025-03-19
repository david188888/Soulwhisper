<template>
	<view class="profile-container">
		<!-- User Info Card -->
		<view class="user-card">
			<view class="user-info">
				<view class="avatar-section">
					<view class="avatar">
						<uni-icons type="person" size="40" color="#8A2BE2"></uni-icons>
					</view>
					<view class="user-details">
						<view class="user-name-container">
							<text class="user-name">{{username}}</text>
							<text class="edit-name-btn" @click="showEditNameDialog">✍️</text>
						</view>
						<text class="diary-count">{{totalDiaries}} Diaries</text>
					</view>
				</view>
			</view>
			
			<!-- User Stats -->
			<view class="user-stats">
				<view class="stat-item">
					<text class="stat-number">{{totalDiaries}}</text>
					<text class="stat-label">Diaries</text>
				</view>
				<view class="stat-item">
					<text class="stat-number">{{totalLikes}}</text>
					<text class="stat-label">Likes</text>
				</view>
				<view class="stat-item">
					<text class="stat-number">{{totalComments}}</text>
					<text class="stat-label">Comments</text>
				</view>
			</view>
		</view>

		<!-- Function List -->
		<view class="function-list">
			<view class="function-group">
				<view class="group-title">Account Settings</view>
				<view class="function-item" @click="goToPrivacySettings">
					<view class="item-left">
						<uni-icons type="locked" size="20" color="#8A2BE2"></uni-icons>
						<text>Privacy Settings</text>
					</view>
					<uni-icons type="right" size="16" color="#999"></uni-icons>
				</view>
				<view class="function-item" @click="goToHelpCenter">
					<view class="item-left">
						<uni-icons type="help" size="20" color="#8A2BE2"></uni-icons>
						<text>Help Center</text>
					</view>
					<uni-icons type="right" size="16" color="#999"></uni-icons>
				</view>
				<view class="function-item" @click="goToAboutUs">
					<view class="item-left">
						<uni-icons type="info" size="20" color="#8A2BE2"></uni-icons>
						<text>About Us</text>
					</view>
					<uni-icons type="right" size="16" color="#999"></uni-icons>
				</view>
			</view>
			
			<view class="function-group">
				<view class="group-title">Other Features</view>
				<view class="function-item" @click="clearCache">
					<view class="item-left">
						<uni-icons type="trash" size="20" color="#8A2BE2"></uni-icons>
						<text>Clear Cache</text>
					</view>
					<text class="cache-size">{{cacheSize}}</text>
				</view>
				<view class="function-item" @click="checkUpdate">
					<view class="item-left">
						<uni-icons type="refresh" size="20" color="#8A2BE2"></uni-icons>
						<text>Check Update</text>
					</view>
					<text class="version">v{{version}}</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				totalDiaries: 28,
				totalLikes: 156,
				totalComments: 42,
				username: 'Anonymous User',
				cacheSize: '2.5MB',
				version: '1.0.0'
			}
		},
		onLoad() {
			this.getUserInfo()
		},
		methods: {
			getUserInfo() {
				// TODO: Get user info from backend
				this.username = 'Anonymous User'
				this.totalDiaries = 28
				this.totalLikes = 156
				this.totalComments = 42
			},
			
			showEditNameDialog() {
				uni.showModal({
					title: 'Edit Username',
					editable: true,
					placeholderText: 'Enter new username',
					success: (res) => {
						if (res.confirm && res.content) {
							this.validateAndUpdateUsername(res.content)
						}
					}
				})
			},
			
			validateAndUpdateUsername(newUsername) {
				if (newUsername.length > 10) {
					uni.showToast({
						title: 'Username cannot exceed 10 characters',
						icon: 'none'
					})
					return
				}
				
				if (!/^[a-zA-Z\u4e00-\u9fa5]+$/.test(newUsername)) {
					uni.showToast({
						title: 'Only letters and Chinese characters allowed',
						icon: 'none'
					})
					return
				}
				
				this.username = newUsername
				uni.showToast({
					title: 'Successfully updated',
					icon: 'success'
				})
			},
			
			goToPrivacySettings() {
				uni.navigateTo({
					url: '/frontend/pages/profile/privacy/index'
				})
			},
			
			goToHelpCenter() {
				uni.navigateTo({
					url: '/frontend/pages/profile/help/index'
				})
			},
			
			goToAboutUs() {
				uni.navigateTo({
					url: '/frontend/pages/profile/about/index'
				})
			},
			
			clearCache() {
				uni.showModal({
					title: 'Clear Cache',
					content: 'Are you sure to clear cache?',
					success: (res) => {
						if (res.confirm) {
							uni.showLoading({
								title: 'Clearing...'
							})
							setTimeout(() => {
								this.cacheSize = '0B'
								uni.hideLoading()
								uni.showToast({
									title: 'Cleared successfully',
									icon: 'success'
								})
							}, 1500)
						}
					}
				})
			},
			
			checkUpdate() {
				uni.showLoading({
					title: 'Checking...'
				})
				setTimeout(() => {
					uni.hideLoading()
					uni.showToast({
						title: 'Already up to date',
						icon: 'none'
					})
				}, 1000)
			}
		}
	}
</script>

<style lang="scss">
page {
	background-color: #f8fafc;
	height: 100%;
}

.profile-container {
	min-height: 100%;
	padding: 20px;
	
	.user-card {
		background: linear-gradient(135deg, #8A2BE2 0%, #9370DB 100%);
		border-radius: 20px;
		padding: 30px 20px;
		margin-bottom: 20px;
		box-shadow: 0 4px 15px rgba(138, 43, 226, 0.2);
		
		.user-info {
			margin-bottom: 30px;
			
			.avatar-section {
				display: flex;
				align-items: center;
				
				.avatar {
					width: 80rpx;
					height: 80rpx;
					background-color: rgba(255, 255, 255, 0.2);
					border-radius: 12rpx;
					display: flex;
					align-items: center;
					justify-content: center;
					margin-right: 20rpx;
					
					.uni-icons {
						color: #fff !important;
					}
				}
				
				.user-details {
					flex: 1;
					
					.user-name-container {
						display: flex;
						align-items: center;
						margin-bottom: 4px;
						
						.user-name {
							font-size: 24px;
							font-weight: bold;
							color: #fff;
							margin-right: 10px;
						}
						
						.edit-name-btn {
							font-size: 16px;
							padding: 4px;
							cursor: pointer;
						}
					}
					
					.diary-count {
						font-size: 14px;
						color: rgba(255, 255, 255, 0.8);
					}
				}
			}
		}
		
		.user-stats {
			display: flex;
			justify-content: space-around;
			padding-top: 20px;
			border-top: 1px solid rgba(255, 255, 255, 0.1);
			
			.stat-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				
				.stat-number {
					font-size: 24px;
					font-weight: bold;
					color: #fff;
					margin-bottom: 4px;
				}
				
				.stat-label {
					font-size: 12px;
					color: rgba(255, 255, 255, 0.8);
				}
			}
		}
	}
	
	.function-list {
		.function-group {
			background: #fff;
			border-radius: 15px;
			padding: 15px;
			margin-bottom: 20px;
			box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
			
			.group-title {
				font-size: 16px;
				font-weight: bold;
				color: #333;
				margin-bottom: 15px;
				padding-left: 10px;
				border-left: 4px solid #8A2BE2;
			}
			
			.function-item {
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 15px 0;
				border-bottom: 1px solid #f5f5f5;
				
				&:last-child {
					border-bottom: none;
				}
				
				.item-left {
					display: flex;
					align-items: center;
					
					.uni-icons {
						margin-right: 10px;
					}
					
					text {
						font-size: 16px;
						color: #333;
					}
				}
				
				.cache-size, .version {
					font-size: 14px;
					color: #999;
				}
			}
		}
	}
}
</style>
