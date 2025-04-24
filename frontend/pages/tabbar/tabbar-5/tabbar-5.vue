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
		
		<!-- Logout Button -->
		<view class="logout-button" @click="handleLogout">
			<text>Sign Out</text>
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
				username: '',
				cacheSize: '2.5MB',
				version: '1.0.0'
			}
		},
		onLoad() {
			this.getUserInfo()
		},
		methods: {
			getUserInfo() {
				const userInfo = uni.getStorageSync('userInfo')
				if (userInfo) {
					this.username = userInfo.name || userInfo.username
				} else {
					this.username = 'Anonymous User'
				}
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
			},
			
			handleLogout() {
				uni.showModal({
					title: 'Sign Out',
					content: 'Are you sure you want to sign out?',
					success: (res) => {
						if (res.confirm) {
							// TODO: Add logout logic here
							uni.showToast({
								title: 'Signed out successfully',
								icon: 'success'
							});
							// Redirect to login page or home page
							setTimeout(() => {
								uni.reLaunch({
									url: '/frontend/pages/login/index'
								});
							}, 1500);
						}
					}
				});
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
	display: flex;
	flex-direction: column;
	height: 100vh;
	justify-content: flex-start;
	position: relative;
	
	.user-card {
		background: linear-gradient(135deg, #A18BFF 0%, #7B89F9 100%);
		border-radius: 10px;
		padding: 20px;
		margin-bottom: 10px;
		box-shadow: 0 4px 12px rgba(123, 137, 249, 0.15);
		flex: 0.4;
		
		.user-info {
			margin-bottom: 20px;
			
			.avatar-section {
				display: flex;
				align-items: center;
				margin-bottom: 25px;
				
				.avatar {
					width: 100rpx;
					height: 100rpx;
					background-color: rgba(255, 255, 255, 0.2);
					border-radius: 8rpx;
					display: flex;
					align-items: center;
					justify-content: center;
					margin-right: 15rpx;
					
					.uni-icons {
						color: #fff !important;
						font-size: 28px;
					}
				}
				
				.user-details {
					flex: 1;
					
					.user-name-container {
						display: flex;
						align-items: center;
						margin-bottom: 10px;
						
						.user-name {
							font-size: 22px;
							font-weight: bold;
							color: #fff;
							margin-right: 12px;
						}
						
						.edit-name-btn {
							font-size: 14px;
							padding: 2px;
							cursor: pointer;
						}
					}
					
					.diary-count {
						font-size: 14px;
						color: rgba(255, 255, 255, 0.9);
					}
				}
			}
		}
		
		.user-stats {
			display: flex;
			justify-content: space-between;
			padding: 0 20px;
			padding-top: 20px;
			border-top: 1px solid rgba(255, 255, 255, 0.1);
			
			.stat-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				
				.stat-number {
					font-size: 20px;
					font-weight: bold;
					color: #fff;
					margin-bottom: 8px;
				}
				
				.stat-label {
					font-size: 13px;
					color: rgba(255, 255, 255, 0.9);
				}
			}
		}
	}
	
	.function-list {
		flex: none;
		display: flex;
		flex-direction: column;
		gap: 15px;
		
		.function-group {
			background: #fff;
			border-radius: 15px;
			padding: 15px;
			box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
			
			&:first-child {
				height: 180px;
			}
			
			&:last-child {
				height: 120px;
			}
			
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
	
	.logout-button {
		position: absolute;
		bottom: 20%;
		left: 50%;
		transform: translateX(-50%);
		padding: 12px 40px;
		text-align: center;
		background: rgba(250, 6, 6, 0.1);
		border-radius: 20px;
		border: 1px solid rgba(240, 19, 19, 0.2);
		width: auto;
		transition: all 0.3s ease;
		
		text {
			color: #FF4444;
			font-size: 16px;
			font-weight: 500;
		}
		
		&:active {
			background: rgba(245, 27, 27, 0.2);
			transform: translateX(-50%) scale(0.98);
		}
	}
}
</style>
