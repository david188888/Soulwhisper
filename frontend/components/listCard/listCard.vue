<template>
	<view>
		<!-- 基础卡片 -->
		<view v-if="mode === 'base'" class="list-card">
			<view class="listcard-image">
				<image src="/frontend/static/img/logo.jpg" mode="aspectFill"></image>
			</view>
			<view class="listcard-content">
				<view class="listcard-content_title">
					<text>今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情</text>
				</view>
				<view class="listcard-content_des">
					<view class="listcard-content_des-browse">120浏览</view>
				</view>
			</view>
		</view>
        <!-- 多图卡片 -->
		<view v-if="mode === 'column'" class="list-card mode-column">
			<view class="listcard-content">
				<view class="listcard-content_title">
					<text>今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情</text>
				</view>
				<view class="listcard-image">
					<view v-for="item in 3" :key="item" class="listcard-image_item">
						<image src="/frontend/static/img/logo.jpg" mode="aspectFill"></image>
					</view>
				</view>
				<view class="listcard-content_des">
					<view class="listcard-content_des-browse">120浏览</view>
				</view>
			</view>
		</view>
		<!-- 大图卡片 -->
		<view v-if="mode === 'image'" class="list-card mode-image">
			<view class="listcard-image">
				<image src="/frontend/static/img/logo.jpg" mode="aspectFill"></image>
			</view>
			<view class="listcard-content">
				<view class="listcard-content_title">
					<text>今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情</text>
				</view>
				<view class="listcard-content_des">
					<view class="listcard-content_des-browse">120浏览</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default{
		props:{
			mode:{
				type:String,
				default:'base'
			}
		}
	}
</script>

<style lang="scss">
	.list-card{
		display: flex;
		padding: 10px;
		margin: 10px;
		border-radius: 5px;
		box-shadow: 0 0 5px 1px rgba($color:#000000, $alpha:0.1);
		box-sizing: border-box;
		.listcard-image{
			flex-shrink: 0;
			width: 60px;
			height: 60px;
			border-radius: 5px;
			overflow: hidden;
			image{
				width: 100%;
				height: 100%;
			}
		}
		.listcard-content{
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			padding-left: 10px;
			width: 100%;
			.listcard-content_title{
				font-size: 14px;
				color: #333;
				font-weight: 400;
				line-height: 1.2;
				text{
					overflow: hidden;
					text-overflow: ellipsis;
					display: -webkit-box;
					-webkit-line-clamp: 2;
					-webkit-box-orient: vertical;
				}
			}
			.listcard-content_des{
				display: flex;
				justify-content: space-between;
				font-size: 12px;
				.listcard-content_des-browse{
					color: #999;
					line-height: 1.5;
				}
			}
		}
		
		&.mode-column{
			.listcard-content{
				width: 100%;
				padding-left: 0;
			}
			.listcard-image{
				display: flex;
				margin-top: 10px;
				width: 100%;
				height: 70px;
				.listcard-image_item{
					margin-left: 10px;
					width: 100%;
					border-radius: 5px;
					overflow: hidden;
					&:first-child{
						margin-left: 0;
					}
					image{
						width: 100%;
						height: 100%;
					}
				}
			}
			.listcard-content_des{
				margin-top: 10px;
			}
		}
		&.mode-image{
			flex-direction: column;
			.listcard-image{
				width: 100%;
				height: 100px;
			}
			.listcard-content{
				padding-left: 0;
				margin-top: 10px;
				.listcard-content_des{
					display: flex;
					align-items: center;
					margin-top: 10px;
				}
			}
		}
	}
</style>