<template>
	<view>
	    <!-- 纯文字版 -->
		<view class="list-card">
			<view class="listcard-content">
				<view class="listcard-content_title">
					<text>今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情</text>
				</view>
				<view class="listcard-content_user">
					<image src="/frontend/static/img/logo.jpg" mode="aspectFill"></image>
					<text>雨后的彩虹</text>
				</view>
				<view class="listcard-content_body">
					<text>哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈</text>
				</view>
				<view class="listcard-content_des">
					<view class="listcard-content_des-browse">120浏览</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
</script>

<style lang="scss">
	.list-card{
		display: flex;
		padding: 10px;
		margin: 10px;
		border-radius: 5px;
		box-shadow: 0 0 5px 1px rgba($color:#000000, $alpha:0.1);
		box-sizing: border-box;
		.listcard-content{
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			padding-left: 10px;
			width: 100%;
			.listcard-content_title{
				font-size: 20px;
				color: #333;
				font-weight: 600;
				line-height: 1.2;
				text{
					overflow: hidden;
					text-overflow: ellipsis;
					display: -webkit-box;
					-webkit-line-clamp: 1;
					-webkit-box-orient: vertical;
				}
			}
		    .listcard-content_user{
				display: flex;
				image{
					width: 40px;
					height: 40px;
					border-radius: 100px;
					overflow: hidden;
				}
				text{
					font-size: 12px;
					margin: 10px 0 0 10px;
					flex-direction: column;
					justify-content: space-between;
				}
			}
			.listcard-content_body{
				font-size: 14px;
				color: #333;
				font-weight: 400;
				line-height: 1.2;
				margin-bottom: 10px;
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
	}
</style>