<template>
	<view class="detail">
		<view class="detail-title">
			{{fromData.title}}
		</view>
		<view class="detail-header">
			<view class="detail-header-logo">
				<image src="@/frontend/static/img/list-detaiil/Starry Voyager.png" mode="aspectFill"></image>
			</view>
			<view class="detail-header-content">
				<view class="detail-header-content-title">
					{{fromData.author.author_name}}
				</view>
				<view class="detail-header-content-info">
					<text>{{fromData.create_time}}</text>
					<text>{{fromData.browse_count}} views</text>
					<text>{{fromData.thumbs_up_count}} likes</text>
				</view>
			</view>
		</view>
		<view class="detail-content">
			<view class="detail-html">
				<u-parse :content="fromData.content" :noData="noData"></u-parse>
				<image src="/frontend/static/img/list-detaiil/forest_squirrel.png"></image>
			</view>
			<view class="detail-comment">
				<view class="comment-title">Latest comment</view>
				<view class="comment-content" v-for="item in 5">
				<commentsBox></commentsBox>
				</view>
			</view>
		</view>
		<view class="detail-bottom">
			<view class="detail-bottom-input" @click="openComment">
				<text>Share your opinion</text>
				<uni-icons type="compose" size="16px" color="#84709B"></uni-icons>
			</view>
			<view class="detail-bottom-icons">
				<view class="detail-bottom-icons-box">
					<uni-icons type="chat" size="22px" color="#5D7DB3"></uni-icons>
				</view>
				<view class="detail-bottom-icons-box">
					<uni-icons type="heart" size="22px" color="#F07373"></uni-icons>
				</view>
				<view class="detail-bottom-icons-box">
					<uni-icons type="hand-up" size="22px" color="#F4BB44"></uni-icons>
				</view>
			</view>
		</view>
		<uni-popup ref="popup" type="bottom" :maskClick="false">
			<view class="popup-wrap">
				<view class="popup-header">
					<text class="popup-header-item" @click="close">Delete</text>
					<text class="popup-header-item" @click="submit">publish</text>
				</view>
				<view class="popup-content">
					<textarea class="popup-textarea" v-model="commentsValue" maxlength="200" fixed placeholder="Please enter the comment content"></textarea>
					<view class="popup-count">{{commentsValue.length}}/200</view>
				</view>
			</view>
		</uni-popup>
	</view>
</template>

<script>
	import uParse from '@/uni_modules/uv-parse/components/uv-parse/uv-parse.vue'
	import commentsBox from '@/frontend/components/commentsBox/commentsBox.vue';
	export default {
		components:{
			commentsBox,
			uParse
		},
		data() {
			return {
				fromData:{author: {}},
				noData:'<p style="aligin:center;color:#666">On Loading...<p>',
				// content: "Today's mood feels like a walk through an autumn forest.\nUnderfoot are thick layers of fallen leaves, and every step is accompanied by the soft rustling sound.\nQuiet yet full of poetry.",
				//输入框的值
				commentsValue:''
			}
		},
		onLoad(query) {
			this.fromData = JSON.parse(query.params),
			this.getDetail(),
			this.$refs.popup.open()
		},
		onReady(){
			// this.$refs.popup.open()
		},
		methods: {
			//获取详情信息
			getDetail(){
				this.$api.get_detail({
					article_id:this.fromData._id,
				}).then((res) =>{
					const {data} = res
					this.fromData = data
					console.log(res);
				})
			},
			//打开评论
			openComment() {
				this.$refs.popup.open()
				},
			//关闭评论
			close() {
				this.$refs.popup.close()
				},
			//发布评论
			submit(){
				console.log('发布');
				this.$refs.popup.close()
			}
		}
	}
</script>

<style lang="scss">
	.detail{
		padding: 15px 0;
		padding-bottom: 54px;
	}
	.detail-title{
		padding: 0 15px;
		font-size: 18px;
		font-weight: bold;
		color: #333;
	}
	.detail-header{
		display: flex;
		align-items: center;
		margin-top: 10px;
		padding: 0 15px;
		.detail-header-logo{
			flex-shrink: 0;
			width: 40px;
			height: 40px;
			border-radius: 50%;
			overflow: hidden;
			image{
				width: 100%;
				height: 100%;
			}
		}
		.detail-header-content{
			width: 100%;
			padding-left: 10px;
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			font-size: 12px;
			.detail-header-content-title{
				font-size: 14px;
				color: #333;
			}
			.detail-header-content-info{
				color: #999;
				text{
					margin-right: 10px;
				}
			}
		}
	}
	.detail-content{
		margin-top: 20px;
		min-height: 500px;
		.detail-html{
			padding: 0 15px;
			white-space: pre-line;
		}
		.detail-comment{
			margin-top: 30px;
			.comment-title{
				padding: 10px 15px;
				font-size: 14px;
				color: #666;
				border-bottom: 1px #f5f5ff solid;
			}
			.comment-content{
				padding: 0 15px;
				border-top: 1px #eee solid;
			}
		}
	}
	.detail-bottom{
		position: fixed;
		bottom: 0;
		left: 0;
		display: flex;
		align-items:center;
		width: 100%;
		height: 44px;
		border-top: 1px #f5f5f5 solid;
		background-color: #fff;
		box-sizing: border-box;
		.detail-bottom-input{
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-left: 10px;
			padding: 0 10px;
			width: 100%;
			height: 30px;
			border: 1px #ddd solid;
			border-radius: 10px;
			text{
				font-size: 14px;
				color: #999;
			}
		}
		.detail-bottom-icons{
			display: flex;
			flex-shrink: 0;
			padding: 0 10px;
			.detail-bottom-icons-box{
				position: relative;
				display: flex;
				align-items: center;
				justify-content: center;
				width: 44px;
			}
		}
	}
	.popup-wrap{
		background-color: #fff;
		.popup-header{
			display: flex;
			justify-content: space-between;
			font-size: 14px;
			color: #666;
			border-bottom: 1px #F5F5F5 solid;
			.popup-header-item{
				height: 40px;
				line-height: 50px;
				padding: 0 15px;
			}
		}
		.popup-content{
			width: 100%;
			padding: 15px;
			box-sizing: border-box;
			.popup-textarea{
				width: 100%;
				height: 200px;
			}
			.popup-count{
				display: flex;
				justify-content: flex-end;
				font-size: 12px;
				color: #999;
			}
		}
	}
</style>
