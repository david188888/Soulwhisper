<template>
	<view class="profile-container">
		<!-- User Info Area -->
		<view class="header">
			<text class="title">SoulWhisper</text>
		</view>
		
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
					<text class="diary-count">{{totalDiaries}} diaries recorded</text>
				</view>
			</view>
		</view>

		<!-- Function List -->
		<view class="function-list">
			<view class="function-item" @click="goToPrivacySettings">
				<text>Privacy Settings</text>
				<uni-icons type="right" size="16" color="#999"></uni-icons>
			</view>
			<view class="function-item" @click="goToHelpCenter">
				<text>Help Center</text>
				<uni-icons type="right" size="16" color="#999"></uni-icons>
			</view>
			<view class="function-item" @click="goToAboutUs">
				<text>About Us</text>
				<uni-icons type="right" size="16" color="#999"></uni-icons>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				totalDiaries: 28, // Default value, should get from backend
				username: 'Anonymous User'
			}
		},
		onLoad() {
			// Get user info
			this.getUserInfo()
		},
		methods: {
			// Get user information
			getUserInfo() {
				// TODO: Get user info from backend
				// Using mock data for now
				this.username = 'Anonymous User'
				this.totalDiaries = 28
			},
			
			// Show edit username dialog
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
			
			// Validate and update username
			validateAndUpdateUsername(newUsername) {
				// Validate username length
				if (newUsername.length > 10) {
					uni.showToast({
						title: 'Username cannot exceed 10 characters',
						icon: 'none'
					})
					return
				}
				
				// Validate characters (only letters and Chinese characters)
				if (!/^[a-zA-Z\u4e00-\u9fa5]+$/.test(newUsername)) {
					uni.showToast({
						title: 'Only letters and Chinese characters allowed',
						icon: 'none'
					})
					return
				}
				
				// Update username
				this.username = newUsername
				uni.showToast({
					title: 'Successfully updated',
					icon: 'success'
				})
			},
			
			// Navigate to privacy settings
			goToPrivacySettings() {
				uni.navigateTo({
					url: '/frontend/pages/profile/privacy/index'
				})
			},
			
			// Navigate to help center
			goToHelpCenter() {
				uni.navigateTo({
					url: '/frontend/pages/profile/help/index'
				})
			},
			
			// Navigate to about us
			goToAboutUs() {
				uni.navigateTo({
					url: '/frontend/pages/profile/about/index'
				})
			}
		}
	}
</script>

<style lang="scss">
page {
	background-color: #fff;
	height: 100%;
}

.profile-container {
	min-height: 100%;
	
	.header {
		padding: 20px;
		text-align: center;
		
		.title {
			font-size: 24px;
			color: #8A2BE2;
			font-weight: bold;
		}
	}
	
	.user-info {
		padding: 20px;
		margin-bottom: 20px;
		
		.avatar-section {
			display: flex;
			align-items: center;
			
			.avatar {
				width: 80rpx;
				height: 80rpx;
				background-color: #f0e6ff;
				border-radius: 12rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-right: 20rpx;
			}
			
			.user-details {
				flex: 1;
				
				.user-name-container {
					display: flex;
					align-items: center;
					margin-bottom: 4px;
					
					.user-name {
						font-size: 18px;
						font-weight: bold;
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
					color: #999;
				}
			}
		}
	}
	
	.function-list {
		padding: 0 20px;
		
		.function-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 15px 0;
			border-bottom: 1px solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			text {
				font-size: 16px;
				color: #333;
			}
		}
	}
}
</style>
