<template>
	<view @click="open">
		<view class="list-card">
			<view class="listcard-image">
				<image src="/frontend/static/img/logo.jpg" mode="aspectFill"></image>
			</view>
			<view class="listcard-content">
				<view class="listcard-content_title">
					<text>今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情今天的心情</text>
					<likes></likes>
				</view>
				<view class="listcard-content_des">
					<view class="listcard-content_des-browse">120浏览</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import likes from "@/frontend/components/likes/likes.vue";
	export default {
		components:{
			likes,
		},
		props:{
			item:{
				type: Object,
				default(){
					return{}
				}
			}
		},
		data() {
				return {
				};
			},
		methods: {
			open(){
				console.log('打开详情页面')
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
				position: relative;
				padding-right: 30px;
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
				.icons{
					position: absolute;
					right: 0;
					top: 0;
					display: flex;
					justify-content: center;
					align-items: center;
					width: 20px;
					height: 20px;
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