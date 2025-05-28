<template>
	<view class="comments-box">
		<view class="comments-header">
			<view class="comments-header-logo">
				<image src="@/static/img/list-detaiil/touxiang.jpg" mode="aspectFill"></image>
			</view>
			<view class="comments-header-info">
				<!-- <view v-if="!comments.is_reply" class="title">{{comments.author.author_name}}</view>
				<view v-else class="title">{{comments.author.author_name}}</view> -->
				<view class="title">{{comments.author.author_name}}</view>
				<!-- <view><text reply-text>Reply</text> -->
				<!-- {{comments.to}}</view> -->
				<!-- <view class="time">{{comments.create_time}}</view> -->
			</view>
		</view>
		<view class="comments-content">
			<view>{{comments.comment_content}}</view>
			<view class="comments-info">
				<view class="comments-button" @click="commentsReply({comments:comments,is_reply:reply})">Reply</view>
			</view>
			<view class="comments-reply" v-for="item in comments.replys" :key="item.comment_id">
				<comments-box :reply="true" :comments="item" @reply="commentsReply"></comments-box>
			</view>
		</view>
	</view>
</template>

<script>
	import CommentBox from '@/frontend/components/commentsBox/commentsBox.vue'
	export default{
		name:"comments-box",
		// components:{
		// 	CommentBox,
		// },
		props:{
			comments:{
				type:Object,
				default(){
					return{}
				}
			},
			reply:{
				type:Boolean,
				default:false
			}
		},
		data(){
			return{
				
			};
		},
		methods:{
			commentsReply(comment){
				if(comment.is_reply){
					comment.comments.reply_id = comment.comments.comment_id
					comment.comments.comment_id = this.comments.comment_id
				}
				// console.log(comment)
				this.$emit('reply',comment)
			}
		}
	}
</script>

<style lang="scss">
	.comments-box{
		margin: 10px 0;
		.comments-header{
			display: flex;
			.comments-header-logo{
				flex-shrink: 0;
				width: 20px;
				height: 20px;
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
					margin-bottom: 5px;
					font-size: 12px;
					color: #333;
					.reply-text{
						margin: 0 10px;
						color: #000;
					}
				}
			}
		}
		.comments-content{
			margin-top: 5px;
			font-size: 10px;
			color: #000;
			.comments-info{
				margin-top: 10px;
				display: flex;
				.comments-button{
					padding: 2px 8px;
					font-size: 10px;
					color: darkblue;
					background-color: lightblue;
					border-radius: 30px;
					// border: 1px #ccc solid;
				}
			}
			.comments-reply{
				// display: flex;
				margin: 15px 0;
				padding: 0px 15px;
				border: 1px #eee solid;
				border-radius: 30px;
			}
		}
	}
</style>