<template>
	<view class="tab">
		<scroll-view class="tab-scroll" scroll-x>
			<view class="tab-scroll_box">
				<view v-for="(item,index) in list" :key="index" class="tab-scroll_item">
					{{item.name}}
				</view>
			</view>
		</scroll-view>
		<view class="tab-icons">
			<uni-icons type="gear" size="26" color="#666"></uni-icons>
		</view>
	</view>
</template>

<script>
	export default{
		data(){
			return{
				list:[{
					name:'幸福'
				},
				{
					name:'悲伤'
				},
				{
					name:'厌恶'
				},
				{
					name:'恐惧'
				},
				{
					name:'惊讶'
				},
				{
					name:'愤怒'
				},
				{
					name:'骄傲'
				},
				{
					name:'羞耻'
				},
				{
					name:'尴尬'
				},
				{
					name:'兴奋'
				},
				]
			}
		}
	}
</script>

<style lang="scss">
	.tab{
		display: flex;
		width: 100%;
		border-bottom: 3px #f5f5f5 solid;
		background-color: #fff;
		box-sizing: border-box;
		.tab-scroll{
			flex: 1;
			overflow: hidden;
			box-sizing: border-box;
			
			.tab-scroll_box{
				display: flex;
				align-items: center;
				flex-wrap: nowrap;
				height: 45px;
				box-sizing: border-box;
				.tab-scroll_item{
					flex-shrink: 0;
					padding: 0 10px;
					color: #333;
					font-size: 14px;
				}
			}
		}
		.tab-icons{
			position: relative;
			display: flex;
			justify-content: center;
			align-items: center;
			width: 45px;
			&::after{
				content: '';
				position: absolute;
				top: 12px;
				bottom: 12px;
				left: 0;
				width: 2px;
				background-color: #ddd;
			}
		}
	}
</style>