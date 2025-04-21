<template>
	<view class="comments-box">
		<view class="comments-header">
			<view class="comments-header-logo">
				<image src="/frontend/static/img/list-detaiil/DreamCrasher.png" mode="aspectFill"></image>
			</view>
			<view class="comments-header-info">
				<view class="title">Dream Chaser</view>
				<view>2025-04 21 16:18:02</view>
			</view>
		</view>
		<view class="comments-content">
			<view>Love this! Autumn really does bring peace. Thanks for sharing.</view>
			<view class="comments-info">
				<view class="comments-button">Reply</view>
			</view>
			<view class="comments-reply" >
				<!-- v-for="item in comments.replys" :key="item.comment_id" --!>
				<!-- <commentsBox></commentsBox> -->
				
				<view class="comments-header">
					<view class="comments-header-logo">
						<image src="/frontend/static/img/list-detaiil/Starry Voyager.png" mode="aspectFill"></image>
					</view>
					<view class="comments-header-info">
						<view class="title">Starry Voyager</view>
						<view>2025-04 21 16:20:02</view>
					</view>
				</view>
				<view class="comments-content">
					<view>You're welcome! Glad it resonated with you. Nature has its way of calming us down.</view>
				</view>
				
				
			</view>
		</view>
	</view>
</template>

<script>
	// import commentsBox from '@/frontend/components/commentsBox/commentsBox.vue'
	export default{
		// components:{
		// 	commentsBox,
		// },
		data(){
			return{
				
			};
		}
	}
</script>

<style lang="scss">
	.comments-box{
		margin: 15px 0;
		.comments-header{
			display: flex;
			.comments-header-logo{
				flex-shrink: 0;
				width: 30px;
				height: 30px;
				border-radius: 50px;
				overflow: hidden;
				image{
					width: 100%;
					height: 100%;
				}
			}
			.comments-header-info{
				display: flex;
				flex-direction: column;
				padding-left: 15px;
				font-size: 12px;
				color: #999;
				line-height: 1;
				.title{
					margin-bottom: 10px;
					font-size: 14px;
					color: #333;
				}
			}
		}
		.comments-content{
			margin-top: 10px;
			font-size: 14px;
			color: #000;
			.comments-info{
				margin-top: 15px;
				display: flex;
				.comments-button{
					padding: 2px 10px;
					font-size: 12px;
					color: #999;
					border-radius: 20px;
					border: 1px #ccc solid;
				}
			}
			.comments-reply{
				// display: flex;
				margin: 15px 0;
				padding: 10px 10px;
				border: 1px #eee solid;
				//嵌入
				.comments-header{
					display: flex;
					.comments-header-logo{
						flex-shrink: 0;
						width: 30px;
						height: 30px;
						border-radius: 50px;
						overflow: hidden;
						image{
							width: 100%;
							height: 100%;
						}
					}
					.comments-header-info{
						display: flex;
						flex-direction: column;
						padding-left: 15px;
						font-size: 12px;
						color: #999;
						line-height: 1;
						.title{
							margin-bottom: 10px;
							font-size: 14px;
							color: #333;
						}
					}
				}
				.comments-content{
					margin-top: 10px;
					font-size: 14px;
					color: #000;
				}
				
			}
		}
	}
</style>