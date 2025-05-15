<template>
	<view @click="open">
		<view class="list-card">
			<view class="listcard-image">
				<image :src="item.cover[0]" mode="aspectFill"></image>
			</view>
			<view class="listcard-content">
				<view class="listcard-content_title">
					<text>{{item.title}}</text>
					<likes></likes>
				</view>
				<view class="listcard-content_des">
					<view class="listcard-content_des-label">
						<view class="listcard-content_des-label-item">
							{{item.classify}}
						</view>
					</view>
					<view class="listcard-content_des-browse">{{item.browse_count}}浏览</view>
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
				const item = this.item
				this.$emit('click',this.item)
				console.log('打开详情页面',this.item);
				//内容预渲染
				// const params = {
				// 	_id:item._id,
				// 	title:item.title,
				// 	create_time:item.create_time,
				// 	thumbs_up_count:item.thumbs_up_count,
				// 	browse_count:item.browse_count
				// }
				//传参数
				uni.navigateTo({
					url:'/frontend/pages/list-detail/list-detail',
					// url:'/frontend/pages/list-detail/list-detail?params='+JSON.stringify(params)
				})
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
				.listcard-content_des-label{
					display: flex;
					.listcard-content_des-label-item{
						padding: 0 5px;
						margin-right: 5px;
						border-radius: 15px;
						border: 1px #8A2BE2 solid;
						color: #8A2BE2;
					}
				}
				.listcard-content_des-browse{
					color: #999;
					line-height: 1.5;
				}
			}
		}
	}
</style>