<template>
	<view>
		<view class="title">Title：</view>
			<view class="title-content">
				<textarea class="text" value="" placeholder="Please Enter Title..."></textarea>
			</view>
		<view class="content">Content:</view>
			<view class="content-content">
				<textarea class="text" value="" placeholder="At this moment..."></textarea>
			</view>
			<view class="title">Add picture: </view>
			<view class="image-box">
				<view class="item">
					<view class="close-icon">
						<uni-icons type="close" size="20" color="#fff"></uni-icons>
					</view>
					<view class="box">
						<image src="/static/img/logo.jpg" mode="aspectFill"></image>
					</view>
				</view>
				<view class="item">
					<view class="box">
						<uni-icons type="plusempty" size="50" color="#eee"></uni-icons>
					</view>
				</view>
			</view>
			<button class="button" type="primary">Publish</button>
	</view>
</template>

<script>
</script>

<style lang="scss">
	.title{
		margin:15px;
		margin-bottom: 0;
		font-size: 14px;
		color: #666;
	}
	.title-content{
		height: 8%;
		width: 100%;
		margin:15px;
		padding: 10px;
		box-sizing: border-box;
		border: 1px #eee solid;
		border-radius: 20px;
		.text{
			font-size: 15px;
		}
	}
	.content{
		margin:15px;
		margin-bottom: 0;
		font-size: 14px;
		color: #666;
	}
	.content-content{
		height: 30%;
		width: 100%;
		margin:15px;
		padding: 10px;
		box-sizing: border-box;
		border: 1px #eee solid;
		border-radius: 20px;
		.text{
			font-size: 15px;
		}
	}
	.image-box{
		display: flex;
		flex-wrap: wrap;
		padding: 10px;
		.item{
			position: relative;
			width: 33.33%;
			height: 0;
			padding-top: 33.33%;
			box-sizing: border-box;
			// border: 1px red solid;
			.close-icon{
				display: flex;
				justify-content: center;
				align-items: center;
				position: absolute;
				right: 0;
				top: 0;
				width: 16px;
				height: 16px;
				border-radius: 50%;
				background-color: #ff5a5f;
				z-index: 2;
			}
			.box{
				display: flex;
				justify-content: center;
				align-items: center;
				position: absolute;
				top: 5px;
				right: 5px;
				bottom: 5px;
				left: 5px;
				border: 1px #eee solid;
				border-radius: 5px;
				overflow: hidden;
				image{
					width: 100%;
					height: 100%;
				}
			}
		}
	}
	.button{
		margin: 0 20px;
		border-radius: 30px;
		background:linear-gradient(135deg, #A18BFF 0%, #7B89F9 100%) ;
	}
</style>